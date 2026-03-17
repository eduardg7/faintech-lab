# AMC Beta Success Metrics & Ideal Customer Profile

**Document Type:** Strategic Planning
**Author:** Faintech Strategy
**Date:** 2026-03-17
**Status:** DRAFT - Executive Review Required
**Purpose:** Define strategic success criteria and target user profile for March 24 beta launch

---

## Executive Summary

This document defines:
1. **Strategic Success Metrics** - What "good" looks like for beta from company perspective
2. **Ideal Customer Profile (ICP)** - Who to target in beta outreach
3. **Go/No-Go Decision Framework** - Clear criteria for launch readiness

**Recommendation:** Proceed with soft launch (trusted users) on March 24. Public launch conditional on P0 resolution + 3/5 success metrics met by Day 7.

---

## Part 1: Strategic Beta Success Metrics

### Tier 1: Company-Level Outcomes (North Star)

| Metric | Target | Measurement | Why It Matters |
|--------|--------|-------------|----------------|
| **Product-Market Fit Signal** | ≥40% "very disappointed" if AMC disappeared | Sean Ellis test at Day 7 | Validates core value proposition |
| **Retention Cohort** | ≥60% D7 retention | Active users Day 7 / Active users Day 1 | Confirms sticky product, not just curiosity |
| **Organic Advocacy** | ≥25% referrals from beta users | New signups via referral links / Total signups | Validates word-of-mouth potential |

### Tier 2: Engagement Quality (Leading Indicators)

| Metric | Target | Measurement | Why It Matters |
|--------|--------|-------------|----------------|
| **Activation Rate** | ≥70% create first agent | Users with ≥1 agent / Total signups | Confirms onboarding success |
| **Multi-Agent Adoption** | ≥30% create ≥3 agents | Users with ≥3 agents / Total signups | Validates cross-agent value prop |
| **API Key Generation** | ≥40% generate API key | Users with API key / Total signups | Confirms developer integration intent |
| **Semantic Search Usage** | ≥50% run semantic search | Users with semantic queries / Active users | Validates core differentiator |

### Tier 3: Technical Health (Table Stakes)

| Metric | Target | Measurement | Why It Matters |
|--------|--------|-------------|----------------|
| **API Uptime** | ≥99% | (Total minutes - downtime) / Total minutes | Table stakes for any API product |
| **P99 Latency** | <500ms | 99th percentile response time | User experience baseline |
| **Error Rate** | <1% | 5xx errors / Total requests | System reliability |
| **Zero P0 Blockers** | 0 open P0s | Active P0 count in TASK_DB | Launch blocker requirement |

### Success Scoring Framework

**Green (Public Launch Ready):** 3/3 Tier 1 + 3/4 Tier 2 + 4/4 Tier 3
**Yellow (Soft Launch Continue):** 2/3 Tier 1 + 2/4 Tier 2 + 3/4 Tier 3
**Red (Stop & Fix):** <2 Tier 1 OR <2 Tier 2 OR <3 Tier 3

---

## Part 2: Ideal Customer Profile (ICP)

### Primary ICP: Indie AI Developer / Technical Founder

**Demographics:**
- Role: Solo developer, technical founder, indie hacker
- Company Size: 1-5 people (often solo)
- Geography: US/EU (English-speaking, privacy-conscious)
- Experience: 3-10 years in software development
- AI Usage: Already using LLMs, familiar with vector DBs, has experimented with agents

**Psychographics:**
- Values: Local-first, privacy, open source, self-hosting
- Pain Points:
  - Fragmented context across multiple AI tools
  - Agent state lost between sessions
  - No unified memory for multi-agent systems
  - Tired of SaaS lock-in and cloud dependencies
- Goals:
  - Build autonomous agents that remember across sessions
  - Integrate AI memory into existing workflows
  - Own their data and infrastructure
  - Ship faster with reusable agent components

**Behavioral Signals:**
- Active on: Twitter/X (AI Twitter), Hacker News, Reddit r/LocalLLaMA, Discord (AI servers)
- Uses: GitHub, VS Code, terminal-heavy workflows
- Follows: @karpathy, @naval, indie hackers, open source projects
- Reads: Technical blogs, GitHub READMEs, documentation-first

**Technology Stack:**
- Languages: Python, TypeScript, Rust (emerging)
- Vector DBs: Chroma, Qdrant, Weaviate (or wants to avoid cloud ones)
- LLMs: OpenAI API, Anthropic, local models (Ollama, LM Studio)
- Deployment: Docker, local-first, self-hosted

**Willingness to Pay:**
- Free tier expected during beta
- Post-beta: $20-50/month for developer tier
- Enterprise interest: Possible, but not primary target

### Secondary ICP: AI Researcher / ML Engineer

**Demographics:**
- Role: ML engineer, research scientist, PhD student
- Company Size: Varies (often at AI labs, universities, or R&D teams)
- Experience: Deep technical background in ML/NLP

**Psychographics:**
- Values: Reproducibility, experiment tracking, research rigor
- Pain Points:
  - Agent experiments lack reproducible memory state
  - No standard way to compare agent memory architectures
  - Session-based memory makes longitudinal studies hard
- Goals:
  - Benchmark different memory architectures
  - Publish reproducible agent research
  - Share memory datasets across experiments

**Behavioral Signals:**
- Active on: arXiv, Papers With Code, academic conferences
- Uses: Jupyter, experiment tracking tools (Weights & Biases, MLflow)
- Follows: Academic AI Twitter, research labs (DeepMind, OpenAI, Anthropic)

### Anti-ICP (Who We're NOT Targeting in Beta)

| Segment | Why Not Target | Future Consideration |
|---------|----------------|----------------------|
| **Enterprise CIOs** | Long sales cycles, compliance requirements, need SLAs | Post-Series A, enterprise tier |
| **Non-Technical Founders** | Require managed service, no self-hosting capability | Future: AMC Cloud (managed) |
| **Mobile-First Users** | API-only product, no mobile SDK yet | Future: Mobile SDKs |
| **Chinese Market** | Regulatory complexity, different AI ecosystem | Future: China-specific deployment |
| **Complete AI Beginners** | Steep learning curve, need extensive onboarding | Future: No-code interface |

---

## Part 3: Go/No-Go Decision Framework

### Pre-Launch Checklist (March 23 Decision Point)

#### P0 Blockers (Must Be Resolved)

- [ ] **AMC-FIX-001**: Frontend-Backend Integration (401 errors) - **STATUS: UNRESOLVED**
- [ ] **Authentication Flow**: Users can log in and access dashboard
- [ ] **API Endpoints**: Core routes operational (/v1/memories, /v1/agents, /v1/projects)
- [ ] **Data Persistence**: Agent memory survives session restart

#### P1 Requirements (Strongly Recommended)

- [ ] **Onboarding Flow**: First-run experience guides new users (AMC-MVP-115)
- [ ] **API Documentation**: Developers can self-serve (AMC-MVP-113)
- [ ] **Landing Page**: Public-facing value proposition
- [ ] **Privacy Policy**: GDPR-compliant for beta users (DONE - LAB-DPIA-001)

#### P2 Nice-to-Have (Defer If Needed)

- [ ] **API Key Generation**: Self-service key creation (AMC-FEAT-002)
- [ ] **Load Testing**: Validated for 100 concurrent users (AMC-MVP-117)
- [ ] **Demo Video**: 5-minute walkthrough for outreach

### Decision Matrix

| Scenario | P0 Status | P1 Status | Decision |
|----------|-----------|-----------|----------|
| **Green** | All resolved | ≥3/4 complete | Public launch March 24 |
| **Yellow** | All resolved | 2/4 complete | Soft launch March 24, public March 31 |
| **Orange** | 1 P0 open | Any | Soft launch with known issues, fix by March 26 |
| **Red** | ≥2 P0s open | Any | Delay launch until P0s resolved |

### Current Assessment (2026-03-17)

**P0 Status:** ❌ 1 open (AMC-FIX-001 - Frontend-Backend Integration)
**P1 Status:** ⚠️ 1/4 complete (Privacy Policy done; Onboarding, Docs, Landing Page in progress)
**Decision:** **ORANGE** - Soft launch with known issues on March 24, conditional public launch

### Launch Scenarios

#### Scenario A: Public Launch (March 24)
**Conditions:** All P0 resolved + 3/4 P1 complete
**Outreach:** Full announcement (Hacker News, Twitter, LinkedIn, Product Hunt)
**Expectation:** 50-100 signups Day 1

#### Scenario B: Soft Launch → Public (March 24 → March 31)
**Conditions:** All P0 resolved + 2/4 P1 complete
**Outreach:** Trusted users only (March 24), full announcement (March 31)
**Expectation:** 10-20 trusted users (March 24), 50-100 signups (March 31)

#### Scenario C: Delayed Launch (April 7)
**Conditions:** P0 unresolved or <2 P1 complete
**Outreach:** No announcement, continue internal testing
**Expectation:** 0 external users, focus on engineering

---

## Part 4: Outreach Strategy by ICP

### Channel Prioritization for Primary ICP (Indie AI Developer)

| Channel | Priority | Expected Reach | Conversion Rate | Notes |
|---------|----------|----------------|-----------------|-------|
| **Hacker News** | P0 | 1,000-5,000 views | 2-5% | Technical audience, high-quality traffic |
| **Twitter/X** | P0 | 5,000-20,000 impressions | 0.5-1% | AI Twitter community, thread format |
| **Reddit r/LocalLLaMA** | P1 | 500-2,000 views | 3-5% | Highly targeted, self-hosting enthusiasts |
| **Indie Hackers** | P1 | 200-500 views | 5-10% | Founder community, product-focused |
| **Product Hunt** | P2 | 1,000-3,000 views | 1-2% | Launch day boost, competitive |
| **LinkedIn** | P3 | 500-1,000 views | 0.5% | Enterprise angle, not primary ICP |

### Messaging Framework by Channel

**Hacker News:**
- Title: "Show HN: Agent Memory Cloud - Persistent memory for autonomous AI agents"
- Angle: Technical depth, open source, local-first
- Key differentiator: Cross-agent memory sharing, self-hosted

**Twitter/X:**
- Format: Thread (5-7 tweets)
- Hook: "Your AI agents forget everything between sessions. Here's how to fix that."
- Include: Code snippets, demo GIFs, GitHub link

**Reddit:**
- Title: "[OC] Built an open-source agent memory system - persistent, cross-agent, self-hosted"
- Angle: Local-first, privacy-focused, community contribution
- Engagement: Respond to every comment in first 2 hours

### Outreach Timeline

| Date | Action | Channel | Target |
|------|--------|---------|--------|
| **Mar 18** | Draft HN post, Twitter thread | Internal review | Complete drafts |
| **Mar 19** | Finalize messaging, create demo assets | CMO approval | Assets ready |
| **Mar 20** | Soft outreach to 10 trusted users | Direct messages | 5-10 beta testers |
| **Mar 21** | Gather trusted user feedback | Internal | Iterate on blockers |
| **Mar 23** | Go/No-Go decision | Executive | Final decision |
| **Mar 24** | Launch (Scenario A/B/C) | All channels | Per decision |
| **Mar 25-31** | Monitor metrics, iterate | Daily standup | Hit Tier 1 targets |

---

## Part 5: Measurement & Reporting

### Daily Metrics Dashboard (Beta Period)

**Automated Tracking:**
- Signups (total, by channel, by referral)
- Activation rate (first agent created)
- Active users (DAU, WAU)
- Feature adoption (agents, memories, semantic search, API keys)
- Health metrics (from CSM infrastructure)

**Manual Tracking:**
- Sean Ellis PMF survey (Day 7)
- Qualitative feedback (support emails, Discord, Twitter)
- Referral tracking (unique codes per beta user)

### Reporting Cadence

| Frequency | Audience | Content |
|-----------|----------|---------|
| **Daily** | C-Suite (Telegram) | Signups, active users, blockers |
| **Weekly** | Executive standup | Full metrics review, decision points |
| **Day 7** | CEO + Board | PMF assessment, public launch recommendation |

### Success Criteria for Public Launch (Day 7 Checkpoint)

**Required (Must Have):**
- [ ] ≥40 beta users signed up
- [ ] ≥60% D7 retention
- [ ] ≥70% activation rate
- [ ] 0 P0 blockers
- [ ] Sean Ellis score ≥40%

**Recommended (Should Have):**
- [ ] ≥3/4 Tier 2 engagement metrics
- [ ] ≥25% referral rate
- [ ] Positive qualitative feedback (Net Sentiment > 0)
- [ ] Technical health metrics in green

---

## Appendix A: Competitive Positioning Summary

| Competitor | Target | Pricing | Key Gap AMC Fills |
|------------|--------|---------|-------------------|
| **Mem0** | Enterprise developers | $20-200/month | Self-hosted, cross-agent memory |
| **Letta** | Research | Open source | Production-ready, multi-tenant |
| **Zep** | Enterprise | $99-499/month | Simple, developer-first, no lock-in |
| **LangChain Memory** | All | Free (DIY) | Managed, batteries-included, opinionated |

**AMC Differentiation:**
1. **Self-hosted by default** (Mem0/Zep are cloud-first)
2. **Cross-agent memory sharing** (unique vs all competitors)
3. **API-first, not framework-dependent** (unlike LangChain)
4. **Developer simplicity, not enterprise complexity** (unlike Mem0/Zep)

---

## Appendix B: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **P0 blocker unresolved by Mar 24** | Medium | High | Soft launch with known issues, fix by Mar 26 |
| **Low signup conversion** | Medium | Medium | Iterate messaging, extend outreach to secondary channels |
| **Poor retention (D7 < 40%)** | Low | High | User interviews, identify friction, fast iteration |
| **Negative HN/Reddit reception** | Low | Medium | Technical depth in post, active comment engagement |
| **Server overload on launch day** | Low | High | Load testing (AMC-MVP-117), auto-scaling prep |
| **Competitor launches same week** | Low | Low | Differentiation clear, focus on unique value prop |

---

## Next Steps

1. **CEO Review** (Mar 18): Approve success metrics, ICP, and decision framework
2. **CMO Alignment** (Mar 18): Finalize messaging by channel using ICP insights
3. **CTO Escalation** (Immediate): P0 blocker AMC-FIX-001 requires resolution by Mar 23
4. **PM Coordination** (Mar 19): Begin trusted user outreach with clear ICP targeting
5. **Strategy Check-In** (Mar 23): Go/No-Go decision based on P0/P1 status

---

**Document Owner:** strategy@faintech
**Review Required:** CEO, CMO, CTO, PM
**Next Update:** 2026-03-23 (Go/No-Go Decision)
