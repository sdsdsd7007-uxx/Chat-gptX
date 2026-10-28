# Project Q & Z — ASSD Foundation

This branch introduces a small, dependency-free foundation for validating telemetry events before they can be considered by the Project QZ master register.

## Scope
- Versioned telemetry contract: schemas/telemetry-event.v1.schema.json
- Fail-closed validator: src/validate-event.mjs
- Automated tests: test/validate-event.test.mjs
- CI test workflow: .github/workflows/qz-validation.yml

This is a starter implementation, not a deployed telemetry service. It does not connect to production systems, write to a master register, route to a backup channel, or execute autonomous actions.

## Requirements
Node.js 20 or newer. No third-party runtime dependencies.

## Run tests
Run: node --test

## Validate one JSON event
Run: node src/validate-event.mjs < event.json

Exit code 0 means valid; exit code 1 means invalid event or invalid JSON. The validator emits a compact JSON result. Do not send secrets, credentials, or unnecessary personal data in telemetry.

## Production gate
Production remains HOLD / NOT APPROVED until owners are assigned, permissions are reviewed, staging tests pass with evidence, backup/restore and rollback are demonstrated, telemetry is connected and verified, and an independent approver signs off.

Financial impact must be classified as forecast, estimated, attributed, or realized. A value must not be described as realized unless it is reconciled to an approved source of record.
