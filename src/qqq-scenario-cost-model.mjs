const requiredFields = [
  'supplier_share_pct',
  'freight_share_pct',
  'local_share_pct',
  'supplier_price_change_pct',
  'freight_change_pct',
  'fx_change_pct',
  'local_cost_change_pct'
];

const allowedFields = new Set(requiredFields);
const MAX_ABSOLUTE_SHOCK_PCT = 500;
const EPSILON = 1e-9;

/**
 * Compute a bounded deterministic cost-sensitivity index for a synthetic basket.
 * Shares are baseline cost shares summing to 100. Positive FX change means
 * depreciation of the local currency against the invoicing currency.
 * This pure function performs no network access, persistence, or execution.
 */
export function calculateScenarioCostIndex(input) {
  if (input === null || typeof input !== 'object' || Array.isArray(input)) {
    throw new TypeError('input must be a JSON object');
  }

  const errors = [];
  for (const field of requiredFields) {
    if (!Object.hasOwn(input, field)) errors.push('missing field: ' + field);
  }
  for (const field of Object.keys(input)) {
    if (!allowedFields.has(field)) errors.push('unsupported field: ' + field);
  }
  for (const field of requiredFields) {
    if (Object.hasOwn(input, field)) {
      if (typeof input[field] !== 'number' || !Number.isFinite(input[field])) {
        errors.push(field + ' must be a finite number');
      }
    }
  }
  if (errors.length) throw new TypeError(errors.join('; '));

  const shares = [input.supplier_share_pct, input.freight_share_pct, input.local_share_pct];
  if (shares.some((value) => value < 0 || value > 100)) {
    throw new RangeError('cost shares must be between 0 and 100');
  }
  if (Math.abs(shares.reduce((sum, value) => sum + value, 0) - 100) > EPSILON) {
    throw new RangeError('supplier, freight and local cost shares must sum to 100');
  }

  const shocks = [
    input.supplier_price_change_pct,
    input.freight_change_pct,
    input.fx_change_pct,
    input.local_cost_change_pct
  ];
  if (shocks.some((value) => value < -100 || value > MAX_ABSOLUTE_SHOCK_PCT)) {
    throw new RangeError('each percentage change must be between -100 and 500');
  }

  const fxFactor = 1 + input.fx_change_pct / 100;
  const supplierCost = input.supplier_share_pct *
    (1 + input.supplier_price_change_pct / 100) * fxFactor;
  const freightCost = input.freight_share_pct *
    (1 + input.freight_change_pct / 100) * fxFactor;
  const localCost = input.local_share_pct *
    (1 + input.local_cost_change_pct / 100);
  const costIndex = supplierCost + freightCost + localCost;
  if (!Number.isFinite(costIndex)) throw new RangeError('computed cost index is not finite');

  const round4 = (value) => Math.round((value + Number.EPSILON) * 10000) / 10000;
  return {
    baseline_index: 100,
    cost_index: round4(costIndex),
    change_pct: round4(costIndex - 100),
    components: {
      supplier: round4(supplierCost),
      freight_and_insurance: round4(freightCost),
      local_and_other: round4(localCost)
    },
    assumptions: { ...input },
    status: 'SYNTHETIC_SCENARIO_ONLY_NOT_A_FORECAST'
  };
}
