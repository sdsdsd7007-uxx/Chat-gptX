# Project Q & Z — ASSD Foundation

This repository contains a small, dependency-free foundation for validating telemetry events before they can be considered by the Project QZ master register, plus proposed QQQ architecture, study and integration documentation.

## Implementation baseline
- Versioned telemetry contract: `schemas/telemetry-event.v1.schema.json`
- Fail-closed validator: `src/validate-event.mjs`
- Automated tests: `test/validate-event.test.mjs`
- CI test workflow: `.github/workflows/qz-validation.yml`

## QQQ architecture & sub-project documentation
- [QQQ Master Framework v53.0](docs/QQQ-MASTER-FRAMEWORK-v53.md)
- [QQQ-Mega-Engine v53.2 Master Inventory](docs/QQQ-MEGA-ENGINE-v53.2-MASTER-INVENTORY.md)
- [QQQ-SP1 Integration Vanguard Charter](docs/QQQ-SP1-CHARTER.md)
- [QQQ-SP1 Dashboard Verification Notes](docs/QQQ-SP1-DASHBOARD.md)
- [QQQ Master Sovereign Final Report](docs/QQQ-MASTER-SOVEREIGN-FINAL-REPORT.md)
- [Online Operations Matrix](docs/ONLINE-OPERATIONS-MATRIX.md)
- [Validation Hardening Plan](docs/VALIDATION-HARDENING-PLAN.md)
- [Autopilot Engine Protocol](docs/AUTOPILOT-ENGINE-PROTOCOL.md)

## Study & Knowledge Assimilation
- [QQQ-Study & Knowledge Assimilation Core](docs/QQQ-STUDY-KNOWLEDGE-CORE.md)
- [QQQ-ISP-JassimSultan-Leadership Project](docs/QQQ-ISP-JASSIMSULTAN-LEADERSHIP.md)
- [First Strategic Thinking Executive Synthesis](docs/QQQ-JS-ST-01-EXECUTIVE-SYNTHESIS.md)

The Jassim Sultan study project uses the author's official description and published contents as the initial evidence base. The first synthesis is an original high-level summary, not a substitute for the book; full chapter-by-chapter study and reconciliation of the complete book/programme catalogue remain in progress.

## NextGen AI project family
- [NextGen AI Ecosystem](docs/QQQ-SP-NEXTGEN-AI-ECOSYSTEM.md)
- [Gemini](docs/QQQ-SP-Gemini.md)
- [ChatGPT / OpenAI](docs/QQQ-SP-ChatGPT.md)
- [WebVerse](docs/QQQ-SP-WebVerse.md)
- [NextGenAI Observatory](docs/QQQ-SP-NextGenAI.md)
- [Cross-Platform AI Comparative Evaluation](docs/QQQ-SP-AI-COMPARATIVE-EVALUATION.md)

## Requirements & local checks
Node.js 24.x LTS is the CI target. No third-party runtime dependencies are required.

Run tests:
```sh
node --test
```

Validate one JSON event:
```sh
node src/validate-event.mjs < event.json
```

Exit code 0 means valid; exit code 1 means invalid event or invalid JSON. The validator emits a compact JSON result. Do not send secrets, credentials or unnecessary personal data in telemetry.

## Evidence and production gate
This is a starter implementation and documentation/prototype workspace, not a deployed telemetry or autonomous service. Repository documents and a local dashboard do not themselves connect to cloud storage, Dropbox, Odoo, Gemini, ChatGPT, disaster feeds or production systems. A scheduled review is not a 24/7 live agent.

Live status remains **UNKNOWN** unless a current, direct health check and fresh heartbeat prove otherwise. Production remains **HOLD / NOT APPROVED** until accountable owners and independent reviewers are assigned, permissions are reviewed, current-head CI and staging tests pass, backup/restore and rollback are demonstrated, live telemetry is connected and verified, and an authorized approver signs off.

Financial impact must be classified as forecast, estimated, attributed or realized. A value must not be described as realized unless reconciled to an approved source of record. Do not claim zero latency, zero risk, 100% accuracy, complete web coverage or a cryptographic certification without a defined method and reproducible evidence.
