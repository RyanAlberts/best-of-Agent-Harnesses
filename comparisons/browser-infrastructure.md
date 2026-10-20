# Browser infrastructure for agents: Browser Use vs Browserbase vs Steel vs Hyperbrowser

Agent libraries like browser-use and Stagehand decide what to click; something still has to run the browsers they click in. At small scale that's Chrome on your own machine. At production scale it becomes its own operations problem: hundreds of concurrent sessions, sites that block automation, CAPTCHAs, logins that must persist between runs, and recordings you'll need when a run goes wrong. Browser infrastructure vendors sell exactly that: hosted browsers with the ugly parts handled. These four are the names buyers actually weigh ([our browser-agents guide](browser-agents.md) covers the other two lanes: agent libraries and MCP tool servers).

| | [Browser Use Cloud](https://browser-use.com/cloud-browsers) | [Browserbase](https://www.browserbase.com/) | [Steel](https://steel.dev/) | [Hyperbrowser](https://hyperbrowser.ai/) |
|---|---|---|---|---|
| What it sells | Managed stealth Chromium driven over CDP, plus a hosted agent API on the same browsers | Managed cloud browsers with automation, search, and extraction APIs | An open-source browser API you run hosted or self-hosted | Cloud browsers with agent-focused scraping and extraction APIs |
| Open source? | No: closed infra; its open source is the [browser-use agent library](https://github.com/browser-use/browser-use) (118k stars, MIT) and [Browser Harness](https://github.com/browser-use/browser-harness) | No: closed infra; its open source is the [Stagehand SDK](https://github.com/browserbase/stagehand) and an [MCP server](https://github.com/browserbase/mcp-server-browserbase) | Yes: [steel-dev/steel-browser](https://github.com/steel-dev/steel-browser) (7.5k stars, Apache-2.0) is the actual product core, Docker-deployable | No: closed infra; peripheral MIT tooling only |
| Steward | Browser Use (Y Combinator) | Browserbase ($40M Series B, [company blog](https://www.browserbase.com/blog/series-b-and-beyond)) | Nen Labs | Hyperbrowser (Y Combinator) |
| Anti-bot and CAPTCHAs | Maintained stealth Chromium builds, CAPTCHA solving included, residential proxies in 195+ countries, per its [docs](https://docs.browser-use.com/cloud/browser/stealth) | Via partnerships (Cloudflare, Fingerprint), per its [docs](https://docs.browserbase.com/introduction/what-is-browserbase) | Stealth mode, residential proxies, CAPTCHA solving, per its [docs](https://docs.steel.dev) | "Ultra Stealth Mode"; CAPTCHA solving priced into agent steps, per its [docs](https://hyperbrowser.ai/docs/introduction) |
| Session recording | Yes, MP4 recordings plus live view with human takeover ([docs](https://docs.browser-use.com/cloud/browser/live-preview)) | Yes, every agent step plus live view | Yes, session replays | Yes, video recordings |
| Logged-in state between runs | Persistent profiles, plus local-to-cloud cookie sync | Context-style persistence | Persistent profiles | Profiles via API |
| Pricing shape (checked 2026-08-12; Browser Use 2026-10-20) | Pure usage, no subscription: [$0.02 per browser-hour](https://browser-use.com/pricing), residential proxy $5/GB, $1 free credit to start | Base fee plus usage: free tier, then [$20 and $99/month tiers](https://www.browserbase.com/pricing) with browser-hour overage around $0.10 to $0.12/hr | Usage-based with plan fees: [$0/month plus $30 one-time credit](https://steel.dev/pricing) to start, $250/month at scale | Pure credits (1,000 = $1): [$0.10 per browser-hour, $0.02 per agent step](https://hyperbrowser.ai/docs/reference/pricing) |
| Works with | Any CDP client: Playwright, Puppeteer, Selenium, Stagehand; the browser-use agent natively; MCP server for Claude Code, Cursor and others | Stagehand natively; LangChain, CrewAI, Mastra | Framework-agnostic: any Playwright or Puppeteer stack | Claude, OpenAI, Gemini, and browser-use agents built in |

_Only Steel has an open-source core, so this page carries no star-ranked table; Steel's list entry lives in [Libraries and SDKs](../README.md#libraries-and-sdks). Pricing shapes summarize each vendor's own pricing page on the date shown; check them before committing._

## Pick by situation

Three independent comparison write-ups ([APIScout](https://apiscout.dev/guides/browserbase-vs-steel-vs-hyperbrowser-browser-infrastructure-2026), [PkgPulse](https://www.pkgpulse.com/guides/browserbase-vs-hyperbrowser-vs-steel-cloud-browsers-ai-2026), and [Steel's own head-to-head](https://steel.dev/blog/steel-vs-browserbase-a-practical-comparison), bias noted) land on the same split, which is rare enough to trust. Browser Use Cloud is not covered by those write-ups:

- **Cost per browser-hour or getting past bot checks decides it** → **Browser Use Cloud**. $0.02 per browser-hour with no subscription, the lowest listed price of the four, with stealth, CAPTCHA solving and profiles included and proxies metered separately. Its own [Stealth Bench V2](https://browser-use.com/benchmarks/browsers) puts it first on 100 bot-protected sites (vendor benchmark, bias noted: the sites were picked where it historically got through). The trade: closed infra and hosted only, no self-hosting.
- **You want the safest managed default with the most polish** → **Browserbase**. The most mature tooling story (Stagehand is its SDK), session visibility on every agent step, and the most generous named free tier of the three. The trade: fully closed, and features track plan level.
- **Openness or self-hosting is a buying criterion** → **Steel**. The only one whose core you can read, run in your own Docker, and walk away from without losing the integration; the hosted product is the same code with the ops handled. This is also the pick when procurement rules out closed infra handling logged-in sessions.
- **You're scraping or crawling at volume, agent-first** → **Hyperbrowser**. Credit pricing that meters agent steps rather than plans, stealth as the headline feature, and built-in support for driving it from browser-use and the major model providers.

Also in the lane, one tier out: [Browserless](https://www.browserless.io/comparison), the long-running self-hosted headless-Chrome standard, and Anchor Browser, a newer managed entrant focused on agent identity. Neither shows up in buyer comparisons as often as these three yet.

## The question to ask first

*Does your agent hold credentials?* A hosted browser that logs into your users' accounts concentrates real risk with the vendor: recordings, cookies, and persistent profiles all live on someone else's infrastructure. If the answer is yes and that sentence made you uncomfortable, Steel's self-hosted mode is the escape hatch the other two don't offer. If the answer is no (public-web scraping, testing, research), pick on developer experience and unit economics, which is the fight Browserbase and Hyperbrowser are actually having.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
