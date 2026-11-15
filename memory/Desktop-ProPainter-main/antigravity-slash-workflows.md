---
name: antigravity-slash-workflows
description: "User drives the pipeline from Antigravity; its /commands are workflows in .agents/workflows/, not skills"
metadata:
  node_type: memory
  type: reference
  originSessionId: 7453e2ac-3985-464a-baec-d31186572047
  modified: 2026-10-13T05:21:53.397Z
---

The user runs the pipeline from Google Antigravity. Antigravity's `/name` slash commands come from workflow files (`.agents/workflows/<name>.md`, also `.agent/`, `_agents/`, global `~/.gemini/config/global_workflows/`). Skills in `.agents/skills/` are only auto-activated from their description, never by `/`. `/history-video-producer` = `.agents/workflows/history-video-producer.md` (created 2026-10-13), which routes to the modes of `.agents/skills/history-video-producer/SKILL.md` in the fixed order prepare-inbox -> briefs -> import-assets -> review -> assets -> render.
