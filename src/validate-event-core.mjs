const required = ['schema_version','project','framework','execution_id','event_id','node_id','module','event_type','timestamp_utc','status','data_quality','environment','redaction_status'];
const enums = {
  module: ['MCU','CERE','ARRE','IPSU','MASTER_CONTROL','TELEMETRY','OTHER'],
  status: ['started','succeeded','failed','rejected','quarantined','investigating','corrected','verified'],
  data_quality: ['valid','invalid','unknown'],
  risk_level: ['low','medium','high','critical','unknown'],
  environment: ['local','test','staging','production'],
  redaction_status: ['checked','redacted','not_checked','not_applicable']
};
const allowed = new Set([...required,'duration_ms','retry_count','risk_level','approval_required','owner_id','evidence_reference','correlation_id','source_version','financial_impact']);
export function validateEvent(event) {
  const errors = [];
  if (!event || typeof event !== 'object' || Array.isArray(event)) return { valid:false, errors:['event must be a JSON object'] };
  for (const key of required) if (!(key in event)) errors.push('missing required field: ' + key);
  for (const key of Object.keys(event)) if (!allowed.has(key)) errors.push('unsupported field: ' + key);
  if ('schema_version' in event && event.schema_version !== '1.0') errors.push('schema_version must be 1.0');
  if ('project' in event && event.project !== 'QZ') errors.push('project must be QZ');
  if ('framework' in event && event.framework !== 'ASSD') errors.push('framework must be ASSD');
  for (const [key, values] of Object.entries(enums)) if (key in event && !values.includes(event[key])) errors.push('invalid ' + key);
  for (const key of ['execution_id','event_id','node_id','module','event_type']) if (key in event && (typeof event[key] !== 'string' || event[key].trim() === '')) errors.push(key + ' must be a non-empty string');
  if ('timestamp_utc' in event && (typeof event.timestamp_utc !== 'string' || !event.timestamp_utc.endsWith('Z') || Number.isNaN(Date.parse(event.timestamp_utc)))) errors.push('timestamp_utc must be a valid UTC ISO timestamp ending in Z');
  if ('duration_ms' in event && (typeof event.duration_ms !== 'number' || !Number.isFinite(event.duration_ms) || event.duration_ms < 0)) errors.push('duration_ms must be a non-negative finite number');
  if ('retry_count' in event && (!Number.isInteger(event.retry_count) || event.retry_count < 0)) errors.push('retry_count must be a non-negative integer');
  if ('approval_required' in event && typeof event.approval_required !== 'boolean') errors.push('approval_required must be boolean');
  for (const key of ['owner_id','evidence_reference','correlation_id','source_version']) if (key in event && typeof event[key] !== 'string') errors.push(key + ' must be a string');
  if (event.financial_impact !== undefined) {
    const f = event.financial_impact;
    if (!f || typeof f !== 'object' || Array.isArray(f)) errors.push('financial_impact must be an object');
    else {
      const fa = new Set(['classification','currency','value','source_reference','reconciled']);
      for (const key of Object.keys(f)) if (!fa.has(key)) errors.push('unsupported financial_impact field: ' + key);
      if (!['forecast','estimated','attributed','realized'].includes(f.classification)) errors.push('invalid financial_impact classification');
      if (typeof f.currency !== 'string' || !/^[A-Z]{3}$/.test(f.currency)) errors.push('financial_impact currency must be a 3-letter uppercase code');
      if (typeof f.value !== 'number' || !Number.isFinite(f.value)) errors.push('financial_impact value must be a finite number');
      if (f.classification === 'realized' && (f.reconciled !== true || typeof f.source_reference !== 'string' || f.source_reference.trim() === '')) errors.push('realized financial impact requires reconciled=true and a non-empty source_reference');
    }
  }
  return { valid: errors.length === 0, errors };
}
