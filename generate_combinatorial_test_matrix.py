#!/usr/bin/env python3

"""Generate a matrix of all possible cases which the tool might encounter."""

import csv
import itertools

workspace_bookmark_magic_file = ("none", "present")
workspace_bookmarks = ("none", "present")
target_location = ("none", "invalid", "inside current .repo",
                   "outside current .repo")
optional_target_location_postfix = ("none", "present")
current_location = ("outside workspace", "inside .repo", "outside .repo")
optional_prefix_path = ("none", "present")
environment = {
    "workspace_bookmark_magic_file": workspace_bookmark_magic_file,
    "workspace_bookmarks": workspace_bookmarks,
    "target_location": target_location,
    "optional_target_location_postfix": optional_target_location_postfix,
    "current_location": current_location,
    "optional_prefix_path": optional_prefix_path,
}

with open("possible_environments.csv", "w", encoding="UTF-8") as f:
    csv_writer = csv.writer(f)
    flattened_env = ((env,) + environment[env] for env in environment)
    csv_writer.writerows(itertools.zip_longest(*flattened_env, fillvalue=""))

with open("combinatorial_test_matrix.csv", "w", encoding="UTF-8") as f:
    combinatorial_test_matrix = itertools.product(*environment.values())

    csv_writer = csv.writer(f)
    csv_writer.writerow(environment.keys())
    csv_writer.writerows(combinatorial_test_matrix)
