---
name: glabs-lite-upscale
description: G-Labs nano_banana_2_lite supports upscale 2K (user-confirmed 2026-10-11); 2K is the default image quality
metadata:
  node_type: memory
  type: project
  originSessionId: 64603525-a62d-4555-80f2-b851ffe7ed66
  modified: 2026-10-11T05:53:04.246Z
---

G-Labs `nano_banana_2_lite` does upscale to 2K (the user confirmed it on 2026-10-11). Earlier docs only showed 2K working with `nano_banana_pro`, whose daily quota ran out.

**Why:** the user wants 2K images. `config/providers.json` image.primary is now lite + `upscale: "2K"`. A project can override it with `make-video --image-model / --image-quality 1k|2k|4k` (saved in project.json `imageGen`).

**How to apply:** don't probe G-Labs again or spend quota to check lite + 2K. If `IMAGE_QUALITY_NOT_REACHED` shows up for lite at 2K, the cause is something else (a server change, a model swap), not missing lite support.
