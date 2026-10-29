import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, '..');
const schema = JSON.parse(readFileSync(resolve(repoRoot, 'schemas/telemetry-event.v1.schema.json'), 'utf8'));
const cliPath = resolve(repoRoot, 'src/validate-event.mjs');

const validEvent = () => ({
  schema_version:'1.0', project:'QZ', framework:'ASSD',
  execution_id:'schema-cli-execution-001', event_id:'schema-cli-event-001',
  node_id:'QZ-TELEMETRY-001', module:'TELEMETRY', event_type:'contract.test',
  timestamp_utc:'2026-10-28T09:00:00Z', status:'succeeded',
  data_quality:'valid', environment:'test', redaction_status:'checked'
});

test('schema is fail-closed and contains the fields required by the event contract', () => {
  assert.equal(schema.type, 'object');
  assert.equal(schema.additionalProperties, false);
  for (const key of ['schema_version','project','framework','execution_id','event_id','node_id','module','event_type','timestamp_utc','status','data_quality','environment','redaction_status']) {
    assert.ok(schema.required.includes(key), 'schema missing required field: ' + key);
    assert.ok(Object.hasOwn(schema.properties, key), 'schema has no property definition for: ' + key);
  }
  assert.equal(schema.properties.project.const, 'QZ');
  assert.equal(schema.properties.framework.const, 'ASSD');
});

test('CLI accepts a valid event and emits structured JSON', () => {
  const result = spawnSync(process.execPath, [cliPath], { input: JSON.stringify(validEvent()), encoding:'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(JSON.parse(result.stdout), { valid:true, errors:[] });
});

test('CLI rejects invalid JSON and returns a non-zero exit code', () => {
  const result = spawnSync(process.execPath, [cliPath], { input:'{broken json', encoding:'utf8' });
  assert.equal(result.status, 1);
  assert.equal(JSON.parse(result.stdout).valid, false);
});

test('CLI rejects unrecognized sensitive fields', () => {
  const result = spawnSync(process.execPath, [cliPath], { input:JSON.stringify({ ...validEvent(), api_key:'do-not-accept' }), encoding:'utf8' });
  assert.equal(result.status, 1);
  assert.equal(JSON.parse(result.stdout).valid, false);
});
