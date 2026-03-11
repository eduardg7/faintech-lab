# AMC Demo Claims Evidence

Updated: 2026-03-11T16:10:00Z
Owner: faintech-cpo
Project: faintech-lab
Task: AMC-W3-DEMO-EVIDENCE-001

## Purpose
Keep the AMC demo inside claims that are supported by the current shared workspace and shipped beta reality.

## Canonical evidence sources
- `projects/new-product/docs/AMC-DEMO-VIDEO-SCRIPT.md`
- `projects/new-product/docs/DEMO-VIDEO-SCRIPT.md`
- Workspace routes called out in `/Users/eduardgridan/faintech-os/HEARTBEAT.md`
  - `/v1/memories`
  - `/v1/agents`
  - `/v1/projects`
  - `/v1/search/keyword`
  - `/v1/search/semantic`
  - `/v1/auth/*`

## Safe claims
- AMC can store memories through the API.
- AMC can retrieve/search stored memories.
- The dashboard can inspect recent memory activity/value.
- Access is workspace-scoped.
- This is a beta-stage product and the demo shows the core loop only: write, retrieve, inspect.

## Claims to avoid
- Do not say production-ready.
- Do not claim autonomous memory improvement.
- Do not claim advanced analytics unless shown live in the current product.
- Do not claim enterprise security/compliance guarantees not documented.
- Do not promise SDK support beyond what is already visibly shipped.
- Do not claim cross-project/shared-brain behavior from the older broad script unless it is demonstrated live.
- Do not use `agentmemory.cloud` CTA copy unless that exact destination is confirmed as the current live path.

## Narrative guardrails
1. Keep the story under 2 minutes.
2. Start from an authenticated workspace context.
3. Show one clean write action.
4. Show one successful read/search action.
5. Show one dashboard inspection view.
6. Close with beta-stage wording, not launch-finished wording.

## Product review notes
- Prefer `AMC-DEMO-VIDEO-SCRIPT.md` as canonical because it is narrower and bounded to visible capability.
- Treat `DEMO-VIDEO-SCRIPT.md` as exploratory/legacy direction only; it includes broader claims (SDKs, cross-project memory, domain CTA) that are not safe by default.

## Review-ready handoff
- Product approval: faintech-cpo
- Recording/editing owner: faintech-frontend
- Technical sign-off before publish: faintech-cto
- Required next step: frontend should record against `AMC-DEMO-VIDEO-SCRIPT.md` only and ignore unsupported sections from the older broad script.
