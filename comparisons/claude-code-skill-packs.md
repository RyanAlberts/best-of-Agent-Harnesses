# Claude Code skill packs: superpowers vs GStack vs Anthropic Skills vs addyosmani/agent-skills

Skill packs are the cheapest tier on this whole list: folders of markdown the harness loads when relevant, with no runtime, no new agent loop, and switching costs near zero. That is why [How to pick a harness](how-to-pick-a-harness.md) tells you to start at this tier. The four big packs are not four versions of one thing; each is a different bet on what belongs in the folders.

| | [superpowers](https://github.com/obra/superpowers) | [GStack](https://github.com/garrytan/gstack) | [Anthropic Skills](https://github.com/anthropics/skills) | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
|---|---|---|---|---|
| ⭐ Stars | 270k | 127k | 167k | 84.9k |
| The bet | **Process**: TDD, systematic debugging, planning, and verification, applied before any work starts | **Roles**: 23 slash-command modes (CEO review, eng review, design, QA, ship) that structure one assistant as a virtual team | **The format**: the official SKILL.md reference, plus production document skills (docx, pdf, pptx, xlsx) | **Portability**: 24 senior-dev workflow skills and 4 personas that travel across agents |
| Runs on | Claude Code, Codex, OpenCode, Cursor | Claude Code | Claude Code, Claude.ai, the API | 70+ coding agents |
| Enforcement | A SessionStart hook re-injects the rules at startup and after compaction; skill use itself is instruction-level, not a technical gate | Checkpoint mode auto-commits after each step; /freeze and /careful guardrails; the browser skill runs behind a deny-default CDP allowlist | None: pure content, the host platform decides | None: skills bundle, the host decides |
| Memory | Basic: session-continuity hook; cross-session recall is a separate companion plugin | Strong: per-repo /learn learnings plus an optional GBrain backend | None | None of its own |
| License | MIT | MIT | ⚠️ Per-skill Anthropic terms ("all rights reserved", governed by your Anthropic agreement) | MIT |
| Adoption surface (list tier) | complex (product suite) | slightly complex | mostly simple | mostly simple |

_Stars as captured for the main list (see [README](../README.md#guide-to-rankings) for the capture date). Enforcement and memory rows come from this list's [deep-dive research](../attributes/RUBRIC.md) (July 2026)._

## Pick by situation

- **You want the agent to work like a disciplined engineer** → **superpowers**. The most-starred pack of the four. Its skills are process (test-driven development, systematic debugging, verification before claiming done), and its one hook re-injects that discipline after every compaction, which is exactly the moment packs usually lose their grip.
- **You want a product team, not just an engineer** → **GStack**. Garry Tan's daily-driver stack turns one assistant into reviewers, QA, and a ship pipeline, and it has the strongest memory story of the four: per-repo learnings that feed later sessions, plus an optional GBrain backend for indexed cross-session search.
- **You're authoring skills, or you need documents produced** → **Anthropic Skills**. The reference implementations of the format every other pack builds on, plus the docx/pdf/pptx/xlsx workhorses. Read the licensing before you redistribute: the official skills are not standard open source; each ships its own Anthropic-terms LICENSE.txt.
- **You run more than one agent** → **addyosmani/agent-skills**. Cross-agent portability is the design goal, so the same senior-dev workflows follow you from Claude Code to Cursor to Copilot instead of being rebuilt per harness.

## They compose, up to a point

Skills are folders, so nothing stops you from installing two packs. The failure mode is trigger overlap: two packs claiming the same situation ("before any bug fix, use MY debugging skill") leave the model arbitrating between constitutions. Start with the pack whose bet matches your gap, add single skills from the others, and prune anything that never fires. None of the four owns an agent loop, so autonomy, recovery, and sandboxing are whatever your harness provides; the list rates all four n/a on those axes. When you outgrow the big four, larger catalogs exist: [ECC](https://github.com/affaan-m/ECC) is the breakout mega-pack (28 subagents, 119 skills, 60 slash commands), and [wshobson/agents](https://github.com/wshobson/agents) is the cross-harness marketplace of drop-in agent definitions.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
