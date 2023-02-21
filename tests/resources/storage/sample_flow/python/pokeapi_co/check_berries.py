# type: ignore

"""
This script contains sample code for calling an testcase spec. file
and use the results
"""

import subprocess
import json
import time

from pathlib import Path

# import var_dump


# set specification file path
berries_f = f"{str(Path(__file__).parent.resolve())}/Berries.chk"
berry_f = f"{str(Path(__file__).parent.resolve())}/Berry.chk"


# execute command and get response
result = subprocess.check_output(
    ["chk", "testcase", "--result", "--no-format", berries_f]
)

# convert response to json
# get separate assertion results, and response
(assertion_results, response) = json.loads(result.rstrip())

# check is all assertion was successful
assert all([assertion_result["is_success"] for assertion_result in assertion_results])

# get berries from response body
berries = response["body"]["results"]

# check if a list came in
assert isinstance(berries, list)

# for all the berries
for berry_item in berries:
    # call individual berry
    result = subprocess.check_output(
        [
            "chk",
            "http",
            "--result",
            "--no-format",
            berry_f,
            f"URL={ berry_item['url'] }",
        ]
    )

    # print and wait
    print(f"Calling {berry_f} with URL={berry_item['url']}")
    time.sleep(2)

    response = json.loads(result.rstrip())
    berry = response[0]["body"]

    # print berry
    print(f"Found {berry['name']} with max_harvest={berry['max_harvest']}")
