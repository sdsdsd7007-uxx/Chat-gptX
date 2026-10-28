"""Disposable local recovery simulation; never targets Dropbox or production paths."""
import hashlib
import os
import shutil
import stat
import tempfile
import unittest
from pathlib import Path


def tree_digest(root):
    root = Path(root)
    records = []
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs.sort()
        files.sort()
        current_path = Path(current)
        for name in list(dirs) + files:
            path = current_path / name
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                raise ValueError("symlink rejected in recovery source")
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(info.st_mode):
                records.append(("directory", relative, ""))
            elif stat.S_ISREG(info.st_mode):
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                records.append(("file", relative, digest))
            else:
                raise ValueError("special file rejected in recovery source")
    payload = "\n".join("|".join(item) for item in sorted(records))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def copy_disposable_tree(source, destination):
    source = Path(source).resolve(strict=True)
    destination = Path(destination).resolve(strict=False)
    if destination.exists():
        raise FileExistsError("recovery destination must not already exist")
    if destination == source or source in destination.parents or destination in source.parents:
        raise ValueError("source and recovery destination must be disjoint")
    destination.mkdir(parents=True)
    for current, dirs, files in os.walk(source, topdown=True, followlinks=False):
        dirs.sort()
        files.sort()
        current_path = Path(current)
        relative_dir = current_path.relative_to(source)
        target_dir = destination / relative_dir
        for name in list(dirs):
            item = current_path / name
            if item.is_symlink():
                raise ValueError("symlink rejected during recovery copy")
            (target_dir / name).mkdir()
        for name in files:
            item = current_path / name
            if item.is_symlink() or not item.is_file():
                raise ValueError("non-regular file rejected during recovery copy")
            target = target_dir / name
            with item.open("rb") as source_stream, target.open("xb") as target_stream:
                shutil.copyfileobj(source_stream, target_stream)


class RecoverySimulationTests(unittest.TestCase):
    def build_source(self, root):
        (root / "nested").mkdir(parents=True)
        (root / "nested" / "record.json").write_text('{"synthetic":true}', encoding="utf-8")
        (root / "README.txt").write_text("disposable recovery fixture", encoding="utf-8")

    def test_backup_restore_round_trip_matches_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "source"
            source.mkdir()
            self.build_source(source)
            expected = tree_digest(source)
            backup = base / "backup"
            copy_disposable_tree(source, backup)
            self.assertEqual(tree_digest(backup), expected)
            restored = base / "restored"
            copy_disposable_tree(backup, restored)
            self.assertEqual(tree_digest(restored), expected)
            self.assertEqual((source / "README.txt").read_text(encoding="utf-8"),
                             "disposable recovery fixture")

    def test_corrupted_backup_is_detectable(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "source"
            source.mkdir()
            self.build_source(source)
            expected = tree_digest(source)
            backup = base / "backup"
            copy_disposable_tree(source, backup)
            (backup / "README.txt").write_text("changed", encoding="utf-8")
            self.assertNotEqual(tree_digest(backup), expected)

    def test_symlink_is_rejected_and_external_target_is_untouched(self):
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "source"
            source.mkdir()
            external = base / "external.txt"
            external.write_text("outside", encoding="utf-8")
            (source / "escape.txt").symlink_to(external)
            with self.assertRaises(ValueError):
                tree_digest(source)
            with self.assertRaises(ValueError):
                copy_disposable_tree(source, base / "backup")
            self.assertEqual(external.read_text(encoding="utf-8"), "outside")

    def test_existing_recovery_destination_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "source"
            source.mkdir()
            self.build_source(source)
            destination = base / "backup"
            destination.mkdir()
            sentinel = destination / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                copy_disposable_tree(source, destination)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
