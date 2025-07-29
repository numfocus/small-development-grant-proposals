# Instructions

## Confirming submission

NumFOCUS will check whether the project leads have either submitted the project or has approved such submission if done by someone else.

Labels are then changed from `awaiting approval` to `YYYY-RX`.

A label can be created with the `gh` cli as:

```
gh label create 2025-R1 -d "2025 - Round 1"
```

> [!IMPORTANT]
> The above command and the examples below needs to be executed from within a clone of the repository and from an account with write permissions to the repository.
> If we want to run it from somewhere else, then the command needs to specify the org and repository to be executed on adding the following argument to the commands:
> ` -R numfocus/small-development-grant-proposals` 

To find all the open issues with the `"Awaiting approval"` label:

```
gh issue list -l "Awaiting approval" -L 100
```

Since it may be easier to label them all first with the `YYYY-RX` and then remove the `"Awaiting approval"`, we can label them all with:

```
gh issue edit $(gh issue list -l "Awaiting approval" -L 100 --json 'number' --jq '[.[].number] | @sh') --add-label "2025-R1"
```

Similarly we can remove the Awaiting approval automatically to all as:
```
gh issue edit $(gh issue list -l "Awaiting approval" -L 100 --json 'number' --jq '[.[].number] | @sh') --remove-label "Awaiting approval"
```

> [!NOTE]
> This check could be automated if a list of gh project leads is created.

## Check for multiple submissions from same project

The check duplication workflow is triggered manually, either clicking on the [action page](https://github.com/dpshelio/sample-gh/actions/workflows/duplicate.yml) or through the cli:
   ```
   gh workflow run duplicate.yml -f round=1
   ```
   
   The status of the workflow can be seen as
   
   ```
   gh run list --workflow=duplicate.yml
   ```
   If there are two issues with the same project name, they both get labelled as "duplicate" and they need to be sorted before continuing (by closing one of them with a comment and removing the `"duplicate"` label to the one put forward).

## Distribute the proposals between the reviewers

The proposals are distributed through a non-public project board
The project board is update for distributing the proposals according to the Conflict of Interest ([`CoI.yaml`](./CoI.yaml)) file. As before, either through the [Extract SDG action page](https://github.com/numfocus/small-development-grant-proposals/actions/workflows/sdg.yml) or through the CLI:

```
gh workflow run sdg.yml -f round=1
```

Then the reviewers check the proposals and set as approved if fulfil the requirements.
Through a reviewers meeting, a project is selected to be awarded skipping the random allocation, by setting the issue with the label "awarded".

## Random selection

The rest of the issues for this round are ready to be randomised and the funds to be allocated. To do so the [Allocate funds workflow](https://github.com/dpshelio/sample-gh/actions/workflows/funding.yml) needs to be triggered providing the funds available for this round, or through the CLI as:

```
gh workflow run funding.yml -f round=1 -f budget=15000
```

This will run the action and label as "funded" the projects that have been randomly selected.


## Close the not funded projects

Once that the projects from a particular round have been selected and funded, the rest can be closed as "not planned".

```
gh issue list -S "-label:funded label:2025-RX-CHANGEME" -L 100 --json 'number' --jq '[.[].number] | @sh' | tr -d '\n' | xargs -d " " -I% gh issue close % -r "not planned"
```

