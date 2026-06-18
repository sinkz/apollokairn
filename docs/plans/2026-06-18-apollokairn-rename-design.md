# ApolloKairn Rename Design

## Status

Accepted for implementation planning.

## Date

2026-06-18

## Context

The project is currently named Cairn and ships a `cairn` CLI. That name is
crowded in adjacent knowledge, memory, MCP, and agent tooling spaces. It is also
already taken on PyPI by an unrelated package.

The project is still early enough that a public rename is cheaper than carrying
long-term ambiguity. The rename should improve public discoverability without
creating unnecessary churn in the implementation.

Checks performed on 2026-06-18:

- `cairn` exists on PyPI as an unrelated package:
  <https://pypi.org/project/cairn/>.
- `apollokairn` and `apollokairn-cli` returned 404 through the PyPI JSON API.
- GitHub repository search for `apollokairn` returned no repository matches.
- `sinkz/apollokairn` returned 404 through the GitHub API.
- The `.dev` RDAP server listed by IANA is
  `https://pubapi.registry.google/rdap/`.
- `apollokairn.dev` returned 404 through that RDAP endpoint. This suggests the
  domain is unregistered, but final availability must still be confirmed at a
  registrar before public launch.

## Decision

Rename the public project to ApolloKairn using an incremental compatibility
approach.

Public identity:

- Product name: `ApolloKairn`
- Repository target: `sinkz/apollokairn`
- GitHub Pages target: `https://sinkz.github.io/apollokairn/`
- Optional domain target: `https://apollokairn.dev`
- PyPI distribution target: `apollokairn-cli`
- Official CLI command: `apollokairn`
- Optional short alias: `ak`

Compatibility:

- Keep `cairn` as a CLI alias for at least one public release.
- Show a deprecation notice for direct `cairn` CLI use after the rename lands.
- Keep the internal Python module as `cairn` for now.
- Keep `.cairn/` as the vault metadata directory for now.
- Keep `CAIRN_*` environment variables initially.
- Add new `APOLLOKAIRN_*` environment variables later only where they improve
  user-facing install or release flows, with `CAIRN_*` fallbacks.

## Non-Goals

This rename does not include:

- renaming `src/cairn` to `src/apollokairn`;
- changing the vault metadata directory from `.cairn`;
- breaking existing vaults;
- removing the `cairn` command immediately;
- adding agent packs, MCP servers, or TUI work.

Those can be separate changes after the public rename is stable.

## Architecture

The rename has three layers.

```text
Public surface
├── README and guides
├── GitHub Pages
├── install scripts
├── release assets
├── PyPI package metadata
└── CLI entry points

Compatibility layer
├── cairn command alias
├── existing python -m cairn usage
├── .cairn vault metadata
└── CAIRN_* environment variables

Internal implementation
└── src/cairn remains the package name for now
```

The public surface should say ApolloKairn. Compatibility surfaces may mention
Cairn only as the former command or implementation name.

## CLI Behavior

After the rename:

```bash
apollokairn --version
apollokairn init --path PATH_TO_VAULT
apollokairn search "deploy 403" --path PATH_TO_VAULT
```

Optional short alias:

```bash
ak search "deploy 403" --path PATH_TO_VAULT
```

Compatibility alias:

```bash
cairn search "deploy 403" --path PATH_TO_VAULT
```

The compatibility alias should keep working, but it should not be the primary
command in new docs.

## Release And Install

Future release assets should use the public name:

```text
apollokairn-linux-x64.tar.gz
apollokairn-linux-arm64.tar.gz
apollokairn-macos-x64.tar.gz
apollokairn-macos-arm64.tar.gz
apollokairn-windows-x64.zip
```

Install scripts should default to `sinkz/apollokairn` after the GitHub
repository is renamed. During transition, tests should make the expected repo
explicit so the scripts do not silently drift.

The installed binary should be named `apollokairn`. If the release pipeline can
install aliases safely, it may also install `ak` and `cairn`; otherwise alias
coverage can remain in Python entry points and documentation.

## Documentation

Public docs should use ApolloKairn and the `apollokairn` command by default.
They may include a short migration note:

```text
ApolloKairn was previously named Cairn. The `cairn` command remains available as
a compatibility alias for one release.
```

Docs that should be updated:

- `README.md`
- `README.pt-BR.md`
- `AGENTS.md`
- `ROADMAP.md`
- `CHANGELOG.md`
- `docs/index.html`
- `docs/learn.html`
- `docs/benchmarks.html`
- `docs/guides/*.md`
- `docs/install.sh`
- `docs/install.ps1`

Private historical docs under ignored planning and report paths can remain
unchanged unless they are referenced from public docs.

## Testing

The rename must be test-driven. Before implementation, add or update tests that
fail for the current behavior.

Required test coverage:

- console scripts include `apollokairn`, `ak`, and compatibility `cairn`;
- `python -m cairn --version` still works;
- help/version text uses ApolloKairn for the public name;
- install scripts reference `apollokairn-*` release assets;
- release workflow builds `apollokairn-*` archives;
- README install commands use the new GitHub Pages path after repo rename;
- generated agent guides use the new command where appropriate;
- deterministic retrieval benchmark remains unchanged;
- deterministic writeback benchmark remains unchanged.

Before claiming completion, run:

```bash
python -m unittest discover -v
python bench/run_eval.py --quiet --compare-golden bench/golden.json
python bench/run_writeback_eval.py --quiet --compare-golden bench/writeback/golden.json
python -m json.tool docs/data/benchmarks.json
git diff --check
```

For docs and installer changes on Windows:

```powershell
& 'C:\Program Files\Git\usr\bin\bash.exe' -n docs/install.sh
$errors = $null
[System.Management.Automation.PSParser]::Tokenize((Get-Content -Raw docs\install.ps1), [ref]$errors) > $null
if ($errors) { $errors | ForEach-Object { $_.Message }; exit 1 }
```

## Rollout

1. Commit this design.
2. Create an implementation plan.
3. Implement the rename with tests.
4. Push the code change.
5. Rename the GitHub repository from `sinkz/cairn` to `sinkz/apollokairn`.
6. Verify GitHub Pages at the new path.
7. Reserve the PyPI package and domain before broader public sharing.

## Rationale

This approach solves the public naming collision while preserving the working
implementation. A full internal package rename would touch nearly every import
and test without improving the CLI experience. Keeping the internal module
stable lets the rename focus on what users actually see: the project name,
install path, release assets, and executable commands.
