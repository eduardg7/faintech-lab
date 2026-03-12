# AMC Demo Video Script

## Goal
Show the shortest believable path from "I have unstructured agent memory" to "I can store it, retrieve it, and inspect value in the dashboard" without making unsupported claims.

## Runtime
- Target: 1m45s to 2m00s
- Format: screen recording with light captions
- CTA: beta waitlist / beta request flow already present on the landing page

## Claims we can safely make
- "Store memories through the AMC API"
- "Search stored memories"
- "Inspect memory activity in the dashboard"
- "Workspace-scoped API access"

## Claims to avoid
- Do not say production-ready if launch is still beta
- Do not claim autonomous memory improvement or advanced analytics unless visible in the current product
- Do not imply enterprise security/compliance guarantees not yet documented
- Do not promise SDK support beyond what is already shipped

## Shot-by-shot flow

### 1. Opening hook — 0:00-0:10
**Visual:** AMC landing page or app dashboard hero state.
**Voice/Captions:**
"Agent Memory Cloud gives your agents one place to write, search, and inspect memory across a workspace. Here’s the core flow in under two minutes."

### 2. Login / workspace context — 0:10-0:20
**Visual:** Authenticated app state or API auth-ready context.
**Voice/Captions:**
"We start inside an authenticated workspace so every memory action stays scoped to the right environment."

### 3. Memory write — 0:20-0:50
**Visual:** API request or UI action creating a memory.
**Voice/Captions:**
"First, we write a memory entry. Each memory is stored with workspace context so the system can keep data isolated and queryable."
**On-screen emphasis:** payload, successful response, created memory id.

### 4. Memory read / search — 0:50-1:20
**Visual:** Search or list endpoint returning the created item.
**Voice/Captions:**
"Next, we retrieve that memory through read and search flows. This is the shortest proof that memory is not just stored — it’s usable."
**On-screen emphasis:** search query, matching result, returned metadata.

### 5. Dashboard value — 1:20-1:45
**Visual:** Dashboard showing memory list/activity/summary.
**Voice/Captions:**
"Finally, the dashboard makes recent memory activity visible so teams can inspect what was stored and verify the system is working end to end."

### 6. Closing CTA — 1:45-2:00
**Visual:** Landing page beta CTA or closing frame.
**Voice/Captions:**
"That’s the AMC beta core loop: write, retrieve, inspect. If you want early access, join the beta and we’ll share onboarding details."

## Recording handoff
- Recording owner: faintech-frontend
- Product script approval: faintech-cpo
- Technical review before publish: faintech-cto

## Pre-record checklist
- Use only screens/routes already working in beta
- Use one clean demo dataset
- Keep cursor movement deliberate and slow enough for captions
- Show success states, not setup/debug noise
- Export final cut under 2 minutes
