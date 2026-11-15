---
name: qa-runner-baselines
description: "How full QA / validator baselines are run in ProPainter-main (gitignored temp scripts, UTF-16 outputs, never edit code while it runs)"
metadata:
  node_type: memory
  type: project
  originSessionId: 177ce018-1d50-4eee-bb43-1f98a8e9f2cd
  modified: 2026-10-10T07:34:25.898Z
---

Full regression QA is a gitignored PowerShell script: `temp/phase4/run-qa.ps1 -Out <dir>` (copied from
`temp/phase3/run-qa.ps1`): every `scripts/test-*.ts`, check-legacy-baselines, tsc, eslint, check:secrets,
the 6 project validators on narration-01, dump-subtitles. Outputs are UTF-16 (PowerShell `*>`): decode
with `iconv -f UTF-16` before diffing. Validator baseline for phase 4 = `temp/phase3/precommit/val`
(commit 48fc5c0 was byte-identical to it).

**Why:** checking out old code into the tree for a baseline was blocked by the auto-mode classifier, and
editing source while the QA script runs contaminates its results (tests read files at run time).

**How to apply:** run QA only when no edits are pending; compare against the stored baseline folder
instead of re-checking-out old commits. Related: [[narration-01-render-flow]]
