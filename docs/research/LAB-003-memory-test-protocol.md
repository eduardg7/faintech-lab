# LAB-003: 3-Session Memory Test Protocol

## Hypothesis
File-based structured memory (MEMORY.md + daily notes) enables agents to maintain context across sessions with >80% accuracy on follow-up questions.

## Test Design
- **Duration**: 3 sessions across 1-2 days
- **Test Agent**: faintech-pm (PM agent)
- **Test Content**: Mixed factual + contextual information shared in Session 1
- **Evaluation**: Recall accuracy measured in Sessions 2 and 3

---

## Session 1: Information Injection
**Date**: 2026-03-15 ~16:00 EET

**Goal**: Share specific information that agent must remember across sessions.

### Information Categories

#### 1. Factual Information (5 items)
1. **Project**: faintech-lab has 4 active experiments (LAB-001 through LAB-004)
2. **Team**: Faintech has 7 active agents (CEO, CTO, COO, CFO, CPO, CISO, PM)
3. **Date**: Sprint 2 Day 1 is March 15, 2026
4. **Location**: Workspace is at /Users/eduardgridan/faintech-lab
5. **Tech Stack**: Using OpenClaw framework with glm-4.7 model

#### 2. Contextual Nuance (5 items)
1. **Decision**: QA ownership is temporarily assigned to PM until dedicated QA agent exists
2. **Blocker**: OS-019 (PR DIRTY state) is blocking Sprint Board merge
3. **Priority**: P0 tasks override P1/P2 even if P0 is newer
4. **Protocol**: All task handoffs include owner, evidence, blocker, and next checkpoint
5. **Risk**: Chat API 404 errors are affecting inter-agent messaging reliability

#### 3. Preferences & Style (3 items)
1. **Communication**: Romanian and English allowed, never Chinese/Japanese
2. **Tone**: Direct and data-driven for PM role
3. **Workflow**: Git workflow requires PRs for all development work

### Session 1 Actions
1. Share all 13 information items with faintech-pm
2. Ask agent to verify understanding
3. Confirm agent writes to memory (MEMORY.md or daily note)
4. Record timestamp and session end

---

## Session 2: Short-Term Recall Test
**Date**: 2026-03-15 ~18:00 EET (2 hours after Session 1)
**Type**: Direct questions about factual + contextual info

### Questions (10 total, mixed)

#### Factual Recall (5 questions)
1. "How many active experiments does faintech-lab have? List their IDs."
2. "What is the complete list of active Faintech agents?"
3. "What is the date of Sprint 2 Day 1?"
4. "What is the full path to the faintech-lab workspace?"
5. "What framework and model does Faintech use?"

#### Contextual Nuance (5 questions)
1. "Who is handling QA responsibilities right now and why?"
2. "What is blocking the Sprint Board merge?"
3. "How should we prioritize tasks if we have a P0 from today and a P1 from yesterday?"
4. "What 4 elements must every task handoff include?"
5. "What risk affects inter-agent messaging reliability?"

### Scoring
- **Factual**: 1 point per correct answer (max 5)
- **Contextual**: 1 point per correct answer (max 5)
- **Partial credit**: 0.5 points for partially correct answers

**Expected Performance (Session 2)**:
- Factual: ≥80% (4/5 or 5/5)
- Contextual: ≥60% (3/5 or better)

---

## Session 3: Long-Term Recall Test
**Date**: 2026-03-16 ~10:00 EET (next day morning)
**Type**: Applied scenarios requiring context from Session 1

### Scenario Questions (6 total)

#### Scenario-Based Recall (3 questions)
1. "We need to schedule a meeting for all agents. Who should be invited?"
2. "A new P0 task arrives. How should it be prioritized against a P1 task from yesterday?"
3. "The Sprint Board PR is stuck. What blocker is causing this?"

#### Preference-Based Recall (3 questions)
1. "Draft a task description for a new experiment. What language and tone should you use?"
2. "You need to submit code for LAB-004. What workflow must you follow?"
3. "A developer asks about QA approval. What's the current ownership model?"

### Scoring
- **Scenario-based**: 1 point per correct application of context (max 3)
- **Preference-based**: 1 point per correct application of preference (max 3)
- **Partial credit**: 0.5 points for partially correct applications

**Expected Performance (Session 3)**:
- Overall: Same thresholds as Session 2 (≥80% factual, ≥60% contextual)

---

## Evaluation Criteria

### Success Thresholds
- **Factual Recall**: ≥80% across Sessions 2 and 3
- **Contextual Recall**: ≥60% across Sessions 2 and 3
- **Overall**: Both thresholds must be met for hypothesis validation

### Data Collection
- Record all questions and answers verbatim
- Time response latency (seconds from question to answer)
- Track which agent memory sources are referenced (MEMORY.md, daily notes, or neither)
- Note any confusion or "I don't remember" responses

### Hypothesis Outcomes

#### Result: Validated
- Factual ≥80% AND Contextual ≥60%
- Agent consistently references MEMORY.md or daily notes
- Answers are accurate and contextually appropriate

#### Result: Partially Validated
- Factual ≥80% but Contextual <60%
- OR Factual <80% but Contextual ≥60%
- Agent recalls some information but misses nuance

#### Result: Not Validated
- Factual <80% AND Contextual <60%
- Agent shows no evidence of cross-session retention
- Multiple "I don't remember" responses

---

## Artifacts
- Session transcripts (all 3 sessions)
- Scoring spreadsheet with detailed results
- Analysis of memory sources accessed
- Recommendations for improving agent memory (if needed)

---

**Created**: 2026-03-15T16:00:00Z
**Experiment ID**: LAB-003
**Status**: Protocol designed, ready for Session 1 execution
