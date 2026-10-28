import test from 'node:test';
import assert from 'node:assert/strict';
import { calculateScenarioCostIndex } from '../src/qqq-scenario-cost-model.mjs';

const base = (overrides = {}) => ({
  supplier_share_pct: 65,
  freight_share_pct: 20,
  local_share_pct: 15,
  supplier_price_change_pct: 0,
  freight_change_pct: 0,
  fx_change_pct: 0,
  local_cost_change_pct: 0,
  ...overrides
});

test('baseline index is 100 with no shocks', () => {
  const result = calculateScenarioCostIndex(base());
  assert.equal(result.cost_index, 100);
  assert.equal(result.change_pct, 0);
  assert.equal(result.status, 'SYNTHETIC_SCENARIO_ONLY_NOT_A_FORECAST');
});

test('reproduces the managed-stress calculation', () => {
  const result = calculateScenarioCostIndex(base({
    supplier_price_change_pct: 3,
    freight_change_pct: 15,
    fx_change_pct: 5
  }));
  assert.equal(result.cost_index, 109.4475);
  assert.equal(result.change_pct, 9.4475);
});

test('reproduces the severe-stress calculation', () => {
  const result = calculateScenarioCostIndex(base({
    supplier_price_change_pct: 5,
    freight_change_pct: 30,
    fx_change_pct: 8
  }));
  assert.equal(result.cost_index, 116.79);
  assert.equal(result.change_pct, 16.79);
});

test('reproduces the recovery/easing calculation', () => {
  const result = calculateScenarioCostIndex(base({
    freight_change_pct: -10,
    fx_change_pct: -2
  }));
  assert.equal(result.cost_index, 96.34);
  assert.equal(result.change_pct, -3.66);
});

test('keeps component totals consistent with the resulting index', () => {
  const result = calculateScenarioCostIndex(base({
    supplier_price_change_pct: 3,
    freight_change_pct: 15,
    fx_change_pct: 5
  }));
  const sum = Object.values(result.components).reduce((total, part) => total + part, 0);
  assert.ok(Math.abs(sum - result.cost_index) < 1e-10);
});

test('rejects missing required fields', () => {
  const input = base();
  delete input.fx_change_pct;
  assert.throws(() => calculateScenarioCostIndex(input), /missing field: fx_change_pct/);
});

test('rejects cost shares that do not sum to 100', () => {
  assert.throws(() => calculateScenarioCostIndex(base({ local_share_pct: 14 })), /must sum to 100/);
});

test('rejects non-finite values', () => {
  assert.throws(() => calculateScenarioCostIndex(base({ freight_change_pct: Infinity })), /finite number/);
});

test('rejects changes below minus 100 percent and out-of-policy shocks', () => {
  assert.throws(() => calculateScenarioCostIndex(base({ fx_change_pct: -101 })), /between -100 and 500/);
  assert.throws(() => calculateScenarioCostIndex(base({ supplier_price_change_pct: 501 })), /between -100 and 500/);
});

test('rejects unknown fields and non-object input', () => {
  assert.throws(() => calculateScenarioCostIndex({ ...base(), run_live: true }), /unsupported field: run_live/);
  assert.throws(() => calculateScenarioCostIndex(null), /input must be a JSON object/);
});
