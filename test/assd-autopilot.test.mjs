import test from 'node:test';
import assert from 'node:assert/strict';
import { applyApprovedEngineUpdate, runStudyCycle } from '../src/assd-autopilot.mjs';

const config = () => ({
  version: 1, minStudyConfidence: 0.8,
  routing: { confidenceThreshold: 0.85 },
  telemetry: { maxRetryCount: 3 },
  kpi: { alertTolerancePercent: 5 },
  resourceEfficiency: { targetPercent: 80 }
});

const study = (overrides = {}) => ({
  studyId: 'study-001',
  studiedAtUtc: '2026-10-28T09:00:00Z',
  requestedBy: 'analyst-1',
  confidence: 0.95,
  sourceReferences: ['evidence:study-001'],
  subsystems: Object.fromEntries(['MCU','CERE','ARRE','IPSU'].map((id) => [id, { status:'pass', evidenceReferences:['evidence:study-001'], reason:id + ' checks passed' }])),
  recommendation: {
    configPath:'routing.confidenceThreshold',
    proposedValue:0.9,
    rationale:'Staging evidence supports a conservative increase.',
    expectedOutcome:'Reduce low-confidence routing by 10% without increasing failed tasks.',
    evidenceReferences:['evidence:study-001']
  },
  ...overrides
});

test('creates an update proposal only when all four subengines pass with evidence', () => {
  const result = runStudyCycle(study(), config());
  assert.equal(result.state, 'REVIEW_UPDATE');
  assert.equal(result.updateProposal.status, 'PENDING_APPROVAL');
  assert.deepEqual(result.subengines.map((item) => item.engineId), ['MCU','CERE','ARRE','IPSU']);
});

test('unknown subsystem signals force investigation and block the update', () => {
  const input = study();
  delete input.subsystems.ARRE;
  const result = runStudyCycle(input, config());
  assert.equal(result.state, 'INVESTIGATE');
  assert.equal(result.updateProposal.status, 'BLOCKED');
});

test('a pass signal without evidence is not accepted', () => {
  const input = study();
  input.subsystems.MCU.evidenceReferences = [];
  const result = runStudyCycle(input, config());
  assert.equal(result.state, 'INVESTIGATE');
  assert.equal(result.subengines.find((item) => item.engineId === 'MCU').status, 'NOT_VERIFIED');
});

test('a failed critical subengine blocks an update', () => {
  const input = study();
  input.subsystems.MCU.status = 'fail';
  const result = runStudyCycle(input, config());
  assert.equal(result.state, 'INVESTIGATE');
  assert.equal(result.subengines.find((item) => item.engineId === 'MCU').severity, 'CRITICAL');
});

test('low-confidence study blocks updates', () => {
  const result = runStudyCycle(study({ confidence:0.5 }), config());
  assert.equal(result.state, 'INVESTIGATE');
  assert.equal(result.updateProposal.status, 'BLOCKED');
});

test('missing source references blocks updates', () => {
  const result = runStudyCycle(study({ sourceReferences:[] }), config());
  assert.equal(result.state, 'INVESTIGATE');
  assert.equal(result.updateProposal.status, 'BLOCKED');
});

test('protected or unknown config paths cannot be proposed', () => {
  const input = study({ recommendation: { configPath:'security.requireApproval', proposedValue:false, rationale:'disable gate', expectedOutcome:'fewer prompts', evidenceReferences:['evidence:study-001'] } });
  const result = runStudyCycle(input, config());
  assert.equal(result.updateProposal.status, 'BLOCKED');
  assert.ok(result.updateProposal.issues.some((item) => item.includes('allowlist')));
});

test('out-of-range or wrong-type values cannot be proposed', () => {
  const input = study({ recommendation: { configPath:'telemetry.maxRetryCount', proposedValue:99, rationale:'retry more', expectedOutcome:'fewer transient failures', evidenceReferences:['evidence:study-001'] } });
  const result = runStudyCycle(input, config());
  assert.equal(result.updateProposal.status, 'BLOCKED');
});

test('study engine emits verified no-update state when no tuning recommendation exists', () => {
  const input = study();
  delete input.recommendation;
  const result = runStudyCycle(input, config());
  assert.equal(result.state, 'STUDY_VERIFIED_NO_UPDATE');
  assert.equal(result.updateProposal, null);
});

test('engine update cannot be applied without explicit approval', () => {
  const result = runStudyCycle(study(), config());
  assert.throws(() => applyApprovedEngineUpdate(config(), result.updateProposal, null), /explicit approval/);
});

test('self-approval is rejected', () => {
  const result = runStudyCycle(study(), config());
  assert.throws(() => applyApprovedEngineUpdate(config(), result.updateProposal, {
    status:'approved', proposalId:result.updateProposal.proposalId, reviewerId:'analyst-1',
    evidenceReference:'approval:123', approvedAtUtc:'2026-10-28T10:00:00Z', baseConfigVersion:1
  }), /independent reviewer/);
});

test('stale config versions are rejected', () => {
  const base = config();
  const result = runStudyCycle(study(), base);
  const changed = { ...config(), version:2 };
  assert.throws(() => applyApprovedEngineUpdate(changed, result.updateProposal, {
    status:'approved', proposalId:result.updateProposal.proposalId, reviewerId:'reviewer-2',
    proposalFingerprint:result.updateProposal.fingerprint,
    evidenceReference:'approval:123', approvedAtUtc:'2026-10-28T10:00:00Z', baseConfigVersion:1
  }), /stale configuration version/);
});

test('approved, independently reviewed tuning update increments version and preserves audit evidence', () => {
  const base = config();
  const result = runStudyCycle(study(), base);
  const updated = applyApprovedEngineUpdate(base, result.updateProposal, {
    status:'approved', proposalId:result.updateProposal.proposalId, reviewerId:'reviewer-2',
    proposalFingerprint:result.updateProposal.fingerprint,
    evidenceReference:'approval:123', approvedAtUtc:'2026-10-28T10:00:00Z', baseConfigVersion:1
  });
  assert.equal(updated.version, 2);
  assert.equal(updated.routing.confidenceThreshold, 0.9);
  assert.equal(updated.lastUpdate.approvedBy, 'reviewer-2');
  assert.deepEqual(updated.lastUpdate.sourceReferences, ['evidence:study-001']);
});

test('cannot apply an update when the current value differs from the study baseline', () => {
  const base = config();
  const result = runStudyCycle(study(), base);
  base.routing.confidenceThreshold = 0.88;
  assert.throws(() => applyApprovedEngineUpdate(base, result.updateProposal, {
    status:'approved', proposalId:result.updateProposal.proposalId, reviewerId:'reviewer-2',
    proposalFingerprint:result.updateProposal.fingerprint,
    evidenceReference:'approval:123', approvedAtUtc:'2026-10-28T10:00:00Z', baseConfigVersion:1
  }), /configuration changed since the study/);
});
test('subengine evidence outside the registered study sources blocks updates', () => {
  const input = study();
  input.subsystems.CERE.evidenceReferences = ['unregistered:reference'];
  const result = runStudyCycle(input, config());
  assert.equal(result.state, 'INVESTIGATE');
  assert.equal(result.subengines.find((item) => item.engineId === 'CERE').status, 'NOT_VERIFIED');
});

test('invalid confidence policy blocks the study rather than falling back silently', () => {
  const invalidConfig = config();
  invalidConfig.minStudyConfidence = 2;
  const result = runStudyCycle(study(), invalidConfig);
  assert.equal(result.state, 'INVESTIGATE');
  assert.ok(result.issues.some((item) => item.includes('minStudyConfidence')));
});

test('not-applicable subengine without evidence blocks study updates', () => {
  const input = study();
  input.subsystems.CERE.status = 'not_applicable';
  input.subsystems.CERE.evidenceReferences = [];
  input.subsystems.CERE.reason = 'No resource-flow domain applies to this test.';
  const result = runStudyCycle(input, config());
  const cere = result.subengines.find((item) => item.engineId === 'CERE');
  assert.equal(result.state, 'INVESTIGATE');
  assert.equal(cere.status, 'NOT_VERIFIED');
  assert.equal(cere.decision, 'INVESTIGATE');
  assert.match(cere.reason, /evidence reference/);
  assert.equal(result.updateProposal.status, 'BLOCKED');
});

test('not-applicable subengine with registered evidence and rationale remains explicit', () => {
  const input = study();
  input.subsystems.CERE.status = 'not_applicable';
  input.subsystems.CERE.evidenceReferences = ['evidence:study-001'];
  input.subsystems.CERE.reason = 'No resource-flow domain applies to this test.';
  const result = runStudyCycle(input, config());
  const cere = result.subengines.find((item) => item.engineId === 'CERE');
  assert.equal(result.state, 'REVIEW_UPDATE');
  assert.equal(cere.status, 'NOT_APPLICABLE');
  assert.equal(cere.decision, 'CONTINUE');
  assert.equal(result.updateProposal.status, 'PENDING_APPROVAL');
});


test('post-approval changes to any material proposal field are rejected', () => {
  const mutations = [
    (proposal) => { proposal.proposedValue = 0.92; },
    (proposal) => { proposal.rationale = 'Changed after review'; },
    (proposal) => { proposal.expectedOutcome = 'Different outcome after review'; },
    (proposal) => { proposal.evidenceReferences = ['evidence:substituted']; },
    (proposal) => { proposal.baseValue = 0.86; },
    (proposal) => { proposal.issues = ['review bypass attempt']; }
  ];

  for (const mutate of mutations) {
    const base = config();
    const result = runStudyCycle(study(), base);
    const proposal = structuredClone(result.updateProposal);
    const approval = {
      status:'approved', proposalId:proposal.proposalId, reviewerId:'reviewer-2',
      proposalFingerprint:proposal.fingerprint, evidenceReference:'approval:123',
      approvedAtUtc:'2026-10-28T10:00:00Z', baseConfigVersion:1
    };
    const before = structuredClone(base);
    mutate(proposal);
    assert.throws(
      () => applyApprovedEngineUpdate(base, proposal, approval),
      /proposal contents changed since its fingerprint was recorded/
    );
    assert.deepEqual(base, before);
  }
});

test('approval must carry the exact fingerprint that was reviewed', () => {
  const base = config();
  const result = runStudyCycle(study(), base);
  const proposal = result.updateProposal;
  const before = structuredClone(base);
  assert.throws(() => applyApprovedEngineUpdate(base, proposal, {
    status:'approved', proposalId:proposal.proposalId, reviewerId:'reviewer-2',
    proposalFingerprint:'0'.repeat(64), evidenceReference:'approval:123',
    approvedAtUtc:'2026-10-28T10:00:00Z', baseConfigVersion:1
  }), /approval fingerprint does not match the proposal/);
  assert.deepEqual(base, before);
});

test('post-approval changes to proposal identity, version, route, or status are rejected', () => {
  const mutations = [
    (proposal) => { proposal.proposalId = 'forged-proposal-id'; },
    (proposal) => { proposal.studyId = 'substituted-study'; },
    (proposal) => { proposal.baseConfigVersion = 2; },
    (proposal) => { proposal.configPath = 'kpi.alertTolerancePercent'; },
    (proposal) => { proposal.requestedBy = 'reviewer-2'; },
    (proposal) => { proposal.status = 'BLOCKED'; }
  ];

  for (const mutate of mutations) {
    const base = config();
    const result = runStudyCycle(study(), base);
    const proposal = structuredClone(result.updateProposal);
    const approval = {
      status:'approved', proposalId:proposal.proposalId, reviewerId:'reviewer-2',
      proposalFingerprint:proposal.fingerprint, evidenceReference:'approval:123',
      approvedAtUtc:'2026-10-28T10:00:00Z', baseConfigVersion:1
    };
    const before = structuredClone(base);
    mutate(proposal);
    assert.throws(() => applyApprovedEngineUpdate(base, proposal, approval));
    assert.deepEqual(base, before);
  }
});

test('tampering with the stored fingerprint and copying it into approval is rejected', () => {
  const base = config();
  const result = runStudyCycle(study(), base);
  const proposal = structuredClone(result.updateProposal);
  proposal.fingerprint = 'f'.repeat(64);
  const approval = {
    status:'approved', proposalId:proposal.proposalId, reviewerId:'reviewer-2',
    proposalFingerprint:proposal.fingerprint, evidenceReference:'approval:123',
    approvedAtUtc:'2026-10-28T10:00:00Z', baseConfigVersion:1
  };
  const before = structuredClone(base);
  assert.throws(
    () => applyApprovedEngineUpdate(base, proposal, approval),
    /proposal contents changed since its fingerprint was recorded/
  );
  assert.deepEqual(base, before);
});
