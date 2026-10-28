import test from 'node:test';
import assert from 'node:assert/strict';
import { validateDiipEnvelope } from '../src/qqq-diip-contract.mjs';

const validEnvelope = () => ({
  contract_version: '1.0',
  run_id: 'synthetic-run-001',
  record_id: 'synthetic-record-001',
  source_id: 'synthetic-source-001',
  source_ref: 'fixture://synthetic/source-001',
  retrieved_at_utc: '2026-10-28T12:00:00Z',
  claim: 'Synthetic fixture: inventory count equals three.',
  evidence_state: 'VERIFIED',
  evidence_refs: ['fixture://synthetic/source-001#item-1'],
  uncertainty: 'Synthetic fixture only; not a real-world finding.'
});

test('accepts a supported synthetic evidence envelope', () => {
  assert.deepEqual(validateDiipEnvelope(validEnvelope()), { valid: true, errors: [] });
});

test('accepts explicit UNKNOWN with no evidence refs and a reason', () => {
  const envelope = {
    ...validEnvelope(),
    evidence_state: 'UNKNOWN',
    evidence_refs: [],
    reason: 'The synthetic fixture does not establish this claim.'
  };
  assert.deepEqual(validateDiipEnvelope(envelope), { valid: true, errors: [] });
});

test('rejects missing source identity', () => {
  const envelope = validEnvelope();
  delete envelope.source_id;
  const result = validateDiipEnvelope(envelope);
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('source_id')));
});

test('rejects impossible UTC dates', () => {
  const result = validateDiipEnvelope({
    ...validEnvelope(),
    retrieved_at_utc: '2026-02-30T12:00:00Z'
  });
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('retrieved_at_utc')));
});

test('rejects a supported evidence state without evidence references', () => {
  const result = validateDiipEnvelope({ ...validEnvelope(), evidence_refs: [] });
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('evidence_refs must not be empty')));
});

test('rejects UNKNOWN without an explanatory reason', () => {
  const envelope = { ...validEnvelope(), evidence_state: 'UNKNOWN', evidence_refs: [] };
  const result = validateDiipEnvelope(envelope);
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('requires a non-empty reason')));
});

test('rejects unsupported evidence states', () => {
  const result = validateDiipEnvelope({ ...validEnvelope(), evidence_state: 'CERTAIN' });
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('invalid evidence_state')));
});

test('rejects a recommendation embedded in the intelligence envelope', () => {
  const result = validateDiipEnvelope({
    ...validEnvelope(),
    recommendation: { action: 'activate-production' }
  });
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('unsupported field: recommendation')));
});

test('rejects non-object input', () => {
  assert.deepEqual(validateDiipEnvelope(null), {
    valid: false,
    errors: ['envelope must be a JSON object']
  });
});
