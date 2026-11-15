# A concise, auditable handoff

Lead with the recommended action and the conditions under which it is supported. Keep the decision paper roughly 1–2 pages; link deeper evidence instead of deleting qualifications or shrinking a large table to fit. Do not require separate documents when a small table or paragraph is sufficient.

## Alternatives considered and tested

This section is required even when the recommendation is inconclusive. Use a compact table:

| Approach and scope | Work performed / evidence | Results and strengths | Disposition and reason | Revisit condition |
|---|---|---|---|---|

Include the strongest alternatives in the paper and link the complete candidate record when needed. Account for every substantively researched and every implemented/tested candidate there, including the current-design baseline. Do not invent extra candidates to populate the table.

Distinguish **selected**, **viable but not selected**, **ruled out under current constraints**, **inconclusive**, **deferred/not tested**, and **incorporated into a hybrid**. State the evidence level separately from the decision. "Not selected" does not mean "disproved" or "slow."

For tested alternatives, link experiments, comparable results, quality checks, and retained PoC code/run commands. For research-only alternatives, explain the cited constraint or tradeoff and explicitly say they were not tested locally. Tie rejection reasons to evidence and current requirements. Distinguish implementation failures from evidence against an approach. Explain integration failures at the combination level rather than condemning otherwise viable components.

For advanced PoCs, link directly to their standalone demos or selectable variants and provide launch instructions. Keep meaningful finalist demos available even when not selected. Show agent verification and user review status with the relevant revision; a link or screenshot alone is not a user-testable demo.

Record useful ideas retained in the final solution. Give concrete changes in hardware, workload, quality requirements, interfaces, or evidence that could reverse the decision; state when no justified revisit condition is known. Keep detailed histories and logs in linked evidence.

## Coverage and limits

Map each hard acceptance criterion to the relevant source, experiment, or study observation, result, and status: passed, failed, or unverified. Include quality and the requested combined behavior, not just speed. Separate technical feasibility, usability, and product-outcome claims where relevant. For a small task, a short list suffices. An overall evidence label must not imply that untested requirements passed.

State the environment, scenarios/populations, and operating range actually evaluated. Separate measured limits from extrapolation, supplied records from reproduced results, and genuine uncertainty from known failures. If every required criterion has not passed in its intended context, make the remaining validation explicit and do not declare the whole task target-validated. Include the strongest unresolved objection that could change the recommendation.

## Ready for implementation

Describe the smallest practical production integration sequence, using actual repository files, APIs, and extension points when inspected. Include data/asset preparation, dependencies and license obligations for reused materials, platform capabilities, and any integration assumptions the PoC did not exercise. Mark effort estimates as estimates with their assumptions.

Separate the standalone demo, reusable implementation, and integration guide in the handoff, even if they share one package. Explain where the demo matches the target and what it leaves untested. Combined behavior inside the demo does not establish that it has been integrated into or validated within the intended app/engine.

Identify prototype shortcuts that must be replaced, retained validation checks, and a fallback or migration path where relevant. Keep unresolved design decisions visible rather than hiding them behind "productionize." Link the relevant code, interactive prototype, evaluation materials, raw evidence, and reproduction instructions. If user or platform validation remains pending, include its protocol without implying it already ran. Execution of the production rollout remains outside an R&D handoff unless requested.
