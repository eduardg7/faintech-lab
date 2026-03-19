#!/usr/bin/env node

/**
 * Auto-Promote Cross-Agent Patterns Cron Job
 *
 * Analyzes all agent LEARNINGS.md files weekly and promotes
 * patterns that appear 3+ times across different agents to
 * the shared-learnings.md for each role.
 *
 * Usage: node scripts/promote-cross-agent-patterns.js
 * Cron: 0 0 * * 0 (weekly on Sunday)
 */

const fs = require('fs');
const path = require('path');

// Configuration
const AGENTS_DIR = '/Users/eduardgridan/.openclaw/agents';
const MIN_OCCURRENCES = 3; // Promote patterns seen 3+ times
const SHARED_LEARNINGS_FILE = 'notes/areas/shared-learnings.md';
const LOG_FILE = 'data/ops/pattern-promotion-log.json';

/**
 * Parse LEARNINGS.md file and extract patterns
 */
function parseLearningsFile(agentPath, agentId) {
  const learningsPath = path.join(agentPath, '.learnings', 'LEARNINGS.md');

  if (!fs.existsSync(learningsPath)) {
    return [];
  }

  const content = fs.readFileSync(learningsPath, 'utf-8');
  const patterns = [];

  // Pattern detection: Look for "keep the winning pattern for X" or similar
  // This captures the core insight/learning
  const patternRegex =
    /keep the winning pattern for ([\w\-]+)|(?:solid|good|effective|useful) (?:pattern|approach|method|practice|learning|insight|finding)/gi;

  let match;
  while ((match = patternRegex.exec(content)) !== null) {
    patterns.push({
      agent: agentId,
      timestamp: extractTimestamp(content, match.index),
      pattern: match[1] || extractPatternName(content, match.index),
      raw: match[0],
      source: agentId
    });
  }

  return patterns;
}

/**
 * Extract timestamp from line before pattern match
 */
function extractTimestamp(content, matchIndex) {
  const linesBefore = content.substring(0, matchIndex).split('\n');
  const lastLine = linesBefore[linesBefore.length - 1] || '';
  const timeMatch = lastLine.match(/(\d{4}-\d{2}-\d{2})/);
  return timeMatch ? timeMatch[1] : null;
}

/**
 * Extract pattern name from context around match
 */
function extractPatternName(content, matchIndex) {
  const contextStart = Math.max(0, matchIndex - 200);
  const contextEnd = Math.min(content.length, matchIndex + 200);
  const context = content.substring(contextStart, contextEnd);

  // Look for task context or pattern description
  const taskMatch = context.match(/\[(?:OS|LAB)[\w\-]+\]/);
  if (taskMatch) {
    return taskMatch[0].replace(/[\[\]]/g, '');
  }

  return 'general-pattern';
}

/**
 * Scan all agents and collect patterns
 */
function scanAllAgents() {
  const agentDirs = fs.readdirSync(AGENTS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('_') && !d.name.startsWith('.'));

  const allPatterns = [];

  agentDirs.forEach(agentDir => {
    const agentPath = path.join(AGENTS_DIR, agentDir.name);
    const patterns = parseLearningsFile(agentPath, agentDir.name);
    allPatterns.push(...patterns);
  });

  return allPatterns;
}

/**
 * Count pattern occurrences across agents
 */
function analyzePatterns(patterns) {
  const patternCounts = {};

  patterns.forEach(p => {
    const key = p.pattern.toLowerCase().replace(/\s+/g, '-');
    if (!patternCounts[key]) {
      patternCounts[key] = {
        pattern: p.pattern,
        count: 0,
        agents: new Set(),
        sources: [],
        firstSeen: p.timestamp,
        rawExamples: []
      };
    }

    patternCounts[key].count++;
    patternCounts[key].agents.add(p.agent);
    patternCounts[key].sources.push(p.source);
    if (p.raw) {
      patternCounts[key].rawExamples.push(p.raw.substring(0, 100));
    }
  });

  return patternCounts;
}

/**
 * Filter patterns that meet promotion criteria
 */
function filterPromotablePatterns(patternCounts) {
  const promotable = [];

  Object.entries(patternCounts).forEach(([key, data]) => {
    if (data.count >= MIN_OCCURRENCES && data.agents.size >= 2) {
      promotable.push({
        key,
        ...data,
        agentCount: data.agents.size
      });
    }
  });

  return promotable.sort((a, b) => b.count - a.count);
}

/**
 * Update shared-learnings.md with promoted patterns
 */
function updateSharedLearnings(agentPath, promotablePatterns) {
  const sharedLearningsPath = path.join(agentPath, SHARED_LEARNINGS_FILE);

  if (!fs.existsSync(sharedLearningsPath)) {
    console.log(`No shared-learnings.md found for ${agentPath}`);
    return;
  }

  let content = fs.readFileSync(sharedLearningsPath, 'utf-8');

  // Find and update "Promoted Patterns" section
  const promotedSectionStart = content.indexOf('## Promoted Patterns');
  const roleReminderStart = content.indexOf('## Role Reminder');

  if (promotedSectionStart === -1 || roleReminderStart === -1) {
    console.log('Expected sections not found in shared-learnings.md');
    return;
  }

  const insertPoint = roleReminderStart;
  const newPromotedEntries = promotablePatterns.map(p =>
    `- [learning] ${p.pattern} (occurrences: ${p.count}, sources: ${p.sources.join(', ')})`
  ).join('\n  ');

  // Remove duplicate patterns
  const existingPatterns = content.substring(promotedSectionStart, insertPoint);
  const newSection = existingPatterns + '\n  ' + newPromotedEntries;

  content = content.substring(0, insertPoint) + newSection + content.substring(insertPoint);

  // Update summary stats
  const newTotalCount = parseInt(content.match(/Promoted patterns: (\d+)/)?.[1] || 0) + promotablePatterns.length;
  content = content.replace(/Promoted patterns: (\d+)/, `Promoted patterns: ${newTotalCount}`);

  // Update last sync timestamp
  const now = new Date().toISOString();
  content = content.replace(/Last sync: [^\n]+/, `Last sync: ${now}`);

  fs.writeFileSync(sharedLearningsPath, content, 'utf-8');
  console.log(`Updated shared-learnings.md for ${agentPath} with ${promotablePatterns.length} patterns`);
}

/**
 * Log promotion activity
 */
function logPromotion(agentPath, promotablePatterns) {
  const logPath = path.join('/Users/eduardgridan/faintech-os', LOG_FILE);
  const logDir = path.dirname(logPath);

  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }

  let log = [];
  if (fs.existsSync(logPath)) {
    try {
      log = JSON.parse(fs.readFileSync(logPath, 'utf-8'));
    } catch (e) {
      log = [];
    }
  }

  const promotion = {
    timestamp: new Date().toISOString(),
    agentPath,
    patternsPromoted: promotablePatterns.length,
    patterns: promotablePatterns.map(p => ({
      pattern: p.pattern,
      occurrences: p.count,
      uniqueAgents: p.agentCount
    }))
  };

  log.push(promotion);
  fs.writeFileSync(logPath, JSON.stringify(log, null, 2), 'utf-8');
  console.log(`Logged promotion activity to ${LOG_PATH}`);
}

/**
 * Main execution
 */
function main() {
  console.log('='.repeat(60));
  console.log('Cross-Agent Pattern Promotion Cron Job');
  console.log('='.repeat(60));
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log(`Min occurrences for promotion: ${MIN_OCCURRENCES}`);
  console.log('');

  try {
    // Scan all agents
    console.log('Scanning agent LEARNINGS.md files...');
    const patterns = scanAllAgents();
    console.log(`Found ${patterns.length} pattern entries across all agents`);
    console.log('');

    // Analyze patterns
    console.log('Analyzing pattern distribution...');
    const patternCounts = analyzePatterns(patterns);
    console.log(`Unique patterns: ${Object.keys(patternCounts).length}`);
    console.log('');

    // Filter promotable patterns
    console.log(`Filtering patterns with ${MIN_OCCURRENCES}+ occurrences...`);
    const promotablePatterns = filterPromotablePatterns(patternCounts);
    console.log(`Found ${promotablePatterns.length} promotable patterns`);
    console.log('');

    if (promotablePatterns.length > 0) {
      console.log('Promotable patterns:');
      promotablePatterns.forEach((p, i) => {
        console.log(`  ${i + 1}. "${p.pattern}" (${p.count}x, ${p.agentCount} agents)`);
      });
      console.log('');

      // Update each agent's shared-learnings.md
      const agentDirs = fs.readdirSync(AGENTS_DIR, { withFileTypes: true })
        .filter(d => d.isDirectory() && !d.name.startsWith('_') && !d.name.startsWith('.'));

      agentDirs.forEach(agentDir => {
        const agentPath = path.join(AGENTS_DIR, agentDir.name);
        updateSharedLearnings(agentPath, promotablePatterns);
      });
      console.log('');

      // Log promotion activity
      logPromotion('all', promotablePatterns);
    } else {
      console.log('No patterns meet promotion criteria.');
    }

    console.log('');
    console.log('Promotion job completed successfully.');
    console.log('='.repeat(60));

  } catch (error) {
    console.error('Error during pattern promotion:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main, scanAllAgents, analyzePatterns, filterPromotablePatterns };
