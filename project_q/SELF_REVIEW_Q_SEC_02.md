# Project Q Q-SEC-02 — Internal Self-Review Record

**Review type:** implementation-author self-review; not independent assurance  
**Policy:** 1.2.0  
**Branch:** project-q/security-hardening-q-sec-02  
**Environment:** non-production only  
**Disposition:** continue controlled development; do not merge or deploy.

## Changes completed during this review cycle

- Constrained the optional audit object to known metadata fields.
- Required non-empty source URL/document references.
- Required at least one approval scope and prohibited duplicate scopes.
- Cross-checked registry-level and evidence-level source-record lists.
- Rejected future-dated evidence retrieval and verification timestamps.
- Documented the deterministic Python JSON serialization profile and explicitly disclaimed RFC 8785/JCS compatibility.
- Added regression coverage for source references, scope uniqueness, audit schema, key-order-independent digest, non-finite numbers, provenance consistency, future timestamps, and malformed direct signature-helper inputs.
- Hardened the standalone signature-verification helper to return false on malformed input instead of relying on the outer evaluator's exception handler.

## Findings and residual risks

| ID | Severity for production use | Finding | Disposition |
|---|---|---|---|
| SR-01 | High | Trusted public-key registry and revocation set are caller-supplied; no authenticated lifecycle service is implemented. | Production blocked; design and operate an authenticated trust service. |
| SR-02 | High | Verifier identity is a string claim, not cryptographically bound to an independently verified human or organizational identity. | Require identity proofing and separation of duties outside this reference evaluator. |
| SR-03 | High | Recovery evidence reference is syntactically required but is not dereferenced or independently authenticated by this code. | Require a separate evidence-verification service/reviewer. |
| SR-04 | Medium | Serialization is deterministic for the documented Python profile but is not RFC 8785/JCS and is not a cross-language standard. | Keep one controlled implementation; define and test a standard canonicalization migration before multi-language signing. |
| SR-05 | Medium | Caller-supplied revocation data can be stale even when present. | Require authenticated freshness metadata, expiry and fail-closed behavior in the future trust service. |
| SR-06 | Medium | CI executes repository-controlled code and installs repository-controlled dependencies on a hosted runner. Token permissions are read-only and checkout credentials are not persisted, but supply-chain isolation remains necessary. | Review untrusted-PR isolation, dependency pinning and repository protections independently. |
| SR-07 | Medium | Evidence source presence and verifier fields do not establish source truth, source authority or reviewer competence. | Independent source validation and audit trail required. |
| SR-08 | Medium | Trusted clock, clock skew and emergency revocation propagation are not implemented. | Define trusted-time and operational incident procedures before real authorization use. |

Severity labels above describe the impact if the reference implementation were used as a production trust service; they are not an independent audit rating.

## Verification evidence

The final CI run for commit 13cdd848780beeb0043986354764b01e9b6babd7 completed successfully (run 40625129839). Project Q: 33/33 tests passed. Project Z: 25/25 tests passed. Total: 58/58 tests passed. The 500-event synthetic benchmark (30 repetitions) reported ingestion median/p95 6.376/7.123 ms, lexical search median/p95 1.509/1.612 ms, and combined pipeline median/p95 7.917/8.735 ms. These are hosted-runner microbenchmark observations, not representative workload or production SLO evidence.

## Independent review required

An independent application-security/cryptography reviewer must inspect the exact final commit, reproduce the tests, assess the findings above, add any further findings, and record an attributable disposition. No reviewer identity is presumed or fabricated.

## Release decision

**Not approved for merge or deployment by this self-review.** Keep PR draft/open. Production remains blocked pending independent review, trust-service design, recovery evidence verification, repository protection review and separate explicit authorization.
