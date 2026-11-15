# Reproducible R&D evaluations

Choose the protocol using [methods.md](methods.md). The comparison and provenance rules apply broadly; timing, warmup, and hardware controls below apply when benchmarking. For qualitative studies, use traceable observations and consistent tasks instead of inventing numerical scores or performance tests.

## Design the comparison before tuning

Separate hard acceptance gates from ranked objectives. Faster code or a preferred concept that fails required behavior is not a winner. Record scenarios, feature coverage, quality criteria, protocol, primary observations/metrics, and what difference would matter. If unknown user priorities change the recommendation, show the tradeoffs instead of manufacturing a score.

Use a credible baseline under comparable conditions. Label external results; do not combine them with local observations as if collected by one controlled comparison. For benchmarks, check instrumentation with a small known case before trusting it. For task studies, verify that instructions and tasks actually test the intended question. Fix a flawed protocol openly and reevaluate affected comparisons.

Generate the project-specific harness or evaluation protocol needed by the question. Separate evaluation from candidate development where practical. Candidates must not change thresholds, omit required work, reuse hidden answers, or lower quality to improve the score.

## Minimum run record

Use suitable structured data for quantitative results and traceable notes for qualitative observations. Retain enough context to reproduce decisive evaluations. For executable experiments, a run record can contain:

```text
experiment_id, hypothesis, candidate, baseline
source revision or content hashes, harness revision, contract revision
command, configuration, dataset/scene identity, seed
CPU/GPU, memory, OS, driver, API/runtime/compiler, build mode
requested features and quality settings
warmup, repetitions, sample counts, timing method
raw result/log paths, metrics with units and aggregation
correctness/quality outcomes, failures, exclusions, limitations
```

Adapt fields to the domain and omit inapplicable hardware/build fields. For user studies, record the prototype version, tasks, participant/population context, collection method, observations, and limitations. Mark missing information. Record relevant commands, dependency versions, materials, and controlled inputs. Preserve failed, rejected, and inconclusive evaluations. Keep interpretations separate from raw observations.

Link runs to stable candidate IDs in the candidate record. Retain non-selected prototype revisions and reproduction commands where generated, so a later investigation can reuse the work. Record why an experiment stopped or was invalidated. A crash, missing dependency, exhausted budget, or unavailable device is not proof that the underlying approach is inferior; scope the conclusion to what the experiment established.

## Fair performance measurement

- Use comparable optimized builds, inputs, feature coverage, and measurement boundaries. Separate setup, compilation, cold start, and steady state when they answer different questions.
- Warm up relevant caches/pipelines. Repeat runs and vary order to mitigate drift. Report sample counts and variability. A difference within observed noise is inconclusive.
- Choose relevant statistics: throughput, memory, latency tails, frame-time distributions, error rates, or quality. Do not present a lone best run as typical performance.
- Avoid unrelated work competing for constrained resources. Record unavoidable contention, power modes, throttling, or virtualization when they limit interpretation.
- Ensure asynchronous work actually completed. CPU submission timing does not measure GPU execution. Use supported GPU timing/profiling when available; label instrumentation limits.
- Measure total behavior and component costs. Overlap, synchronization, caching, and shared bandwidth mean isolated times may not add to integrated results.

Choose holdout inputs or stress conditions before final tuning when overfitting is plausible. If repeatedly tuning against a failed holdout, treat it as development data and obtain a fresh final check when feasible. Avoid inflated statistical claims: adjacent frames are correlated, and tiny sample counts do not establish reliable extreme percentiles.

## Fidelity and quality

State what the standalone PoC preserves from the target and what it simplifies. A CPU model of GPU work cannot establish GPU frame time; an interactive mock cannot establish backend correctness or real-user adoption. Explain why synthetic data or simulated conditions represent the scenario, and what remains unvalidated. Match the demo's relevant platform APIs, workloads, assets, and quality constraints to the intended use. Measurements describe the recorded demo environment; app/engine integration overhead and behavior remain unverified until separately checked.

For visual systems, inspect actual rendered outputs and a sequence/capture when motion matters. Check relevant artifacts: popping, flicker, motion/shadow mismatch, temporal lag, leakage, or incorrect occlusion. Use target-specific criteria; a screenshot alone cannot prove temporal correctness or performance. Record performed quality checks.

For application flows, inspect interaction, accessibility, errors, and recovery where relevant, and use observed task evidence when claiming usability. For other systems, use appropriate correctness checks, invariants, data integrity assertions, or reference outputs. Performance evidence requires preservation of requested behavior.

## Integrated decision

Compare the baseline, strongest viable alternatives, and combined candidate on relevant scenarios and failure conditions. Use targeted interaction tests or component comparisons to locate wins and regressions. Avoid exhaustive combinations unless affordable and justified.

When the decision may change with load or environment, test a small meaningful sweep around the target workload and plausible operating extremes. Identify crossovers, saturation, and failure boundaries where observed; do not claim a curve or operating range from one point. Separate measured limits from extrapolation. A solution meeting one workload's budget may need a different recommendation for other target devices, network conditions, or quality levels.

For executable experiments, reproduce the decisive result from documented commands, preferably with a non-author reviewer. For observational studies, audit the protocol, provenance, and observations; seek independent corroboration when it would materially affect the decision and is feasible within scope. Do not demand identical human responses on repetition. Link important claims to sources or evaluations. Scope recommendations to evaluated environments, scenarios/populations, quality constraints, and known exceptions. If target validation is unavailable, provide its procedure and label the result provisional.
