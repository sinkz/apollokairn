# ApolloKairn Commands

Use `--vault NAME` after selecting a registered vault. Use `--path PATH_TO_VAULT`
only when the vault is not registered.

```bash
apollokairn vault current --json
apollokairn vault list --json
apollokairn vault doctor --json

apollokairn search "deploy 403 token" --vault work --json --limit 5
apollokairn retrieve "deploy 403 token" --vault work --mode passages --ranker auto --budget 800 --json
apollokairn similar "deploy fails after token rotation" --vault work --json

apollokairn update knowledge/deploy-403.md --append-file note.md --vault work
cat note.md | apollokairn update knowledge/deploy-403.md --append-stdin --vault work
apollokairn capture --title "Deploy 403 after token rotation" --description "Fix for CI deploy failures." --type Runbook --tag deploy --body-file note.md --vault work
cat note.md | apollokairn capture --title "Deploy 403 after token rotation" --description "Fix for CI deploy failures." --type Runbook --tag deploy --body-stdin --vault work
apollokairn validate --vault work
apollokairn index --vault work

apollokairn usage status --vault work --json
apollokairn usage evidence --vault work --json
```
