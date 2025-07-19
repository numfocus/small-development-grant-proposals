import numpy as np


def select_proposals_to_fund(budget, funding_limit, proposals, seed=None):
    """
    Randomly selects which proposals to fund in a round.

    `budget` is a number referring to the amount of funding to be allocated _in that round_.

    `funding_limit` is the maxumum amount any project can be funded for in a given year.

    `proposals` is a list of tuples of the form `(name, requested_amount, previous_funding)`
    where `name` is the name of the proposal, `requested_amount` is the amount of funding
    that proposal requests and `previos_funding` is the amount of funding the project
    associated with that proposal has received that year.

    This function will throw and not produce any results if any of its inputs are invalid.
    """

    np.random.seed(seed)

    for p in proposals:
        if len(p) != 3:
            raise ValueError("Malformed proposal")
        if p[1] + p[2] > funding_limit:
            raise ValueError(
                f'If proposal "{p[0]}" were funded it would receive more than the funding limit this year.'
            )

    names = [str(p[0]) for p in proposals]
    weights = [(funding_limit - p[2]) / p[1] for p in proposals]

    for w in weights:
        assert w >= 1  # this should be redundant with the validation check above.

    if len(set(names)) != len(names):
        raise ValueError("Proposal names are not unique")

    funded = []
    budget_remaining = budget
    temp_budget_remaining = budget + 0
    while budget_remaining > 0 and len(funded) < len(proposals):
        total_weight = sum(weights)
        if total_weight == 0:
            # When all the proposals have been evaluated and there's still budget
            break
        i = np.random.choice(range(len(weights)), p=[w / total_weight for w in weights])
        weights[i] = 0
        proposal = proposals[i]
        proposal_budget = proposal[1]
        temp_budget_remaining -= proposal_budget
        if temp_budget_remaining > -proposal_budget / 2:
            funded.append(proposal)
            budget_remaining = temp_budget_remaining

    print("Inputs:")
    print(f"Budget: ${budget}")
    print(f"Per-project funding limit: ${funding_limit}")
    print("Proposals in the drawing:")
    for p in proposals:
        print(
            f'"{p[0]}" requests ${p[1]} and is proposed by a project that has previously received ${p[2]} this year.'
        )

    print()
    print("Random Outputs:")
    print(
        f"Allocated: ${round(budget - budget_remaining, 2)} (${round(abs(budget_remaining), 2)} {'over' if budget_remaining < 0 else 'under'} budget)"
    )
    print(f"{len(funded)} proposals funded out of {len(proposals)} total proposals in the drawing")
    print()
    print("Funded the following projects")

    for p in funded:
        print(f'Fund "{p[0]}" for ${p[1]} bringing its project\'s annual total to ${p[1] + p[2]}.')

    return [f[0] for f in funded]
