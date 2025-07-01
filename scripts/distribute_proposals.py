import json
import random

import yaml

def extract_pwc(reviewers):
    return list(set(sum(filter(lambda x: x, list(reviewers.values())), [])))

def produce_conflicts_dict(reviewers, projects_with_confict):
    return {proj: list(filter(lambda x: proj in reviewers[x],  {k:v for k,v in reviewers.items() if v})) for proj in projects_with_confict}

def distribute_proposals(proposals, seed, reviews_per_proposal):

    with open("CoI.yaml", 'r') as f:
        reviewers_coi = yaml.safe_load(f.read())
        
    random.seed(seed)
    reviews_per_proposal = reviews_per_proposal
    reviewers = list(reviewers_coi.keys())
    projects_with_confict = extract_pwc(reviewers_coi)
    conflicts = produce_conflicts_dict(reviewers_coi, projects_with_confict)

    (proposals_per_reviewer := 1 + (len(proposals) * reviews_per_proposal // len(reviewers)))

    def who_is_reviewing(proposal):
        # Takes assignments by closure from globals.
        return [r for r in reviewers if proposal in assignments[r]]

    def has_conflict(reviewer, proposal):
        return proposal in conflicts and reviewer in conflicts[proposal]


    # Sometimes this will fail because of a pathological random order of review
    # assignments. If it's run often enough, it should eventually succeed.

    assignments = {r: [] for r in reviewers}
    reviewers_left = reviewers.copy()

    for proposal in proposals:
        # Reset the working list
        working_reviewers = reviewers_left.copy()

        # Remove reviewers with conflicts on the current proposal.
        # Also an attempt here at avoiding reviewers being under-assigned,
        #  but this became brittle when the CoI handling was implemented.
        for reviewer in working_reviewers[:]:
            if (
                has_conflict(reviewer, proposal)
                or
                (  # This really might be more trouble than it's worth.
                    (
                        # If a reviewer has at least two more assignments than the
                        # other reviwer(s) with the least number of assignments.
                        len(assignments[reviewer]) - min(len(assignments[r]) for r in reviewers) > 1
                    )
                    # and
                    # (
                    #     # If we're getting low on non-conflicted reviewers,
                    #     # don't worry about skewed review allocations.
                    #     len(reviewers_left) - len(working_reviewers) >= (REVIEWS_PER_PROPOSAL - 1)
                    # )
                )
            ):
                working_reviewers.remove(reviewer)

        for _ in range(reviews_per_proposal):
            if working_reviewers:
                reviewer = random.choice(working_reviewers)
                assignments[reviewer].append(proposal)
                working_reviewers.remove(reviewer)
            else:
                print(f"proposal: {proposal} hasn't got reviewers")

            # Could be ==, but playing it safe
            if len(assignments[reviewer]) >= proposals_per_reviewer:
                reviewers_left.remove(reviewer)

    # How many proposals was each reviewer assigned?
    # Sometimes 1-2 reviewers are under-assigned. Can re-run
    # until a good split is achieved, or rebalance manually,
    # or leave as-is.
    print([f'{r}: {len(assignments[r])}' for r in reviewers])

    # Who has been assigned to each proposal?
    for p in proposals:
        print(f"{p}: {who_is_reviewing(p)}")


    # Which proposals was each person assigned?
    for r in assignments:
        print(r)
        print("  " + "\n  ".join(assignments[r]))

    # Are there any conflicts? A 'False' value here means no conflicts.
    for p, rs in conflicts.items():
        print(f"{p}: {any(p in assignments[r] for r in rs)}")

    payload = {
        "reviewers": reviewers,
        "proposals": proposals,
        "conflicts": conflicts,
        "assignments": assignments,
    }
    # base64.b64encode(json.dumps(payload).encode("utf-8"))
    print(json.dumps(payload, indent=2))
    return assignments

