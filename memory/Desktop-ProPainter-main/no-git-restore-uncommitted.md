---
name: no-git-restore-uncommitted
description: Never git checkout/restore/reset a file with uncommitted changes in ProPainter-main; never delete baselines
metadata:
  node_type: memory
  type: feedback
  originSessionId: 177ce018-1d50-4eee-bb43-1f98a8e9f2cd
  modified: 2026-10-10T11:01:09.370Z
---

Never run `git checkout -- <file>`, `git restore`, or `git reset` on a file that has uncommitted
changes. For experiments (negative tests, isolating a cause), `git stash` or copy the file to temp
first and restore from that copy. Never delete baselines (temp/phase3/precommit, docs/baselines).

**Why:** on 2026-10-10 a negative-test command ran `git checkout --` on
src/lib/narration/SegmentSubtitleTrack.ts and wiped uncommitted work (recovered from a temp copy);
the user made this a rule in AGENTS.md / CLAUDE.md.

**How to apply:** negative tests use temp/phase4/neg.sh (cp backup -> sed -> run -> cp back -> cmp).
Related: [[qa-runner-baselines]]
