# Workers for PR review

Use one lead by default. There is no evidence that every PR needs workers. Extra reviewers consume context, time and coordination effort; they can share the same wrong assumption. Select a mode from the change's risks, not a fixed file or line count.

| Need | Suitable mode | Main risk to check |
|---|---|---|
| One reviewer can inspect the complete change and consumers | Lead uses discovery, challenge and coverage passes | Stopping after the salient faults |
| Distinct behavior or risk areas need more inspection | Focused workers in parallel, each owns a coherent path | A producer/consumer fault falls between assignments |
| High-impact, tightly coupled change needs a fresh view | One independent full reviewer before seeing lead findings | Shared blind spots and duplicate claims |
| Consequential or disputed candidate needs a specific check | One verifier asks how the candidate can be disproved | Anchoring on the first explanation |

Start with one extra worker. Add more only for a named unserved area and enough budget for lead integration. A small change with one critical risk can justify a verifier; a large mechanical change can need no worker. If tools/budget do not support workers, run the relevant passes sequentially and state material coverage limits.

## Assign the work

Give all workers the same exact repo/base-ref/base/head/merge-base identity, PR intent, applicable instructions, available evidence, read-only scope, responsibilities and bounded budget. Responsibility for an area does not restrict reading related code. Do not partition solely by file count. Identify shared interfaces before sending work. The lead owns the cross-area path and final batch.

For independent discovery, use a fresh context and do not provide the lead's findings, suspected bug or expected answer. Provide raw requirements and code. Sharing the whole conversation can remove this separation. A new conversation context can include host instruction files. Do not claim that those files were excluded without evidence. If the independent pass cannot run, record it as not run. A lead pass in the same context does not replace it. For verification, provide the actual claim and supporting evidence, then request concrete counterevidence rather than agreement.

Write the report in ASD-STE100 Simplified Technical English. Use [ste-writing.md](ste-writing.md) for the language passes. Keep code identifiers, paths and commands exact. A worker returns these fields:

1. **Scope:** inspected areas/dependencies, commit IDs, blocked/uninspected areas.
2. **Candidates:** distinct causes with location, trigger, consequence, evidence and essential assumptions.
3. **Counterevidence:** guards, tests, contracts or exceptions checked; refuted/unresolved claims.
4. **Boundary risks:** interfaces, related instances and effects that need lead or another area's check.
5. **Verification:** exact commands and observed results; unfinished work and available cost/time facts.

Workers must not post comments, approve, resolve threads, or edit the PR. Do not require recursive delegation or debate until agreement.

Use [review-record.md](review-record.md) for code references, check records and evidence artifacts. Keep the target revision on each result. Give workers different ID prefixes when their records will be put together. The lead maps duplicate causes to one final finding ID. An independent discovery worker must not receive the lead's candidate records before its discovery pass.

## Integrate evidence

Wait for the assigned scope to return or mark it incomplete. A failed worker is not a clean result. Inspect the decisive code yourself. Take the union of supported findings, remove duplicate root causes, and validate locations at the same head. Do not count votes or confidence scores as evidence. Retain a supported minority finding when no concrete refutation exists.

Put worker evidence in the lead's review record. Keep check IDs and artifact paths correct. Run the record validator on the integrated batch. A satisfactory record result does not replace examination of the worker's source evidence or test harness.

For each interface, compare both sides: emitted/accepted values, data shape, defaults, versions, order and failure handling. For example, a producer's new enum and a consumer's old switch can each look valid in isolation. Check adapters before reporting a mismatch.

Bound a challenge by an answerable uncertainty: one code trace, contract lookup or focused experiment. Stop when the claim is established, refuted, or blocked by named missing evidence. Repeated discussion without new evidence does not improve trust.

Return one integrated batch. Do not forward raw worker reports as separate user reviews. If either repo identity, base ref, base SHA or head SHA changes, recompute the merge-base and scope. Invalidate and recheck affected worker and lead evidence. An unchanged head alone does not establish an unchanged review target.

Process reference: [EGM context limits](https://github.com/google/elephant-goldfish-model/blob/72d06f52a2482885d9a64bd24b291c6e8628942c/docs/harnesses.md). Apply the context distinction to PR review. Worker use stays optional.
