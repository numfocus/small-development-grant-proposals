import numpy as np

from project_selection import select_proposals_to_fund


def test_select_proposals_all_funds(capfd):
    np.random.seed(2025)
    budget = 5
    funding_limit = 2
    proposals = [
        ('A', 2, 0),
        ('B', 1, 0),
        ('C', 1, 0),
        ('D', 0.5, 0),
        ('E', 0.5, 0)
    ]

    expected_result = {'A', 'B', 'C', 'D', 'E'}
    expected_captured = ("Inputs:\n"
                         "Budget: $5\n"
                         "Per-project funding limit: $2\n"
                         "Proposals in the drawing:\n"
                         '"A" requests $2 and is proposed by a project that has previously received $0 this year.\n'
                         '"B" requests $1 and is proposed by a project that has previously received $0 this year.\n'
                         '"C" requests $1 and is proposed by a project that has previously received $0 this year.\n'
                         '"D" requests $0.5 and is proposed by a project that has previously received $0 this year.\n'
                         '"E" requests $0.5 and is proposed by a project that has previously received $0 this year.\n'
                         "\n"
                         "Random Outputs:\n"
                         "Allocated: $5.0 ($0.0 under budget)\n"
                         "5 proposals funded out of 5 total proposals in the drawing\n\n"
                         "Funded the following projects\n"
                         "Fund \"B\" for $1 bringing its project's annual total to $1.\n"
                         "Fund \"E\" for $0.5 bringing its project's annual total to $0.5.\n"
                         "Fund \"D\" for $0.5 bringing its project's annual total to $0.5.\n"
                         "Fund \"C\" for $1 bringing its project's annual total to $1.\n"
                         "Fund \"A\" for $2 bringing its project's annual total to $2.\n"
                         )
    result = select_proposals_to_fund(budget, funding_limit, proposals)
    captured = capfd.readouterr()


    assert set(result) == expected_result
    assert captured.out == expected_captured
