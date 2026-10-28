# Project Q — Trust and Approval Lifecycle

**Status:** design specification for independent review; not a production trust service.  
**Policy version:** 1.2.0  
**Environment:** non-production reference implementation.

## 1. Evidence provenance

An evidence record must include:
- at least one source-record reference;
- a source URL or source-document reference;
- retrieval timestamp;
- verification status and method;
- verifier identity and verification timestamp;
- confidence and limitations.

A `VEF` classification is a claim that must be supported by the recorded provenance. The schema validates presence and shape; it does not independently establish source authenticity, verifier competence, or truth.

## 2. Approval envelope

The signed approval binds:
- the SHA-256 digest of the evidence record (excluding the approval envelope);
- approval status and reference;
- target environment and scopes;
- policy version;
- not-before and expiry timestamps;
- key identifier.

The policy version is `1.2.0`. Any change to the approval claims invalidates the signature. Any change to the evidence record invalidates the artifact digest.

## 3. Validity window

An approval is valid only when:
- evaluation time is timezone-aware;
- `not_before <= now < expires_at`;
- `expires_at > not_before`;
- the approval is signed by a currently trusted, non-revoked key.

The reference evaluator requires an explicitly supplied `revoked_approval_key_ids` set. If this input is omitted, the evaluator blocks with `REVOCATION_STATUS_UNAVAILABLE`; it does not silently assume that no keys are revoked. If a key is listed in the set, its approval is blocked even when the signature verifies.

## 4. Trust-key operations — required before real use

This repository does not implement a key-management service. Before any real approval workflow, an accountable security owner must define and operate:
1. identity proofing and mapping from verified approver identities to key IDs;
2. key generation in an approved secure environment;
3. custody, access control and separation of duties;
4. rotation, revocation, compromise response and emergency suspension;
5. auditable key-registry changes and historical verification rules;
6. backup and recovery of trust metadata;
7. algorithm/version migration and key retirement.

The caller-supplied public-key map and revocation set are configuration inputs, not a complete lifecycle system. The revocation set must be present and sourced from an authenticated, current registry; absence blocks approval. They must come from an authenticated, access-controlled source. Never embed production private keys in this repository, CI variables exposed to untrusted code, or test fixtures.

## 5. Recovery evidence

When recovery is required, the record must contain a recovery test evidence reference, a tested status and a non-empty recovery plan. The schema only checks that the reference exists syntactically; a reviewer or separate evidence verifier must inspect the referenced test result and confirm its scope, date, environment and outcome.

## 6. Serialization and interoperability contract

The current implementation computes its digest and signature payload using Python's JSON serializer with sorted object keys, compact separators, UTF-8 output, Unicode preserved, and non-finite numbers rejected. This is a deterministic Python serialization profile, not a claim of RFC 8785/JCS conformance.

Until a formally specified cross-language canonicalization profile and shared test vectors are adopted:
- all signing and verification must use the same versioned implementation/profile;
- do not assume another language's default JSON serializer produces identical bytes;
- treat any serializer/profile change as a cryptographic policy migration requiring new test vectors and reviewer approval;
- test Unicode, numeric representations, escaping, nested objects and key-order permutations.

## 7. Limits and release boundary

- Schema validity is not proof of evidence truth.
- A valid Ed25519 signature proves possession of the corresponding private key, not the real-world identity or authority of the signer.
- Revocation is only as current as the externally supplied revocation set.
- Clock trust and allowed clock skew are operational dependencies; this reference policy does not define a trusted time service.
- The evaluator never authorizes production promotion. Production requires a separate reviewed workflow and a separate explicit authorization.
- No account synchronization, external publishing, financial operation, sensitive-data ingestion or physical-system control is implemented here.

## 8. Independent review checklist

The reviewer should independently test:
- Python serialization profile, cross-language canonicalization limits and JSON edge cases;
- signature binding and key-ID handling;
- not-before/expiry boundary conditions and clock skew;
- revocation freshness and emergency behavior;
- provenance source quality and verifier identity;
- recovery evidence traceability;
- schema evolution and policy-version migration;
- CI trust boundaries and repository protection settings.

**Completion criterion:** all Critical/High findings resolved or formally dispositioned by an accountable independent reviewer; regression tests pass; the exact release scope is separately authorized.
