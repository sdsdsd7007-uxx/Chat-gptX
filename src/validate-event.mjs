import { validateEvent } from './validate-event-core.mjs';
let input = '';
for await (const chunk of process.stdin) input += chunk;
try {
  const event = JSON.parse(input);
  const result = validateEvent(event);
  process.stdout.write(JSON.stringify(result) + '\n');
  if (!result.valid) process.exitCode = 1;
} catch {
  process.stdout.write(JSON.stringify({ valid: false, errors: ['input is not valid JSON'] }) + '\n');
  process.exitCode = 1;
}
