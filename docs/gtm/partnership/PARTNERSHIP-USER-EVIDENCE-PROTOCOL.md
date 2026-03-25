# Partnership Channel User Evidence Protocol

**Created:** 2026-03-23 22:30 EET
**Owner:** faintech-user-researcher
**Purpose:** Specialized evidence collection for partnership-sourced beta users
**Channels:** LangChain Discord, Indie Hackers

---

## Why Partnership Users Are Different

Partnership users differ from organic Tier 2 signups:
- **Higher engagement:** They're already active in AI/build communities
- **Better feedback quality:** Technical users can articulate nuanced pain points
- **Influencer potential:** Moderators/power users have credibility in their communities
- **Network effects:** Positive experience can trigger word-of-mouth referrals

**Implication:** These users warrant **high-priority tracking** and **1:1 interview outreach**.

---

## Evidence Collection Protocol

### For Each Partnership Signup

#### Step 1: Identify Partnership Origin
Check beta code used:
- `FAIN-LC-2026-*` → LangChain Discord
- `FAIN-IH-2026-*` → Indie Hackers

Record in signup JSON:
```json
{
  "acquisition": {
    "source": "partnership",
    "partner": "langchain_discord|indie_hackers",
    "beta_code": "FAIN-LC-2026-X7K9",
    "referral_type": "moderator|power_user|community_member"
  }
}
```

#### Step 2: Immediate Classification
Assign **follow_up.priority = "high"** for all partnership signups.

Reasoning:
- Limited number of partnership slots (5-10 total)
- High-quality feedback expected
- Potential for long-term champion users

#### Step 3: Trigger Outreach Sequence
**Within 24h of signup:**
1. Send personalized thank-you email (acknowledge partnership connection)
2. Schedule 20-min interview (prioritize over organic signups)
3. Add to "Partnership Cohort" tracking list

**Interview Script Adaptation:**
Add partnership-specific questions to standard beta interview:
- "How did you first hear about AMC? [Partner community name?]"
- "What made you trust the referral from [partner]?"
- "What other tools do you use alongside [LangChain/your stack]?"
- "Would you recommend AMC to others in [partner community]?"

---

## Success Metrics (Partnership Channel)

### Quantitative
| Metric | Target | Tracking Method |
|--------|--------|-----------------|
| Partnership signups | 5-10 (within Week 1) | Beta code redemption |
| Interview completion | 80%+ | Calendar tracking |
| NPS score | 9+ | Survey |
| Feature requests | 3+ per user | Interview notes |
| Referral to community | 2+ users | Signup attribution |

### Qualitative
- **Endorsement quality:** Would they publicly recommend AMC?
- **Integration depth:** Are they using AMC with LangChain/other tools?
- **Feedback richness:** Depth of technical feedback (not just "works/doesn't work")
- **Community signal:** Did they share in partner community? (Discord posts, threads)

---

## Partnership-Specific Evidence Files

### Directory Structure
```
/research/beta-user-evidence/
├── partnerships/
│   ├── langchain-discord/
│   │   ├── SIGNUP-LC-001.json
│   │   ├── SIGNUP-LC-002.json
│   │   └── interview-notes/
│   │       ├── INTERVIEW-LC-001.md
│   │       └── INTERVIEW-LC-002.md
│   ├── indie-hackers/
│   │   ├── SIGNUP-IH-001.json
│   │   └── interview-notes/
│   └── PARTNERSHIP-COHORT-ANALYSIS.md
```

### Cohort Analysis Template
**File:** `PARTNERSHIP-COHORT-ANALYSIS.md`

**Structure:**
```markdown
# Partnership Cohort Analysis

## LangChain Discord (Target: 3-5 users)
- Signups: X/5
- Interviews completed: Y/X
- Avg NPS: Z
- Top pain points: [list]
- Feature requests: [list]
- Referrals generated: N
- Endorsement status: [Yes/No/Pending]

## Indie Hackers (Target: 2 users)
- Signups: X/2
- [Same structure]

## Cross-Partner Insights
- Common pain points across both communities
- Different needs by community
- Product-market fit signals
```

---

## Interview Scheduling Priority

### Priority Queue
1. **Moderators** (highest) → Schedule within 24h
2. **Power users** (high) → Schedule within 48h
3. **Community members** (medium) → Schedule within 72h
4. **Organic signups** (standard) → Schedule within 1 week

### Scheduling Template
**Email for partnership users:**
```
Subject: Thanks for joining AMC beta + interview request

Hi [Name],

Thanks for signing up for Faintech Lab beta via [LangChain Discord/Indie Hackers]!

As a [moderator/power user] in the community, your feedback is especially valuable. Would you be open to a 20-min call this week to share your initial impressions?

[Calendly link]

In return, I'll prioritize any feature requests you have and keep you updated on roadmap decisions.

Best,
Eduard
```

---

## Red Flags to Watch For

### Warning Signs
- Partnership signup with **no engagement** after 48h → Escalate to CMO
- **Negative feedback** from moderator → Immediate escalation to CEO/CPO
- **Beta code sharing** outside intended recipients → Revoke code, notify partnerships
- **No interview responses** after 3 attempts → Downgrade to standard user

### Escalation Path
- CMO: Partnership health issues
- CPO: Product feedback from partners
- CEO: Strategic partnership concerns

---

## Reporting Cadence

### Daily (Week 1)
- Partnership signups count
- Interview completion rate
- Any red flags

### Weekly (Week 2-4)
- Cohort analysis update
- NPS trends
- Referral tracking
- Feature request synthesis

### End of Beta
- Comprehensive partnership ROI analysis
- Recommendations for post-beta partnership strategy

---

## Integration with Day 1 Checklist

**Add to Day 1 Evidence Collection Checklist:**

After "Launch Hour 0" section, add:
```
### Partnership Signup Detection
- [ ] Monitor for beta code redemptions (FAIN-LC-*, FAIN-IH-*)
- [ ] Create signup JSON for each partnership user
- [ ] Assign priority="high" and schedule interview within 24h
- [ ] Send personalized thank-you email same day
```

---

**Status:** READY FOR USE
**Integration:** Update Day 1 checklist with partnership detection steps
**Next Update:** After first partnership signup (Mar 24+)
