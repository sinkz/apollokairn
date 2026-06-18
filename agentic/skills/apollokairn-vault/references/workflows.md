# ApolloKairn Workflows

## Before answering

1. Resolve the vault with `vault current` or `vault list`.
2. Search first, then retrieve a passage-sized packet.
3. Use the retrieved context as evidence, not as unquestioned truth.
4. If nothing relevant appears, say that the vault had no matching note.

## After solving

1. Summarize the reusable lesson in one or two sentences.
2. Run `similar` with that summary.
3. Update the best matching note when the new lesson belongs there.
4. Create a note only when it is a distinct reusable process, bug, decision, or reference.
5. Validate and index after a successful write.

## Vocabulary mismatch

When a query may use different words than the vault, run `vocab suggest`. Add or
request aliases only when the evidence is clear, such as `k8s` and `kubernetes`.
