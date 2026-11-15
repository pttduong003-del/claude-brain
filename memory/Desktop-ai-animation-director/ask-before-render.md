---
name: ask-before-render
description: "do not start a full Remotion preview/video render without the user's go-ahead"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 75d7f4ee-7424-4711-833d-98779d945ac4
  modified: 2026-11-07T05:54:51.266Z
---

Do not launch `make_video.py render` (full preview or final) on my own initiative; finish edits, show what changed, and ask first.

**Why:** User stopped a render mid-run on 2026-11-07 ("chưa cho phép render vội") — they wanted research and design accuracy before spending render time.

**How to apply:** After code changes, report and ask "render?" via wrap_up. Quick single-frame `remotion still` checks were not objected to, but prefer asking when the user is steering design. Related: [[detective-protagonist]].
