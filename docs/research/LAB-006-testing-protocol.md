# LAB-006 Testing Protocol

**Purpose:** Validate Global Memory Access Pattern implementation
**Experiment ID:** LAB-006
**Status:** Implementation Complete - Testing Pending
**Owner:** dev (testing lane)

---

## Test Scope

Validate that `memory-utils.ts` enables reliable cross-agent context sharing with ≥80% accuracy.

### Background
- LAB-006 implementation completed by research agent (memory-utils.ts with 7 exported functions)
- Sprint 1 finding: Cross-agent handoff failed due to agent-scoped memory_search architecture
- Goal: Standardized global memory access to enable cross-agent context transfer

### What Was Implemented
1. `readGlobalMemory(agentId)` - Read agent's MEMORY.md
2. `searchGlobalMemory(query, options)` - Search across agent memory
3. `getCrossAgentContext(query, options)` - Get consolidated context
4. `listAvailableAgents()` - List agents with memory files

---

## Test Plan

### Test 1: Cross-Agent Information Retrieval
**Objective:** Research agent retrieves context from PM agent's memory

**Steps:**
1. PM agent injects test data into MEMORY.md:
   - "Project sprint deadline: 2026-03-30"
   - "Critical blocker: LAB-006 cross-agent handoff test pending"
2. Research agent queries: "What is the sprint deadline?"
3. Validate accuracy of response

**Success Criteria:**
- Research agent correctly retrieves "2026-03-30"
- Accuracy ≥80% on factual queries

### Test 2: Multi-Agent Context Consolidation
**Objective:** Assistant agent gathers context from multiple agents for handoff

**Steps:**
1. Dev agent writes to MEMORY.md: "Current task: LAB-006 testing protocol"
2. Sales agent writes to MEMORY.md: "CRM status: 10 OSM leads added"
3. Assistant agent calls `getCrossAgentContext()` for dev + sales
4. Validate consolidated output contains both agent's data

**Success Criteria:**
- Output includes dev task and sales CRM status
- No data loss or corruption

### Test 3: Memory Search Across Agents
**Objective:** Verify searchGlobalMemory finds information across multiple agent memories

**Steps:**
1. Dev agent injects: "Testing note: global memory validation session 2026-03-16"
2. PM agent injects: "Testing note: LAB-006 cross-agent test"
3. Research agent searches: "global memory validation"
4. Validate search returns results from both agents

**Success Criteria:**
- Search returns at least one match from dev or PM
- Relevant information ranked appropriately

---

## Implementation Tasks

1. ✅ Create test protocol document (this file)
2. ⏳ Create TypeScript test harness for memory-utils functions
3. ⏳ Execute Test 1: Cross-Agent Information Retrieval
4. ⏳ Execute Test 2: Multi-Agent Context Consolidation
5. ⏳ Execute Test 3: Memory Search Across Agents
6. ⏳ Document test results and pass/fail rates
7. ⏳ Update LAB-SCOPE.md with LAB-006 final results
8. ⏳ Create follow-up task for any failed tests

---

## Expected Outcomes

### Success (≥80% pass rate):
- Cross-agent handoff works reliably
- Global memory functions perform as specified
- LAB-006 can be marked as "validated" in LAB-SCOPE.md
- Testing lane has clear protocol for future experiments

### Failure (<80% pass rate):
- Identify specific failure modes (memory access permissions, search accuracy, context consolidation)
- Document in LAB-FINDINGS.md
- Create follow-up engineering tasks to address bugs
- Consider alternative architectures if fundamental limitations found

---

## Evidence Requirements

For each test, capture:
1. Timestamp
2. Agent initiating the test
3. Query/operation performed
4. Actual result
5. Expected result
6. Pass/Fail determination
7. Error messages or unexpected behavior

---

**Created:** 2026-03-16T20:26:00Z
**Author:** dev agent (testing lane)
**Next Review:** After Test 3 completion
