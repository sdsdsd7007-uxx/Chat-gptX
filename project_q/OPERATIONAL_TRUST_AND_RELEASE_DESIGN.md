# Project Q — Operational Trust and Release-Control Design

**Status:** design specification; not deployed  
**Policy target:** 1.2.x  
**Environment:** non-production  
**Purpose:** define the operational controls that must exist before the reference release evaluator can be considered for production use.

## 1. Trust bundle contract

The evaluator currently accepts a caller-supplied public-key mapping and revoked-key set. Those parameters are inputs, not a trust service. A future trust provider must supply an authenticated, versioned trust bundle with at least:

- bundle_id, bundle_version, issuer_id, issued_at, expires_at, retrieved_at;
- issuer signature and an independently configured trust anchor;
- key_id, algorithm (Ed25519 only unless a reviewed migration approves otherwise), public_key_fingerprint, public_key, status, valid_from, valid_until;
- revocation entries with effective_at, reason_code, source_event_id and sequence;
- monotonic sequence number and previous_bundle_digest to detect rollback/forking;
- source authentication, transport protection, audit event ID and validation result.

### Fail-closed rules
1. Reject missing, invalidly signed, expired, future-issued, stale, malformed or rollback-detected bundles.
2. Reject unknown key IDs, unsupported algorithms, invalid key lengths and keys outside their validity interval.
3. Reject revoked/suspended keys regardless of a cached prior active state.
4. Never silently fall back to a stale trust bundle when freshness cannot be established.
5. Preserve the last known-good bundle for forensic audit, but do not use it to authorize new releases after its expiry.
6. Emergency revocation must have a documented distribution and maximum propagation time; until received and validated, the service cannot claim globally current revocation status.
7. Record bundle digest, issuer, sequence, retrieval time, validation outcome and decision ID for every authorization decision.

### Operational requirements
- Key generation and custody must use an approved managed cryptographic boundary; private keys must not be stored in source control, test fixtures, application configuration or logs.
- Identity proofing binds key IDs to a real person/service principal and an authorization role.
- Key rotation uses overlapping validity windows with explicit retirement; compromise response supports immediate suspension and re-issuance.
- Revocation updates must be authenticated, monotonic, auditable and tested.
- Separation of duties: approver cannot approve their own change; trust administrators cannot unilaterally approve releases.
- Trusted time source and bounded clock-skew policy must be specified and monitored.

## 2. Replay prevention contract

The current evaluator checks signatures and time windows but does not provide durable replay prevention. A process-local set or in-memory cache is not an acceptable substitute.

A production authorization service must atomically consume a unique approval identifier/nonce in a durable store. A local SQLite reference implementation now exists in `project_q/src/project_q/replay_ledger.py`; it binds consumption to the evaluator's `GateDecision`, uses `BEGIN IMMEDIATE` and unique constraints, and is covered by concurrent-consumption tests. It remains a single-node non-production reference, not a distributed or production authorization service. Suggested signed claims:

- approval_id: globally unique opaque identifier;
- nonce: cryptographically random, unique per approval;
- record_digest and policy_version;
- key_id and approver identity reference;
- environment and exact allowed scopes;
- not_before and expires_at;
- issue timestamp and approval request ID.

### Atomic decision
Within one serializable transaction:
1. Validate the signed approval envelope and current trust bundle.
2. Verify record digest, policy version, environment, scopes and validity window.
3. Insert approval_id and nonce under unique constraints.
4. Reject if either identifier was previously consumed or conflicts with another approval.
5. Persist decision ID, evidence references, trust-bundle digest and audit metadata.
6. Commit consumption and authorization decision atomically.

If the transaction fails, authorization fails. If a client retries after a timeout, it must retrieve the prior decision by idempotency key; it must not create a second authorization. Define retention, backup, restore, replication consistency and disaster-recovery behavior for the replay ledger.

## 3. Recovery evidence verification

A non-empty `test_evidence_ref` is only a reference. Before production use, a separate verifier must resolve it and validate:
- evidence artifact digest and immutable storage/version;
- test plan, environment, execution timestamp and target system identity;
- actual observed result, exit status and logs;
- reviewer identity and independence;
- restore point, data integrity checks and recovery time;
- evidence freshness and scope match to the release being authorized.

A reference that cannot be resolved or whose digest/identity/scope does not match must block release.

## 4. Repository governance baseline

Repository owner/admin must configure and verify protections for `main` and the protected foundation branch:
- require pull requests; prohibit direct pushes and force pushes;
- require at least one independent approval (prefer two for high-risk changes);
- dismiss stale approvals after new commits;
- require approval from code owners for security-sensitive paths;
- require the named CI status check from the current head;
- require conversation resolution;
- restrict bypass and administrator bypass, with documented emergency exception;
- require signed commits where supported by the repository policy;
- restrict branch deletion;
- use CODEOWNERS for `.github/workflows/`, `project_q/src/`, `project_q/schemas/`, and security policy files.

The connector used in this work can inspect branch-protection state but cannot administer repository protection settings. This design document does not claim those controls are enabled.

## 5. Release gate sequence

1. Configure repository protections.
2. Obtain independent review against the exact commit SHA.
3. Resolve all Critical/High findings and record residual-risk acceptance by an authorized owner.
4. Deploy trust-bundle provider and replay ledger in a test environment.
5. Test key rotation, revocation, replay, stale bundle, clock skew, restore and partial outage.
6. Independently verify recovery evidence.
7. Re-run CI on the exact candidate commit.
8. Obtain a separate, scoped release authorization.
9. Only then consider a production-specific gate and deployment plan.

## 6. Explicit non-claims

This file is a design contract. The repository now includes a non-production SQLite replay-ledger prototype, but it does not implement a trust provider, key custody, identity proofing, revocation distribution, trusted time, production-grade distributed nonce consumption, recovery-evidence verification, repository protection, independent review or production deployment.
