# Agent Instructions

Use this file when working on the Cairn repository. Keep changes small,
verified, and aligned with the project constraints.

## Project Principles

- Cairn is a local-first, agent-agnostic CLI for Markdown knowledge vaults.
- Markdown files are the source of truth; `.cairn/index.db` is rebuildable.
- Keep the core dependency-free at runtime. `pyproject.toml` should keep
  `dependencies = []` unless a deliberate architecture decision changes that.
- Human-readable CLI output remains the default. Machine-readable JSON should be
  added deliberately and covered by tests.
- Do not move MCP servers, watch daemons, embeddings, or product-specific
  adapters into the dependency-free core. They belong behind optional boundaries.
- Never store secrets, private keys, tokens, credentials, or passwords in
  fixtures, docs, vaults, examples, or tests.

## Current Priority

Follow `ROADMAP.md`. The current focus is:

- stable JSON output for agent workflows;
- structured retrieval packets with source provenance and budget metadata;
- safer writeback through dry-run, no-op reasons, and conflict detection;
- deterministic writeback benchmarks for update-vs-create behavior.

Do not treat ranking scores as confidence. Do not add persistent query cache
before benchmarks show SQLite FTS latency is a real bottleneck.

## Development Setup

From the repository root:

```bash
python -m pip install -e .
cairn --version
```

Without installing:

```bash
export PYTHONPATH="$PWD/src"
python -m cairn --help
```

PowerShell:

```powershell
$env:PYTHONPATH = Join-Path (Resolve-Path .).Path "src"
python -m cairn --help
```

## Verification

Run focused tests while developing, then run the full checks before claiming the
work is done:

```bash
python -m unittest discover
python bench/run_eval.py --quiet --compare-golden bench/golden.json
git diff --check
```

For docs/site or install-script changes, also run:

```bash
python -m json.tool docs/data/benchmarks.json
```

On Windows, validate installer syntax:

```powershell
& 'C:\Program Files\Git\usr\bin\bash.exe' -n docs/install.sh
$errors = $null
[System.Management.Automation.PSParser]::Tokenize((Get-Content -Raw docs\install.ps1), [ref]$errors) > $null
if ($errors) { $errors | ForEach-Object { $_.Message }; exit 1 }
```

If a local GitHub Pages server is running, spot-check:

```powershell
$base='http://127.0.0.1:8767'
foreach ($path in @('/', '/learn.html', '/install.sh', '/install.ps1', '/data/benchmarks.json')) {
  $res = Invoke-WebRequest -UseBasicParsing ($base + $path)
  "${path} $($res.StatusCode) $($res.Content.Length)"
}
```

## Benchmarks

The deterministic benchmark is the source of truth for retrieval regressions:

```bash
python bench/run_eval.py --quiet --compare-golden bench/golden.json
```

When benchmark numbers change intentionally, update:

- `bench/golden.json` only when expected result prefixes change for a good
  reason;
- `docs/data/benchmarks.json` when public metrics change;
- README badges/tables if public counts or metrics are shown there.

## Release Process

Use semantic version tags like `v0.1.0`.

Before tagging:

1. Update `src/cairn/__init__.py`.
2. Update `pyproject.toml`.
3. Update `CHANGELOG.md`.
4. Run tests and benchmark.
5. Commit and push `main`.

Then create and push the tag:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

The `Release` workflow builds standalone binaries for Linux, macOS, and
Windows, publishes `checksums.txt`, and creates the GitHub Release. After it
finishes, verify at least one asset download and `cairn --version`.

## Editing Rules

- Prefer existing code patterns and standard-library solutions.
- Keep unrelated refactors out of feature changes.
- Do not revert user changes or generated artifacts unless explicitly asked.
- Use `apply_patch` for manual edits.
- Keep docs in sync across `README.md`, `README.pt-BR.md`, `docs/guides`, and
  the GitHub Pages files when behavior changes.
- If changing public CLI behavior, add or update tests in `tests/` and document
  the command in the relevant guide.
