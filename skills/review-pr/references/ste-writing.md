# Write the review in ASD-STE100

Read this file before you write the final batch. Apply it to titles, comments, questions, worker reports and scope notes.

Use [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) as the source for words and rules. A short sentence alone does not establish compliance. A mechanical tool cannot establish compliance with all the rules.

## Write, then do a language audit

1. Keep the full finding list. Use one term for one meaning. Keep exact code names, paths, commands and quotations.
2. Use active voice when you know the actor. Give one action in each instruction. Use no prose semicolons.
3. Use a maximum of 20 words per sentence in this skill's output. This house limit also applies to descriptions.
4. Run `python3 <skill-dir>/scripts/ste_gate.py <draft.md>` on the complete draft. Correct the reported prose. Run it again.
5. Do a separate word and meaning audit. Read the trigger, effect and correction again after the language changes.

The standard permits 25 words in a description and 20 in an instruction. A paragraph can have a maximum of six sentences. Use short paragraphs. Use the standard's word-count rules for the manual audit. The script uses an approximate count and a short list of known faults. It does not have the full dictionary or a grammar model. If Python is not available, do the mechanical pass manually and state this limit.

For the word audit, use the dictionary's approved part of speech, meaning and word forms. Do not use ordinary English knowledge as proof. Use permitted technical nouns and technical verbs only in their specified subject categories. For software, these can include computer-process terms. Record the category and meaning when the term is in doubt. A technical term exception does not permit an ordinary adjective or verb.

Do not put ordinary prose in code spans to bypass the audit. Exact identifiers and quoted source text are different from your own prose. If you cannot establish an approved word use, rewrite the sentence with simpler words. If a source is not available, state the audit limit. Do not assert full compliance from a script result.

## Known traps from earlier reviews

| Do not use this ordinary form | Use this form when the meaning agrees |
|---|---|
| “Check the key.” | “Make sure that the key includes the user ID.” |
| “Test two users.” | “Do a test with two users.” |
| “both users” | “the two users” |
| “still returns” | “returns” |
| “needs a value” | “must have a value” |
| “wrong key” | “incorrect key” |
| “valid input” | State the permitted input, for example “a positive integer”. |
| “existing record” | State which record, for example “the saved record”. |

`CHECK` and `TEST` are approved nouns. Their ordinary verb uses are not approved. Other known traps include “now”, “avoid”, “confirm”, “require”, “remain” and “identical”. This list is not the dictionary. A script pass does not clear other words or uses.

Preserve the finding's conditions during revision. Do not replace “when the table is missing” with “in legacy mode”. Do not remove a supported finding to make the language pass. Deliver the full revised batch only after these passes.
