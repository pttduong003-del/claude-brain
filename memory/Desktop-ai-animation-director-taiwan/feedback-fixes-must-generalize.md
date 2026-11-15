---
name: feedback-fixes-must-generalize
description: Visual/staging fixes in the animation pipeline must also land as a rule or automatic check for future videos
metadata:
  node_type: memory
  type: feedback
  originSessionId: 00c1be0d-4679-4534-a81a-a64bb9164f2c
  modified: 2026-11-04T10:53:23.864Z
---

When the user reports a visual problem in a rendered video (dull hook, character covering on-screen text), fix the current video AND make it stick for future videos: a lint/render check plus a rule in references/*.md and .agent/workflows/make-video.md. The user renders with Antigravity, which only follows what the docs and checks enforce.

**Why:** user said "sửa phải áp dụng được cho các video tiếp theo"; Antigravity-written scenes repeated the same flaw (TaiwanChibi centred at scale 1.45 over info cards in video-05).

**How to apply:** prefer an automatic gate (e.g. `make_video.py overlap`, run by `render`) over doc-only advice; then update the docs Antigravity reads.
