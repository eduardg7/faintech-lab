# Beta User Onboarding Surveys

## Overview
Three structured surveys to capture beta user journey data, track engagement, and gather actionable feedback. All surveys use Typeform-style question patterns with clear, actionable questions.

---

## Survey 1: Day 3 Check-in

**Timing:** 3 days after signup
**Purpose:** Early engagement check, identify blockers, gather initial product feedback
**Estimated completion time:** 3-5 minutes

### Questions

1. **How's your onboarding experience so far?**
   - ⚪ Smooth - got started quickly
   - ⚪ Some friction but manageable
   - ⚪ Difficult - encountered blockers
   - ⚪ Haven't started yet

2. **What's your primary goal with Faintech Lab?**
   - [ ] Build AI agents for personal projects
   - [ ] Research AI memory systems
   - [ ] Test before using in production
   - [ ] Evaluate for team adoption
   - [ ] Other: _______

3. **Which feature have you tried?** (Select all that apply)
   - [ ] Agent creation
   - [ ] Memory experiments
   - [ ] Workspace management
   - [ ] Documentation
   - [ ] None yet

4. **What's the main blocker you've encountered?**
   - [ ] Technical issue (please describe below)
   - [ ] Unclear documentation
   - [ ] Feature not working as expected
   - [ ] No blocker so far

   *If technical issue, describe:*
   __________________________________________________________________

5. **Would you like a 1:1 sync with the team?**
   - ⚪ Yes - schedule a call
   - ⚪ No - continue exploring
   - ⚪ Maybe - email me options

**Success metric:** 80%+ completion rate, identify top 3 blockers

---

## Survey 2: Week 1 Progress

**Timing:** 7 days after signup
**Purpose:** Capture first-week engagement, feature adoption, and early feedback
**Estimated completion time:** 5-7 minutes

### Questions

1. **How often have you used Faintech Lab this week?**
   - ⚪ Daily
   - ⚪ 3-5 times
   - ⚪ 1-2 times
   - ⚪ Logged in but haven't built anything

2. **Which features have you used in the past week?** (Select all that apply)
   - [ ] Created agents
   - [ ] Ran memory experiments
   - [ ] Explored sample projects
   - [ ] Read documentation
   - [ ] Joined Discord/community
   - [ ] Reviewed code
   - [ ] Other: _______

3. **Rate your experience with the core features:**

   | Feature | Poor | Fair | Good | Excellent | Haven't tried |
   |---------|-------|-------|-------|-----------|--------------|
   | Agent creation | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |
   | Memory experiments | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |
   | Documentation | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |
   | Performance | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

4. **What's the most valuable feature so far?**
   __________________________________________________________________

5. **What's the biggest limitation you've encountered?**
   __________________________________________________________________

6. **Have you encountered any bugs or unexpected behavior?**
   - ⚪ No bugs found
   - ⚪ Minor issue (describe below)
   - ⚪ Blocking issue (describe below)

   *Describe issue:*
   __________________________________________________________________

7. **How likely are you to continue using Faintech Lab?** (NPS)
   - ⚪ 0-2 (Not likely)
   - ⚪ 3-5 (Unlikely)
   - ⚪ 6-7 (Neutral)
   - ⚪ 8-9 (Likely)
   - ⚪ 10 (Very likely)

**Success metric:** 70%+ completion rate, NPS baseline established

---

## Survey 3: Week 2 Deep Dive

**Timing:** 14 days after signup
**Purpose:** Detailed feedback on product fit, feature requests, and retention intent
**Estimated completion time:** 7-10 minutes

### Questions

1. **What specific use cases have you explored with Faintech Lab?**
   __________________________________________________________________

2. **How has Faintech Lab helped you?** (Select all that apply)
   - [ ] Saved time on agent development
   - [ ] Improved understanding of AI memory
   - [ ] Enabled faster prototyping
   - [ ] Provided learning resources
   - [ ] Other: _______
   - [ ] No value yet / Not applicable

3. **Which features would you like to see improved?** (Rank top 3)
   1. ___________________
   2. ___________________
   3. ___________________

4. **Which features would you like to see added?** (Rank top 3)
   1. ___________________
   2. ___________________
   3. ___________________

5. **How would you rate the overall experience?**

   | Aspect | Poor | Fair | Good | Excellent |
   |--------|-------|-------|-------|-----------|
   | Onboarding flow | ⚪ | ⚪ | ⚪ | ⚪ |
   | Feature discoverability | ⚪ | ⚪ | ⚪ | ⚪ |
   | Performance | ⚪ | ⚪ | ⚪ | ⚪ |
   | Documentation quality | ⚪ | ⚪ | ⚪ | ⚪ |
   | Support responsiveness | ⚪ | ⚪ | ⚪ | ⚪ |
   | Overall satisfaction | ⚪ | ⚪ | ⚪ | ⚪ |

6. **What's the primary reason you would continue using Faintech Lab?**
   - ⚪ Unique AI memory capabilities
   - ⚪ Ease of use
   - ⚪ Performance
   - ⚪ Documentation and learning
   - ⚪ Community support
   - ⚪ Other: _______

7. **What's the primary reason you would NOT continue?** (If applicable)
   - ⚪ Features don't meet my needs
   - ⚪ Performance issues
   - ⚪ Learning curve too steep
   - ⚪ Found better alternative
   - ⚪ Not using enough to justify
   - ⚪ Other: _______

8. **Would you recommend Faintech Lab to others?**
   - ⚪ Definitely would
   - ⚪ Probably would
   - ⚪ Might or might not
   - ⚪ Probably would not
   - ⚪ Definitely would not

9. **Open feedback - anything else you'd like to share?**
   __________________________________________________________________

**Success metric:** 60%+ completion rate, actionable feature prioritization data

---

## Technical Implementation

### Survey Platform
- **Primary:** Typeform (free tier)
- **Backup:** Google Forms
- **Selection rationale:** Typeform provides better UX, conditional logic, and professional appearance

### Automation Triggers

| Survey | Trigger | Delivery Method |
|---------|----------|-----------------|
| Day 3 Check-in | 72h after signup | Email (SendGrid) |
| Week 1 Progress | 7 days after signup | Email + In-app notification |
| Week 2 Deep Dive | 14 days after signup | Email + In-app notification |

### Data Collection

All survey responses will be stored in:
- **Primary:** Typeform export to CSV
- **Backup:** Faintech Lab database (beta_feedback table)
- **Access:** CSM, CPO, Analytics team

### Response Tracking

Metrics to track:
- Completion rate per survey
- Average time to complete
- NPS score trend
- Top 3 blockers
- Top 3 feature requests
- Retention intent correlation

---

## Coordination Notes

### Dependencies
- **SendGrid integration:** Required for email triggers (contact devops)
- **In-app widget:** Required for in-app delivery (contact dev)
- **Database schema:** beta_feedback table ready (CISO verified)

### Handoff to CPO
Survey results will be shared with CPO on:
- Day 4: Initial blocker summary
- Day 8: Week 1 adoption insights
- Day 15: Week 2 deep dive + feature prioritization

### Escalation Triggers
Escalate to CPO if:
- Critical blocker identified by 3+ users
- NPS drops below 40
- Completion rate below 50% for any survey

---

**Document created:** 2026-03-22 22:22 EET
**Owner:** CSM (Customer Success Manager)
**Status:** Ready for CPO review and technical implementation
