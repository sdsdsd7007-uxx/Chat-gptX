const evidenceStates = new Set([
  'VERIFIED',
  'REPORTED',
  'INFERRED',
  'HYPOTHESIS',
  'UNKNOWN',
  'BLOCKED'
]);

const requiredFields = [
  'contract_version',
  'run_id',
  'record_id',
  'source_id',
  'source_ref',
  'retrieved_at_utc',
  'claim',
  'evidence_state',
  'evidence_refs',
  'uncertainty'
];

const allowedFields = new Set([...requiredFields, 'reason']);
const stringLimits = {
  run_id: 128,
  record_id: 128,
  source_id: 128,
  source_ref: 2048,
  claim: 4000,
  uncertainty: 1000,
  reason: 1000
};

const isRecord = (value) =>
  value !== null && typeof value === 'object' && !Array.isArray(value);

function isRealUtcTimestamp(value) {
  if (typeof value !== 'string') return false;
  const match = value.match(
    /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?Z$/
  );
  if (!match) return false;

  const instant = new Date(value);
  return !Number.isNaN(instant.getTime()) &&
    Number(match[1]) >= 1 &&
    instant.getUTCFullYear() === Number(match[1]) &&
    instant.getUTCMonth() + 1 === Number(match[2]) &&
    instant.getUTCDate() === Number(match[3]) &&
    instant.getUTCHours() === Number(match[4]) &&
    instant.getUTCMinutes() === Number(match[5]) &&
    instant.getUTCSeconds() === Number(match[6]);
}

/**
 * Validate one offline DIIP evidence envelope.
 * This pure function performs no network access, persistence, or execution.
 */
export function validateDiipEnvelope(envelope) {
  const errors = [];
  if (!isRecord(envelope)) {
    return { valid: false, errors: ['envelope must be a JSON object'] };
  }

  for (const key of requiredFields) {
    if (!Object.hasOwn(envelope, key)) {
      errors.push('missing required field: ' + key);
    }
  }
  for (const key of Object.keys(envelope)) {
    if (!allowedFields.has(key)) {
      errors.push('unsupported field: ' + key);
    }
  }

  if ('contract_version' in envelope && envelope.contract_version !== '1.0') {
    errors.push('contract_version must be 1.0');
  }

  for (const [key, max] of Object.entries(stringLimits)) {
    if (key in envelope) {
      const value = envelope[key];
      if (typeof value !== 'string') {
        errors.push(key + ' must be a string');
      } else if (value.trim() === '' || value.length > max) {
        errors.push(key + ' must be non-empty and at most ' + max + ' characters');
      }
    }
  }

  if ('retrieved_at_utc' in envelope && !isRealUtcTimestamp(envelope.retrieved_at_utc)) {
    errors.push('retrieved_at_utc must be a real UTC ISO timestamp ending in Z');
  }

  if ('evidence_state' in envelope && !evidenceStates.has(envelope.evidence_state)) {
    errors.push('invalid evidence_state');
  }

  if ('evidence_refs' in envelope) {
    if (!Array.isArray(envelope.evidence_refs)) {
      errors.push('evidence_refs must be an array');
    } else {
      if (envelope.evidence_refs.length > 32) {
        errors.push('evidence_refs must contain at most 32 items');
      }
      envelope.evidence_refs.forEach((ref, index) => {
        if (typeof ref !== 'string' || ref.trim() === '' || ref.length > 2048) {
          errors.push('evidence_refs[' + index + '] must be a non-empty string of at most 2048 characters');
        }
      });
    }
  }

  if (
    evidenceStates.has(envelope.evidence_state) &&
    !['UNKNOWN', 'BLOCKED'].includes(envelope.evidence_state) &&
    Array.isArray(envelope.evidence_refs) &&
    envelope.evidence_refs.length === 0
  ) {
    errors.push('evidence_refs must not be empty for a supported evidence state');
  }

  if (
    ['UNKNOWN', 'BLOCKED'].includes(envelope.evidence_state) &&
    (typeof envelope.reason !== 'string' || envelope.reason.trim() === '')
  ) {
    errors.push('UNKNOWN or BLOCKED evidence_state requires a non-empty reason');
  }

  return { valid: errors.length === 0, errors };
}
