# AMC Demo Recording Runbook

**Purpose:** Execute a clean screen recording following `AMC-DEMO-VIDEO-SCRIPT.md`
**Owner:** faintech-frontend
**Review:** faintech-qa → faintech-cto
**Script source:** `AMC-DEMO-VIDEO-SCRIPT.md` (canonical)

## Pre-Recording Checklist

- [ ] AMC beta environment is running and accessible
- [ ] Authenticated in a test workspace (API key ready)
- [ ] Recording tool ready (CleanShot X, OBS, or Loom)
- [ ] Cursor movement will be deliberate and slow
- [ ] Browser/app window sized to standard viewport (e.g., 1920x1080)
- [ ] Notifications disabled on recording device

## Recording Flow (1:45-2:00 target runtime)

### Shot 1: Opening hook (0:00-0:10)
- **Visual:** AMC landing page or dashboard hero
- **What to show:** Product branding, clean entry point
- **Narration:** "Agent Memory Cloud gives your agents one place to write, search, and inspect memory across a workspace."

### Shot 2: Workspace context (0:10-0:20)
- **Visual:** Authenticated dashboard or API key header
- **What to show:** `x-api-key` header or logged-in workspace indicator
- **Narration:** "We start inside an authenticated workspace so every memory action stays scoped to the right environment."

### Shot 3: Memory write (0:20-0:50)
- **Visual:** POST request to `/v1/memories` with valid payload
- **What to show:**
  - Request payload: `{ "content": "User prefers dark mode", "tags": ["preference"] }`
  - Response: `201 Created` with memory `id`
  - Verify the memory appears in the list
- **Narration:** "First, we write a memory entry. Each memory is stored with workspace context so the system can keep data isolated and queryable."

### Shot 4: Memory read/search (0:50-1:20)
- **Visual:** GET `/v1/memories` or `/v1/search/keyword?q=preference`
- **What to show:**
  - Search query matching the written memory
  - Returned memory object with full metadata
  - Cursor/filter options visible
- **Narration:** "Next, we retrieve that memory through read and search flows. This is the shortest proof that memory is not just stored—it's usable."

### Shot 5: Dashboard inspection (1:20-1:45)
- **Visual:** Dashboard page showing recent memories list
- **What to show:**
  - Memory we just wrote appears in the list
  - Timestamp and metadata are visible
  - Activity/summary view if available
- **Narration:** "Finally, the dashboard makes recent memory activity visible so teams can inspect what was stored and verify the system is working end to end."

### Shot 6: Closing CTA (1:45-2:00)
- **Visual:** Landing page beta CTA or closing frame
- **What to show:** Clear call to action with beta wording
- **Narration:** "That's the AMC beta core loop: write, retrieve, inspect. If you want early access, join the beta and we'll share onboarding details."

## Export Specifications

- **Format:** MP4 (H.264)
- **Resolution:** 1920x1080 minimum (4K preferred if recording tool supports)
- **Frame rate:** 30fps
- **Duration:** 1:45-2:00 (do not exceed 2:05)
- **Bitrate:** 8-15 Mbps (web-optimized)
- **File size:** < 100MB

## Captions

- **Format:** SRT
- **Style:** Pop-on captions (minimal, clean)
- **Content:** Match narration exactly, no embellishments
- **Placement:** Bottom-center, readable over video content

## Quality Checks Before Export

1. **Claims check:** All claims in video are supported by `AMC-DEMO-CLAIMS-EVIDENCE.md`
2. **No bugs shown:** Only success states, no error handling or debug screens
3. **Consistent branding:** AMC/Faintech logos appear correctly
4. **Clean audio:** No background noise, narration is clear
5. **Beta language:** Use "beta" wording, not "production" or "launch"

## Post-Recording Handoff

1. **Export file:** Save as `amc-demo-beta-cut-v1.mp4`
2. **Update TASK_DB:** Record asset path and runtime
3. **Handoff to QA:** faintech-qa reviews against script and claims evidence
4. **Technical review:** faintech-cto signs off before publish

## Alternative Routes If Recording Fails

- If a UI route is unstable during capture, cut that claim/shot instead of faking behavior
- If the beta environment has downtime, reschedule recording—do not work around with mocks
- If script sections don't match current product reality, update script to match live state first, then record

## Verification Criteria

- [ ] Video follows the exact flow in `AMC-DEMO-VIDEO-SCRIPT.md`
- [ ] All UI actions shown are from the live beta environment
- [ ] Runtime is between 1:45 and 2:00
- [ ] Claims made are within the safe list in `AMC-DEMO-CLAIMS-EVIDENCE.md`
- [ ] Captions SRT file is generated
- [ ] File size is under 100MB
- [ ] Asset path is updated in TASK_DB

---

**Created:** 2026-03-11
**Status:** Ready for recording
**Next:** Execute recording following this runbook, update TASK_DB with exported asset.
