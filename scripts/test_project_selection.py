from collections import Counter

import numpy as np

import pytest

from project_selection import select_proposals_to_fund


@pytest.mark.parametrize(
    "proposals, errmessage",
    [
        (
            [("A", 3, 1)],
            r'If proposal "A" were funded it would receive more than '
            'the per-project funding limit this year.',
        ),
        (
            [("A", 2, 1)],
            r'If proposal "A" were funded it would receive more than '
            'the per-project funding limit this year.',
        ),
        ([("A", 0.5, 1), ("A", 0.5, 1)], r"Proposal names are not unique"),
    ],
)
def test_select_proposals_wrong_input(proposals, errmessage):
    budget = 5
    funding_limit = 2
    with pytest.raises(ValueError, match=errmessage):
        select_proposals_to_fund(budget, funding_limit, proposals, seed=2025)


def test_malformed():
    with pytest.raises(TypeError):
        select_proposals_to_fund(5, 2, [("A", 2, 0, 3)])
    with pytest.raises(TypeError):
        select_proposals_to_fund(5, 2, [("A", 2)])


def test_select_proposals_all_funds(capfd):
    budget = 5
    funding_limit = 2
    proposals = [("A", 2, 0), ("B", 1, 0), ("C", 1, 0), ("D", 0.5, 0), ("E", 0.5, 0)]

    # Enough budget for all proposals.
    expected_result = {"A", "B", "C", "D", "E"}
    expected_captured = (
        "Inputs:\n"
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
        'Fund "A" for $2 bringing its project\'s annual total to $2.\n'
        'Fund "B" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "C" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "D" for $0.5 bringing its project\'s annual total to $0.5.\n'
        'Fund "E" for $0.5 bringing its project\'s annual total to $0.5.\n'
    )
    result = select_proposals_to_fund(budget,
                                      funding_limit,
                                      proposals,
                                      seed=2025)
    captured = capfd.readouterr()

    assert set(result) == expected_result
    assert captured.out == expected_captured


def check_proportions(proposals, budget, limit, rng=None):
    # Check proportions (roughly) as expected.
    rng = np.random.default_rng(rng)
    results = []
    n_iters = 1000
    for i in range(n_iters):
        results += select_proposals_to_fund(budget, limit, proposals, seed=rng)
    # Proportion of time each proposal was funded.
    prop_funded = {n: c / n_iters for n, c in Counter(results).items()}
    # Replicate weight algorithm.
    weights = {n: (limit - previous) / ask for n, ask, previous in proposals}
    # Assert that higher weights give higher proportions.
    for n, w in weights.items():
        for test_n, test_prop in prop_funded.items():
            if w > weights[test_n]:
                assert prop_funded[n] > test_prop


def test_select_proposals_more_than_funds(capfd):
    budget = 5
    funding_limit = 2
    # Weights inverse of requested funds.
    proposals = [
        ("A", 2, 0),
        ("B", 1, 0),
        ("C", 1, 0),
        ("D", 0.5, 0),
        ("E", 1.5, 0),
        ("F", 0.25, 0),
        ("G", 1.9, 0),
        ("H", 0.7, 0),
    ]

    check_proportions(proposals, budget, funding_limit, 2025)
    # Reset output.
    capfd.readouterr()

    expected_result = {'B', 'C', 'D', 'F', 'G', 'H'}
    expected_captured = (
        "Inputs:\n"
        "Budget: $5\n"
        "Per-project funding limit: $2\n"
        "Proposals in the drawing:\n"
        '"A" requests $2 and is proposed by a project that has previously received $0 this year.\n'
        '"B" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"C" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"D" requests $0.5 and is proposed by a project that has previously received $0 this year.\n'
        '"E" requests $1.5 and is proposed by a project that has previously received $0 this year.\n'
        '"F" requests $0.25 and is proposed by a project that has previously received $0 this year.\n'
        '"G" requests $1.9 and is proposed by a project that has previously received $0 this year.\n'
        '"H" requests $0.7 and is proposed by a project that has previously received $0 this year.\n'
        "\n"
        "Random Outputs:\n"
        'Allocated: $5.35 ($0.35 over budget)\n'
        '6 proposals funded out of 8 total proposals in the drawing\n\n'
        'Funded the following projects\n'
        'Fund "B" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "C" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "D" for $0.5 bringing its project\'s annual total to $0.5.\n'
        'Fund "F" for $0.25 bringing its project\'s annual total to $0.25.\n'
        'Fund "G" for $1.9 bringing its project\'s annual total to $1.9.\n'
        'Fund "H" for $0.7 bringing its project\'s annual total to $0.7.\n'
    )
    result = select_proposals_to_fund(budget,
                                      funding_limit,
                                      proposals,
                                      seed=2025)
    captured = capfd.readouterr()

    assert set(result) == expected_result
    assert captured.out == expected_captured


def test_select_proposals_more_than_funds_under(capfd):
    budget = 4.1
    funding_limit = 2
    proposals = [
        ("A", 2, 0),  # *1
        ("B", 1, 0),  # *2  2-0/1
        ("C", 1, 0),  # *2
        ("D", 0.5, 0),  # *4
        ("E", 1.5, 0),  # 1.3
        ("F", 0.25, 0),  # *8
        ("G", 1.9, 0),  # 1.052
        ("H", 0.7, 0),  # *2.85
    ]

    check_proportions(proposals, budget, funding_limit, rng=2025)
    # Reset output.
    capfd.readouterr()

    expected_result = {'C', 'D', 'E', 'F', 'H'}
    expected_captured = (
        "Inputs:\n"
        "Budget: $4.1\n"
        "Per-project funding limit: $2\n"
        "Proposals in the drawing:\n"
        '"A" requests $2 and is proposed by a project that has previously received $0 this year.\n'
        '"B" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"C" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"D" requests $0.5 and is proposed by a project that has previously received $0 this year.\n'
        '"E" requests $1.5 and is proposed by a project that has previously received $0 this year.\n'
        '"F" requests $0.25 and is proposed by a project that has previously received $0 this year.\n'
        '"G" requests $1.9 and is proposed by a project that has previously received $0 this year.\n'
        '"H" requests $0.7 and is proposed by a project that has previously received $0 this year.\n'
        "\n"
        "Random Outputs:\n"
        'Allocated: $3.95 ($0.15 under budget)\n'
        '5 proposals funded out of 8 total proposals in the drawing\n\n'
        'Funded the following projects\n'
        'Fund "C" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "D" for $0.5 bringing its project\'s annual total to $0.5.\n'
        'Fund "E" for $1.5 bringing its project\'s annual total to $1.5.\n'
        'Fund "F" for $0.25 bringing its project\'s annual total to $0.25.\n'
        'Fund "H" for $0.7 bringing its project\'s annual total to $0.7.\n'
    )
    result = select_proposals_to_fund(budget,
                                      funding_limit,
                                      proposals,
                                      seed=2026)
    captured = capfd.readouterr()

    assert set(result) == expected_result
    assert captured.out == expected_captured


def test_select_proposals_more_than_funds_eqweight_zero(capfd):
    budget = 6
    funding_limit = 2
    proposals = [
        ("A", 1, 0),
        ("B", 1, 0),
        ("C", 1, 0),
        ("D", 1, 0),
        ("E", 1, 0),
        ("F", 1, 0),
        ("G", 1, 0),
        ("H", 1, 0),
    ]

    check_proportions(proposals, budget, funding_limit, rng=2025)
    # Reset output.
    capfd.readouterr()

    expected_result = {'A', 'C', 'D', 'F', 'G', 'H'}
    expected_captured = (
        "Inputs:\n"
        "Budget: $6\n"
        "Per-project funding limit: $2\n"
        "Proposals in the drawing:\n"
        '"A" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"B" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"C" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"D" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"E" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"F" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"G" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"H" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        "\n"
        "Random Outputs:\n"
        "Allocated: $6 ($0 under budget)\n"
        "6 proposals funded out of 8 total proposals in the drawing\n\n"
        "Funded the following projects\n"
        'Fund "A" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "C" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "D" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "F" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "G" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "H" for $1 bringing its project\'s annual total to $1.\n'
    )
    result = select_proposals_to_fund(budget,
                                      funding_limit,
                                      proposals,
                                      seed=2025)
    captured = capfd.readouterr()

    assert set(result) == expected_result
    assert captured.out == expected_captured


def test_select_proposals_more_than_funds_eqweight_under(capfd):
    budget = 5.4
    funding_limit = 2
    proposals = [
        ("A", 1, 0),
        ("B", 1, 0),
        ("C", 1, 0),
        ("D", 1, 0),
        ("E", 1, 0),
        ("F", 1, 0),
        ("G", 1, 0),
        ("H", 1, 0),
    ]

    check_proportions(proposals, budget, funding_limit, rng=2025)
    # Reset output.
    capfd.readouterr()

    expected_result = {'A', 'C', 'D', 'G', 'H'}
    expected_captured = (
        "Inputs:\n"
        "Budget: $5.4\n"
        "Per-project funding limit: $2\n"
        "Proposals in the drawing:\n"
        '"A" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"B" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"C" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"D" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"E" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"F" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"G" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"H" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        "\n"
        "Random Outputs:\n"
        "Allocated: $5.0 ($0.4 under budget)\n"
        "5 proposals funded out of 8 total proposals in the drawing\n\n"
        "Funded the following projects\n"
        'Fund "A" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "C" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "D" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "G" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "H" for $1 bringing its project\'s annual total to $1.\n'
    )
    result = select_proposals_to_fund(budget,
                                      funding_limit,
                                      proposals,
                                      seed=2025)
    captured = capfd.readouterr()

    assert set(result) == expected_result
    assert captured.out == expected_captured


def test_select_proposals_more_than_funds_eqweight_over(capfd):
    budget = 6.6
    funding_limit = 2
    proposals = [
        ("A", 1, 0),
        ("B", 1, 0),
        ("C", 1, 0),
        ("D", 1, 0),
        ("E", 1, 0),
        ("F", 1, 0),
        ("G", 1, 0),
        ("H", 1, 0),
    ]

    expected_result = {"A", "B", "C", "D", "F", "H", "G"}
    expected_captured = (
        "Inputs:\n"
        "Budget: $6.6\n"
        "Per-project funding limit: $2\n"
        "Proposals in the drawing:\n"
        '"A" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"B" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"C" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"D" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"E" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"F" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"G" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        '"H" requests $1 and is proposed by a project that has previously received $0 this year.\n'
        "\n"
        "Random Outputs:\n"
        "Allocated: $7.0 ($0.4 over budget)\n"
        "7 proposals funded out of 8 total proposals in the drawing\n\n"
        "Funded the following projects\n"
        'Fund "A" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "B" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "C" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "D" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "F" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "G" for $1 bringing its project\'s annual total to $1.\n'
        'Fund "H" for $1 bringing its project\'s annual total to $1.\n'
    )
    result = select_proposals_to_fund(budget,
                                      funding_limit,
                                      proposals,
                                      seed=2025)
    captured = capfd.readouterr()

    assert set(result) == expected_result
    assert captured.out == expected_captured
