# Browser agents: browser-use vs Playwright MCP vs chrome-devtools-mcp

One of these is an agent and two are tools, and the two tools barely overlap. browser-use owns an agent loop: hand it a goal and it drives the browser. Playwright MCP and chrome-devtools-mcp are MCP servers: the agent you already run keeps the loop and gains browser hands. Even then the servers split the job between them: Playwright MCP acts on pages, chrome-devtools-mcp inspects what the page did.

| | [browser-use](https://github.com/browser-use/browser-use) | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
|---|---|---|---|
| ⭐ Stars | 108k | 35.9k | 48.8k |
| Shape | Agent loop: Python library over Playwright | MCP server: act (navigate, click, fill, extract) | MCP server: inspect (console, network, performance traces) |
| Who owns the loop | It does | Your harness | Your harness |
| Page interface | Natural-language goals become browser actions | Accessibility tree, not screenshots: structured and deterministic | Chrome DevTools Protocol surfaces as tool calls |
| Guardrails | `allowed_domains` allowlist with [documented bypasses](https://docs.browser-use.com/examples/templates/sensitive-data); process isolation is a hosted-cloud feature, not in the OSS core | Inherits your harness's permission model | Inherits your harness's permission model |
| Steward | Browser Use (company) | Microsoft (Playwright team) | Google (Chrome DevTools team) |
| License | MIT | Apache-2.0 | Apache-2.0 |
| Autonomy (list axis) | bounded | n/a: tool, host owns the loop | n/a: tool, host owns the loop |
| Recovery (list axis) | retry | n/a | n/a |
| Adoption surface (list tier) | slightly complex | mostly simple | mostly simple |

_Stars as captured for the main list (see [README](../README.md#guide-to-rankings) for the capture date). Guardrail details come from this list's [deep-dive research](../attributes/RUBRIC.md) (July 2026)._

## Pick by situation

- **The browser task is the product** ("compare these prices", "fill this form on 40 sites") → **browser-use**. The biggest community in the category and the shortest path from a sentence to browser actions. Two operational notes from the deep-dive research: its hooks fire per step but cannot block an individual action before it runs, and the domain allowlist has documented bypasses, so keep credentialed sessions away from untrusted pages.
- **Your coding agent needs browser hands** (end-to-end tests, scraping, driving forms from inside Claude Code, opencode, or Cursor) → **Playwright MCP**. First-party from the Playwright team, built on the accessibility tree so actions are structured lookups rather than pixel guessing. The default answer inside a harness you already run.
- **Your agent needs to see why the page broke** (console errors, failed requests, slow traces) → **chrome-devtools-mcp**. First-party from the Chrome team; it turns the DevTools panel into tool calls. It complements Playwright MCP rather than replacing it, and running both (one to act, one to inspect) is a natural pairing.
- **The site blocks automation** → [puppeteer-real-browser-mcp](https://github.com/withLinda/puppeteer-real-browser-mcp-server): real-browser mode and anti-detection for pages that refuse headless visitors.

## Agent or tool?

If you already run a coding harness, you rarely need a second agent with its own loop, its own model bill, and its own failure modes; you need hands. That points to the MCP servers, gated by the permission prompts you already configured. Reach for browser-use when the browser work stands alone: a scheduled job, a product feature, a task no coding harness is party to. And for grading whichever you pick, [WebArena](https://github.com/web-arena-x/webarena) and [WebVoyager](https://github.com/MinorJerry/WebVoyager) are the standard exams; see [Agent eval harnesses](agent-eval-harnesses.md).

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
