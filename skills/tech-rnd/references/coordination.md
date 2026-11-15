# Coordinating an R&D campaign

## One owner, focused workers

The lead owns the brief, shared contracts, evidence ledger, experiment queue, and integrated decision. Delegate independent work to subagents when tools and budget permit. Prefer subagents inside the current task; create separate user-visible chats only if the user explicitly requests new chats. A skill does not grant capabilities or override host limits.

Use a small number of concurrent workers, often two or three, capped by actual capacity. Assign work by uncertainty or competing approach, not one agent per keyword. The lead can implement or analyze while investigators work. Reuse workers for follow-ups; add a fresh reviewer when an unanchored challenge is valuable. Avoid recursive delegation by default.

Parallelize research, source inspection, and isolated implementation. Serialize benchmarks competing for the same CPU/GPU/storage resource, unless contention is intentionally the experiment. Separate directories prevent edit conflicts but do not prevent measurement interference.

## Delegation brief

Provide only the necessary context in a self-contained brief:

```text
Question or hypothesis:
Target environment and representative workloads:
Hard constraints, objective priorities, and relevant shared contracts:
Existing baseline and raw artifact paths, if relevant:
Approach to investigate, or request for an independent proposal:
Owned writable path; files/interfaces that must not change:
Bounded deliverable and budget:
Required evidence and reproduction instructions:
Relevant literature questions/search coverage; source IDs and reading depth:
Return: recommendation, supporting evidence, uncertainty, counterexample,
        dependency effects, artifact paths, and next discriminating experiment;
        other approaches investigated/tested, their strengths, evidence level,
        disposition, reason not selected, and conditions for reconsideration.
```

For independent discovery, use a fresh agent context when supported and supply the self-contained brief rather than inheriting the lead's whole conversation. Omitting a preferred answer from the task message is insufficient if the inherited context already contains it. Ask first-pass investigators to record their proposals before reading peer conclusions; provide the shared requirements and raw evidence they need. Reusing an agent that already saw the recommendation is appropriate for follow-up work, but does not create a fresh independent proposal. If context separation is unavailable, describe the independence limit.

For dependent work, provide relevant prior evidence explicitly. A reviewer reproducing a proposed solution needs its artifacts; independence here means a non-author check, not ignorance of the candidate. Ask workers to separate source claims from locally measured facts. Short returns should link details instead of pasting logs into the lead's context.

## Reconciliation loop

1. Collect independent proposals and evidence into one candidate record, including alternatives each worker did not select. Preserve their evidence and reasons rather than retaining only each worker's winner.
2. Identify contradictions or incompatibilities that could change the decision.
3. Assign a targeted experiment or source check with an observable answer.
4. Integrate surviving components and measure the shared objective.
5. Send measured failures or contract changes back only to affected owners.
6. Update the recommendation and uncertainty, then stop or choose another experiment within budget.

Do not equate majority votes, repeated claims, or matching prose with verification. Cite raw observations. Preserve unresolved disagreement. A failed integrated experiment may require replacing an excellent subsystem.

## Coupled systems

Keep a dependency table with producer, consumer, contract, resource impact, and validation case. Include feedback edges when dependencies are cyclic; successive approximations can resolve them without pretending every problem is a DAG.

Track shared contract revisions when changes could invalidate evidence. Record which candidates and runs used each revision. Do not silently compare runs with different workloads, APIs, quality settings, or feature coverage.

When separate campaigns need to work together, create or resume an integration campaign that links their specific decision and artifact revisions. Preserve each campaign's history. Reconcile objectives, environments, contracts, and acceptance criteria before reusing conclusions; identify stale or incompatible evidence. Reuse verified findings where applicable, and commission only the missing cross-system experiments. An integration campaign owns the combined verdict: individually validated components do not establish a validated composition. Record which upstream changes would reopen the integrated decision.

By default, combine candidate components in the standalone comparison demo. An integration campaign here means validating their composition; it does not require changing the existing app/engine. Assign ownership of the combined demo so separate worker prototypes become one reviewable result when compatible.

Choose shared contracts for the system or journey being investigated. Examples:

| Shared concern | Example consumers | Question to validate |
|---|---|---|
| Data representation and ownership | UI, API, storage, sync | Do components agree on identity, schema, updates, and conflicts? |
| Timing, order, and lifecycle | Background jobs, clients, simulations | Are delayed, retried, interrupted, or concurrent updates handled consistently? |
| Access and user expectations | Sign-in, feature flow, backend | Does the combined behavior match permissions and what the user is told? |
| Failure and recovery | Offline clients, services, device processes | Can the complete task recover without incorrect state or lost work? |
| Resource and quality budgets | All participating components | Does the overall experience meet the agreed criteria? |

For example, offline web/mobile editing couples the interaction design, local storage, synchronization, and backend conflict behavior. Forest rendering couples geometry, motion, lighting, and visibility. Both require combined validation, but their contracts and metrics differ. Test relevant complete journeys/workloads and targeted feature toggles; do not estimate total behavior by simply combining isolated scores or timings.

## Resume and budget discipline

At meaningful checkpoints, record the recommendation, strongest counter-evidence, validated contracts, completed/failed experiment IDs, active assignments, and next action. Persist enough to resume without worker memory. Use content/version identifiers to avoid duplicate experiments or stale results.

If a round cannot finish, preserve actual status and commands. Identify whether the limit is budget, unavailable environment, an unresolved requirement, or a failed hypothesis. More compute, elapsed time, and agent agreement do not themselves improve the evidence level.
