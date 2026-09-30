# Auto-documentation result PoC

This repository's `main` branch is the documentation source of truth for the [calculator source repository](https://github.com/kohei-yoshida/auto-doc-source-test). Automation may propose changes only through an `auto-doc/...` branch and pull request. Humans own final approval and merge.

## Structure

- `overview/features.md`: feature index
- `features/calculator.md`: behavior and constraints
- `manual/calculator.md`: user instructions
- `changes/issue-xxx.md`: issue-oriented change notes
- `templates/`: guidance for new feature pages and change notes

The Markdown-first layout keeps the PoC minimal and makes a later `main  static-site build  hosting` pipeline straightforward.

## Setup

Repository administrators must configure:

- Secret `OPENAI_API_KEY`: OpenAI project API key used for review-driven revisions.
- Optional repository variable `OPENAI_MODEL`; default is `gpt-4.1-mini`.
- Actions setting **Workflow permissions  Read and write permissions** so `GITHUB_TOKEN` can update the PR branch.
- Branch protection on `main`: require a PR and at least one human approval; do not allow automation to bypass protection.

The source repository separately needs an `AUTO_DOC_GITHUB_TOKEN` with access to create branches and PRs here. No secret value belongs in source control.

## Review revision flow

1. The source workflow opens a Docs PR from an `auto-doc/...` branch.
2. A human adds a line-level PR review comment.
3. `revise-docs.yml` supplies the comment text, file and line, current Docs PR, current Markdown, related source PR, and source diff to the OpenAI Responses API.
4. The model proposes a bounded Markdown-only revision.
5. The workflow commits it to the same Docs PR branch with an `[auto-doc]` marker and pushes.
6. A human reviews, approves, and merges.

Only newly created review comments trigger the workflow. Bot comments are ignored; generated commits do not trigger the review-comment event; runs are serialized per PR. These controls prevent automation loops.

## Local verification

```sh
python -m unittest discover -s test -p 'test_*.py'
```

End-to-end verification requires Secrets: merge a source PR that closes an issue, confirm this repository receives a Docs PR, add a line-level review comment, and confirm the same branch receives one new automation commit.

## Calculator

Open `index.html` through any static web server. It supports add, subtract, multiply, divide, clear, invalid-input feedback, and a dedicated divide-by-zero error. Pressing Enter in either number input performs addition.

```sh
npm test
```
