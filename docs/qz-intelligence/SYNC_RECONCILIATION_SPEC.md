# Sync Reconciliation Specification
**Parent:** Project Q & Z v114.0 concept track  
**Status:** Proposed design only; no service deployed.

## Purpose
Define a consistent way to compare approved records in Dropbox, GitHub and spreadsheets without assuming that a matching folder name or a successful upload means that every record is current or reconciled.

## Required record fields
Stable record ID; source location; source revision where available; schema version; event time; observation time; content digest; update identifier; permission state; parent record; reconciliation checkpoint; current status and error reason.

When a source does not expose a field, record that limitation rather than inventing a value.

## Reconciliation procedure
1. Read the source metadata and confirm the approved scope.
2. Validate the record schema and freshness rule.
3. Compare the source revision and destination revision.
4. Use a stable update identifier so retries do not duplicate work.
5. Preserve both versions when concurrent edits conflict.
6. Apply a documented ordering rule to late-arriving updates.
7. Compare source and destination inventories at a named checkpoint.
8. Report missing, extra, stale, conflicting and changed records.
9. Route unclear material conflicts to the accountable owner.
10. Verify restore against a known-good record manifest.
11. Stop write-capable operations when permission or critical evidence cannot be verified.

## Dropbox scope note
Dropbox documentation describes conflicted copies that can arise from concurrent or offline edits. Therefore the goal is no silent loss and no unresolved mismatch at a verified reconciliation checkpoint, not a promise that conflicts can never occur. The namespace identifier 13757222513 identifies a storage location; it does not prove that 18 branches are active or that synchronization is currently running. Enumerate the approved folders, files, revisions, owners and permissions before claiming coverage.

## Cryptographic migration research
Maintain an inventory of supported protocols, algorithms, software versions, key lifetimes, retained data, external dependencies and interoperability needs. Review applicable NIST post-quantum migration guidance before selecting a supported implementation. Do not design a custom cipher or state that a cloud provider has changed its internal cryptography without official evidence.

Sources:
- NIST IR 8547 final: https://csrc.nist.gov/pubs/ir/8547/final
- NIST post-quantum cryptography project: https://csrc.nist.gov/Projects/post-quantum-cryptography
- Dropbox conflicted copy guidance: https://help.dropbox.com/organize/conflicted-copy

## Proposed acceptance tests — NOT RUN
- Repeated delivery creates no duplicate logical update.
- Older revisions do not silently replace newer revisions.
- Concurrent/offline edits create a visible conflict.
- Missing source/destination records are listed by ID.
- A changed content digest is flagged.
- Expired permission blocks a write.
- Recovery verifies record content and source revision.
- Retry/resource limits stop further work safely.
- Branch-coverage claims remain unknown until the approved inventory is reconciled.

## Measures
Anomaly detection coverage; unresolved mismatches per reconciliation checkpoint; duplicate logical updates; conflict resolution time; restore success; and p50/p95/p99 per adapter operation. Set targets only after approving the scope, denominator and workload.
