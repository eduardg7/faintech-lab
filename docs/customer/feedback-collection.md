# Beta Feedback Collection Mechanism

**Project:** Faintech Lab Beta
**Owner:** Customer Success Manager
**Last Updated:** 2026-03-17
**Purpose:** Systematically collect, triage, and act on beta user feedback

---

## Feedback Channels

### 1. In-App One-Click Rating (Primary)

**Trigger:** After key user actions
- Agent creation
- First message sent to agent
- Memory added
- Project created
- Search executed

**UI Component:**
```
+-----------------------------------+
| How was this experience?          |
|                                   |
| 😐 😊 😄                           |
|   ^  ^   ^                        |
|  /  /    \                        |
| |  |     |                        |
| 0  5    10                        |
|                                   |
| [Skip]                            |
+-----------------------------------+
```

**Data Stored:**
- User ID
- Action type (e.g., "agent_creation")
- Rating (0-10)
- Timestamp
- Anonymous (no message content)

**Frequency:**
- Maximum 1 rating per action type per day
- Skip button dismisses for 7 days

---

### 2. Net Promoter Score (NPS) Survey

**Trigger:** Weekly on Day 7 of beta usage

**UI Component:**
```
+-----------------------------------+
| How likely are you to recommend  |
| Faintech Lab to a friend or      |
| colleague?                        |
|                                   |
| [0] [1] [2] [3] [4] [5]          |
| [6] [7] [8] [9] [10]             |
|                                   |
| Not at all likely                |
|           Extremely likely       |
|                                   |
| [Submit] [Remind me later]       |
+-----------------------------------+
```

**Follow-up Question (conditional):**

If score 9-10:
```
What's the one thing you love most?
[Text input]
```

If score 0-6:
```
What could we do better?
[Text input]
```

**Data Stored:**
- User ID
- NPS score (0-10)
- Qualitative feedback (optional)
- Timestamp

**Frequency:**
- Once per week during beta (max 4 surveys)
- Opt-out option available in settings

---

### 3. In-App Feedback Form (On-Demand)

**Trigger:** User-initiated via "Give Feedback" button in sidebar

**UI Component:**
```
+-----------------------------------+
| Feedback for Faintech Lab        |
|                                   |
| Category: [Bug Report v]          |
|           [Feature Request v]     |
|           [General Feedback v]   |
|           [Other v]               |
|                                   |
| How was your experience?          |
| [😐 😊 😄]                        |
|                                   |
| Your feedback:                    |
| [                                  |
|   Text area                       |
|   (max 500 chars)                 |
| ]                                  |
|                                   |
| [Submit Feedback] [Cancel]       |
+-----------------------------------+
```

**Data Stored:**
- User ID
- Category
- Rating (0-10)
- Feedback text
- Timestamp
- Screenshots (optional, if user attaches)

**Frequency:**
- Unlimited, but throttled to max 3/hour per user

---

### 4. Support Email (Fallback)

**Trigger:** User-initiated via "Contact Support" link

**Email Template:**
```
Subject: [Feedback] {Category} - {User Name}

User ID: {user_id}
Email: {user_email}
Beta User Since: {signup_date}

Feedback:
{feedback_text}

---

This feedback was collected via email.
```

**Routing:**
- "Bug Report" → CTO (technical)
- "Feature Request" → CPO (product)
- "General Feedback" → CSM (customer success)
- "Other" → COO (general)

**SLA:**
- Bug Report: 24h response
- Feature Request: 48h response
- General Feedback: 72h response
- Other: 48h response

---

### 5. Passive Signals (Automated)

**Behavioral Signals (No user action required):**

| Signal | Definition | Threshold | Action |
|--------|------------|-----------|--------|
| **Rage Click** | Rapid repeated clicks on same element | 5 clicks in 3s | Log "UX friction" |
| **Session Timeout** | Session ends after <30s | <30s duration | Log "quick exit" |
| **Repeated Errors** | Same error appears 3+ times | 3 identical errors | Log "technical blocker" |
| **Feature Abandonment** | User starts flow, doesn't complete | 3 abandoned flows | Log "confusion point" |
| **Negative Keywords** | User types "frustrated", "broken", etc. | Any occurrence | Flag for review |

**Data Stored:**
- User ID
- Signal type
- Context (URL, action)
- Timestamp
- Anonymous (no user content)

---

## Feedback Triage

### Triage Categories

| Category | Owner | SLA | Action |
|----------|-------|-----|--------|
| **Critical Bug** | CTO | 4h | Fix immediately |
| **Major Bug** | CTO | 24h | Fix in next sprint |
| **Minor Bug** | CTO | 72h | Add to backlog |
| **Feature Request** | CPO | 1 week | Evaluate, prioritize |
| **UX Issue** | CPO | 48h | Review with design |
| **General Feedback** | CSM | 48h | Acknowledge, thank |
| **Billing/Account** | COO | 24h | Resolve directly |
| **Security** | CISO | 2h | Immediate investigation |

### Triage Process

1. **Ingest:** Feedback arrives via any channel
2. **Categorize:** Auto-categorize based on keywords, route to owner
3. **Prioritize:** Assign severity (P0-P2) based on impact
4. **Acknowledge:** Send "We received your feedback" email (within 1h)
5. **Action:** Owner acts within SLA
6. **Close:** Update user when action is complete

### Priority Matrix

```
                    User Impact
                    High              Low
              +-------------------+-------------------+
   Frequency |                   |                   |
      High   |  P0 - Critical     |  P2 - Backlog      |
              |  Fix immediately   |  Review later      |
              +-------------------+-------------------+
      Low    |  P1 - Major        |  P2 - Backlog      |
              |  Fix soon          |  Review later      |
              +-------------------+-------------------+
```

---

## Feedback Analytics Dashboard

### Real-Time Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| **Total Feedback** | All feedback received this week | - |
| **Positive Feedback** | Ratings 7-10 | ≥60% |
| **Negative Feedback** | Ratings 0-6 | ≤20% |
| **Bugs Reported** | Bug category feedback | ≤5% |
| **Feature Requests** | Feature request category | 10-20% |
| **NPS Score** | Average net promoter score | ≥7 |
| **Response Rate** | % of feedback with response | 100% |

### Trends to Monitor

- **Sentiment trend:** Is feedback getting more positive over time?
- **Bug frequency:** Are new bugs being introduced?
- **Feature requests:** Which features are most requested?
- **User engagement:** Are users giving feedback?

### Alert Thresholds

| Alert | Trigger | Action |
|-------|---------|--------|
| **Negative feedback spike** | Negative feedback >30% for 2 days | CSM investigates |
| **Critical bug surge** | Critical bugs >5 in 24h | CTO immediately |
| **NPS drop** | NPS drops by ≥2 points week-over-week | CEO review |
| **Unresponded feedback** | Feedback >SLA unresponded | COO escalates |

---

## Feedback-Driven Product Iteration

### Loop: Feedback → Action → Validation

1. **Collect:** User submits feedback
2. **Triage:** Categorize, prioritize, route to owner
3. **Implement:** Owner builds/fixes the feature/bug
4. **Notify:** Email user: "Your feedback led to X"
5. **Validate:** User tries new feature/fix
6. **Measure:** Is user happier? Check NPS/sentiment

### Example Flow

```
User submits: "Search is slow for large datasets"
  ↓
Triaged: Feature Request → CPO → P1
  ↓
CPO adds to backlog: "Optimize search for large datasets"
  ↓
Dev implements: Search optimization (2 weeks)
  ↓
CSM emails user: "Thanks to your feedback, search is now 2x faster"
  ↓
User tries search, gives feedback: "Much better! 😊"
  ↓
Sentiment improves: NPS +1 point
```

### Feedback Recognition

**Top Contributors:**
- Users who give ≥5 pieces of actionable feedback during beta
- Recognition: "Beta Contributor" badge, early access to features

**Implemented Features:**
- Public list: "You asked, we built"
- Each feature linked to feedback contributor
- Shows community impact

---

## Privacy & Consent

### Data Collected

| Data Type | Stored? | Purpose | Retention |
|-----------|---------|---------|-----------|
| Feedback text | ✅ | Improve product | 2 years |
| Ratings | ✅ | Analytics | 2 years |
| User ID | ✅ | Respond to user | 2 years |
| Email | ✅ | Send updates | Until opt-out |
| Screenshots | ✅ | Debug issues | 90 days |
| Console message content | ❌ | Privacy | N/A |
| Memory content | ❌ | Privacy | N/A |

### Consent

- **In-app feedback:** Implicit consent (user initiates)
- **Email feedback:** Explicit consent (user sends email)
- **Passive signals:** Implicit consent (Terms of Service)
- **Opt-out:** Users can opt out of all feedback collection

### Data Usage

- Feedback is used ONLY to improve the product
- Never shared with third parties
- Anonymized for public sharing
- GDPR-compliant (right to deletion)

---

## Implementation Roadmap

### Phase 1 (Pre-Launch)
- [ ] One-click rating component built (frontend)
- [ ] NPS survey component built (frontend)
- [ ] Feedback form component built (frontend)
- [ ] Backend API for feedback ingestion
- [ ] Triage automation (category routing)
- [ ] SLA tracking system

### Phase 2 (Launch Week)
- [ ] Feedback collection active
- [ ] Real-time analytics dashboard
- [ ] Alert monitoring (CSM)
- [ ] Triage process running

### Phase 3 (Post-Launch)
- [ ] Refine feedback forms based on usage
- [ ] Add more granular categories
- [ ] Implement feedback recognition system
- [ ] Publish "You asked, we built" list

---

## Dependencies

- Onboarding checklist: `onboarding-checklist.md`
- Health metrics: `health-metrics.md`
- Welcome email template: `welcome-email.md`
- TASK_DB: Feedback integration for user health scoring

---

**Owner:** csm
**Status:** Ready for implementation
**Priority:** P1 (Beta launch: March 24)
