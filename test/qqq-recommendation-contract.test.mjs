import test from 'node:test';
import assert from 'node:assert/strict';
import { validateRecommendationSet } from '../src/qqq-recommendation-contract.mjs';

const option = (overrides = {}) => ({
  recommendation_id: 'rec-001',
  linked_finding_ids: ['finding-001'],
  title: 'Run a synthetic offline evaluation',
  rationale: 'Test the contract before any integration.',
  evidence_state: 'SUPPORTED',
  trade_offs: ['Limited realism because all inputs are synthetic.'],
  acceptance_criteria: ['All deterministic contract tests pass.'],
  rollback_plan: 'Revert the feature-branch commit.',
  owner_role: 'implementation owner',
  reviewer_role: 'independent reviewer',
  gate: 'RECOMMEND',
  ...overrides
});

const set = (overrides = {}) => ({
  contract_version: '1.0',
  report_id: 'report-001',
  created_at_utc: '2026-10-29T07:00:00Z',
  recommendations: [option()],
  ...overrides
});

test('accepts a complete recommendation set separate from intelligence findings', () => {
  assert.deepEqual(validateRecommendationSet(set()), { valid: true, errors: [] });
});

test('rejects a non-object recommendation set', () => {
  assert.equal(validateRecommendationSet(null).valid, false);
});

test('rejects unsupported set fields and embedded execution commands', () => {
  const result = validateRecommendationSet(set({ execute_now: true }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('unsupported set field: execute_now')));
});

test('rejects an invalid timestamp', () => {
  const result = validateRecommendationSet(set({ created_at_utc: '2026-02-30T07:00:00Z' }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('created_at_utc')));
});

test('requires at least one option', () => {
  const result = validateRecommendationSet(set({ recommendations: [] }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('at least one option')));
});

test('requires evidence links, trade-offs, acceptance criteria and rollback', () => {
  const result = validateRecommendationSet(set({
    recommendations: [option({ linked_finding_ids: [], trade_offs: [], acceptance_criteria: [], rollback_plan: '' })]
  }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('linked_finding_ids')));
  assert.ok(result.errors.some((error) => error.includes('trade_offs')));
  assert.ok(result.errors.some((error) => error.includes('acceptance_criteria')));
  assert.ok(result.errors.some((error) => error.includes('rollback_plan')));
});

test('does not allow unsupported evidence to receive a RECOMMEND gate', () => {
  const result = validateRecommendationSet(set({
    recommendations: [option({ evidence_state: 'NEEDS_EVIDENCE', gate: 'RECOMMEND' })]
  }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('RECOMMEND gate requires SUPPORTED evidence')));
});

test('requires HOLD for blocked evidence', () => {
  const result = validateRecommendationSet(set({
    recommendations: [option({ evidence_state: 'BLOCKED', gate: 'HUMAN_APPROVAL' })]
  }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('BLOCKED evidence requires HOLD gate')));
});

test('requires owner and reviewer roles to be distinct', () => {
  const result = validateRecommendationSet(set({
    recommendations: [option({ owner_role: 'same role', reviewer_role: 'same role' })]
  }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('must be distinct roles')));
});

test('rejects execution payloads inside an option', () => {
  const result = validateRecommendationSet(set({
    recommendations: [{ ...option(), tool_call: { action: 'write' } }]
  }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('unsupported field: tool_call')));
});

test('rejects duplicate recommendation IDs across options', () => {
  const result = validateRecommendationSet(set({
    recommendations: [
      option({ recommendation_id: 'rec-duplicate' }),
      option({ recommendation_id: 'rec-duplicate', title: 'A second option with a conflicting ID' })
    ]
  }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('duplicate recommendation_id: rec-duplicate')));
});

test('rejects duplicate linked finding IDs within an option', () => {
  const result = validateRecommendationSet(set({
    recommendations: [option({ linked_finding_ids: ['finding-001', 'finding-001'] })]
  }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('duplicate linked_finding_ids entry')));
});

test('returns stable validation output for the same input', () => {
  const input = set({
    recommendations: [
      option({ recommendation_id: 'rec-duplicate' }),
      option({ recommendation_id: 'rec-duplicate' })
    ]
  });
  assert.deepEqual(validateRecommendationSet(input), validateRecommendationSet(input));
});

test('normalizes surrounding whitespace when checking recommendation IDs', () => {
  const result = validateRecommendationSet(set({
    recommendations: [
      option({ recommendation_id: 'rec-normalized' }),
      option({ recommendation_id: '  rec-normalized  ' })
    ]
  }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('duplicate recommendation_id: rec-normalized')));
});

test('normalizes surrounding whitespace when checking linked finding IDs', () => {
  const result = validateRecommendationSet(set({
    recommendations: [option({ linked_finding_ids: ['finding-002', ' finding-002 '] })]
  }));
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('duplicate linked_finding_ids entry')));
});
