---
name: scene-style-approved
description: "Visual style the user confirmed for JP explainer scenes (video-17): bubbles, pointer arrows, clean frames"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 75d7f4ee-7424-4711-833d-98779d945ac4
  modified: 2026-11-07T10:55:57.326Z
---

User confirmed this direction for video-17 scenes ("đúng hướng rồi", 2026-11-07):
- Short 吹き出し speech bubbles (kit `SpeechBubble`: say/think/shout, typewriter), 1–2 per shot, 5–10 chars, no extra voice track; narration stays the main voice.
- Animated pointer arrow + glowing card outline (kit `PointerArrow`) to show which card/frame is being talked about.
- No decorative connecting lines/strings across cards: user said they clutter the frame.
- 漫符 must never cover the face (gloom lines only on the forehead).

**Why:** user wants rich but readable frames; clutter and hidden expressions were called out as defects.
**Kit location:** each project has its own `scenes/kit.tsx` copy (no shared kit). The fixed version (SpeechBubble, PointerArrow, forehead-only Manpu, wider TextCard) lives only in `du-an/video-17/scenes/kit.tsx`. A new video must start by copying that file, not video-15/16's older kit.
**How to apply:** use these for new scenes (S14+ and later videos); check stills for bubble/face overlap before asking to render. Related: [[detective-protagonist]], [[ask-before-render]].
