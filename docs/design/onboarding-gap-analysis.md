# Onboarding Flow Gap Analysis

**Date:** 2026-03-22 23:20 EET
**Owner:** faintech-product-designer
**Status:** Documented for post-beta roadmap

---

## Executive Summary

Design spec and implementation have diverged. The spec describes an **agent-centric flow** (create agent → write memory → search memory), while the implementation uses a **workspace-centric flow** (workspace setup → API key → first memory).

**Key Gap:** Search Memory step is missing from implementation.

**Beta Impact:** LOW - Current implementation is acceptable for beta launch (Mar 24, 2 days)
**Post-Beta Priority:** HIGH - Add search step to demonstrate full value loop

---

## Spec vs Implementation Comparison

### Design Spec Flow
**Source:** `/Users/eduardgridan/faintech-lab/docs/design/onboarding-flow-first-run-spec.md`

1. **Welcome** (20s) - Orient user, set expectations
2. **Setup Agent** (60s) - Create agent identity
3. **Write Memory** (120s) - Demonstrate storage
4. **Search Memory** (90s) - **Demonstrate retrieval** ← CORE VALUE
5. **Success** (10s) - Celebrate completion

**Total Time:** 5 minutes

### Implementation Flow
**Source:** `/Users/eduardgridan/faintech-lab/amc-frontend/src/components/OnboardingFlow.tsx`

1. **Welcome** - Introduction
2. **Workspace Setup** - Name workspace
3. **API Key Generation** - Auth setup
4. **First Memory** - Write memory
5. **Success** - Completion

**Missing:** Search Memory step

---

## Gap Analysis

### 1. Search Memory Step (MISSING)

**Why It Matters:**
- **Core value prop:** AMC is about *persistent memory + retrieval*, not just storage
- **First Magic Moment:** Search/retrieval is the "magic" - without it, users only see half the value
- **User understanding:** Users won't understand the full product without experiencing search
- **Success metric:** Spec targets 85% search success rate - can't measure without the step

**Current Mitigation:**
- Users can discover search in dashboard post-onboarding
- Quick Start Guide mentions search functionality
- Not blocking for beta launch

**Recommendation:**
- **Beta (Mar 24):** Accept current implementation
- **Post-beta (Week 1-2):** Add Search Memory step as Step 4

### 2. Agent vs Workspace Centric

**Spec:** Agent-centric (create agent first)
**Implementation:** Workspace-centric (setup workspace first)

**Analysis:**
- Both approaches are valid
- Workspace-centric may be better for team context
- Agent creation can happen in dashboard
- **No action needed** - implementation choice is acceptable

### 3. API Key Step

**Spec:** Not explicitly mentioned (assumed backend handles)
**Implementation:** Explicit API key generation step

**Analysis:**
- Implementation is more explicit about auth
- Good for technical users (beta audience)
- Aligns with security best practices
- **No action needed** - implementation improves on spec

---

## Recommendations

### For Beta Launch (Mar 24, 2 days)
✅ **PROCEED** with current implementation
- Onboarding flow is functional
- Users can complete setup and write first memory
- Search can be discovered in dashboard
- No blocking issues

### For Post-Beta (Week 1-2)
🔴 **HIGH PRIORITY:** Add Search Memory step

**Implementation Plan:**
1. Add new step between "First Memory" and "Success"
2. Pre-populate search with keywords from user's memory
3. Show instant results with highlighting
4. Celebrate successful retrieval
5. Update success screen to include search accomplishment

**Success Metrics:**
- 85% users successfully search and find their memory
- Average 2-3 search queries per user
- 90% find memory in first 3 results

---

## Design Principles Applied

1. **Recognition over Recall (Nielsen):** Users need to see search to understand its value
2. **First Magic Moment:** Search/retrieval is the magic - demonstrates full value prop
3. **Progressive Disclosure:** Show core features during onboarding, advanced features in dashboard
4. **User Control:** Allow skip, but encourage completion

---

## Next Steps

1. **faintech-frontend:** Review this analysis for post-beta roadmap
2. **cpo:** Prioritize search step for Week 1-2 post-launch
3. **pm:** Add to post-beta task backlog
4. **qa:** Test search functionality in dashboard (ensure it works for beta users)

---

## References

- Design Spec: `/Users/eduardgridan/faintech-lab/docs/design/onboarding-flow-first-run-spec.md`
- Implementation: `/Users/eduardgridan/faintech-lab/amc-frontend/src/components/OnboardingFlow.tsx`
- Quick Start Guide: `/Users/eduardgridan/faintech-lab/docs/customer-success/quick-start-guide.md`

---

**Document Status:** Complete
**Review Required:** faintech-frontend, cpo
**Timeline:** Post-beta Week 1-2
