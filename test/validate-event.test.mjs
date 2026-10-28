import test from 'node:test';
import assert from 'node:assert/strict';
import { validateEvent } from '../src/validate-event-core.mjs';

const validEvent = () => ({
  schema_version:'1.0', project:'QZ', framework:'ASSD',
  execution_id:'test-execution-001', event_id:'test-event-001',
  node_id:'QZ-TELEMETRY-001', module:'TELEMETRY', event_type:'validation.test',
  timestamp_utc:'2026-10-28T09:00:00Z', status:'succeeded',
  data_quality:'valid', environment:'test', redaction_status:'checked'
});

test('accepts a well-formed event', () => { assert.deepEqual(validateEvent(validEvent()), { valid:true, errors:[] }); });
test('rejects missing required fields', () => { const e=validEvent(); delete e.event_id; const r=validateEvent(e); assert.equal(r.valid,false); assert.ok(r.errors.some(x=>x.includes('event_id'))); });
test('rejects unsupported fields', () => { const r=validateEvent({...validEvent(),password:'never-log-this'}); assert.equal(r.valid,false); assert.ok(r.errors.some(x=>x.includes('unsupported field'))); });
test('rejects invalid timestamps', () => { assert.equal(validateEvent({...validEvent(),timestamp_utc:'not-a-time'}).valid,false); });
test('rejects negative duration and retry count', () => { const r=validateEvent({...validEvent(),duration_ms:-1,retry_count:-2}); assert.equal(r.valid,false); assert.ok(r.errors.some(x=>x.includes('duration_ms'))); assert.ok(r.errors.some(x=>x.includes('retry_count'))); });
test('rejects unverified realized financial impact', () => { const r=validateEvent({...validEvent(),financial_impact:{classification:'realized',currency:'UGX',value:1000,reconciled:false}}); assert.equal(r.valid,false); assert.ok(r.errors.some(x=>x.includes('realized financial impact'))); });
test('accepts realized financial impact only with reconciliation evidence', () => { const r=validateEvent({...validEvent(),financial_impact:{classification:'realized',currency:'UGX',value:1000,reconciled:true,source_reference:'finance-close-2026-10'}}); assert.deepEqual(r,{valid:true,errors:[]}); });
test('rejects a non-object event', () => { assert.equal(validateEvent(null).valid,false); });
