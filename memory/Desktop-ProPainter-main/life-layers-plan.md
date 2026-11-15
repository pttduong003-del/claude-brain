---
name: life-layers-plan
description: "Approved plan (2026-10-11) to make env pictures move like a competitor's video: auto light flicker/embers, props entering on their word, STATIC_SHOT gate"
metadata:
  node_type: memory
  type: project
  originSessionId: f7262526-405b-4ab3-8fa5-b378354285eb
  modified: 2026-10-11T07:32:29.753Z
---

On 2026-10-11 the user analysed a competitor video (2D cutout-animated WW2 history, cut every ~2.6 s, props enter on the spoken word) and approved "plan A: tách lớp + diễn theo lời". They were "khá hài lòng" with the Python prototype (`temp/life-proto/proto_v2.mp4`, script kept in the session scratchpad).

The order agreed: A1 auto-detected warm light sources in `env-` images -> flicker, halo, embers, smoke. A3 object cut-out springs into the foreground on its word, background focus-pull (blur + dim), the object on the side away from lights/presenter, its base above the subtitle band. A4 gates `STATIC_SHOT` (post-render frame diff) + `LIFE_LAYER_MISSING` (preflight). A2 mood particles from the bible location description, keyword table in `config/style.json`. Project mode only; legacy rome-han unchanged; lip-sync untouched.

**Why:** today `env-` scenes move only through the sine drift in `ParallaxEnvironment.tsx`, so they read as a slideshow. Room flames in `RoomBackdrop.tsx` are measured by hand for each room picture.

Status: A1 is done and committed (d2c6502, 2026-10-11): `scripts/pipeline/lights.ts`, `LivingLightLayer.tsx`, preflight LIGHTS_MISSING / LIGHTS_NOT_FOUND. Pixels alone could not tell flames from the warm palette (sunset fields), so a bible fire-word gate came first. A3 done and committed (4ee5f54): `PropEntrance.ts`, `PropStage.tsx`, preflight PROP_PLACEMENT, `qa/props.txt`. Cut-out only for flat-template images, else a framed card, because pixel metrics could not separate clean cut-outs. narration-01 gets only 1 prop (mentions are mostly INSERT or room scenes). A4 done and committed (b9a1564): STATIC_SHOT is post-render and blocking (1 s luma change < 0.4 for >= 2 s); LIFE_LAYER_MISSING is a preflight warning (still picture > 6 s). Baseline on narration-01: 33 % still, 18 stretches, 179 s. A2 done and committed (96afea8): moods from bible kind and words; indoors get dust in the lit areas, outdoors get cloud shadows (+ mist, rain, snow by words). Still-picture time went 399 s -> 0 s; LIFE_LAYER_MISSING now blocks. Plan A is complete. Open: a full qa:full on narration-01 is blocked on the user reviewing 8 images.

**How to apply:**
- The prototype found 5/11 narration-01 cutouts still carrying ground or background (pot cloth, codex board, aqueduct, irrigation, concrete). A3 needs a clean-cutout gate first.
- Putting objects in the "emptiest region" made them float on the back wall. Use the foreground instead.
