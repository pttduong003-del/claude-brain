---
name: narrator-voice-masane
description: "JP narrator = ElevenLabs v3 \"Akio shima\" (not the masane clone, which can't do emotion on AI33)"
metadata:
  node_type: memory
  type: user
  originSessionId: f30f3d65-6684-4dbd-b476-620add5ff24f
  modified: 2026-11-12T16:03:18.581Z
---

Main JP narrator for `/ai33-voice` is `Akio shima - Rich, Deep Japanese Actor`, voice_id `elevenlabs_BSPow8LcoXJ0UVg1ws3x`, run on `eleven_v3` with v3 audio tags ([sighs], [whispers], [curious]…). Use it without asking.

The user's cloned voice `masane` (`clone_2583346`) was the first pick, but on AI33 clones run MiniMax speech-02/2.6 and ignore tags, `emotion` and `pitch` (tested 2026-11-12, flat delivery). Use masane only if the user asks for it and warn it will read flat.

**Why:** user wanted audible emphasis/emotion; approved the v3 Akio test on 2026-11-12 and said "switch the skill".
**How to apply:** default `--voice elevenlabs_BSPow8LcoXJ0UVg1ws3x` for JP scripts; tag rules live in the ai33-voice SKILL.md. Related: [[detective-protagonist]].
