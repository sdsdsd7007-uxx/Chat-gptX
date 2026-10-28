# Project Q — Inventory Scanner Security Review

**Review type:** implementation-author self-review; not independent assurance  
**Scanner:** inventory_scanner.py, version 2.0.0  
**Mode:** local read-only inventory; synthetic tests  
**Cloud permissions:** not inspected  
**Source writes:** 0 by design

## Implemented controls

- Rejects a symlink supplied as the source root.
- Traverses from open directory file descriptors using descriptor-relative stat/open operations rather than recursively joining untrusted path strings.
- Rejects symlink entries without following them.
- Opens child directories and files with O_NOFOLLOW; verifies the opened object type with fstat.
- Rechecks device identity after opening and rejects cross-device entries to avoid silently traversing ordinary mount boundaries.
- Rejects non-regular special files.
- Records the source root, all encountered directories, regular files and rejected symlink/special/cross-device entries.
- Computes SHA-256 for readable regular files and marks exact-hash duplicate candidates for review; it does not automatically deduplicate.
- Produces stable sorted records and a snapshot SHA-256 over record metadata excluding the per-run UUID.
- Captures scanner version, run ID, UTC start time, source root, counts, exception counts and explicit source_writes=0 in a JSON manifest.
- Requires CSV and manifest destinations to resolve outside the source root.
- Uses exclusive file creation and mode 0600; refuses to overwrite an existing report.
- Keeps cloud permission status as not_checked and version/revision as unknown where local APIs do not provide them.

## Regression coverage

Automated tests cover:
- root, nested directory and file records;
- file and directory symlink rejection without reading an external target;
- rejection of a symlink source root;
- output path inside source root;
- existing report no-overwrite behavior;
- reproducible snapshot digest for an unchanged tree;
- explicit unknown cloud-permission status and zero source writes.

## Residual limitations

1. This is a local-folder scanner, not a Dropbox API crawler; it cannot enumerate remote-only files, cloud sharing ACLs, team policy, or Dropbox revision history.
2. Cross-device checks reject ordinary different-device mount boundaries. Same-device bind mounts may not be distinguishable by st_dev and require an OS-specific mount-table policy if they are in scope.
3. The scanner records local path identity, not a durable cloud file ID; rename/move changes the path-derived source_record_id.
4. File metadata can change while the scan runs; the manifest records a snapshot digest but does not provide a filesystem-wide atomic snapshot.
5. CSV and JSON manifest are separately created. If the second output creation fails after the CSV succeeds, a partial report pair may remain; preserve it as an exception rather than treating the run as accepted.
6. Ownership, permissions, sensitivity classification and reviewer fields are not independently verified. They remain unknown/not_checked until a separate review.
7. The implementation is not an authorization boundary and must not be pointed at production or sensitive directories without scope approval.

## Release decision

The scanner is suitable for further isolated non-production tests after its CI suite passes. It is not a production inventory service and does not authorize Dropbox staging writes. Independent code review and a separately authorized staging pilot remain required.
