# Beta Customer Onboarding Checklist

**Project:** Faintech Lab Beta
**Owner:** Customer Success Manager
**Last Updated:** 2026-03-17
**Target Audience:** Technical founders, AI system builders, autonomous agent researchers

---

## Purpose

This checklist ensures every beta user has a successful first experience with Faintech Lab. The goal is to get users from signup to their first autonomous agent workflow within 15 minutes.

---

## Phase 1: Sign-up & Account Setup (5 minutes)

### Pre-Signup
- [ ] User lands on public landing page
- [ ] User understands value proposition ("autonomous R&D for AI systems")
- [ ] User clicks "Join Beta Program" CTA

### Account Creation
- [ ] User completes OnboardingFlow
- [ ] Email verified (if applicable)
- [ ] User redirected to Dashboard
- [ ] First API key generated automatically
- [ ] Welcome message displayed: "Your first agent is ready"

### Post-Signup Automation
- [ ] Welcome email sent (within 1 minute)
- [ ] User profile created with signup metadata
- [ ] User added to "Beta Users" segment
- [ ] Initial health score calculated (see health-metrics.md)

---

## Phase 2: First Agent Creation (5 minutes)

### Guided Setup
- [ ] Dashboard shows "Create your first agent" CTA
- [ ] Modal: Agent creation form with example agent template
- [ ] Pre-filled template: "Hello World Agent" (simple task)
- [ ] User clicks "Create Agent"
- [ ] Agent status: "active"
- [ ] Console shows: "Agent is running. Try it now."

### First Test
- [ ] Console input field visible
- [ ] User sends test message (e.g., "Hello")
- [ ] Agent responds successfully
- [ ] User sees agent capability in action

---

## Phase 3: Explore Core Features (5 minutes)

### Discovery
- [ ] Dashboard sidebar shows: Agents, Memories, Projects, Search
- [ ] User clicks "Memories" tab
- [ ] Empty state: "No memories yet. Agents create them as they work."
- [ ] User clicks "Projects" tab
- [ ] Empty state: "Create a project to organize your agents."

### Onboarding Progress Badge
- [ ] Progress bar: "Onboarding Progress: 1/3 complete"
- [ ] Step 1: ✅ "Account created"
- [ ] Step 2: ⏳ "Create your first agent"
- [ ] Step 3: ⏸️ "Explore features"

---

## Phase 4: Real-World Workflow (Optional, Day 2)

### Proactive Email (24h after signup)
- [ ] Email subject: "Day 2: Build your first real agent"
- [ ] Suggestion: "Try a semantic search agent with your own data"
- [ ] Link to tutorial: Getting Started Guide

### User Action
- [ ] User creates second agent (real workflow)
- [ ] User uploads data to memory (if applicable)
- [ ] Agent executes workflow
- [ ] User sees value: "This saves me time"

---

## Phase 5: Success Metrics & Health Check (Day 3)

### Automated Check
- [ ] Health score calculated (see health-metrics.md)
- [ ] If score < 6: Trigger check-in email
- [ ] If score >= 6: Send "You're doing great!" email

### Feedback Collection
- [ ] In-app feedback prompt: "How's your beta experience so far?"
- [ ] One-click rating: 😐 😊 😄
- [ ] Optional: text feedback field

---

## Rollback Criteria

If any of these occur, flag user for manual outreach:

### Engagement Drop
- [ ] No agent creation within 24h of signup
- [ ] No console messages sent in first 2 days
- [ ] Health score drops below 5 on Day 3

### Technical Issues
- [ ] Multiple failed API key attempts (>3 in 1h)
- [ ] Agent creation errors (>2 in 1h)
- [ ] Console timeouts (>5 in 1h)

### Signals for Manual Intervention
- User submits feedback with "frustrated" or "confused" keywords
- User sends 3+ emails in 24h
- User mentions "quitting" or "giving up" in feedback

---

## Success Definition

A beta user is "successfully onboarded" when:

1. **Day 1:** Account created, first agent created, test message sent
2. **Day 2:** Second agent created or agent executed real workflow
3. **Day 3:** Health score >= 6 OR user provides positive feedback

**Target Success Rate:** 70% of beta users successfully onboarded by Day 3

---

## Communication Triggers

### Automated Emails
| Timing | Trigger | Email Template | Goal |
|--------|---------|----------------|------|
| Immediate | Account creation | Welcome Email | Activate user |
| 24h later | No second agent | "Build your first real agent" | Drive engagement |
| 48h later | Health score < 6 | "Need help?" | Prevent churn |
| 72h later | Health score >= 6 | "You're doing great!" | Reinforce success |

### Manual Outreach Triggers
- User sends negative feedback (3+ negative keywords)
- Health score drops to <=3
- User emails "support" or "help"
- No activity for 7 days

---

## Dependencies

- Welcome email template: `welcome-email.md`
- Health metrics definition: `health-metrics.md`
- Feedback collection mechanism: `feedback-collection.md`
- Getting Started Guide: TBD (content team)

---

## Next Steps

1. ✅ Onboarding checklist created
2. [ ] Beta health metrics defined
3. [ ] Feedback collection mechanism designed
4. [ ] Welcome email template drafted
5. [ ] Integrate checklist with OnboardingFlow component
6. [ ] Set up automated email triggers
7. [ ] Configure health score calculations

---

**Owner:** csm
**Status:** Ready for implementation
**Priority:** P1 (Beta launch: March 24)
