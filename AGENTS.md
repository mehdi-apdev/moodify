# Repository Guidelines

## Project Structure & Module Organization
- Root folders: `frontend` (Angular app), `backend` (placeholder for future services), and `shared/api-contracts.ts` for typed API shapes shared across layers.
- Angular entry points live in `frontend/src/main.ts` and `src/app/app.routes.ts`; global styles and tokens sit in `src/styles.scss` and `src/_variables.scss`.
- Feature code stays under `frontend/src/app/features` (e.g., `playlist-view`), cross-cutting logic under `frontend/src/app/core/services`. Unit specs live beside implementations as `.spec.ts`.
- Mock data for local experiments resides in `frontend/mock-db.json`; assets served from `frontend/public`.

## Build, Test, and Development Commands
- Run commands from `frontend/` after `npm install`.
- Local app: `npm start` (Angular dev server at `http://localhost:4200` with live reload).
- Mock API: `npm run mock` (json-server on `http://localhost:3000` using `mock-db.json`).
- Production build: `npm run build` (outputs to `frontend/dist/`).
- Linting: `npm run lint` (ESLint + Angular template checks).
- Tests: `npm test` (Vitest via `ng test`).

## Coding Style & Naming Conventions
- Formatting: 2-space indentation, UTF-8, final newline, trim trailing whitespace (see `.editorconfig`). Prettier uses 100-char line width and single quotes; HTML uses the Angular parser.
- Angular selectors: components use element selectors `app-example` (kebab-case), directives use attribute selectors `appExample` (camelCase) per ESLint rules.
- Keep styles scoped to component `.scss` files; share design tokens through `_variables.scss`. Favor typed APIs and avoid unused exports; colocate related assets within feature folders.

## Testing Guidelines
- Place unit tests alongside code as `*.spec.ts` (e.g., `playlist-view.spec.ts`). Use Angular TestBed for components and spy/stub services instead of hitting the mock server during unit runs.
- Cover new logic paths (happy paths and edge cases) when touching a file. Run `npm test` before pushing; add regression cases when fixing bugs.

## Commit & Pull Request Guidelines
- Follow Conventional Commits seen in history: `type(scope): summary` (e.g., `feat(ui): setup global design system`). Common types: `feat`, `fix`, `chore`, `refactor`, `test`.
- PRs should include a brief change summary, linked issue/reference, test evidence (commands run), and screenshots/GIFs for UI changes. Keep changes scoped to a single feature area and update `shared/api-contracts.ts` when API shapes evolve.
