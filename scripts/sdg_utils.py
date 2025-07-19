import os
import re
import json
import requests
from datetime import date
import shlex
import subprocess


GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

LABEL_PATTERN = re.compile(r"(\d{4})-R(\d+)")


def get_all_issues():
    issues = []
    page = 1
    while True:
        response = requests.get(
            API_URL,
            headers=HEADERS,
            params={"state": "open", "per_page": 100, "page": page},
        )
        if response.status_code != 200:
            raise Exception(f"Failed to fetch issues: {response.status_code} - {response.text}")
        page_issues = response.json()
        if not page_issues:
            break
        issues.extend(page_issues)
        page += 1
    return issues


def parse_issue(issue):
    label_info = next(
        (
            LABEL_PATTERN.match(label["name"])
            for label in issue["labels"]
            if LABEL_PATTERN.match(label["name"])
        ),
        None,
    )
    if not label_info:
        return None

    year, round_number = label_info.groups()
    labels = [label["name"] for label in issue["labels"]]

    body = issue["body"]
    project_match = re.search(r"(?i)Project\s*[\n\r]+(.+?)(?=\n\S|$)", body, re.DOTALL)
    project_name = project_match.group(1).strip() if project_match else ""
    if url := re.search(r"\[(.*)\]\(.*\)", project_name):
        project_name = url.group(1)

    amount_match = re.search(r"(?i)Amount requested\s*[\n\r]+(.+?)(?=\n\S|$)", body, re.DOTALL)
    funded_amount = 0
    try:
        amount_requested = int(re.sub(r"[^\d]", "", amount_match.group(1)))
    except ValueError:
        amount_requested = 0
    if "funded" in [l.lower() for l in labels] and amount_match:
        funded_amount = amount_requested

    return {
        "awarded": "award" in [l.lower() for l in labels],
        "year": int(year),
        "round_number": int(round_number),
        "funded_amount": funded_amount,
        "amount_requested": amount_requested,
        "issue_number": issue["number"],
        "project_name": project_name,
        "reviewers": [],
    }


def combine_projects_rounds(issues_round, issues_prev):
    for sdg in issues_round:
        for sdg_prev in issues_prev:
            if sdg["project_name"] == sdg_prev["project_name"]:
                sdg["funded_amount"] += sdg_prev["funded_amount"]


def update_board(issues_round, round):
    GH_TOKEN = os.getenv("GH_TOKEN")

    ## Finding the project board id
    command = """
gh api graphql -f query='
  query($organization: String! $number: Int!){
    organization(login: $organization){
      projectV2(number: $number) {
        id
      }
    }
  }' -f organization=numfocus -F number=11
     """
    ## PVT_kwDOABWvJs4A4B5H
    output = subprocess.run(shlex.split(command), capture_output=True)
    if output.returncode == 0:
        project_id = json.loads(output.stdout)["data"]["organization"]["projectV2"]["id"]
    else:
        raise ValueError(output.stderr)

    ## Finding the ids for each field
    ## from https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects#finding-the-node-id-of-a-field)
    command = """
gh api graphql -f query='
  query{{
  node(id: "{project_id}") {{
    ... on ProjectV2 {{
      fields(first: 20) {{
        nodes {{
          ... on ProjectV2Field {{
            id
            name
          }}
          ... on ProjectV2IterationField {{
            id
            name
            configuration {{
              iterations {{
                startDate
                id
              }}
            }}
          }}
          ... on ProjectV2SingleSelectField {{
            id
            name
            options {{
              id
              name
            }}
          }}
        }}
      }}
    }}
  }}
}}'
    """
    # output = subprocess.run(shlex.split(command.format(project_id=project_id)), capture_output=True)
    # if output.returncode == 0:
    #     print(json.dumps(json.loads(output.stdout), indent=2))
    # else:
    #     raise ValueError(output.stderr)

    ### Querying the issue independently to the repo produces a different id.
    #     command = """
    # gh api graphql -f query='query FindIssueID {{
    #   repository(owner:"dpshelio", name:"sample-gh") {{
    #     issue(number:3) {{
    #       id
    #     }}
    #   }}
    # }}'
    # """
    #     output = subprocess.run(shlex.split(command.format(project_id=project_id)), capture_output=True)
    #     if output.returncode == 0:
    #         print(json.dumps(json.loads(output.stdout), indent=2))
    #     else:
    #         raise ValueError(output.stderr)

    ### Finding the issues IDs
    command = """
gh api graphql -f query='
  query{{
    node(id: "{project_id}") {{
        ... on ProjectV2 {{
          items(first: 50) {{
            nodes{{
              id
              content{{
                ...on Issue {{
                  title
                  number
                  labels(first: 10) {{
                   nodes {{
                      name
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}'
"""
    output = subprocess.run(
        shlex.split(
            command.format(
                project_id=project_id,
            )
        ),
        capture_output=True,
    )
    if output.returncode == 0:
        ids = json.loads(output.stdout)["data"]["node"]["items"]["nodes"]
        # simplify the structure received from graphql
        for card in ids:
            labels = [x["name"] for x in card["content"]["labels"]["nodes"]]
            card["content"]["labels"] = labels
            card |= card["content"]
            del card["content"]
        print(json.dumps(ids, indent=2))
    else:
        raise ValueError(output.stderr)

    ### Updating an issue
    command = """
gh api graphql -f query='
  mutation {{
    updateProjectV2ItemFieldValue(
      input: {{
        projectId: "{project_id}"
        itemId: "{issue_n}"
        fieldId: "{fieldId}"
        value: {{
    {type}: {value}
        }}
      }}
    ) {{
      projectV2Item {{
        id
      }}
    }}
  }}'
"""

    for issue in issues_round:
        issue_id = next(filter(lambda x: x["number"] == issue["issue_number"], ids))["id"]
        fields = [
            {  # $project
                "type": "text",
                "fieldId": "PVTF_lADOABWvJs4A4B5HzgtERB4",
                "value": issue["project_name"],
            },
            {  # $amount
                "type": "number",
                "fieldId": "PVTF_lADOABWvJs4A4B5HzgtEQ_c",
                "value": issue["amount_requested"],
            },
            {  # $previously_funded
                "type": "number",
                "fieldId": "PVTF_lADOABWvJs4A4B5Hzgu0-dU",
                "value": issue["funded_amount"],
            },
            {  # $SDG_reviewers
                "type": "text",
                "fieldId": "PVTF_lADOABWvJs4A4B5HzgtEQ-o",
                "value": f'"{",".join(issue["reviewers"])}"',
            },
        ]
        for field in fields:
            output = subprocess.run(
                shlex.split(command.format(project_id=project_id, issue_n=issue_id, **field)),
                capture_output=True,
            )
            if output.returncode != 0:
                raise ValueError(output.stderr)

        ## SDG reviewers ($SDG_reviewers)
        output = subprocess.run(
            shlex.split(
                command.format(
                    project_id=project_id,
                    issue_n=issue_id,
                )
            ),
            capture_output=True,
        )
        if output.returncode != 0:
            raise ValueError(output.stderr)
