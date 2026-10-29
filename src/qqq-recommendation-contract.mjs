const setFields = [
  'contract_version',
  'report_id',
  'created_at_utc',
  'recommendations'
];

const recommendationFields = [
  'recommendation_id',
  'linked_finding_ids',
  'title',
  'rationale',
  'evidence_state',
  'trade_offs',
  'acceptance_criteria',
  'rollback_plan',
  'owner_role',
  'reviewer_role',
  'gate'
];

const gates = new Set(['RECOMMEND', 'NEEDS_EVIDENCE', 'HUMAN_APPROVAL', 'HOLD']);
const evidenceStates = new Set(['SUPPORTED', 'NEEDS_EVIDENCE', 'BLOCKED']);
const isRecord = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);

function isUtcTimestamp(value) {
  if (typeof value !== 'string') return false;
  const match = value.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?Z$/);
  if (!match) return false;
  const date = new Date(value);
  return !Number.isNaN(date.getTime()) &&
    date.getUTCFullYear() === Number(match[1]) &&
    date.getUTCMonth() + 1 === Number(match[2]) &&
    date.getUTCDate() === Number(match[3]) &&
    date.getUTCHours() === Number(match[4]) &&
    date.getUTCMinutes() === Number(match[5]) &&
    date.getUTCSeconds() === Number(match[6]);
}

function nonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function nonEmptyStringArray(value) {
  return Array.isArray(value) && value.length > 0 && value.every(nonEmptyString);
}

/**
 * Validate a Recommendation Set separately from the Intelligence Report.
 * This pure offline contract ranks no options and executes no actions.
 */
export function validateRecommendationSet(input) {
  const errors = [];
  if (!isRecord(input)) {
    return { valid: false, errors: ['recommendation set must be a JSON object'] };
  }

  for (const field of setFields) {
    if (!Object.hasOwn(input, field)) errors.push('missing required field: ' + field);
  }
  for (const field of Object.keys(input)) {
    if (!setFields.includes(field)) errors.push('unsupported set field: ' + field);
  }

  if ('contract_version' in input && input.contract_version !== '1.0') {
    errors.push('contract_version must be 1.0');
  }
  if ('report_id' in input && !nonEmptyString(input.report_id)) {
    errors.push('report_id must be a non-empty string');
  }
  if ('created_at_utc' in input && !isUtcTimestamp(input.created_at_utc)) {
    errors.push('created_at_utc must be a real UTC ISO timestamp ending in Z');
  }
  if ('recommendations' in input) {
    if (!Array.isArray(input.recommendations)) {
      errors.push('recommendations must be an array');
    } else if (input.recommendations.length === 0) {
      errors.push('recommendations must contain at least one option');
    } else {
      input.recommendations.forEach((option, index) => {
        const prefix = 'recommendations[' + index + ']';
        if (!isRecord(option)) {
          errors.push(prefix + ' must be a JSON object');
          return;
        }
        for (const field of recommendationFields) {
          if (!Object.hasOwn(option, field)) errors.push(prefix + ' missing required field: ' + field);
        }
        for (const field of Object.keys(option)) {
          if (!recommendationFields.includes(field)) {
            errors.push(prefix + ' unsupported field: ' + field);
          }
        }
        for (const field of [
          'recommendation_id', 'title', 'rationale', 'rollback_plan', 'owner_role', 'reviewer_role'
        ]) {
          if (field in option && !nonEmptyString(option[field])) {
            errors.push(prefix + ' ' + field + ' must be a non-empty string');
          }
        }
        for (const field of ['linked_finding_ids', 'trade_offs', 'acceptance_criteria']) {
          if (field in option && !nonEmptyStringArray(option[field])) {
            errors.push(prefix + ' ' + field + ' must be a non-empty array of non-empty strings');
          }
        }
        if ('evidence_state' in option && !evidenceStates.has(option.evidence_state)) {
          errors.push(prefix + ' invalid evidence_state');
        }
        if ('gate' in option && !gates.has(option.gate)) {
          errors.push(prefix + ' invalid gate');
        }
        if (option.evidence_state !== 'SUPPORTED' && option.gate === 'RECOMMEND') {
          errors.push(prefix + ' RECOMMEND gate requires SUPPORTED evidence');
        }
        if (option.evidence_state === 'BLOCKED' && option.gate !== 'HOLD') {
          errors.push(prefix + ' BLOCKED evidence requires HOLD gate');
        }
        if (option.owner_role && option.reviewer_role &&
            option.owner_role.trim().toLowerCase() === option.reviewer_role.trim().toLowerCase()) {
          errors.push(prefix + ' owner_role and reviewer_role must be distinct roles');
        }
      });
    }
  }

  return { valid: errors.length === 0, errors };
}
