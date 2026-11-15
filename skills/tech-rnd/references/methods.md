# Adapt the evidence to the question

Keep the core loop: frame the decision, investigate alternatives, design discriminating evaluations, build appropriate prototypes, compare evidence, test interactions, and report the decision plus alternatives. The validation method and artifact change with the question. Use only the dimensions that matter to the requested outcome.

## Types of uncertainty

| Question | Useful evidence or experiment | Important limit |
|---|---|---|
| Can we build or integrate this? | Minimal implementation against the actual APIs, data path, devices, or dependencies | A mock establishes only what it faithfully exercises |
| Is the behavior correct and reliable? | Reference comparisons, invariants, end-to-end cases, failure/recovery experiments | Passing the happy path does not cover failure behavior |
| Can people use it, and does it help? | Existing research/analytics, task-based prototype sessions, observed completion/errors, appropriately designed product experiments | Technical feasibility and agent-generated personas do not prove user value |
| Is it fast or efficient enough? | Profiling, comparable benchmarks, resource measurements across relevant loads | Synthetic workloads and different environments limit generalization |
| Is the tradeoff worth adopting? | Compatibility checks, implementation spikes, operating-cost models, maintenance constraints | Separate measured inputs from estimates and uncertain assumptions |

Mixed questions need separate hypotheses. For example, a web feature may be technically feasible, usable in observed sessions, and still unproven to improve retention. Keep those conclusions separate. Feature absence or the current manual workflow can be the baseline. Do not assume a new feature is necessary.

## Domain examples

These are examples for selecting a protocol, not mandatory checklists or recommended architectures.

| Domain | Possible investigation | Relevant checks |
|---|---|---|
| Web applications | Search, onboarding, large data views, collaboration, offline editing | Task completion, accessibility, browser/device behavior, interaction latency, network interruptions, state consistency |
| Mobile applications | Offline sync, background work, notifications, on-device features | Device/OS behavior, lifecycle transitions, recovery after termination, connectivity, energy/memory, permissions, usability |
| Backend/distributed systems | Queues, caching, storage, service boundaries | Correctness under retries, ordering, consistency, recovery, load/tail latency, operating cost |
| Data/ML | Retrieval, ranking, model or pipeline choice | Representative held-out data, error analysis, leakage controls, latency/cost, data provenance |
| Desktop/embedded systems | Local processing, device integration, constrained runtimes | Platform/hardware capabilities, timing/resource limits, lifecycle and failure recovery, deployment constraints |
| Graphics/game engines | Geometry, animation, lighting, interacting simulations | Visual/temporal correctness, integrated frame time, memory, representative scenes and target hardware |

For web and mobile work, define the complete user journey as well as component boundaries. A local UI success can be undone by authentication, backend errors, sync conflicts, or device lifecycle behavior. For graphics, the equivalent combined check might cover geometry, motion, and shadowing together. Adapt shared contracts to the domain instead of importing rendering concepts into unrelated work.

## Evidence from people and product usage

Use available authorized research and product data. Record who or what was observed, relevant population/context, task/protocol, sample size, collection method, and limitations. Preserve observations separately from interpretation; summaries from multiple agents are not additional participants. Do not invent interviews, user-test sessions, traffic, quotations, or outcome improvements.

For qualitative evaluation, use explicit observation criteria and report concrete findings, contradictory observations, and limits to generalization. Small convenience samples can reveal issues without establishing a population-wide success rate. For quantitative comparisons, check that groups, tasks, exposure, and measurement boundaries support the proposed comparison; correlations and unmatched before/after observations do not automatically establish causation.

When direct evidence is unavailable, distinguish expert/heuristic inspection, simulated behavior, technical checks, and hypotheses about real users. Deliver an appropriate prototype and a concrete study plan where useful, while leaving the relevant user-outcome criteria unverified. Do not substitute extra code or benchmarks for missing evidence about usability or value.

## Platform fidelity

Distinguish browser emulation from physical devices, emulators from actual mobile hardware, mocks from live dependencies, and local tests from deployment conditions. Choose the required fidelity from the claim. A desktop emulator can support functional exploration without establishing phone energy consumption; a mock backend can validate a flow without proving synchronization correctness.

Use domain-specific methods or specialist tools when the question requires them. This skill coordinates evidence-driven R&D; it does not replace the subject knowledge, equipment, participants, or study design needed to establish a claim.
