# Agent Summary — Bounty for issue #21

UNCERTAIN: Issue #21 is not a bug report against this repository. It is a *funded grant
proposal* (labelled `2025-R1` + `funded`) whose deliverables are content, screenshots and
Sphinx/Netlify infrastructure in the **Spyder documentation repository**, not code in
`numfocus/small-development-grant-proposals`. There is no defect here to fix, and no code
change in this repo could satisfy the issue. Per the stop conditions I made **no code
changes**.

## What the issue actually is

`gh issue view 21 -R numfocus/small-development-grant-proposals` returns:

- **Title:** "Comprehensive review and overhaul of Spyder's documentation"
- **State:** OPEN
- **Labels:** `2025-R1` ("2025 - Round 1"), `funded` ("Projects selected through the random selection")
- **Body:** a submission-form proposal — Project `Spyder`, Amount requested `10000`,
  submitter C.A.M. Gerlach, project lead @ccordoba12, plus a 4-month execution plan.

This repository is the *submission interface* for the NumFOCUS Small Development Grants
program: issue templates (`.github/ISSUE_TEMPLATE/`), three workflows, and ~6 Python
scripts that parse proposal issues, check for duplicate projects, distribute proposals to
reviewers, and run the randomised funding allocation. It contains no Spyder documentation
and no Sphinx site.

Per `README.md`, a funded issue is deliberately **kept open to record project progress**
and is closed as `completed` when the work is done. So issue #21 being open is the
documented steady state for a funded grant — it is a tracking issue, not an open defect.

The work the issue requests (review/rewrite docs pages, remaster screenshots and GIFs,
upgrade PyData Sphinx Theme and the Netlify build, produce videos) is 4 months of two
people's effort in a different repo, and parts of it explicitly require external services
(Netlify builds, screenshot/GIF/video production). That trips three stop conditions:
cannot determine the correct behaviour in *this* repo, scope far beyond ~5 files, and
dependence on external services.

## Orientation performed

1. Read `README.md`, `instructions.md`, both issue templates, all three workflows, and
   every script (`sdg_utils.py`, `extract_sdg_issues.py`, `allocate_funds.py`,
   `check_duplicates.py`, `distribute_proposals.py`, `project_selection.py`).
2. Confirmed the checkout is byte-identical to upstream — `git diff --stat upstream/main HEAD`
   is empty and `HEAD`, `origin/main`, `upstream/main` are all `afe555e`. No bug had been
   planted locally for me to find.
3. Tested the one code path in this repo that touches issue #21 — `parse_issue()` in
   `scripts/sdg_utils.py` — against the **real** issue body fetched from GitHub. It parses
   correctly, so there is no issue-specific parsing defect either:

   ```json
   {"awarded": false, "year": 2025, "round_number": 1, "funded_amount": 10000,
    "amount_requested": 10000, "issue_number": 21, "project_name": "Spyder",
    "reviewers": []}
   ```

   I also checked the `## Amount requested` (resubmit template, no `(USD)`) and
   `### Amount requested (USD)` (submission template) spellings; the regex added in
   `b2c0f51`/`0993fc4` handles both.

## Verification

```
cd scripts && python -m pytest -q
```

Result: **6 failed, 5 passed** — unchanged before and after my work, since I changed no
code. These failures are pre-existing on upstream `main` and unrelated to issue #21; see
below.

## Concerns for a reviewer

1. **Pre-existing test failures, unrelated to this issue, left untouched.** All six
   failures are in `scripts/test_project_selection.py`. Cause: the tests set
   `np.random.seed(2025)` and then assert on exact `capfd` output, but
   `select_proposals_to_fund` (`scripts/project_selection.py:20`) unconditionally calls
   `np.random.seed(seed)` with the default `seed=None`, which reseeds NumPy from OS
   entropy and discards the test's seed. Confirmed directly: after `seed(2025)` then
   `seed(None)` the first draw differs from the seeded one. The one-line fix is to seed
   only when `seed is not None`, but that is a different bug from issue #21 and the task
   says to make the minimal change for *this* issue, so I did not touch it. Worth filing
   separately.

2. **Other latent bugs I noticed and deliberately did not touch** (all out of scope):
   - `scripts/check_duplicates.py:15` compares an `int` to a `set`
     (`len(projects) != uniq_projects`), so the duplicate-labelling branch always runs.
   - `scripts/distribute_proposals.py:84` reads `reviewer` after the
     `else: print(... hasn't got reviewers)` branch, where it is either unbound (first
     proposal) or stale from a previous iteration; `reviewers_left.remove(reviewer)` on a
     stale name can also raise `ValueError`.
   - `scripts/sdg_utils.py:66` calls `amount_match.group(2)` without guarding
     `amount_match is None`; only `ValueError` is caught, so a body missing the field
     raises `AttributeError`.
   - `instructions.md` points at `./CoI.yaml`, which was moved to
     `scripts/reviewers_list.yaml` in `d62591c`; the link is dead.

3. **High competition on speculative script fixes.** There are already open PRs doing
   exactly this kind of unrequested cleanup on these scripts: #100 ("Dynamically fetch
   GitHub ProjectV2 field IDs"), #101 ("Improve robustness and clarity of grant management
   scripts"), #102 ("Robustness and consistency in SDG scripts"), #103 ("Improve markdown
   header parsing in SDG issue extraction"). Opening another one against issue #21 would
   be both off-target and redundant.

4. **If a maintainer does want action on #21**, the plausible options are all outside this
   repo or outside code: do the documentation work in the Spyder docs repo, or update the
   execution-plan checkboxes in the issue body to reflect progress. I did not edit the
   issue, as that is the grantee's record to maintain.

## Files changed

None. Only this `AGENT_SUMMARY.md` was added; the working tree is otherwise identical to
`upstream/main`.
