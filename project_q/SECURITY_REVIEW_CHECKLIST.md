# Project Q — Independent Security Review Checklist

**Status:** review aid; not a completed security assessment  
**Scope:** the controlled evidence schema, release-policy evaluator, signature handling, CI workflow and synthetic Project Z pilot on the review branch.  
**Rule:** unresolved critical/high findings block approval. This checklist does not authorize merging or deployment.

## 1. Trust and approver identity
- [ ] Define how approver identities are authenticated and mapped to key IDs.
- [ ] Define trusted-key provisioning, ownership, custody and access boundaries.
- [ ] Define key rotation, revocation, compromise response and historical verification.
- [ ] Confirm a key cannot approve its own unreviewed change where separation of duties is required.
- [ ] Define minimum approver roles and separation-of-duties policy.
- [ ] Ensure test keys and test fixtures cannot enter a production trust registry.

## 2. Signature and canonicalization
- [ ] Independently reproduce the canonical record digest in a second implementation/language.
- [ ] Confirm canonicalization behavior for Unicode, number formats, arrays, nulls and nested objects.
- [ ] Confirm every approval claim that affects policy is signed, including key identifier, scope, environment, expiry and artifact digest.
- [ ] Confirm malformed Base64, invalid key lengths, unknown key IDs and invalid signatures fail closed.
- [ ] Define signature algorithm/version agility and migration behavior.
- [ ] Test duplicate JSON keys and parser differences at ingestion boundaries.

## 3. Approval lifecycle and time
- [ ] Define authoritative time source, clock-skew tolerance and timezone handling.
- [ ] Test expiry boundaries immediately before, at and after expiration.
- [ ] Define approval revocation and emergency suspension behavior.
- [ ] Bind approvals to exact artifact digest, environment, scope and policy version.
- [ ] Ensure approval cannot be replayed for a different artifact, environment or scope.
- [ ] Define audit evidence for who approved what, when, and under which policy.

## 4. Schema and policy robustness
- [ ] Review JSON Schema constraints against actual policy assumptions.
- [ ] Test oversized records, deeply nested objects, unexpected encodings and resource exhaustion.
- [ ] Test schema evolution and backward compatibility.
- [ ] Confirm unknown or missing fields fail closed where required.
- [ ] Confirm exception handling does not leak secrets while preserving useful audit diagnostics.
- [ ] Review policy versioning and deterministic decision reproducibility.

## 5. CI and repository controls
- [ ] Verify all GitHub Actions are pinned to immutable commit SHAs.
- [ ] Confirm workflow permissions remain least-privilege and read-only.
- [ ] Review branch protection, required status checks and review dismissal/stale approval settings.
- [ ] Confirm untrusted pull-request code cannot access secrets or write tokens.
- [ ] Review dependency pinning, update policy and vulnerability response.
- [ ] Confirm workflow triggers and path filters cover all policy-relevant files.

## 6. Project Z ingestion and retrieval
- [ ] Define maximum JSONL line size, batch size and total input size.
- [ ] Test malformed UTF-8, duplicate IDs, timestamps, numeric edge cases and tag limits.
- [ ] Define retention and deletion behavior before any non-synthetic data is considered.
- [ ] Enforce authorization filters before retrieval results are returned.
- [ ] Verify no sensitive payloads or secrets are written to CI logs or benchmark artifacts.
- [ ] Review relevance labels independently before reporting quality comparisons.

## 7. Recovery and operations
- [ ] Define incident severity, notification owner and response timeline.
- [ ] Demonstrate backup restoration and rollback in a disposable test environment.
- [ ] Define audit-log retention, integrity and access.
- [ ] Define monitoring for policy denials, malformed inputs, signature failures and anomalous approvals.
- [ ] Confirm production is blocked by this evaluator and requires a separately reviewed release workflow.

## Required review output

The independent reviewer should record:
- reviewer identity and review date;
- commit SHA reviewed;
- files and threat scenarios covered;
- findings with severity, evidence and remediation;
- residual risks and accepted limitations;
- explicit recommendation: approve, request changes, or unable to conclude.

No reviewer identity or approval is assumed by this document.
