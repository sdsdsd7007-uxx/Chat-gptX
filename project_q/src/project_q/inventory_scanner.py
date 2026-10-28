"""Fail-closed, read-only local inventory scanner for Project Q.

Security properties:
- Traverses directories through directory file descriptors (no path-following walk).
- Rejects symlinks and uses O_NOFOLLOW for directory/file opens.
- Reads only regular files and records directory entries explicitly.
- Writes CSV + JSON manifest only outside the approved source root.
- Uses exclusive creation; existing outputs are never overwritten.
- Does not inspect remote Dropbox-only content or cloud permissions.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import stat
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCANNER_VERSION = "2.0.0"
FIELDS = [
    "inventory_run_id", "source_system", "source_path", "item_name", "item_type",
    "file_extension", "size_bytes", "modified_at_source", "owner_or_team",
    "project_workstream", "taxonomy_labels", "sensitivity_class", "source_record_id",
    "version_or_revision", "checksum_sha256", "duplicate_candidate",
    "metadata_complete", "permission_review_status", "sync_action_proposed",
    "validation_status", "exception_reason", "reviewer", "reviewed_at", "notes",
]


class InventoryError(RuntimeError):
    """A fail-closed inventory or output-safety error."""


def _require_safe_open_flags() -> tuple[int, int]:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None:
        raise InventoryError("platform lacks O_NOFOLLOW/O_DIRECTORY; refusing unsafe traversal")
    return nofollow, directory


def _utc_mtime(ns: int) -> str:
    return datetime.fromtimestamp(ns / 1_000_000_000, timezone.utc).isoformat()


def _source_id(relative_path: str) -> str:
    digest = hashlib.sha256(relative_path.encode("utf-8")).hexdigest()
    return "local-path-sha256:" + digest


def _row(run_id: str, source_system: str, relative_path: str, name: str,
         item_type: str, *, size: int | str = "", modified: str = "",
         checksum: str = "", validation: str = "pending_review",
         exception: str = "") -> dict[str, Any]:
    suffix = Path(name).suffix.lower() if item_type == "file" else ""
    return {
        "inventory_run_id": run_id,
        "source_system": source_system,
        "source_path": relative_path,
        "item_name": name,
        "item_type": item_type,
        "file_extension": suffix,
        "size_bytes": size,
        "modified_at_source": modified,
        "owner_or_team": "unknown",
        "project_workstream": "",
        "taxonomy_labels": "",
        "sensitivity_class": "unclassified_not_assessed",
        "source_record_id": _source_id(relative_path),
        "version_or_revision": "unknown",
        "checksum_sha256": checksum,
        "duplicate_candidate": "no",
        "metadata_complete": "no",
        "permission_review_status": "not_checked",
        "sync_action_proposed": "catalog_only" if item_type == "directory" else "index_candidate_only",
        "validation_status": validation,
        "exception_reason": exception,
        "reviewer": "",
        "reviewed_at": "",
        "notes": "Proposal only; no source action performed.",
    }


def _hash_open_fd(fd: int) -> str:
    digest = hashlib.sha256()
    with os.fdopen(fd, "rb", closefd=True) as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _scan_directory(dir_fd: int, prefix: str, *, run_id: str,
                    source_system: str, rows: list[dict[str, Any]],
                    hash_to_paths: dict[str, list[str]], root_device: int) -> None:
    # scandir(fd) is anchored to the already-open directory, not a reconstructed path.
    with os.scandir(dir_fd) as iterator:
        names = sorted(entry.name for entry in iterator)

    nofollow, directory_flag = _require_safe_open_flags()
    for name in names:
        # Names returned by scandir are single path components; never accept traversal syntax.
        if name in {"", ".", ".."} or os.sep in name or (os.altsep and os.altsep in name):
            rows.append(_row(run_id, source_system, f"{prefix}/{name}", name, "exception",
                             validation="exception", exception="INVALID_DIRECTORY_ENTRY_NAME"))
            continue
        relative = f"{prefix}/{name}" if prefix else name
        try:
            item_stat = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
        except OSError as exc:
            rows.append(_row(run_id, source_system, relative, name, "exception",
                             validation="exception", exception=f"STAT_FAILED:{type(exc).__name__}"))
            continue

        if stat.S_ISLNK(item_stat.st_mode):
            rows.append(_row(run_id, source_system, relative, name, "symlink",
                             validation="exception", exception="SYMLINK_REJECTED_NOT_FOLLOWED"))
            continue
        if item_stat.st_dev != root_device:
            rows.append(_row(run_id, source_system, relative, name, "mount_or_device_boundary",
                             validation="exception", exception="CROSS_DEVICE_ENTRY_REJECTED"))
            continue

        if stat.S_ISDIR(item_stat.st_mode):
            row = _row(run_id, source_system, relative, name, "directory",
                       size=item_stat.st_size, modified=_utc_mtime(item_stat.st_mtime_ns),
                       validation="directory_metadata_recorded")
            row["metadata_complete"] = "yes"
            rows.append(row)
            child_fd = None
            try:
                child_fd = os.open(name, os.O_RDONLY | directory_flag | nofollow, dir_fd=dir_fd)
                opened_stat = os.fstat(child_fd)
                if not stat.S_ISDIR(opened_stat.st_mode):
                    raise InventoryError("opened directory changed type")
                _scan_directory(child_fd, relative, run_id=run_id,
                                source_system=source_system, rows=rows,
                                hash_to_paths=hash_to_paths, root_device=root_device)
            except OSError as exc:
                rows.append(_row(run_id, source_system, relative + "/",
                                 name, "exception", validation="exception",
                                 exception=f"DIRECTORY_OPEN_OR_SCAN_FAILED:{type(exc).__name__}"))
            except InventoryError as exc:
                rows.append(_row(run_id, source_system, relative + "/",
                                 name, "exception", validation="exception",
                                 exception=f"DIRECTORY_REJECTED:{exc}"))
            finally:
                if child_fd is not None:
                    os.close(child_fd)
            continue

        if not stat.S_ISREG(item_stat.st_mode):
            rows.append(_row(run_id, source_system, relative, name, "special",
                             validation="exception", exception="NON_REGULAR_FILE_REJECTED"))
            continue

        file_fd = None
        try:
            file_fd = os.open(name, os.O_RDONLY | nofollow, dir_fd=dir_fd)
            opened_stat = os.fstat(file_fd)
            if not stat.S_ISREG(opened_stat.st_mode):
                raise InventoryError("opened file is not regular")
            fd_to_hash = file_fd
            file_fd = None  # ownership transferred before hashing, including read failures
            checksum = _hash_open_fd(fd_to_hash)
            row = _row(run_id, source_system, relative, name, "file",
                       size=opened_stat.st_size, modified=_utc_mtime(opened_stat.st_mtime_ns),
                       checksum=checksum, validation="file_metadata_and_hash_recorded")
            row["metadata_complete"] = "yes"
            rows.append(row)
            hash_to_paths.setdefault(checksum, []).append(relative)
        except (OSError, InventoryError) as exc:
            rows.append(_row(run_id, source_system, relative, name, "file",
                             validation="exception", exception=f"FILE_READ_REJECTED:{type(exc).__name__}"))
        finally:
            if file_fd is not None:
                os.close(file_fd)


def _ensure_output_outside_root(output: Path, root: Path) -> Path:
    resolved = output.expanduser().resolve(strict=False)
    try:
        if os.path.commonpath((str(root), str(resolved))) == str(root):
            raise InventoryError("all report outputs must be outside the inventoried source root")
    except ValueError:
        raise InventoryError("output and source root must be on a comparable filesystem") from None
    return resolved


def _write_exclusive(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def create_inventory(root_arg: str, output_arg: str, *, manifest_arg: str | None = None,
                     source_system: str = "local_or_synced_folder") -> dict[str, Any]:
    root_input = Path(root_arg).expanduser()
    try:
        if root_input.is_symlink():
            raise InventoryError("source root itself must not be a symlink")
        root = root_input.resolve(strict=True)
        root_stat = root.stat()
    except OSError as exc:
        raise InventoryError(f"source root unavailable: {type(exc).__name__}") from None
    if not stat.S_ISDIR(root_stat.st_mode):
        raise InventoryError("source root must be an existing directory")

    output = _ensure_output_outside_root(Path(output_arg), root)
    manifest = _ensure_output_outside_root(
        Path(manifest_arg) if manifest_arg else output.with_suffix(output.suffix + ".manifest.json"),
        root,
    )
    if output == manifest:
        raise InventoryError("CSV and manifest outputs must be different paths")

    nofollow, directory_flag = _require_safe_open_flags()
    root_fd = os.open(root, os.O_RDONLY | directory_flag | nofollow)
    run_id = str(uuid.uuid4())
    rows: list[dict[str, Any]] = []
    hash_to_paths: dict[str, list[str]] = {}
    started_at = datetime.now(timezone.utc).isoformat()
    try:
        root_row = _row(run_id, source_system, ".", root.name or str(root), "directory",
                        size=root_stat.st_size, modified=_utc_mtime(root_stat.st_mtime_ns),
                        validation="source_root_metadata_recorded")
        root_row["metadata_complete"] = "yes"
        rows.append(root_row)
        _scan_directory(root_fd, "", run_id=run_id, source_system=source_system,
                        rows=rows, hash_to_paths=hash_to_paths, root_device=root_stat.st_dev)
    finally:
        os.close(root_fd)

    for row in rows:
        matches = hash_to_paths.get(row["checksum_sha256"], []) if row["checksum_sha256"] else []
        if len(matches) > 1:
            row["duplicate_candidate"] = "exact_hash_match_review_required"

    rows.sort(key=lambda item: (item["source_path"], item["item_type"], item["item_name"]))
    stable_rows = [{key: value for key, value in row.items() if key != "inventory_run_id"} for row in rows]
    snapshot_bytes = json.dumps(stable_rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    manifest_data = {
        "manifest_version": "1.0.0",
        "scanner_version": SCANNER_VERSION,
        "inventory_run_id": run_id,
        "started_at": started_at,
        "source_system": source_system,
        "source_root": str(root),
        "source_root_modified_at": _utc_mtime(root_stat.st_mtime_ns),
        "record_count": len(rows),
        "file_count": sum(row["item_type"] == "file" for row in rows),
        "directory_count": sum(row["item_type"] == "directory" for row in rows),
        "symlink_rejected_count": sum(row["exception_reason"] == "SYMLINK_REJECTED_NOT_FOLLOWED" for row in rows),
        "exception_count": sum(row["validation_status"] == "exception" for row in rows),
        "source_writes": 0,
        "cloud_permissions_reviewed": False,
        "snapshot_sha256": hashlib.sha256(snapshot_bytes).hexdigest(),
        "csv_report": str(output),
    }
    csv_buffer = __import__("io").StringIO(newline="")
    writer = csv.DictWriter(csv_buffer, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    _write_exclusive(output, csv_buffer.getvalue())
    _write_exclusive(manifest, json.dumps(manifest_data, indent=2, sort_keys=True) + "\n")
    return manifest_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail-closed read-only Project Q inventory")
    parser.add_argument("--root", required=True, help="Approved local source directory")
    parser.add_argument("--output", required=True, help="New CSV report path outside source root")
    parser.add_argument("--manifest", help="New JSON manifest path outside source root")
    parser.add_argument("--source-system", default="local_or_synced_folder")
    args = parser.parse_args()
    try:
        result = create_inventory(args.root, args.output, manifest_arg=args.manifest,
                                  source_system=args.source_system)
    except (InventoryError, OSError) as exc:
        raise SystemExit(f"ERROR: {exc}") from None
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
