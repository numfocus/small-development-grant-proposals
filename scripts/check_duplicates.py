from argparse import ArgumentParser
import os
import shlex
import subprocess
from datetime import date
import json

from sdg_utils import get_all_issues, parse_issue


def find_duplicates(issues):

    projects = [issue['project_name'] for issue in issues]
    uniq_projects = set(projects)

    if len(projects) != uniq_projects:
        for uproj in uniq_projects:
            if projects.count(uproj) > 1:
                # add a label to the issues
                for issue in issues:
                    if issue['project_name'] == uproj:
                        command = f'gh issue edit {issue["issue_number"]} --add-label "duplicate"'
                        output = subprocess.run(shlex.split(command), capture_output=True)
                        if output.returncode != 0:
                            raise ValueError(output.stderr)


def main():
    parser = ArgumentParser(description="Check for SDG proposals from same project")
    parser.add_argument('round', type=int, help='round number to be extracted')
    arguments = parser.parse_args()

    issues = get_all_issues()
    sdg_issues = []
    for issue in issues:
        result = parse_issue(issue)
        if result:
            sdg_issues.append(result)
    sdg_issues_round = [sdg for sdg in sdg_issues if sdg['round_number'] == arguments.round and
                      sdg['year'] == date.today().year]
    print(json.dumps(sdg_issues_round, indent=2))
    find_duplicates(sdg_issues_round)

if __name__ == "__main__":
    main()


