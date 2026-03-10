# PROD-002 Prep: Customer Discovery Interview Questions

Owner: faintech-cpo | Created: 2026-03-10 | Status: Draft

---

## Purpose

Prepared interview questions for PROD-002 (Market Research & Customer Discovery).
Target: 10 interviews with technical founders running AI agent fleets.

---

## Interview Questions

### Screening Questions (2 min)

1. "How many AI agents are you currently running in production?"
2. "What's your current approach to agent memory/persistence?"
   - [ ] Files/JSON
   - [ ] Database (Postgres, SQLite)
   - [ ] Vector DB (Pinecone, Weaviate)
   - [ ] Custom solution
   - [ ] No memory (stateless)

### Problem Discovery (10 min)

3. "Tell me about the last time an agent made a mistake that could have been prevented with better memory."
   - Follow-up: "What was the impact?" (time, money, user trust)

4. "How do you currently share learnings between agents?"
   - [ ] Manual copy-paste
   - [ ] Shared database
   - [ ] Each agent learns independently
   - [ ] Other: _______

5. "What percentage of your time is spent re-explaining context to agents?"
   - [ ] <10%
   - [ ] 10-25%
   - [ ] 25-40%
   - [ ] >40%

### Pain Prioritization (3 min)

6. "Rank these problems from most painful (1) to least (4):"
   - [ ] Agents repeat same mistakes
   - [ ] No compound learning across sessions
   - [ ] Can't share learnings between agents
   - [ ] Debugging why agent made a decision

### Solution Validation (5 min)

7. "If you had a hosted API where agents could read/write memories automatically, and learnings from Agent A helped Agent B — would you use it?"

8. "What would you pay monthly for this?" (give ranges)
   - [ ] $0-25
   - [ ] $25-50
   - [ ] $50-100
   - [ ] $100-200
   - [ ] >$200

9. "What would make you NOT trust this?"
   - Security concerns?
   - Lock-in worries?
   - Latency?
   - Reliability?

### Competitive Landscape (3 min)

10. "Have you tried any existing solutions?"
    - Mem0, MemGPT, LangChain memory, others?
    - What worked / didn't work?

---

## Success Criteria for PROD-002

- 10 completed interviews with target persona
- Clear pattern on willingness to pay
- Feature prioritization based on pain scores
- Competitive gaps identified
- 3-5 beta signup commitments

---

## Interview Scheduling

Target timeline: 2 weeks after CEO approval of PROD-001

**Outreach channels:**
- Twitter/X DM to technical founders
- HN "Who is hiring" thread responders (AI companies)
- Direct outreach to YC W24/W25 AI batch companies
- LinkedIn technical founders

**Incentive:** Early access + free tier upgrade

---

_This document is prep work for PROD-002. Execution pending CEO approval of PROD-001._
