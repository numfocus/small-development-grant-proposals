import pytest

from extract_sdg_issues import combine_projects_rounds


def test_combine():
    issues_round = [
        {
            "awarded": False,
            "year": 2025,
            "round_number": 3,
            "funded_amount": 0,
            "project_name": "A",
        },
    ]
    issues_prev = [
        {
            "awarded": False,
            "year": 2025,
            "round_number": 2,
            "funded_amount": 3000,
            "project_name": "A",
        },
        {
            "awarded": False,
            "year": 2025,
            "round_number": 1,
            "funded_amount": 500,
            "project_name": "A",
        },
    ]
    combine_projects_rounds(issues_round, issues_prev)

    assert issues_round[0]["funded_amount"] == 3500


# @pytest.mark.parametrize()
# def test_parse_issue():
