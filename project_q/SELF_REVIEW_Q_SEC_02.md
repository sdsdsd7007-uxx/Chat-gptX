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
| SR-09 | High | GitHub API inspection reported branch protection disabled on both main and project-q/controlled-foundation; required status checks/enforcement were off. | Repository owner must configure protected branches/rulesets, require independent review and passing CI, restrict bypass, and verify the effective settings. This connector cannot configure repository administration settings. |\n| SR-10 | High | The SQLite replay helper accepts a caller-supplied `GateDecision`; a Python caller can construct this dataclass directly. Its digest/policy binding and database uniqueness do not authenticate the decision or prove that the signature was verified. | Treat the helper only as a storage primitive behind a separately trusted in-process boundary. Do not expose it as an authorization API. Production use requires a service boundary that verifies signed claims against fresh authenticated trust/revocation data before atomic consumption. |
| SR-11 | Medium | Earlier schema revisions allowed duplicate source-record identifiers and whitespace-only provenance/method strings, weakening provenance quality even though records were structurally present. | Added `uniqueItems` and non-whitespace patterns for root/evidence source records, source-document references, verification method and verifier identity; added four regression tests. Re-run CI and obtain independent review of the final head. |

Severity labels above describe the impact if the reference implementation were used as a production trust service; they are not an independent audit rating.

## Verification evidence

Earlier CI run #105 passed on head `25fa11ca149646533cd93b0b6f5ba453fb6c1799`: Project Q 42/42, Project Z 25/25, total 67/67. The 500-event synthetic benchmark (30 repetitions) reported ingestion median/p95 5.241/5.595 ms, lexical search 1.207/1.314 ms, and combined pipeline 6.455/6.854 ms. This is historical evidence for that earlier head only; it does not verify the later provenance-schema, regression-test, CODEOWNERS or workflow-trigger changes. A fresh CI run on the final head is required before this review record can be considered current. These hosted-runner microbenchmarks are not representative workload or production SLO evidence. Runs #98–#102 exposed replay-ledger interface and semantic-version validation defects; both were corrected before run #105.

## Independent review required

An independent application-security/cryptography reviewer must inspect the exact final commit, reproduce the tests, assess the findings above, add any further findings, and record an attributable disposition. No reviewer identity is presumed or fabricated.

## Release decision

**Not approved for merge or deployment by this self-review.** Keep PR draft/open. Production remains blocked pending independent review, trust-service design, recovery evidence verification, repository protection configuration and verification, and separate explicit authorization.
