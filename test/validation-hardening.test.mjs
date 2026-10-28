import test from 'node:test';
import assert from 'node:assert/strict';
import { validateEvent } from '../src/validate-event-core.mjs';

const validEvent = () => ({
  schema_version: '1.0', project: 'QZ', framework: 'ASSD',
  execution_id: 'test-execution-001', event_id: 'test-event-001',
  node_id: 'QZ-TELEMETRY-001', module: 'TELEMETRY',
  event_type: 'validation.test', timestamp_utc: '2026-10-28T09:00:00Z',
  status: 'succeeded', data_quality: 'valid', environment: 'test',
  redaction_status: 'checked'
});

test('rejects optional string fields with wrong types or overlong values', () => {
  assert.equal(validateEvent({ ...validEvent(), owner_id: 42 }).valid, false);
  assert.equal(validateEvent({ ...validEvent(), evidence_reference: 'x'.repeat(2049) }).valid, false);
  assert.equal(validateEvent({ ...validEvent(), source_version: false }).valid, false);
});

test('rejects impossible calendar timestamps even when they end in Z', () => {
  assert.equal(validateEvent({ ...validEvent(), timestamp_utc: '2026-02-30T09:00:00Z' }).valid, false);
  assert.equal(validateEvent({ ...validEvent(), timestamp_utc: '2026-10-28T09:00Z' }).valid, false);
});

test('rejects extra nested financial fields and wrong optional field types', () => {
  assert.equal(validateEvent({
    ...validEvent(),
    financial_impact: {
      classification: 'estimated', currency: 'UGX', value: 12,
      note: 'uncontracted field'
    }
  }).valid, false);
  assert.equal(validateEvent({
    ...validEvent(),
    financial_impact: {
      classification: 'estimated', currency: 'UGX', value: 12,
      source_reference: 123
    }
  }).valid, false);
});

test('rejects non-finite numeric values', () => {
  assert.equal(validateEvent({ ...validEvent(), duration_ms: Number.POSITIVE_INFINITY }).valid, false);
  assert.equal(validateEvent({
    ...validEvent(),
    financial_impact: { classification: 'estimated', currency: 'UGX', value: Number.NaN }
  }).valid, false);
});

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

test('schema declares primitive types for optional and nested financial fields', () => {
  const here = dirname(fileURLToPath(import.meta.url));
  const schema = JSON.parse(readFileSync(resolve(here, '../schemas/telemetry-event.v1.schema.json'), 'utf8'));
  assert.equal(schema.properties.owner_id.type, 'string');
  assert.equal(schema.properties.evidence_reference.type, 'string');
  assert.equal(schema.properties.source_version.type, 'string');
  assert.equal(schema.properties.financial_impact.properties.source_reference.type, 'string');
  assert.equal(schema.properties.financial_impact.properties.reconciled.type, 'boolean');
  assert.equal(schema.properties.financial_impact.properties.value.type, 'number');
});
