from argparse import ArgumentParser
import os
import shlex
import subprocess
from datetime import date
import json

from sdg_utils import get_all_issues, parse_issue, combine_projects_rounds
from project_selection import select_proposals_to_fund

def allocate_funds(issues, budget, funding_limit, seed=None):

    proposals = [(issue['project_name'], issue['amount_requested'], issue['funded_amount']) for issue in issues]
    funded = select_proposals_to_fund(budget, funding_limit, proposals, seed=seed)

    for issue in issues:
        if issue['project_name'] in funded:
            command = f'gh issue edit {issue["issue_number"]} --add-label "funded"'
            output = subprocess.run(shlex.split(command), capture_output=True)
            if output.returncode != 0:
                raise ValueError(output.stderr)

def main():
    parser = ArgumentParser(description="Check for SDG proposals from same project")
    parser.add_argument('round', type=int, help='round number to be extracted')
    parser.add_argument('--budget', type=int, help='total number of budget allowed')
    parser.add_argument('--funding_limit', type=int, default='10000', help='funding limit per year')
    arguments = parser.parse_args()

    issues = get_all_issues()
    sdg_issues = []
    for issue in issues:
        result = parse_issue(issue)
        if result:
            sdg_issues.append(result)
    sdg_issues_round = [sdg for sdg in sdg_issues if sdg['round_number'] == arguments.round and
                      sdg['year'] == date.today().year and
                      not sdg['awarded']] 
    #Filter only this year and combine to calculate all they've been funded ask
    sdg_prev_rounds = [sdg_p for sdg_p in sdg_issues if sdg_p['round_number'] != arguments.round and sdg_p['year'] == date.today().year]
    print("only this round")
    combine_projects_rounds(sdg_issues_round, sdg_prev_rounds)
    seed = int(f"{date.today():%d%w%j}{arguments.round}")
    allocate_funds(sdg_issues_round, arguments.budget, arguments.funding_limit, seed=seed)

if __name__ == "__main__":
    main()


