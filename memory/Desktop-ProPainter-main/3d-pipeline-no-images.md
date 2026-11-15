---
name: 3d-pipeline-no-images
description: "/history-video-producer = 3-step low-poly 3D (Video Studio); never G-Labs, image prompts or picture approval in it"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f114419e-061f-42b5-803b-1e0c2d648464
  modified: 2026-10-18T10:15:44.649Z
---

2026-10-18: the user corrected my first take, which added G-Labs pictures (framed panels for named people/places) to the 3D flow. Their rule: the production target is stylized low-poly 3D. The default 3D pipeline must not call G-Labs, must not generate image prompts, and must not require image approval. A missing model is reported by asset id with a low-poly fallback offer, never replaced by a 2D picture. The contact sheet must show real Remotion + Three.js frames.

**Why:** they want 3D animation, not image-based video; pictures in the 3D flow were the wrong product.
**How to apply:** /history-video-producer = prepare-inbox → approval gate on the 3D storyboard → approve/render (scripts/studio/producer.ts). The make-video 2D/G-Labs path stays only for old projects (references/make-video-2d.md). Approval approves scenes, not images. See [[documentary-mode-direction]], [[antigravity-slash-workflows]].
