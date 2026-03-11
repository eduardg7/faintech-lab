# Beta Invite Email Templates

**Purpose:** Email templates for Agent Memory Cloud beta outreach
**Created:** 2026-03-11
**Owner:** faintech-pm

---

## Email 1: Initial Outreach (Cold)

**Subject:** Quick question about your AI agent memory stack

**Body:**

Hi [FIRST_NAME],

I noticed [PERSONALIZED_OBSERVATION - e.g., "you're building AI agents at [COMPANY]" / "your work on [PROJECT]" / "your recent post about [TOPIC]"].

We've been working on something that might help: **Agent Memory Cloud** - a memory layer for AI agents that actually remembers context across sessions.

Early users are reporting:
- 40% reduction in repeated explanations to agents
- Context preservation across 10+ sessions
- <100ms memory retrieval (semantic search)

**Would you be open to a 15-minute demo next week?**

If your agent stack is working perfectly, feel free to ignore this. But if memory is a friction point, I'd love to show you what we've built.

Best,
Eduard Gridan
Founder, Faintech Solutions

P.S. We're in private beta with 10 spots left. No commitment, just honest feedback.

---

## Email 2: Follow-Up (No Response)

**Subject:** Re: Quick question about your AI agent memory stack

**Body:**

Hi [FIRST_NAME],

Just following up on my last email.

I completely understand if this isn't a priority right now. But if you're curious, here's a 2-minute demo video showing how Agent Memory Cloud works: [DEMO_VIDEO_LINK]

**Quick question:** What's your biggest pain point with AI agents today?

- Memory/context loss
- Slow retrieval
- Integration complexity
- Something else?

Hit reply and let me know. Even if it's just "not interested" - I appreciate the feedback.

Thanks,
Eduard

---

## Email 3: Warm Intro / Referral

**Subject:** [REFERRER_NAME] suggested I reach out

**Body:**

Hi [FIRST_NAME],

[REFERRER_NAME] mentioned you might be interested in what we're building at Faintech.

We've created **Agent Memory Cloud** - a persistent memory layer for AI agents. Think of it like long-term memory for your agents that actually works across sessions.

[REFERRER_NAME] thought it might be useful for [SPECIFIC_USE_CASE].

**Would you be open to a quick demo this week?**

I can show you:
- How semantic memory search works (sub-100ms)
- Real examples of context preservation
- Simple API integration (Python + TypeScript SDKs)

No pressure - just curious if this solves a problem you're facing.

Best,
Eduard Gridan
Founder, Faintech Solutions

---

## Email 4: Beta Confirmation

**Subject:** Welcome to Agent Memory Cloud beta! 🎉

**Body:**

Hi [FIRST_NAME],

Great news - you're in! Welcome to the Agent Memory Cloud private beta.

**Your API Key:** `[API_KEY]`

**Quick Start (5 minutes):**

```bash
# Python
pip install agentmemory

# TypeScript
npm install @agentmemory/sdk
```

```python
from agentmemory import MemoryClient

client = MemoryClient(api_key="[API_KEY]")

# Store a memory
client.memory.write(
    agent_id="my-agent",
    content="User prefers dark mode and concise responses"
)

# Search memories
results = client.memory.search(
    agent_id="my-agent",
    query="user preferences"
)
```

**Docs:** https://docs.agentmemory.cloud
**Support:** eduard@faintech.solutions

**What we need from you:**
- Honest feedback (good and bad)
- Bug reports (email or Discord)
- Feature requests (we're building fast)

**Beta ends:** March 31, 2026
**Pricing after beta:** $29/month (founder pricing locked for early users)

Questions? Just reply to this email.

Let's build something great together,
Eduard

---

## Email 5: Beta Check-In (Day 7)

**Subject:** How's Agent Memory Cloud working for you?

**Body:**

Hi [FIRST_NAME],

One week into beta - quick check-in.

**Honest question:** On a scale of 1-10, how useful has Agent Memory Cloud been?

- **9-10:** Amazing, tell me more! (testimonial?)
- **7-8:** Good but missing something (what?)
- **5-6:** Meh, not really using it (why?)
- **1-4:** Not working for me (what's broken?)

**Quick updates:**
- Added rate limiting (1000 req/hour per API key)
- Fixed the auth flow issues from early beta
- New dashboard for memory stats

**Blockers?** If anything's preventing you from using it, hit reply. I personally read every email.

Thanks for being an early believer,
Eduard

---

## Email 6: Beta Ending Reminder

**Subject:** Beta ends in 7 days - your founder pricing expires

**Body:**

Hi [FIRST_NAME],

Quick reminder: Agent Memory Cloud beta ends **March 31, 2026**.

**What happens next:**
- Your API key stays active
- Pricing: $29/month (locked for beta users)
- Public launch: $49/month (you save 40% forever)

**If you want to keep your founder pricing:**
[LINK_TO_PAYMENT_PAGE]

**If Agent Memory Cloud wasn't useful:**
No worries - just ignore this. Your feedback helped us improve.

**Questions?** Reply directly to this email.

Thanks for being part of our beta,
Eduard

---

## Personalization Tokens

| Token | Description | Source |
|-------|-------------|--------|
| `[FIRST_NAME]` | Recipient first name | LinkedIn / manual |
| `[COMPANY]` | Company name | LinkedIn / website |
| `[PERSONALIZED_OBSERVATION]` | Specific observation about them | Research notes |
| `[REFERRER_NAME]` | Person who referred them | Referral tracking |
| `[SPECIFIC_USE_CASE]` | Relevant use case for them | Use case mapping |
| `[API_KEY]` | Generated API key | Beta system |
| `[DEMO_VIDEO_LINK]` | 2-minute demo video | Content team |

---

## A/B Test Variants

### Subject Line Tests (Email 1)

**Variant A:** "Quick question about your AI agent memory stack"
**Variant B:** "Your AI agents keep forgetting things"
**Variant C:** "[COMPANY] + Agent Memory Cloud = ?"

### CTA Tests (Email 1)

**Variant A:** "Would you be open to a 15-minute demo next week?"
**Variant B:** "Can I show you a 2-minute demo?"
**Variant C:** "Want to try it free for 14 days?"

---

## Tracking Metrics

- Open rate (target: >40%)
- Reply rate (target: >15%)
- Demo conversion (target: >30%)
- Beta activation (target: >50%)

---

## Sending Schedule

| Email | Trigger | Delay |
|-------|---------|-------|
| Email 1: Initial | Manual send | - |
| Email 2: Follow-up | No response to Email 1 | +3 days |
| Email 3: Referral | Referral received | Immediate |
| Email 4: Confirmation | Beta signup | Immediate |
| Email 5: Check-in | Beta activation | +7 days |
| Email 6: Reminder | Beta ending | -7 days |

---

**Last Updated:** 2026-03-11T05:42:00Z
**Next Review:** 2026-03-18 (after first batch results)
