# Project Q & Z — ASSD Foundation

This branch introduces a small, dependency-free foundation for validating telemetry events before they can be considered by the Project QZ master register.

## Scope
- Versioned telemetry contract: schemas/telemetry-event.v1.schema.json
- Fail-closed validator: src/validate-event.mjs
- Automated tests: test/validate-event.test.mjs
- CI test workflow: .github/workflows/qz-validation.yml
- Governed study/update engine: src/assd-autopilot.mjs
- MCU, CERE, ARRE and IPSU evaluators: src/engines/subengines.mjs
- Example tuning config: config/assd-engine-config.example.json
- Engine governance: docs/ASSD-AUTOPILOT.md

This is a starter implementation, not a deployed telemetry service. It does not connect to production systems, write to a master register, route to a backup channel, or execute autonomous actions.

## Requirements
Node.js 24.x LTS is the CI target. No third-party runtime dependencies are required.

## Run tests
Run: node --test

## ASSD autopilot study cycle
Use `runStudyCycle(study, config)` to validate study metadata, evaluate MCU/CERE/ARRE/IPSU signals, and create a proposal only when evidence, confidence and subengine gates pass. `applyApprovedEngineUpdate(config, proposal, approval)` applies an allowlisted config adjustment only after a separate reviewer approves the exact proposal and version. See docs/ASSD-AUTOPILOT.md.

The autopilot does not rewrite its own source code or bypass safety/compliance gates. It proposes bounded configuration changes; it does not auto-approve or deploy them.

## Validate one JSON event
Run: node src/validate-event.mjs < event.json

Exit code 0 means valid; exit code 1 means invalid event or invalid JSON. The validator emits a compact JSON result. Do not send secrets, credentials, or unnecessary personal data in telemetry.

## Production gate
Production remains HOLD / NOT APPROVED until owners are assigned, permissions are reviewed, staging tests pass with evidence, backup/restore and rollback are demonstrated, telemetry is connected and verified, and an independent approver signs off.

Financial impact must be classified as forecast, estimated, attributed, or realized. A value must not be described as realized unless it is reconciled to an approved source of record.
