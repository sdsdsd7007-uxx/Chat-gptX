# Project Q — Controlled Foundation

This repository contribution is a **reviewable, non-production foundation**. It does not deploy services, connect external accounts, or authorize production changes.

## Components
- `schemas/evidence-record.schema.json`: JSON Schema Draft 2020-12 contract.
- `src/project_q/release_gate.py`: fail-closed evidence and approval policy evaluator.
- `tests/test_release_gate.py`: allow/deny tests, including signature-tampering cases.
- `.github/workflows/project-q-checks.yml`: pull-request validation workflow with immutable action references.
- `.github/dependabot.yml`: weekly GitHub Actions dependency update proposals.

## Requirements
- Python 3.11+
- `jsonschema[format]>=4.21,<5`
- `cryptography>=44,<48`

Install and test:

```bash
python -m pip install -r project_q/requirements-dev.txt
python -m unittest discover -s project_q/tests -v
```

## Gate behavior
The evaluator validates the record against the schema, requires verified evidence and lifecycle state, checks an unexpired approval bound to the record digest, verifies an Ed25519 signature over the digest and all approval claims, blocks high/critical/unknown risk, and requires a tested recovery plan when recovery is required. Missing trusted keys, invalid signatures, schema errors, and policy errors fail closed.

The caller must supply a trusted public-key registry to `evaluate_release`. The deterministic private key in the test suite is **test-only** and must never be trusted in a real environment. Production key generation, custody, rotation, revocation, approver identity verification, and audit retention require a separately reviewed trust-management service and operating procedure.

The evaluator is a reference policy component. It does not perform deployment. Production promotion remains blocked and requires a separately reviewed release workflow and scoped human authorization.

## Evidence labels
- `SRC`: source record
- `VEF`: verified evidence
- `PRO`: proposal
- `PEN`: pending
- `UNK`: unknown
- `HAC`: historical assistant claim

Never label a claim `VEF` without a recorded verification method and supporting source.


## Policy v1.2.0 hardening
The current security-hardening branch requires source provenance and verifier identity, binds policy version and approval validity window into the Ed25519 signature, accepts an explicit revoked-key set, and requires a recovery-test evidence reference when recovery is required. See [Trust and Approval Lifecycle](TRUST_AND_APPROVAL_LIFECYCLE.md).

The revocation set and trusted public-key map are caller-supplied controls, not a deployed key-management service. Identity proofing, key custody, rotation, revocation freshness, trusted time, and audit operations remain external prerequisites. This evaluator remains non-production and blocks production promotion.
