# Browser agents: browser-use vs Stagehand vs Playwright MCP vs chrome-devtools-mcp

"Browser agent" covers three different kinds of product, and most bad picks here come from comparing across the lanes instead of within one. **Agent libraries** own the whole job: you hand them a goal in plain language ("find the cheapest flight, fill the form") and they decide every click. browser-use, Stagehand, and Skyvern live here. **Tool servers** give browser abilities to an agent you already run, over MCP (Model Context Protocol, the standard way to plug tools into AI agents); the agent you already pay for stays in charge. Playwright MCP and chrome-devtools-mcp live here, and they split the work between them: one acts on pages, the other inspects what a page did. **Browser infrastructure** is the third lane: hosted browsers (Browserbase, Steel, Hyperbrowser) that the first two lanes can run on when they need scale or stealth.

Why it matters: browser automation fails in production for unglamorous reasons: a login wall, a bot check, a page that changed shape. Picking the wrong lane means rewriting the whole integration the first time that happens.

| | [browser-use](https://github.com/browser-use/browser-use) | [Stagehand](https://github.com/browserbase/stagehand) | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
|---|---|---|---|---|
| ⭐ Stars | 113k | 24.2k | 36.9k | 51.1k |
| Lane | Agent library | Agent library / SDK | Tool server (acts) | Tool server (inspects) |
| You write | A goal in plain language | Plain-language actions mixed with Playwright code | Nothing: your agent calls it | Nothing: your agent calls it |
| How it reads pages | Chrome DevTools Protocol, the browser's own remote-control wire (it [dropped Playwright in August 2025](https://browser-use.com/changelog/19-8-2025)) | Playwright, with plain-language act/extract/observe on top | The accessibility tree: the structured outline browsers build for screen readers, so actions are text lookups, not pixel guessing | Chrome DevTools surfaces: console, network, performance traces |
| Guardrails | A domain allowlist with a [documented bypass](https://github.com/advisories/GHSA-x39x-9qw5-ghrf) (patched, severity critical); no sandbox of its own | Inherits Playwright's controls; Browserbase hosts it for isolation | Your harness's permission prompts | Your harness's permission prompts |
| Steward | Browser Use (company) | Browserbase (company) | Microsoft (Playwright team) | Google (Chrome DevTools team) |
| License | MIT | MIT | Apache-2.0 | Apache-2.0 |

_Stars as captured for the main list; rating definitions live in the [guide to rankings](../README.md#guide-to-rankings). On this list's axes the two libraries own a bounded agent loop; the two tool servers own no loop at all, because the agent calling them stays in charge._

## Pick by situation

- **The browser task is the product** ("compare these prices", "file this form on 40 sites") → **browser-use**. The biggest community in the category and the shortest path from a sentence to browser actions. Treat it as untrusted-by-default: it ships no sandbox of its own, so run it contained (see [Agent sandboxing](sandboxed-code-execution.md)) and keep logged-in sessions away from pages you don't control.
- **You want the agent to draft the automation, then pin it down** → **Stagehand**. Its bet is mixing plain-language steps with regular Playwright code in one script, so what starts flexible can end deterministic and repeatable. The browser-use vs Stagehand choice is [the most-written-about matchup in the lane](https://scrapfly.io/blog/posts/stagehand-vs-browser-use).
- **Your coding agent needs browser hands** (end-to-end tests, scraping, form-driving from inside Claude Code, opencode, or Cursor) → **Playwright MCP**. First-party from the Playwright team; acting on the accessibility tree keeps actions structured and fast. The default answer inside a harness you already run.
- **Your agent needs to see why the page broke** (console errors, failed requests, slow traces) → **chrome-devtools-mcp**. First-party from the Chrome team; it turns the DevTools panel into tool calls. It complements Playwright MCP rather than replacing it, and running both (one to act, one to inspect) is a natural pairing.
- **The site fights automation** → [puppeteer-real-browser-mcp-server](https://github.com/withLinda/puppeteer-real-browser-mcp-server) adds real-browser and anti-detection modes (its own README says no automation is invisible), and the infrastructure lane ([Browserbase vs Steel vs Hyperbrowser](browser-infrastructure.md)) sells hosted stealth browsers at scale. For vision-first form filling, [Skyvern](https://github.com/Skyvern-AI/skyvern) is the common third name next to browser-use and Stagehand.

## Agent or tool?

If you already run a coding harness, you rarely need a second agent with its own loop, its own model bill, and its own failure modes; you need hands, which is what the MCP servers are, gated by permission prompts you already configured. Reach for an agent library when the browser work stands alone: a scheduled job, a product feature, a task no coding harness is part of. One caution applies to every lane: a browser agent reads untrusted pages by definition, and a page can carry instructions aimed at the agent, so treat page content as data, never as commands, and keep credentials out of reach. To grade whichever you pick, [WebArena](https://github.com/web-arena-x/webarena) and [WebVoyager](https://github.com/MinorJerry/WebVoyager) are public test suites that score web agents on realistic sites; see [Agent evals](agent-eval-harnesses.md).

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
