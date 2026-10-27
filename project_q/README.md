# Project Q — Controlled Foundation

This repository contribution is a **reviewable, non-production foundation**. It does not deploy services, connect external accounts, or authorize production changes.

## Components
- `schemas/evidence-record.schema.json`: JSON Schema Draft 2020-12 contract.
- `src/project_q/release_gate.py`: fail-closed evidence and approval gate.
- `tests/test_release_gate.py`: unit tests for allow and deny paths.
- `.github/workflows/project-q-checks.yml`: pull-request validation workflow.

## Requirements
- Python 3.11+
- `jsonschema[format]>=4.21,<5`

Install and test:

```bash
python -m pip install -r project_q/requirements-dev.txt
python -m unittest discover -s project_q/tests -v
```

## Gate behavior
The gate validates the record against the pinned schema, requires verified evidence and lifecycle state, requires an unexpired approval bound to the record digest, blocks critical/unknown risk, and requires a tested recovery plan when recovery is required. Any validation or policy error denies release.

The gate is a reference policy component. It does not perform deployment. Production promotion requires a separately reviewed workflow and scoped human authorization.

## Evidence labels
- `SRC`: source record
- `VEF`: verified evidence
- `PRO`: proposal
- `PEN`: pending
- `UNK`: unknown
- `HAC`: historical assistant claim

Never label a claim `VEF` without a recorded verification method and supporting source.
