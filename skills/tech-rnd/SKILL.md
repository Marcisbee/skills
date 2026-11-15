---
name: tech-rnd
description: Investigate technical and product-feature decisions across web, mobile, backend, data/ML, desktop, embedded, and graphics systems. Compare approaches through independent research, standalone demos of advanced PoCs, and reproducible evaluations or benchmarks, including interacting features and subsystems. Use for feature feasibility, architecture, usability, reliability, cost, and performance R&D; not ordinary implementation or quick factual lookups.
---

# Technical R&D

Find the best-supported feasible solution under the user's constraints. Treat "best" as a bounded decision, never a claim of global optimality. Evaluate the combined outcome. Agreement among agents does not establish correctness, performance, or user value.

Use one lead agent to own requirements, interfaces, comparison criteria, and the final decision. For substantial independent investigations, explicitly delegate to subagents when available. Keep research, prototypes, measurements, and decisions in a resumable workspace. Scale the process to the uncertainty; do not create a department of agents or a paper for every small question.

## Choose the research method

This workflow is platform-independent technical and product R&D. Identify whether the uncertainty concerns feasibility, behavior/correctness, user usefulness/usability, performance, reliability, cost, or a combination. Choose evidence that can answer it; do not turn every feature question into a speed benchmark. Read [methods.md](references/methods.md) to adapt the protocol and deliverables to the domain. Honor explicitly limited research-only or PoC-only requests without claiming later stages are complete.

## Frame the decision

Inspect available project context: requirements, prior research, relevant user evidence, architecture, repositories, prototypes, and evaluation tools. Inspect build commands, runtime, devices, or infrastructure when relevant; an existing codebase is not required to begin. Write a short research brief containing:

- Intended outcome, scope, target environment/users, representative usage scenarios or workloads, and non-goals.
- Hard constraints and acceptance criteria. Define units, measurement boundaries, and aggregation for numeric criteria; use explicit observation criteria for qualitative evaluation.
- Ranked objectives and tradeoffs relevant to the question: correctness, usability/accessibility, performance, reliability, resource/cost limits, and implementation or operating effort.
- Explicit assumptions, missing capabilities, and which conclusions depend on them.
- A bounded experiment plan per round, user-specified overall limits, available parallelism, and decision criteria.

Ask only for missing information that materially changes the investigation and cannot be inferred. Continue independent research while answers are pending. Provisional assumptions permit exploration, but cannot establish acceptance against an unknown target. Do not invent a target audience, device, success threshold, quality bar, or deployment constraint as if the user supplied it.

Respect the user's overall time/compute limits. Plan bounded rounds around the baseline, a small shortlist, informative experiments, and integration/review; set each round's cap after estimating experiment cost. Reserve capacity for integration and reporting. A self-assigned round cap triggers a checkpoint and revised plan; continue necessary feasible work within user and host limits. Do not silently narrow the assignment to fit that cap. End with the strongest supported decision when the stopping criteria are met, or report incompleteness when actual limits prevent required work. Do not create goals, scheduled tasks, or background jobs merely because this workflow uses the word "goal."

## Establish shared state and dependencies

Use the project's research convention, or `research/<campaign>/` when none exists; follow host-specific scratch/output locations when present. Read existing state before creating a campaign. Maintain only artifacts the work needs:

- `brief.md`: decision, constraints, objectives, and experiment budget.
- `state.md`: current candidate, uncertainties, ownership, evidence paths, next actions, and consumed/remaining budget where observable.
- `contracts.md`: shared interfaces, dependency graph, and system resource budgets for coupled work.
- `evidence/`: compact source notes and claim-to-source links; `candidates.md` records every substantively investigated alternative and every implemented or tested candidate.
- `experiments/<id>/`: hypothesis, code/config identity, reproduction command, raw results, and interpretation.
- `poc/`: self-contained demo project(s) for advanced candidates, reusable implementation, sample inputs/assets, and launch/evaluation instructions. Include the combined solution when investigating interacting components.
- `decision.md`: concise final paper and implementation handoff.

Create optional files only when useful. The lead writes shared state; workers own assigned experiment directories or explicitly isolated checkouts. Never assume subagents have separate filesystems. Checkpoint results and rejected approaches so resumed work does not repeat them. On resume, verify that the target, code, environment, and evidence still match before reusing conclusions.

For multiple topics, map shared resources, producers/consumers, interfaces, and feedback dependencies. Define relevant contracts before incompatible prototypes grow: data schemas, identity/access, state ownership, timing/order, error recovery, and user-flow assumptions. Allocate resource budgets provisionally; evaluate the complete system or user journey. A contract, audience, or workload change invalidates affected conclusions and triggers targeted reevaluation.

Read [coordination.md](references/coordination.md) when delegating or coordinating coupled investigations.

## Investigate independently, then reconcile

Start with a credible baseline or current workflow and a small set of materially different candidates. Research existing solutions, primary papers, official documentation, relevant user evidence, and applicable source code. Open sources supporting important claims; record versions/dates, assumptions, implementation constraints, and licensing implications when reusing code. Trace apparently independent sources to their original evidence. Results from other products or environments do not establish outcomes for this project's users or system.

Unless the user restricts online access, actively search the web for relevant prior work before settling the shortlist. For questions informed by research literature, search appropriate paper repositories, indexes, and proceedings, such as arXiv, OpenReview, ACM Digital Library, IEEE Xplore, USENIX, ACL Anthology, or CVF Open Access. All named sources and source types are non-exhaustive examples, not an allowlist: actively discover other relevant resources as the investigation develops. Select sources by relevance, evidence quality, and accessibility; use indexes for discovery and inspect original material for evidence. Read [literature.md](references/literature.md) for discovery and appraisal of papers and other resources, and links to candidate experiments. If search or source access is unavailable, disclose the coverage gap and continue feasible work without implying the search or review was completed.

For optimization work, profile the existing end-to-end path when executable before investing in major alternative implementations. Identify the limiting resources and the improvement needed to meet the target. Include keeping the current design or making a small change as candidates when viable. A baseline must be representative and competently configured; do not compare a tuned contender against an accidentally inefficient baseline. If profiling is unavailable, label bottleneck assumptions and target them with early experiments.

Give first-round investigators the same brief and contracts without another investigator's preferred answer. Ask each to identify established approaches, a plausible alternative or hybrid when useful, failure conditions, and the cheapest discriminating experiment. Do not force novelty if an existing design meets the need.

After initial proposals, share concise evidence and specific objections. Separate disagreements over requirements, source interpretation, interface compatibility, and measured behavior. Resolve each with clarification, source inspection, or an experiment. Keep useful dissent recorded; do not repeat discussion until everyone agrees.

Reject candidates that violate hard constraints before ranking viable ones. If objectives conflict, show meaningful tradeoffs and state which priority determines the recommendation. Avoid opaque weighted scores or exhaustive combinations. Prototype alternatives whose outcome could change the decision.

Maintain the candidate record during investigation, not retrospectively after choosing a winner. Give each candidate a stable ID and scope (subsystem, complete architecture, or combination). Record its rationale, work actually performed, evidence links, strengths, limitations, disposition, and the conditions that would justify reconsidering it. Consolidate duplicate ideas; a passing search mention does not require an entry. Do not implement every alternative merely to fill the report.

## Experiment and integrate

Read [experiments.md](references/experiments.md) before implementing or interpreting evaluations; apply its benchmarking details only to performance questions.

For each experiment, record its hypothesis, comparison, expected discriminating observation, decision criteria, and budget before executing it. Build the smallest faithful implementation, interactive prototype, simulation, or evaluation setup that can answer the question. Match the intended platform's relevant APIs, workloads, and conditions while keeping the PoC independent of the existing app/engine project. Explicitly state what a mock, surrogate, or simulated user can and cannot validate.

Evaluate the baseline and shortlisted alternatives under a comparable protocol and the same relevant constraints. Retain observations, raw outputs, and failures as well as summaries. Prefer experiments whose expected reduction in decision uncertainty justifies their cost. Check cheap feasibility constraints and potentially disqualifying assumptions before expensive development. Preserve a last-known-good prototype. Do not modify evaluation criteria to rescue a preferred candidate.

Bring coupled components or flows together early in the standalone demo. Include the full requested feature combination, representative usage and failure cases, and targeted comparisons that explain interactions. A component win is provisional until the combined system or journey passes its relevant checks. Reopen affected workstreams when integration fails; retain unrelated verified findings.

Inspect the intended project's extension points, data/assets, platform capabilities, lifecycle, and synchronization when accessible to identify adoption constraints. Keep default PoC development in its own project; adapting or integrating it into the actual app/engine is a separate follow-on task unless the user requests that work. Record untested integration assumptions. Standalone results establish behavior in the demo's recorded environment, not performance or correctness inside an untested host application.

Use a non-author reviewer when available to check the leading candidate's claims, reproduce decisive executable checks or audit the study protocol and observations, and seek a counterexample under the same constraints. Independent agent context reduces anchoring but is not independent empirical evidence; a shared evaluation flaw can mislead everyone.

## Deliver hands-on demos

When PoCs are in scope, every candidate promoted beyond early exploration into a serious contender needs a runnable, user-testable demo. Prefer one self-contained comparison project with the baseline, candidate variants, and combined solution; use separate packages when necessary. The user must be able to run it without opening, building, or modifying the existing app/engine. Normal declared platform tooling may still be required. Early ideas ruled out through research do not need demos.

Read [demos.md](references/demos.md) when building or packaging these deliverables. Include source, sample inputs/assets, pinned dependencies, simple launch instructions, meaningful controls or a test client, resettable scenarios, and a short verification guide. Exercise the actual proposed implementation; identify every mocked part. Verify the launch path and relevant interactions before describing a demo as ready for review.

Track **agent-verified** and **user-reviewed** separately for each demo revision. Delivering a reviewable demo does not establish user acceptance. Continue feasible R&D while review is pending unless the user explicitly makes review a prerequisite; use their feedback to reopen affected questions. Technical checks and human feedback remain distinct evidence.

## Converge and hand off

Complete the evidence depth the user requested. A research-only assignment can finish with a sourced comparison and a provisional recommendation; a PoC-only assignment can finish with the specified working behavior and stated limits. Neither establishes unperformed integration, benchmark, user, or target validation. For a full R&D assignment, recommend a validated solution only when its acceptance criteria and relevant combined-system checks pass. Keep remaining uncertainties explicit. Stop exploring when additional experiments are unlikely to change the scoped decision within actual user or host limits. If evidence cannot distinguish candidates, report that and prefer the simpler viable option only when consistent with user priorities. If required criteria remain unmet, report no validated winner and identify the smallest next step; a partial result must not silently replace the requested scope.

Use evidence labels consistently:

- **Researched:** supported by cited external sources or inspected code.
- **Prototyped:** built and exercised for the stated behavior, with mocked parts identified.
- **Evaluated:** assessed using a stated protocol with observations recorded.
- **Measured:** quantitative results collected using the recorded method and environment.
- **Integrated:** combined requested behavior was exercised and checked in the named host, such as the standalone demo; this does not imply integration into the intended app/engine.
- **Target-validated:** stated acceptance checks passed in the intended environment and, where relevant, with the intended users or usage context.

Labels describe observed work, not a progression completed by assertion. A surrogate can be measured and integrated without being target-validated. Build success alone is not runtime verification. For supplied results, state their origin and whether independently reproduced; call unreproduced analysis "supplied-record analysis." Synthetic records can test this workflow's decisions but cannot establish actual performance or target validation.

Read [reporting.md](references/reporting.md) when preparing the handoff. Default to one short decision paper (roughly 1–2 pages) with deeper evidence linked, plus the standalone demos, reusable implementation, and integration guide when PoCs are in scope. Engineering feasibility and performance claims normally require runnable code; a product concept can instead need an interactive flow and user-study evidence. For coupled topics, add supporting notes only when they help implementation; the master recommendation owns the combined result. Include:

1. Recommendation, achieved evidence level, and conditions under which it holds.
2. Compact baseline/alternative/final comparison with uncertainty and quality checks.
3. An **Alternatives considered and tested** section, including why each substantive alternative was not selected, plus unresolved risks.
4. Requirement-to-evidence coverage, architecture/interfaces, and a concrete integration sequence for production.
5. Reproduction instructions: relevant build/run/evaluation commands or study protocol, environment, observations/results, and required materials.
6. Direct links and launch instructions for the recommended demo and meaningful finalist alternatives, with agent verification and user review status for each.

Use actual PoC screenshots, recordings, or generated plots when they substantiate a result. Label conceptual diagrams as such; never substitute an illustration for proof of implementation. Check reproduction commands and relative artifact links. Keep the final chat answer short: decision, main evidence, limitations, and paper/demo links. Do not expand an R&D request into production rollout or publishing.

A skill supplies a workflow, not persistent execution or access to missing resources. If required tools, target environments/devices, representative users, or data are unavailable, complete feasible work, preserve a usable handoff, and identify the exact missing validation without claiming it happened.
