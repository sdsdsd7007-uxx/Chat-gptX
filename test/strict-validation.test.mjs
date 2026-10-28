import test from 'node:test';
import assert from 'node:assert/strict';
import { validateEvent } from '../src/validate-event-core.mjs';

const event = () => ({
  schema_version:'1.0', project:'QZ', framework:'ASSD',
  execution_id:'strict-validation-execution', event_id:'strict-validation-event',
  node_id:'QZ-TELEMETRY-001', module:'TELEMETRY', event_type:'strict.test',
  timestamp_utc:'2026-10-28T09:00:00Z', status:'succeeded',
  data_quality:'valid', environment:'test', redaction_status:'checked'
});

test('accepts strict UTC timestamps with optional fractional seconds', () => {
  assert.equal(validateEvent({ ...event(), timestamp_utc:'2026-10-28T09:00:00.123Z' }).valid, true);
});

test('rejects UTC timestamps without seconds', () => {
  const result = validateEvent({ ...event(), timestamp_utc:'2026-10-28T09:00Z' });
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((item) => item.includes('timestamp_utc')));
});

test('rejects identifiers longer than the declared schema maximum', () => {
  const result = validateEvent({ ...event(), event_id:'e'.repeat(129) });
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((item) => item.includes('event_id length')));
});

test('rejects non-boolean reconciliation metadata', () => {
  const result = validateEvent({
    ...event(),
    financial_impact:{ classification:'estimated', currency:'UGX', value:100, reconciled:'yes' }
  });
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((item) => item.includes('reconciled must be boolean')));
});
test('rejects impossible calendar dates', () => {
  const result = validateEvent({ ...event(), timestamp_utc:'2026-02-31T09:00:00Z' });
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((item) => item.includes('timestamp_utc')));
});
