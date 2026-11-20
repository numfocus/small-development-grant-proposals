# Bounty Fix

**Reward:** $50.00
**Issue:** https://github.com/numfocus/small-development-grant-proposals/issues/21
**Repo:** https://github.com/numfocus/small-development-grant-proposals

---

## Issue

Comprehensive review and overhaul of Spyder's documentation

## Project

Spyder

## Summary

Much of the content and screenshots/GIFs in the Spyder documentation need a comprehensive update for the substantial new features and UI changes in Spyder 6.0, and more will be needed for the forthcoming Spyder 6.1 version, to be released in a few months. Therefore, we will take this opportunity for a thorough review of the current documentation, add and update the text to reflect new and changed features, enhance the website UI as well as implement modern documentation standards, remaster its screenshots/GIFs to be of higher quality and in modern formats, and upgrade the supporting infrastructure to streamline future updates.

## Submitter

C.A.M. Gerlach

## Project lead

@ccordoba12

## Community benefit

While we don’t collect telemetry from the documentation website itself to respect user privacy, our handful of embedded YouTube tutorial videos alone report more than one million unique views over the past few years. Therefore, modern, up to date Spyder documentation with accurate, comprehensive content and high-quality screenshots and recordings will both help our existing hundreds of thousands of users (per our ~500k+ monthly downloads across all media and millions of Anaconda installations) make the most of Spyder, and ensure it is accessible to the many learners, beginners and new users around the world.

Additionally, the new content will focus on the extensive and evolving suite of remote development features being built into Spyder 6, to help users discover, utilize and take full advantage of these capabilities. This is critical to enable getting these years worth of advancements into the hands of the users we built them for, and put to good use.

Finally, the website’s infrastructure upgrades, usability improvements and standardization implemented as part of this process will help ensure that documentation is a more seamless part of new Spyder versions, and streamline the workflow involved in future such updates. Additionally, we expect to help contribute at least some of these improvements upstream to the Pydata-Sphinx-Theme and potentially other widely-used projects (such as shared automation tooling that has been discussed with other maintainers), benefiting the entire NumFOCUS community.

## Amount requested

10000

## Execution plan

### Timeline and detailed task breakdown

#### Month 1*

* [ ] CAM: Perform initial maintenance and upgrades pre-branching 6.x
    * [x] Maintenance cleanup pre-branching
        - [x] Check theme configuration
        - [x] Fix FAQ anchor custom script
        - [x] Deal with custom styles
        - [x] Check proper infra for multi-version
    * [x] PyData Sphinx Theme upgrade
        - [x] Update Netlify image version
        - [x] Fix Font Awesome issue with 0.16
        - [x] Fix sidebar issue with 0.15
    * [x] Upstream language switcher if feasible
    * [x] Add ref target labels and replace hardcoded `:doc:` links
* [x] CAM: Branch Spyder 6 in docs and fix remaining multi-build issues
* [x] Andres: Review and fix outstanding docs theme UI/UX issues


#### Month 2

* [x] CAM: Review and update current docs outside of Panes section
    * [x] Overview/tour
    * [x] Install guide
    * [x] FAQ
    * [x] Plugins
    * [x] Troubleshooting
* [ ] CAM: Overhaul and modernize workshops section
* [ ] Andres: Produce updated screenshots and GIFs for these sections
    * [x] Overview/tour
    * [ ] Install guide
    * [ ] FAQ
    * [ ] Plugins
    * [ ] Troubleshooting
* [x] CAM: Review first batch of Andres’ work


#### Month 3

* [ ] CAM: Review and update Panes documentation for Spyder 6 (minus new content)
    - [ ] Editor
    - [ ] Files
    - [ ] Find
    - [ ] Help
    - [ ] History
    - [ ] IPython Console
    - [ ] Online Help
    - [ ] Outline
    - [ ] Plots
    - [ ] Profiler
    - [ ] Projects
    - [ ] Code Analysis
    - [ ] Variable Explorer
* [ ] Andres: Produce updated screenshots and videos for panes
* [ ] CAM: Review final batch of Andres’ work


#### Month 4

* [ ] CAM: Write new content for Spyder 6
    * [ ] Debugger pane
    * [ ] Remote development functionality
    * [ ] Environment Manager
    * [ ] Others
* [ ] Andres: Design and produce screenshots and videos for new content
* [ ] CAM: Review final batch of Andres’ work


\*Can be started as soon as August 2025


### Project team and personnel budget

C.A.M. Gerlach, Spyder core developer and docs maintainer: Manager, writer, reviewer, infra
Andres Montoya, Spyder UI/UX designer and web developer: Screenshots, GIFs and UI/web
Carlos Cordoba, Spyder lead maintainer: Subject matter expert

16 weeks * 10 hours/week * $50/hour = $8000 for CAM (writing, review, infra, management)
16 weeks * 5 hours/week * $25/hour = $2000 for Andres (screenshot and GIF creation, design)
(Carlos will contribute his expertise without additional funding under this particular grant)

---

## Process

### 1. Orient yourself first
Before touching any code:
- Read the README and any relevant docs
- Run: find . -type f | grep -v node_modules | grep -v .git | grep -v dist | head -60
- Grep for the key terms from the issue title to find the relevant files
- Read the files around the bug — understand what's currently happening

### 2. Find and read the tests
- Look for test files near the relevant code (*.test.ts, *.spec.js, __tests__, etc.)
- Read them — they tell you what behavior is expected
- Understand what a passing fix looks like before writing a line

### 3. Implement the fix
- Make the MINIMAL change that fixes the issue — nothing more
- Do not refactor, rename, reorganize, or clean up unrelated code
- Do not add dependencies unless the issue explicitly requires it
- Do not modify config files (package.json, tsconfig.json, etc.) unless that IS the fix
- One logical change, one commit

### 4. Verify
- Run the test suite: check package.json scripts for "test", "lint", "typecheck"
  Common commands: npm test, yarn test, pnpm test, pytest, go test ./..., cargo test
- If TypeScript is present: npx tsc --noEmit
- Fix any test failures your change caused — if a test was wrong before, update it

### 5. Commit and document
- git add -A
- git commit -m "fix: Comprehensive review and overhaul of Spyder's documentation"
- Write AGENT_SUMMARY.md with:
  - Root cause: what was wrong and why
  - Fix: what you changed and the reasoning
  - Verification: how to confirm it works
  - Concerns: anything a reviewer should know

---

## Stop conditions

If ANY of these are true, write "UNCERTAIN: [reason]" at the top of AGENT_SUMMARY.md, make NO code changes, and stop:
- The fix requires changing more than ~5 files
- You cannot determine what the correct behavior should be
- The issue requires a database migration, API key, or external service
- You find 3+ open PRs already attempting this fix (high competition)
- The repo is not in a language/framework you can reason about confidently

A clean UNCERTAIN is better than a bad PR.
