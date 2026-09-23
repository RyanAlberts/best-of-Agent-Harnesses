# AGENTS.md

<!-- Replace every <...> and delete what does not apply. Keep this file under
     150 lines: it loads into every session, so every line costs context. Put
     long procedures in docs/ and link them below instead of pasting them here. -->

## Project

<one or two sentences: what this repo is, who uses it, and the one thing an agent must not break>

## Commands

- Install: `<npm ci | uv sync | go mod download>`
- Build: `<npm run build>`
- Test, all: `<npm test>`
- Test, one file: `<npm test -- path/to/file.test.ts>`
- Lint and format: `<npm run lint && npm run format>`
- Run locally: `<npm run dev>` (serves on `<http://localhost:3000>`)

Run the one-file test while you work and the full test and lint commands before you say a task is done.

## Layout

- `<src/api/>`: <HTTP handlers; one file per resource>
- `<src/core/>`: <business logic; no I/O here>
- `<src/db/>`: <schema and migrations; migrations are append-only>
- `<tests/>`: <mirrors src/; fixtures in tests/fixtures/>

## Conventions

- <Language and version, e.g. TypeScript 5 strict mode, Python 3.12 with type hints>
- <Error handling rule, e.g. return errors, do not throw across module boundaries>
- <Naming rule, e.g. files kebab-case, types PascalCase>
- Match the style of the file you are editing over any general preference.
- Add or update a test for every behavior change.

## Boundaries

Always:
- Read a file before you edit it.
- Keep changes to what the task asks for; mention other problems you notice instead of fixing them.

Ask first:
- Adding a dependency.
- Changing a public API, a database schema, or CI configuration.
- Deleting files.

Never:
- Commit secrets, or read `.env` files and credentials.
- Push to `<main>`, force-push, or rewrite history.
- Edit generated files: `<dist/, *.lock, src/generated/>`. Change the generator instead.

## More detail, loaded only when needed

- Architecture: `<docs/architecture.md>`
- Release process: `<docs/releasing.md>`
- <Subdirectory rules live in their own AGENTS.md, e.g. `packages/web/AGENTS.md`; the closest file to the code wins.>
