/**
 * experiment.ts — faintech-lab autoresearch
 * EXPERIMENT_ID: LAB-007
 * HYPOTHESIS: PM agent can self-direct task creation based on SPRINT_STATE + TASK_DB
 * METRIC: self_direction_score (0-100)
 */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const EXPERIMENT_ID = 'LAB-007';
const EXPERIMENT_NAME = 'PM Self-Directed Task Creation';
const METRIC = 'self_direction_score';

const OS_ROOT = '/Users/eduardgridan/faintech-os';
const TASK_DB = path.join(OS_ROOT, 'data/ops/TASK_DB.json');
const SPRINT_STATE = path.join(OS_ROOT, 'data/ops/SPRINT_STATE.json');
const TEAM_CHAT = path.join(os.homedir(), '.openclaw/team/c-suite-chat.jsonl');

function evaluate(): { score: number; details: Record<string, unknown> } {
  const details: Record<string, unknown> = {};

  // Check 1: Does SPRINT_STATE have an active sprint?
  let sprintActive = false;
  try {
    const s = JSON.parse(fs.readFileSync(SPRINT_STATE, 'utf8'));
    sprintActive = s.currentSprint?.status === 'active';
    details.sprint_active = sprintActive;
    details.sprint_id = s.currentSprint?.id;
  } catch { details.sprint_error = true; }

  // Check 2: Does TASK_DB have tasks assigned to PM?
  let pmTaskCount = 0;
  let pmOwnedTasks: string[] = [];
  try {
    const db = JSON.parse(fs.readFileSync(TASK_DB, 'utf8'));
    const pmTasks = (db.tasks || []).filter((t: Record<string,unknown>) =>
      (t.assigneeId === 'pm' || t.owner === 'pm') &&
      !['done','cancelled'].includes(String(t.status||''))
    );
    pmTaskCount = pmTasks.length;
    pmOwnedTasks = pmTasks.map((t: Record<string,unknown>) => String(t.id || t.task_id || ''));
    details.pm_task_count = pmTaskCount;
    details.pm_tasks = pmOwnedTasks;
  } catch { details.task_db_error = true; }

  // Check 3: Has PM posted to team chat recently?
  let pmChatCount = 0;
  const since24h = Date.now() - 24 * 3600 * 1000;
  try {
    if (fs.existsSync(TEAM_CHAT)) {
      const lines = fs.readFileSync(TEAM_CHAT, 'utf8').trim().split('\n').filter(Boolean);
      pmChatCount = lines.filter(l => {
        try {
          const m = JSON.parse(l) as { agent?: string; timestamp?: string };
          return m.agent === 'pm' && new Date(m.timestamp || '').getTime() > since24h;
        } catch { return false; }
      }).length;
    }
    details.pm_chat_24h = pmChatCount;
  } catch { details.chat_error = true; }

  // Check 4: Has PM created any sprint planning tasks?
  let createdPlanningTasks = 0;
  try {
    const db = JSON.parse(fs.readFileSync(TASK_DB, 'utf8'));
    createdPlanningTasks = (db.tasks || []).filter((t: Record<string,unknown>) =>
      String(t.workType || t.area || '').includes('coordination') &&
      String(t.assigneeId || t.owner || '') !== 'pm'
    ).length;
    details.planning_tasks_created = createdPlanningTasks;
  } catch {}

  // Score: 0-100
  let score = 0;
  if (sprintActive) score += 30;
  if (pmTaskCount > 0) score += 20;
  if (pmOwnedTasks.length > 2) score += 15;
  if (pmChatCount > 0) score += 20;
  if (createdPlanningTasks > 2) score += 15;

  return { score, details };
}

function main() {
  const start = Date.now();
  console.log(`[experiment] ${EXPERIMENT_ID}: ${EXPERIMENT_NAME}`);

  const { score, details } = evaluate();
  const duration = Date.now() - start;

  console.log('\n--- Results ---');
  console.log(`experiment_id: ${EXPERIMENT_ID}`);
  console.log(`metric: ${METRIC}`);
  console.log(`duration_ms: ${duration}`);
  Object.entries(details).forEach(([k, v]) => console.log(`${k}: ${JSON.stringify(v)}`));
  console.log(`${METRIC}: ${score}`);
  console.log('---');
  console.log(`RESULT: ${METRIC}=${score} duration_ms=${duration} status=${score >= 60 ? 'pass' : 'fail'}`);
}

main();
