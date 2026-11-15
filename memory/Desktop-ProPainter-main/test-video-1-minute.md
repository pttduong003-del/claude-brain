---
name: test-video-1-minute
description: "Test/baseline V3 renders use ~1 minute of audio, never the full narration"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 78660f3f-3503-4f79-8a94-6ca35c5d2f3c
  modified: 2026-10-28T10:04:21.919Z
---

Test and baseline videos only need about 1 minute: trim the audio at a sentence pause near 60 s (ffmpeg `-t`) and run V3 on the excerpt with its own slug.

**Why:** Duong (28/10/2026): full-length runs (4-10 min) waste DeepSeek, G-Labs and ai33 resources.
**How to apply:** for any test render, acceptance check or phase sample, cut the audio first; ask before running a full-length video.
