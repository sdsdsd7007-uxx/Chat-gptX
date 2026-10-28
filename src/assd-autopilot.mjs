import { evaluateAllSubengines } from './engines/subengines.mjs';

const TUNABLE_PATHS = Object.freeze({
  'routing.confidenceThreshold': { type: 'number', min: 0.75, max: 0.99 },
  'telemetry.maxRetryCount': { type: 'integer', min: 0, max: 5 },
  'kpi.alertTolerancePercent': { type: 'number', min: 0, max: 25 },
  'resourceEfficiency.targetPercent': { type: 'number', min: 0, max: 100 }
});
const isRecord = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);

function readPath(object, path) {
  const parts = path.split('.');
  let current = object;
  for (const part of parts) {
    if (!isRecord(current) || !Object.hasOwn(current, part)) return undefined;
    current = current[part];
  }
  return current;
}

function writePath(object, path, value) {
  const parts = path.split('.');
  let current = object;
  for (const part of parts.slice(0, -1)) {
    if (!isRecord(current[part])) throw new TypeError('configuration path is not an object: ' + part);
    current = current[part];
  }
  current[parts.at(-1)] = value;
}

function validUtc(timestamp) {
  if (typeof timestamp !== 'string') return false;
  const match = timestamp.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?Z$/);
  if (!match) return false;
  const date = new Date(timestamp);
  return !Number.isNaN(date.getTime()) && Number(match[1]) >= 1 &&
    date.getUTCFullYear() === Number(match[1]) && date.getUTCMonth() + 1 === Number(match[2]) &&
    date.getUTCDate() === Number(match[3]) && date.getUTCHours() === Number(match[4]) &&
    date.getUTCMinutes() === Number(match[5]) && date.getUTCSeconds() === Number(match[6]);
}

function validValue(path, value) {
  const rule = TUNABLE_PATHS[path];
  if (!rule) return false;
  if (rule.type === 'integer' && !Number.isInteger(value)) return false;
  if (rule.type === 'number' && (typeof value !== 'number' || !Number.isFinite(value))) return false;
  return typeof value === 'number' && value >= rule.min && value <= rule.max;
}

function nonEmptyStrings(value) {
  return Array.isArray(value) ? [...new Set(value.filter((item) => typeof item === 'string' && item.trim().length > 0))] : [];
}

export function runStudyCycle(study, config) {
  const issues = [];
  if (!isRecord(study)) throw new TypeError('study must be a JSON object');
  if (!isRecord(config) || !Number.isInteger(config.version) || config.version < 1) throw new TypeError('config must have a positive integer version');
  if (typeof study.studyId !== 'string' || study.studyId.trim() === '') issues.push('studyId is required');
  if (!validUtc(study.studiedAtUtc)) issues.push('studiedAtUtc must be a real UTC ISO timestamp');
  const sourceReferences = nonEmptyStrings(study.sourceReferences);
  if (sourceReferences.length === 0) issues.push('at least one source reference is required');
  if (typeof study.confidence !== 'number' || !Number.isFinite(study.confidence) || study.confidence < 0 || study.confidence > 1) issues.push('confidence must be a number between 0 and 1');
  const minimumConfidence = config.minStudyConfidence === undefined ? 0.8 : config.minStudyConfidence;
  if (typeof minimumConfidence !== 'number' || !Number.isFinite(minimumConfidence) || minimumConfidence < 0 || minimumConfidence > 1) {
    issues.push('config minStudyConfidence must be a number between 0 and 1');
  } else if (typeof study.confidence === 'number' && study.confidence < minimumConfidence) {
    issues.push('study confidence is below the configured approval threshold');
  }
  const rawAssessment = evaluateAllSubengines(study);
  const verifiedResults = rawAssessment.results.map((item) => {
    const unregisteredReferences = item.evidenceReferences.filter((reference) => !sourceReferences.includes(reference));
    if (unregisteredReferences.length === 0) return item;
    return {
      ...item,
      status: 'NOT_VERIFIED',
      decision: 'INVESTIGATE',
      severity: item.engineId === 'MCU' || item.engineId === 'ARRE' ? 'CRITICAL' : 'HIGH',
      reason: 'Subengine evidence references must be listed in study.sourceReferences.'
    };
  });
  const subsystemAssessment = {
    results: verifiedResults,
    allClear: verifiedResults.every((item) => item.decision === 'CONTINUE'),
    needsInvestigation: verifiedResults.some((item) => item.decision === 'INVESTIGATE'),
    criticalFailures: verifiedResults.filter((item) => (item.engineId === 'MCU' || item.engineId === 'ARRE') && item.decision === 'INVESTIGATE').map((item) => item.engineId)
  };
  if (subsystemAssessment.needsInvestigation) issues.push('one or more subengines are failed, unknown, or missing evidence');
  let updateProposal = null;
  const recommendation = study.recommendation;
  if (recommendation !== undefined && recommendation !== null) {
    const path = isRecord(recommendation) ? recommendation.configPath : undefined;
    const proposedValue = isRecord(recommendation) ? recommendation.proposedValue : undefined;
    const rationale = isRecord(recommendation) && typeof recommendation.rationale === 'string' ? recommendation.rationale.trim() : '';
    const expectedOutcome = isRecord(recommendation) && typeof recommendation.expectedOutcome === 'string' ? recommendation.expectedOutcome.trim() : '';
    const requestedBy = typeof study.requestedBy === 'string' ? study.requestedBy.trim() : '';
    const evidenceReferences = nonEmptyStrings(recommendation?.evidenceReferences).filter((ref) => sourceReferences.includes(ref));
    const currentValue = typeof path === 'string' ? readPath(config, path) : undefined;
    const proposalIssues = [];
    if (typeof path !== 'string' || !Object.hasOwn(TUNABLE_PATHS, path)) proposalIssues.push('configuration path is not on the approved tuning allowlist');
    if (typeof path === 'string' && Object.hasOwn(TUNABLE_PATHS, path) && !validValue(path, proposedValue)) proposalIssues.push('proposed value is outside the approved type or range');
    if (typeof path === 'string' && Object.hasOwn(TUNABLE_PATHS, path) && currentValue === undefined) proposalIssues.push('configuration path is missing from the current configuration');
    if (rationale === '') proposalIssues.push('a non-empty rationale is required');
    if (expectedOutcome === '') proposalIssues.push('a measurable expected outcome is required');
    if (requestedBy === '') proposalIssues.push('requestedBy is required for separation of duties');
    if (evidenceReferences.length === 0) proposalIssues.push('recommendation must cite source references included in the study');
    updateProposal = {
      proposalId: String(study.studyId || 'invalid-study') + ':' + String(path || 'invalid-path'),
      studyId: study.studyId || null,
      baseConfigVersion: config.version,
      configPath: path || null,
      baseValue: currentValue === undefined ? null : currentValue,
      proposedValue: proposedValue === undefined ? null : proposedValue,
      rationale, expectedOutcome, requestedBy, evidenceReferences,
      status: proposalIssues.length === 0 && issues.length === 0 ? 'PENDING_APPROVAL' : 'BLOCKED',
      issues: [...issues, ...proposalIssues]
    };
    if (proposalIssues.length > 0) issues.push(...proposalIssues);
  }
  const blocked = issues.length > 0 || subsystemAssessment.needsInvestigation;
  return {
    engine: 'ASSD_AUTOPILOT',
    studyId: study.studyId || null,
    baseConfigVersion: config.version,
    state: blocked ? 'INVESTIGATE' : (updateProposal ? 'REVIEW_UPDATE' : 'STUDY_VERIFIED_NO_UPDATE'),
    subengines: subsystemAssessment.results,
    issues: [...new Set(issues)],
    updateProposal
  };
}

export function applyApprovedEngineUpdate(config, proposal, approval) {
  if (!isRecord(config) || !Number.isInteger(config.version) || config.version < 1) throw new TypeError('config must have a positive integer version');
  if (!isRecord(proposal) || proposal.status !== 'PENDING_APPROVAL') throw new Error('only a pending, unblocked proposal may be applied');
  if (!isRecord(approval) || approval.status !== 'approved') throw new Error('explicit approval is required');
  if (approval.proposalId !== proposal.proposalId) throw new Error('approval proposalId does not match');
  if (approval.reviewerId === proposal.requestedBy || typeof approval.reviewerId !== 'string' || approval.reviewerId.trim() === '') throw new Error('independent reviewer identity is required');
  if (typeof approval.evidenceReference !== 'string' || approval.evidenceReference.trim() === '') throw new Error('approval evidence reference is required');
  if (!validUtc(approval.approvedAtUtc)) throw new Error('approval timestamp must be a real UTC ISO timestamp');
  if (proposal.baseConfigVersion !== config.version || approval.baseConfigVersion !== config.version) throw new Error('stale configuration version; regenerate and re-review proposal');
  if (!Object.hasOwn(TUNABLE_PATHS, proposal.configPath) || !validValue(proposal.configPath, proposal.proposedValue)) throw new Error('configuration update is outside the approved tuning allowlist');
  const currentValue = readPath(config, proposal.configPath);
  if (currentValue !== proposal.baseValue) throw new Error('configuration changed since the study; regenerate proposal');
  const next = structuredClone(config);
  writePath(next, proposal.configPath, proposal.proposedValue);
  next.version = config.version + 1;
  next.lastUpdate = {
    proposalId: proposal.proposalId, studyId: proposal.studyId, path: proposal.configPath,
    previousValue: currentValue, newValue: proposal.proposedValue,
    approvedBy: approval.reviewerId, approvedAtUtc: approval.approvedAtUtc,
    approvalEvidenceReference: approval.evidenceReference, sourceReferences: [...proposal.evidenceReferences]
  };
  return next;
}

export const AUTOPILOT_TUNING_ALLOWLIST = Object.freeze(Object.keys(TUNABLE_PATHS));
