---
name: feedback-agent-ignores-warnings
description: Antigravity (the video-making agent) ignores lint warnings; new director rules must be lint errors that also block preview renders
metadata:
  node_type: memory
  type: feedback
  originSessionId: b005421b-dcd9-4ca5-b914-3e01f7ea27ad
  modified: 2026-11-08T10:05:03.538Z
---

Lint rules added as warnings do not change Antigravity's output. On 2026-11-08 the director's-craft fields (FILM_DIRECTOR.md 4b) were warnings only, and video-08 still rendered the old way: 49 scenes with the character parked at `x={1030}` beside text cards.

**Why:** the agent works until `make_video.py lint` prints PASS and the render runs; anything that does not block is skipped.

**How to apply:** make each new rule an error in `scripts/make_video.py`, and check that `render --preview` blocks on it too (its error filter only keeps shot-id, `scenes/` and `direction craft` errors). Then lint one real project to confirm it fails. See [[feedback-fixes-must-generalize]].
