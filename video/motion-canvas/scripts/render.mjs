import {readFile, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import process from 'node:process';

const flagIndex = process.argv.indexOf('--plan');
if (flagIndex === -1 || !process.argv[flagIndex + 1]) {
  throw new Error('Usage: npm run render -- --plan <hottop-video-plan.json>');
}

const planPath = resolve(process.cwd(), process.argv[flagIndex + 1]);
const plan = JSON.parse(await readFile(planPath, 'utf8'));

if (plan.schema_version !== 'hottop.video-plan.v1') {
  throw new Error(`Unsupported plan schema: ${String(plan.schema_version)}`);
}
if (!Array.isArray(plan.shots) || plan.shots.length === 0) {
  throw new Error('Motion Canvas requires at least one planned shot.');
}

let cursor = 0;
for (const shot of plan.shots) {
  if (shot.start_seconds < cursor || shot.end_seconds <= shot.start_seconds) {
    throw new Error(`Invalid or overlapping shot timeline at shot ${String(shot.index)}.`);
  }
  cursor = shot.end_seconds;
}
if (cursor > plan.duration_seconds) {
  throw new Error('Shot timeline exceeds plan duration.');
}

const target = resolve(process.cwd(), 'src/generated-plan.ts');
const source = [
  "import type {HottopVideoPlan} from './plan';",
  '',
  `const plan: HottopVideoPlan = ${JSON.stringify(plan, null, 2)};`,
  '',
  'export default plan;',
  '',
].join('\n');

await writeFile(target, source, 'utf8');
console.log(`Prepared src/generated-plan.ts from ${planPath}`);
console.log('Motion Canvas project is ready for the explicit execution adapter; no renderer was spawned.');
