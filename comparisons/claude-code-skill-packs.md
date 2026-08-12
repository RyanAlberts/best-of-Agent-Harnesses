# Claude Code skill packs: superpowers vs GStack vs get-shit-done vs Anthropic Skills

A skill is a folder of instructions (a SKILL.md file, plus any scripts it needs) that a coding agent loads only when the task matches, instead of carrying every instruction all the time. A skill pack is a curated bundle of them: someone else's working habits for your agent, installed as files. Nothing to run, nothing to migrate off, which is why [How to pick a harness](how-to-pick-a-harness.md) says to start at this tier.

The cost is behavioral, not financial. A pack rewrites how your agent plans, tests, and commits, so the wrong pack means weeks of fighting a workflow you didn't choose, and stacking two packs that disagree is worse than running neither. One [published test of popular skills](https://www.firecrawl.dev/blog/best-claude-code-skills) found many made output worse. Install one, watch what changes, prune what never fires.

If you're deciding between a skill and the other extension points, the split is: files like CLAUDE.md hold what the agent must always know, skills hold procedures loaded on demand, subagents are separate workers with their own context, and MCP servers add external tools ([Anthropic's own explainer](https://claude.com/blog/skills-explained) covers this; so does our [context files](progressive-disclosure.md) page). The four packs below are different bets on what belongs in the skill folders.

| | [superpowers](https://github.com/obra/superpowers) | [GStack](https://github.com/garrytan/gstack) | [get-shit-done](https://github.com/open-gsd/gsd-core) | [Anthropic Skills](https://github.com/anthropics/skills) |
|---|---|---|---|---|
| ⭐ Stars | 270k | 127k | 7.9k | 167k |
| The bet | **Process**: test-driven development, systematic debugging, verification before claiming done | **Roles**: 23 slash-command modes (CEO review, eng review, design, QA, ship) that structure one assistant as a virtual team | **Plans**: goal-backward plans on disk, executed in waves over fresh context windows | **The format**: the official reference skills, plus document production (docx, pdf, pptx, xlsx) |
| Runs on | Claude Code plus 13 other harnesses (Codex, Cursor, OpenCode, Gemini CLI, more) | Claude Code | Claude Code, OpenCode, Gemini CLI | Claude Code, Claude.ai, the API |
| How it enforces itself | A startup hook re-injects its rules when a session begins and after compaction (when a long session gets compressed and standing instructions usually fall out) | Checkpoint mode auto-commits work as it goes; /freeze and /careful guardrails; its browser tool only allows pre-approved commands | The plan is a file on disk, so execution survives a dead session and picks back up | It doesn't: pure content, the host platform decides |
| Memory between sessions | Basic: an optional companion plugin adds recall | Strong: per-repo learnings plus an optional GBrain knowledge backend | The plan files are the memory | None |
| License | MIT | MIT | MIT | ⚠️ Per-skill Anthropic terms ("all rights reserved") |

_Stars as captured for the main list; rating definitions live in the [guide to rankings](../README.md#guide-to-rankings). Enforcement and memory rows come from this list's [deep-dive research](../attributes/RUBRIC.md) and each repo's own documentation._

## Pick by situation

- **You want the agent to work like a disciplined engineer** → **superpowers**. The most-starred pack of the category. Its skills are process (write the test first, debug systematically, verify before claiming done), and its startup hook re-injects that discipline exactly when packs usually lose it: after compaction.
- **You want a product team, not just an engineer** → **GStack**. Garry Tan's daily-driver stack turns one assistant into reviewers, QA, and a ship pipeline, with the strongest memory story of the four: what a project teaches the agent feeds its later sessions.
- **Your projects outlive single sessions** → **get-shit-done**. Its whole design is plans as files: work is planned backward from the goal, executed in fresh context windows wave by wave, and a crash or a cleared session resumes from the plan instead of starting over.
- **You're learning the format, or you need documents produced** → **Anthropic Skills**. The first-party reference implementations everything else builds on, plus the docx/pdf/pptx/xlsx workhorses. Read the licensing before you redistribute anything: these are not standard open source; each skill ships an all-rights-reserved Anthropic-terms license file.

## They compose, up to a point

Skills are folders, so nothing stops you from installing two packs, and a [combining guide](https://dev.to/imaginex/a-claude-code-skills-stack-how-to-combine-superpowers-gstack-and-gsd-without-the-chaos-44b3) exists for exactly the trio above. The failure mode is trigger overlap: two packs claiming the same moment ("before any bug fix, use MY debugging skill") leave the model choosing between rulebooks mid-task. Start with the pack whose bet matches your gap, add single skills from the others, and prune anything that never fires.

Beyond these four: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (84.9k stars) optimizes for portability, with 24 senior-dev workflow skills installable across 70+ agents; [ECC](https://github.com/affaan-m/ECC) is the breakout mega-pack (68 specialized subagents and 284 skills at last count); [wshobson/agents](https://github.com/wshobson/agents) is the cross-harness marketplace of drop-in agent definitions; and [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) is the most-followed catalog of the whole genre, the place to discover packs this page doesn't name.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
