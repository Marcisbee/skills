# Find research that can change the decision

## Discover efficiently

Translate each important uncertainty into queries using the problem, established terminology, alternative terminology, key constraints, and possible competing methods. Search for both established work and recent developments. Use relevant repositories and proceedings: for example arXiv, OpenReview, ACM Digital Library, IEEE Xplore, USENIX, ACL Anthology, and CVF Open Access. General web search, Google Scholar, or Semantic Scholar can help discover original sources when accessible. These are non-exhaustive examples, not an allowlist or a requirement to query every service. Discover and use other relevant resources even when their names or types do not appear in this skill.

Expand beyond papers when useful: official documentation and standards, source repositories and issue discussions, engineering articles and postmortems, conference talks, theses, datasets, benchmarks, patents, specialist communities, and other pertinent material. Follow promising references across formats and revise queries as the problem becomes clearer. A source's inclusion here does not establish authority; its absence does not disqualify it.

Choose breadth from the decision. An algorithm or architecture comparison may need papers, author implementations, and reproductions; an API compatibility question may be answered primarily by official documentation and a small test. Do not add a literature quota to unrelated feature work.

For a promising paper, follow relevant references to earlier methods and look for later improvements, independent reproductions, or contradictory findings. Keep this bounded by whether another source could change the shortlist or experiment design. Search for failure cases and limitations as well as successful results. Do not rank evidence solely by recency, citations, venue prestige, or benchmark position.

When delegating, split substantive questions or approaches among investigators. Allow independent first passes, then consolidate queries and source records to avoid repeated searching. Deduplicate by DOI, arXiv identifier, or verified title/authors; a preprint and its published revision are usually versions of one work, not independent evidence.

## Read and appraise

Assess each resource's provenance, firsthand knowledge, supporting evidence, currency, and applicability. Trace technical claims to original specifications, code, data, experiments, or authors where possible. Community discussions and secondary summaries can reveal candidates and failure cases; qualify their claims and corroborate decision-critical conclusions. Keep anecdote, opinion, author-reported findings, and independently reproduced observations distinct. Apply the paper-specific steps below when reading papers, and equivalent source-appropriate checks for other formats.

Use titles and abstracts to triage. For decisive claims, read the relevant full-text methods, evaluation, results, and limitations; inspect figures/tables and linked code when they matter. Do not present a search snippet or abstract as a full-paper review. If access is limited, look for an accessible author manuscript or repository version and record which version was read. State unresolved access limitations.

Record publication status from available evidence: preprint, accepted/published work with a verified venue, or unknown. Hosting on arXiv does not establish peer review. Distinguish peer-review status from independent replication. Note relevant revisions, corrections, withdrawals, or retractions when encountered; do not treat an unverified status as confirmed.

Assess whether the claim transfers to this project: assumptions, workload/data, hardware/platform, quality constraints, baseline fairness, implementation complexity, and hidden preprocessing or training cost. A reported speedup or user outcome remains the authors' result until appropriately reproduced. Check whether linked code actually implements the claimed method and which dependencies/assets are needed.

## Preserve useful evidence

Keep concise records in `evidence/` with verified title/creator, source type, date/version, stable locator, and inspection depth. For papers, include DOI/arXiv ID and publication status when available, and whether the abstract, relevant sections, or full paper was read. For other resources, use appropriate locators such as a repository commit, documentation version, dataset release, or talk timestamp. Never invent citations or identifiers. Link important claims to the supporting passage, figure, table, code, or observation when practical.

For each decision-relevant source, record its contribution, limitations, candidate IDs it supports or challenges, and the experiment needed to test applicability. Include that link in the alternatives record even if the method is not selected. Record important search coverage and unresolved gaps so later agents can resume without repeating everything.

The final paper cites the sources behind its recommendation and substantive alternatives, while keeping author-reported results separate from local measurements. Describe the search as targeted unless an explicit systematic-review protocol was actually completed.
