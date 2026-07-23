# teachWeb — AGENTS.md

## Repo structure

Single-file app — all HTML, CSS, JS in `index.html` (~3450 lines).  
Open `index.html` in a browser to run; no build, dev server, or dependency step.

`src/` holds raw PNG assets plus `convert_img.py` (embeds PNGs as base64 data URIs into the HTML).

## Architecture

- Character-driven interactive tutorial with 6 stages (0–5), 30 steps (0-based).
- Stage → step mapping: `STAGE_START_STEPS` array, `stageOf(idx)` helper.
- Each step defined as `{txt, fn, ...}` in the `STEPS` array.
- Particles (`particle.js` inline) animate on a full-viewport canvas behind the content.
- Theme system: CSS custom properties driven by `chosenThemeColor` (default yellow `#ffd60a`); `ensureDefaultTheme()` applies without adding `themed` class.
- Character/text panels positioned by absolute coordinates from `layout` objects; no responsive framework.

## Key modifiers

- `.intro-finished` on `#intro-stage`: collapses intro to just the map bar (full-chain demo mode). Removing it restores full tutorial.
- `_backendDbPending` flag controls click-to-animate in the ER diagram step.
- `finish()` enters full-chain mode; clicking map nodes calls `initStateForStage()` + `go()` after removing `.intro-finished`.

## Conventions

- **No comments in code** — do not add JS or CSS comments.
- **No emojis** in any output.
- Class naming: `i-*` prefix for tutorial UI elements, descriptive names for demo elements. CSS uses single-class selectors.
- Commit messages are in Chinese, imperative mood, present tense.
- All edits go into `index.html` only; never create new files unless explicitly asked.
- Editor: any plain text editor; no formatter/linter config exists — maintain existing style.

## Image assets

- `convert_img.py src/*.png` produces base64 data URIs; paste output into `index.html` to embed images.
