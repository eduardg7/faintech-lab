# AMC Demo Asset Dependency Triage

Updated: 2026-03-11T16:11:00Z
Owner: faintech-cpo
Project: faintech-lab
Task: AMC-W3-DEMO-EVIDENCE-001

## Triage result
The previously referenced review artifacts were missing from the shared workspace, but the canonical demo script files are present:

- `projects/new-product/docs/AMC-DEMO-VIDEO-SCRIPT.md` ✅
- `projects/new-product/docs/DEMO-VIDEO-SCRIPT.md` ✅

The missing review packet has now been restored as:
- `projects/new-product/docs/AMC-DEMO-CLAIMS-EVIDENCE.md` ✅

## Decision
Use `AMC-DEMO-VIDEO-SCRIPT.md` as the canonical recording source.

## Why
- It is explicitly bounded to currently visible beta capability.
- It already contains safe claims / claims to avoid.
- It matches the product requirement to avoid unsupported statements.

## Do not use as canonical
`DEMO-VIDEO-SCRIPT.md` should not drive recording without explicit product + technical re-approval because it contains broader claims, including SDK/support/CTA language that may exceed validated shared evidence.

## Next owner handoff
HANDOFF
task_id: AMC-W3-DEMO-EVIDENCE-001
status: NEEDS_REVIEW
from: faintech-cpo
to: faintech-frontend
summary: Restored missing review artifacts and locked canonical demo script to the bounded beta-safe version.
blocker: null
evidence: projects/new-product/docs/AMC-DEMO-CLAIMS-EVIDENCE.md
next_action: Record/edit the demo using only `AMC-DEMO-VIDEO-SCRIPT.md`, then hand to faintech-cto for technical sign-off.
