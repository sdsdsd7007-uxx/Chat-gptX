export const SUBENGINE_IDS = Object.freeze(['MCU', 'CERE', 'ARRE', 'IPSU']);
const SIGNALS = new Set(['pass', 'fail', 'unknown', 'not_applicable']);
const HIGH_IMPACT = new Set(['MCU', 'ARRE']);

function evidenceList(value) {
  if (!Array.isArray(value)) return [];
  return [...new Set(value.filter((item) => typeof item === 'string' && item.trim().length > 0))];
}

export function evaluateSubengine(engineId, input = {}) {
  if (!SUBENGINE_IDS.includes(engineId)) throw new TypeError('unsupported subengine: ' + engineId);
  const signal = SIGNALS.has(input.status) ? input.status : 'unknown';
  const evidenceReferences = evidenceList(input.evidenceReferences);
  const reason = typeof input.reason === 'string' ? input.reason.trim() : '';
  if (signal === 'pass' && evidenceReferences.length === 0) {
    return { engineId, status: 'NOT_VERIFIED', decision: 'INVESTIGATE', severity: HIGH_IMPACT.has(engineId) ? 'CRITICAL' : 'HIGH', evidenceReferences: [], reason: 'A pass signal requires at least one evidence reference.' };
  }
  if (signal === 'not_applicable' && (reason.length === 0 || evidenceReferences.length === 0)) {
    const missing = [];
    if (reason.length === 0) missing.push('a recorded rationale');
    if (evidenceReferences.length === 0) missing.push('at least one evidence reference');
    return { engineId, status: 'NOT_VERIFIED', decision: 'INVESTIGATE', severity: 'HIGH', evidenceReferences, reason: 'Not-applicable status requires ' + missing.join(' and ') + '.' };
  }
  if (signal === 'pass') return { engineId, status: 'PASS', decision: 'CONTINUE', severity: 'LOW', evidenceReferences, reason: reason || 'Required checks passed with evidence.' };
  if (signal === 'not_applicable') return { engineId, status: 'NOT_APPLICABLE', decision: 'CONTINUE', severity: 'LOW', evidenceReferences, reason };
  if (signal === 'fail') return { engineId, status: 'FAIL', decision: 'INVESTIGATE', severity: HIGH_IMPACT.has(engineId) ? 'CRITICAL' : 'HIGH', evidenceReferences, reason: reason || 'Subengine reported a failed check.' };
  return { engineId, status: 'NOT_VERIFIED', decision: 'INVESTIGATE', severity: HIGH_IMPACT.has(engineId) ? 'CRITICAL' : 'HIGH', evidenceReferences, reason: reason || 'No validated signal was supplied; unknown is not a pass.' };
}

export function evaluateAllSubengines(study = {}) {
  const supplied = study.subsystems && typeof study.subsystems === 'object' ? study.subsystems : {};
  const results = SUBENGINE_IDS.map((engineId) => evaluateSubengine(engineId, supplied[engineId] || {}));
  return {
    results,
    allClear: results.every((item) => item.decision === 'CONTINUE'),
    needsInvestigation: results.some((item) => item.decision === 'INVESTIGATE'),
    criticalFailures: results.filter((item) => item.severity === 'CRITICAL' && item.decision === 'INVESTIGATE').map((item) => item.engineId)
  };
}
