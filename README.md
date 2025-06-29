# Small Development Grant Proposals

This repository is the new interface to submit your proposals for the NumFOCUS Small Development Grants (SDG) program.

## How does the SDG program work?

At the end of 2024 the SDG prorgram was reviewed and a set of recommendations were put forward that is being implemented from 2025 onwards.
A few things have changed, so read on to know what you'll need to do to take part in the coming rounds.

> [!note]
> The program is still only available for [Sponsored](https://numfocus.org/sponsored-projects) and [Affiliated](https://numfocus.org/sponsored-projects/affiliated-projects) NumFOCUS projects.
> Proposals for projects that are not on these lists won't be considered.

### Where the proposal are submitted?

Proposals are now submitted [as issues to this repository](https://github.com/numfocus/small-development-grant-proposals/issues/new/choose). This means that proposals from now on are fully open and visible to the whole community. 
By using issues on this open repository, people from the community can add comments, questions and even suggest collaborations, as well as providing updates of the evolution of the project once funded. Therefore, making it easier to enable cross-collaborations between NumFOCUS projects.

### How the projects will be selected for funding?

The proposal has been simplified, as well as the selection process. The Small Development Grants program committee will review the approprietness of the proposal (is it aligned with the project's goals? does the funding requested seems reasonable?). Between all the appropriate proposals, a randomisation algorithm will be used to rank the proposals, and they will be awarded till the funds for each round are exhausted. Since each project is limited to $10k of funding per year through this program, the randomisation algorithm will take in consideration what projects have been funded on previous rounds and the total amount of money funded so far.

The committee will select one proposal per round based on their merits that will be awarded the funds skipping the randomisation algorithm.

#### Can I see the randomisation script?

Yes! The [script is available in this repository](./scripts/project_selection.py). The execution of the script will happen using github actions (this is still working on progress)

### How will be GitHub used to manage the projects?

Project proposals will be received as issues. These issues will be originally labelled as `Awaiting approval` till project leads confirm it's real (NumFOCUS will contact them in case they've not reacted). Proposals that aren't confirmed will be closed as `rejected` and labelled as `spam`. Everything else will be labelled as `YYYY-RX` (where `YYYY` is the year, and `RX` will be the selected round in that year - e.g., `2025R1`)

The proposals received will be distributed across the SDG committee. They will review the proposals and check for appropriateness. They may ask for clarification on the issue if required. If the proposal is not considered appropriate, they will be labelled as `non-appropriate` and closed as `rejected`. Between all the appropriate proposals, the SDG committee will select one proposal that will be awarded directly (labelled as `award`). The rest will be put in the randomisation script.

The randomisation script will select projects till the funds are exhausted. The ones that hasn't been selected will be closed as `rejected`. All selected and awarded projects will be labelled as `funded`. Issues will be kept open to record the project progress and it will be closed as `completed` when the project is done.

This flowchart explains the above in a graphical manner:

```mermaid
flowchart TD
    A[proposal submited] -->|label 'awaiting approval'| B{Project leeds confirm}
    B --> |remove 'awaiting approval'; label 'YYYY-RX'| C{Review by SDG}
    B --> |label: 'spam'| D[issue: closed - 'rejected']
    C -->|appropriate| E{considered for award}
    C -->|label: 'non-appropriate'| F[issue: closed - 'rejected']
    E -->|random| G{Included on randomisation}
    E -->|label: 'award'| H[Removed from random]
    G --> I[selected]
    G --> J[No selected - issue:closed - 'rejected']
    I --> |label: 'funded'| K[Project development - issue updated with progress]
    H --> |label: 'funded'| K
    K --> L[Project completed - issue:closed - 'completed']
```

### Can I resubmit the same proposal if it hasn't been awarded?

After every selection process, all the issues with submissions that didn't get funded will be closed (as `rejected`).  You will be able to open a new issue (using the "Resubmit a previous proposal" template) and refer to the previous issue number and add any required updates.

Issues are closed as the project may not be valid anymore due to date or other constraints. This helps keeping the list of issues as lean as possible.


### I have other questions...

Email any other questions you may have to [Arliss](https://mailto:arliss@numfocus.org) at NumFOCUS.
