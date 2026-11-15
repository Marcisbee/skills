# Standalone demos for hands-on review

## What needs a demo

When PoCs are in scope, package every candidate promoted to a serious contender for user testing, including meaningful finalists that are ultimately not selected. Early research ideas and exploratory experiments eliminated before this stage need only their recorded evidence and disposition. Explicit research-only assignments do not require building demos.

Prefer one comparison project per campaign, with a baseline, selectable candidate implementations, and the combined requested behavior. Share fixtures and controls where practical. If alternatives require incompatible platforms or runtimes, provide separate self-contained packages and a common comparison protocol. A candidate does not need a separate polished application when a selectable variant is sufficient.

## Self-contained delivery

The demo must run independently of the existing engine/app checkout and build. It may reside in a research directory alongside that project, but copying or unpacking the demo elsewhere must not break it. Include its own source, representative sample inputs/assets, configuration, dependency versions or lockfiles, and build/launch instructions. Avoid undeclared parent-directory imports, user-specific absolute paths, hidden generated assets, or dependencies on an already-running development server.

Normal declared platform tooling, drivers, or SDKs can be prerequisites. Aim for one launch command after documented setup, or a directly usable artifact where appropriate. Include redistribution-compatible assets or reproducible generators and identify any unavoidable acquisition steps. Provide local fixtures or substitutes for external services where they preserve the experiment's meaning. If a live service, device, account, or restricted asset is essential, disclose that requirement and the resulting limit to self-containment; do not silently present a mock as equivalent evidence.

Use a format suited to the claim: a small native renderer, standalone mobile test app, web application, notebook, CLI, API test client, or another appropriate executable artifact. A graphical interface is useful when it exposes behavior the user should inspect; it is not mandatory for every backend or data experiment. Avoid moving a native/platform-specific question into a browser merely to simplify presentation if that changes what can be validated.

Keep the proposed algorithm or component separate from the demo wrapper where practical, so it can be reused. Actual target-project modifications belong to a separately requested integration step. Preserve explicit boundaries between demonstrated behavior, host-integration assumptions, and target validation.

## A useful verification experience

Include:

- A representative default scenario that exercises the actual implementation.
- Baseline/candidate selection or a documented comparison using equivalent inputs and quality settings. Identify any adapted baseline whose behavior differs from the existing product.
- Controls or test commands for the uncertainties that matter: load, input variation, errors, retries, interruptions, or other relevant conditions.
- A reset path and reproducible scenarios; preserve seeds/configuration where applicable.
- A short guide: what to try, expected behavior, what a failure looks like, and known limitations or mocked parts.
- Relevant live observations and a way to reproduce recorded benchmarks/evaluations. Clearly distinguish current measurements from saved results.

Do not add unrelated UI polish or instrumentation. The review surface should expose the hypothesis and tradeoffs. If a visual side-by-side view makes candidates compete for CPU/GPU resources, benchmark them separately under the recorded protocol. Likewise, account for demo UI/instrumentation overhead when it affects a claim.

For interacting features, make the combined scenario directly testable. Component demos alone do not demonstrate the unified solution. Feature toggles or targeted scenarios should help explain how the parts affect each other.

## Verify and record review state

Before marking the demo ready for review, launch it from its packaged directory or a clean copy using only documented prerequisites. Exercise its default case, important controls/test commands, reset behavior, and claimed comparison paths. Record the tested platform and demo revision, and link results to the exact code/configuration used. If required execution is unavailable, mark the demo unverified and explain the missing step; source files or a successful build alone do not establish a working demo.

For each delivered revision, distinguish:

- **Agent verification:** which launch, behavior, comparison, and benchmark checks ran, with their results.
- **User review:** pending, reviewed with feedback, or explicitly accepted, based on actual user input and scoped to the reviewed revision/claims.

Do not infer acceptance from delivery, silence, or elapsed time. User feedback can expose a new requirement or reopen a specific experiment; preserve prior evidence and update affected conclusions. A user's positive impression does not replace objective checks, and technical verification does not establish that the user has reviewed the result.
