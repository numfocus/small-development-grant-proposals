import numpy as np


class Proposal:

    def __init__(self, name, requested_amount, previous_funding):
        self.name = str(name)
        self.requested_amount = abs(requested_amount)
        self.previous_funding = previous_funding


def select_proposals_to_fund(budget, funding_limit, proposals, seed=None):
    """
    Randomly selects which proposals to fund in a round.

    `budget` is a number referring to the amount of funding to be allocated _in that round_.

    `funding_limit` is the maxumum amount any project can be funded for in a given year.

    `proposals` is a list of tuples of the form `(name, requested_amount, previous_funding)`
    where `name` is the name of the proposal, `requested_amount` is the amount of funding
    that proposal requests and `previous_funding` is the amount of funding the
    project associated with that proposal has received that year.

    This function will throw and not produce any results if any of its inputs are invalid.
    """

    # `seed` can be a seed (integer) or a random number generator.
    rng = np.random.default_rng(seed)

    proposals = [Proposal(*p) for p in proposals]
    n_proposals = len(proposals)

    if len(set(p.name for p in proposals)) != n_proposals:
        raise ValueError("Proposal names are not unique")

    weights = np.zeros(n_proposals)
    for i, p in enumerate(proposals):
        remaining_limit = funding_limit - p.previous_funding
        if p.requested_amount > remaining_limit:
            raise ValueError(
                f'If proposal "{p.name}" were funded it would receive more '
                'than the per-project funding limit this year.'
            )
        # Decrease weight for projects that have already had previous funding.
        weights[i] = remaining_limit / p.requested_amount
        assert weights[i] >= 1  # this should be redundant with the validation check above.

    fund_ordering = rng.choice(proposals,
                               p=weights / np.sum(weights),
                               size=n_proposals,
                               replace=False)

    # Check / filter proposals to those within budget deficit limit.
    funded = []
    budget_remaining = budget
    for proposal in fund_ordering:
        budget_remaining -= proposal.requested_amount
        deficit = -budget_remaining if budget_remaining < 0 else 0
        if deficit > proposal.requested_amount / 2:
            # Deficit is too great, add back project budget, and find
            # another project to try.
            budget_remaining += proposal.requested_amount
            continue
        # Confirm selection.
        funded.append(proposal)
        if budget_remaining <= 0:
            break

    # Final check for spending.
    assert budget_remaining >= -remaining_limit / 2

    # Sort funded proposals in proposal order.
    funded = sorted(funded, key=lambda v : proposals.index(v))

    print("Inputs:")
    print(f"Budget: ${budget}")
    print(f"Per-project funding limit: ${funding_limit}")
    print("Proposals in the drawing:")
    for p in proposals:
        print(
            f'"{p.name}" requests ${p.requested_amount} and is proposed by a '
            f'project that has previously received ${p.previous_funding} this year.'
        )

    print()
    print("Random Outputs:")
    print(
        f"Allocated: ${round(budget - budget_remaining, 2)} (${round(abs(budget_remaining), 2)} {'over' if budget_remaining < 0 else 'under'} budget)"
    )
    print(f"{len(funded)} proposals funded out of {n_proposals} total proposals in the drawing")
    print()
    print("Funded the following projects")

    for p in funded:
        print(f'Fund "{p.name}" for ${p.requested_amount} bringing its '
              f'project\'s annual total to ${p.requested_amount + p.previous_funding}.')

    return [f.name for f in funded]
