# Project Q & Z — Validation Hardening and Release Gates

**Status:** remediation plan; not a production approval  
**Scope:** QZ / ASSD telemetry validation foundation

## Implemented in this change
- Strengthen JSON Schema primitive types for optional string fields and nested financial-impact fields.
- Add regression tests for impossible timestamps, optional-field type/length violations, unsupported nested financial fields, and non-finite numeric values.

## Required next actions

| Priority | Action | Evidence required | Release gate |
|---|---|---|---|
| P1 | Keep JSON Schema and runtime validator behavior aligned | Contract test matrix covering required, optional, boundary, and nested fields | No known schema/validator disagreement |
| P2 | Define event identity and idempotency policy | Approved key (for example, source + event_id), replay tests, collision behavior | Duplicate/replay behavior proven in staging |
| P3 | Add quarantine and conflict handling at the ingestion boundary | Tests for malformed, duplicate, conflicting, and late events; audit trail | Fail-closed behavior and recovery verified |
| P4 | Establish source-of-truth register ownership | Register with record ID, owner, independent reviewer, source, version, status, evidence, last verified, next review | Every production record has accountable ownership |
| P5 | Verify integration boundaries | Staging evidence for Dropbox/Odoo connectors, permissions, retry limits, rate limits, and secret handling | No production credentials in code or telemetry |
| P6 | Prove resilience | Backup/restore, channel failover, rollback, and interrupted-sync tests with timestamps and results | Recovery objectives met and independently reviewed |
| P7 | Approve release | Signed review, risk acceptance, test run links, deployment/rollback plan | Explicit approval from authorized owner |

## Operational metrics to instrument
- Invalid-event rate and reasons
- Duplicate/replay rate
- End-to-end event latency (p50/p95/p99)
- Retry success and dead-letter/quarantine counts
- Sync backlog and oldest pending event
- Restore time and verified recovery point
- Schema/validator version mismatch count

Each metric needs a definition, measurement window, owner, threshold, and response playbook before it can be used as an operational KPI.

## Safety rules
- Treat missing telemetry as **unknown**, not success.
- Do not label a financial value “realized” without reconciled source evidence.
- Do not automatically execute consequential actions based solely on telemetry.
- Keep production disabled until staging evidence and independent approval are complete.
- Never store passwords, API tokens, private keys, or unnecessary personal data in events or audit records.
