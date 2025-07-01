from argparse import ArgumentParser
import os
import re
import json
import requests
from datetime import date
import shlex
import subprocess

from distribute_proposals import distribute_proposals
from sdg_utils import get_all_issues, parse_issue, combine_projects_rounds, update_board



def assign_reviewers(issues, round, reviewers):

    seed = int(f"{date.today().year}{round}")
    assignments = distribute_proposals([issue['project_name'] for issue in issues], seed, reviewers)
    for issue in issues:
        for person, projects in assignments.items():
            if issue['project_name'] in projects:
                issue['reviewers'].append(person)


def main():
    parser = ArgumentParser(description="Runs script to extract SDG issues")
    parser.add_argument('round', type=int, help='round number to be extracted')
    parser.add_argument('--reviewers', type=int, default=3, help='number of reviewers per proposal')
    arguments = parser.parse_args()

    issues = get_all_issues()
    sdg_issues = []
    for issue in issues:
        result = parse_issue(issue)
        if result:
            sdg_issues.append(result)
    print(json.dumps(sdg_issues, indent=2))

    sdg_issues_round = [sdg for sdg in sdg_issues if sdg['round_number'] == arguments.round and
                      sdg['year'] == date.today().year and
                      not sdg['awarded']] 
    #Filter only this year and combine to calculate all they've been funded ask
    sdg_prev_rounds = [sdg_p for sdg_p in sdg_issues if sdg_p['round_number'] != arguments.round and sdg_p['year'] == date.today().year]
    print("only this round")
    combine_projects_rounds(sdg_issues_round, sdg_prev_rounds)
    assign_reviewers(sdg_issues_round, arguments.round, arguments.reviewers)
    print(json.dumps(sdg_issues_round, indent=2))
    update_board(sdg_issues_round, arguments.round)

if __name__ == "__main__":
    main()

