---
name: feedback-reports-describe-plan-not-frames
description: Agent preview reports copy direction.json intent as if on screen; trust only measured output/acting.json + frames
metadata:
  node_type: memory
  type: feedback
  originSessionId: 576d33db-2f70-4391-825d-131e311d2008
  modified: 2026-11-08T10:41:02.533Z
---

Antigravity's video-08 batch-1 report (2026-11-08) claimed "hand on mouse", "close-up", "looks at clock", "slime on shoulder" for frames showing none of it, while all checks said PASS. The user asked to fix the shots and add checks.

**Why:** the agent writes the 4b report from direction.json, not from frames; old checks only measured layout.
**How to apply:** when reviewing a batch report, verify against the frames and `output/acting.json` (acting check in make_video.py `acting_errors`, probe measures pose/lookAt/touch/reach/subject height). New acting gaps become probe checks, per [[feedback-fixes-must-generalize]] and [[feedback-agent-ignores-warnings]].

Batch gate (2026-11-08, user asked): film mode is approved batch by batch (5 beats) via make_video.py batches/approve/reject + work/batches.json. Only run `approve` on the user's own words in chat.
