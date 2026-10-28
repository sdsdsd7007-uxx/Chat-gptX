# Project Q Security Hardening — Independent Review Brief

**Review status:** requested; not yet performed  
**Branch:** `project-q/security-hardening-q-sec-02`  
**Policy version:** 1.2.0  
**Environment:** non-production only; synthetic fixtures only.

## Review objective
Independently assess the provenance requirements, approval envelope, signature binding, time validity, revocation input, recovery evidence and regression tests introduced by this branch. This review is not merge or deployment authorization.

## Required expertise
Independent Python application-security and applied-cryptography experience; familiarity with JSON Schema, authorization systems and GitHub Actions. Reviewer should be independent of the implementation author and disclose conflicts.

## Review scope
1. JSON Schema: root and nested source-record provenance; source URL/document alternatives; verifier identity and timestamp; recovery evidence reference.
2. Cryptographic binding: artifact digest, approval status/reference, environment, scopes, policy version, key ID, not-before and expiry.
3. Revocation: behavior when key ID is revoked; freshness, authenticity and emergency propagation of the external revocation source.
4. Time: timezone handling, exact validity boundaries, expiry ordering and clock-skew assumptions.
5. Trust model: signer identity proofing, key custody, rotation, compromise, historical verification and separation of duties.
6. Recovery: verify that referenced recovery evidence is authentic, current and from the relevant environment.
7. CI/repository: workflow permissions, untrusted PR boundaries, immutable action pins, branch protection and required status checks.
8. Regression coverage and compatibility implications of policy version 1.2.0.

## Adversarial cases
- Missing or empty source references, verifier identity or timestamps.
- Source document/URL absent or conflicting.
- Tampered digest, key ID, policy version, scopes, environment, reference, not-before or expiry.
- Revoked, unknown, malformed or wrong-length public key; malformed signature.
- Future not-before, exact expiry boundary, expiry before not-before, naive timestamps and clock skew.
- Missing or fabricated recovery evidence references.
- Schema downgrade, unknown fields, duplicate JSON keys and cross-language canonicalization differences.
- Untrusted pull-request workflow attempting token or secret access.

## Required findings format
For each finding: ID, severity (Critical/High/Medium/Low/Informational), affected file/line, impact, reproducible evidence, remediation, regression test and residual risk.

## Required conclusion
Choose one:
- Approve for continued non-production development
- Request changes
- Unable to conclude

Record reviewer identity, relevant experience, conflict disclosure, exact commit SHA, review date, coverage and residual risks.

## Known limitations
The revocation set and trusted public-key map are caller-supplied. There is no key-management service, identity-proofing system, trusted-time service, automated revocation distribution, or independent recovery-evidence verifier. The evaluator deliberately blocks production. Passing CI is not security certification.
