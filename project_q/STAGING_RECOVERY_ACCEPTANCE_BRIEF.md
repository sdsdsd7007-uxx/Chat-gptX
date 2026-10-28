# Project Q — Staging Recovery Test and Independent Acceptance Brief

**Status:** local disposable recovery simulation added; Dropbox staging recovery not executed  
**Environment:** local temporary directories only  
**Production:** HOLD  
**Authority:** the Dropbox VALIDATION_PLAN.md remains DRY RUN ONLY and says a write-capable pilot is a later stage requiring separate approval.

## 1. What has actually been tested

The repository test suite includes a disposable local recovery simulation that:
- creates synthetic source files and a nested directory;
- copies the source to a separate temporary backup;
- computes a deterministic tree digest before and after backup;
- restores from the backup into a new temporary destination;
- verifies the restored tree digest matches the source;
- detects a deliberately altered backup;
- rejects symlinks and preserves the external symlink target;
- refuses to overwrite an existing recovery destination.

This is a local unit-test simulation. It is not a Dropbox staging restore, a cloud backup test, a disaster-recovery exercise, or independent acceptance.

## 2. Preconditions for a real staging test

A separate written authorization must specify:
- exact Dropbox staging source and destination paths;
- named operator and independent reviewer;
- exact files and data classification in scope;
- confirmation that the destination is disposable and contains no user data;
- backup snapshot and immutable evidence references;
- permitted write operations and explicit exclusions;
- expected RPO/RTO, restore procedure and stop conditions;
- rollback/cleanup plan and who can authorize it.

Do not infer permission from the existence of the STAGING_PILOT folder or the historical pilot report. The governing validation plan remains dry-run-only.

## 3. Required staging test cases

1. Enumerate source and destination manifests, including directory records.
2. Verify source and backup checksums and metadata.
3. Restore into an empty isolated destination without overwriting.
4. Compare file counts, directory counts, sizes and SHA-256 digests.
5. Test missing, truncated, altered and unreadable backup objects.
6. Test symlink/path-escape rejection and permission-denied behavior.
7. Test interrupted restore and safe retry behavior.
8. Verify no writes outside the authorized staging destination.
9. Record actual start/end times, observed recovery time and data-loss window.
10. Preserve logs and evidence with reviewer identity and exact commit/tool versions.

## 4. Independent acceptance record

The implementation author must not sign as the independent reviewer.

- Reviewer identity:
- Organization / role:
- Relevant recovery/security experience:
- Conflict-of-interest disclosure:
- Dropbox staging authorization reference:
- Source manifest digest:
- Backup manifest digest:
- Restored manifest digest:
- Observed RPO:
- Observed RTO:
- Test date/time:
- Findings and severity:
- Exceptions / residual risks:
- Decision: ACCEPT / ACCEPT WITH CONDITIONS / REJECT
- Reviewer signature or attributable approval reference:

## 5. Stop conditions

Stop if scope, destination ownership, permissions, backup integrity or reviewer independence cannot be verified; if any symlink/path escape is detected; if a destination is not empty; or if a write would affect source or production data.

**Current decision:** local synthetic recovery simulation is implemented for CI. Real Dropbox staging recovery and independent acceptance remain blocked pending separately authorized staging scope and an independent reviewer.
