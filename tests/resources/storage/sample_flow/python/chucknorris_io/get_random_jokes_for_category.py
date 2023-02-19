# type: ignore

"""
This script contains sample code for calling an http spec. file
and use the results
"""

import subprocess
import json
import random

# set spec. for list of all categories
joke_categories_f = (
    "tests/resources/storage/sample_flow/python/chucknorris_io/joke_categories_rq.chk"
)

# execute command and get response
result = subprocess.check_output(
    ["chk", "http", "--result", "--no-format", joke_categories_f]
)

# convert response to json
response = json.loads(result.rstrip())

# get response body
categories = response[0]["body"]

# get one random category
a_category = random.choice(categories)

# --- call another api using `a_category`

# set random joke by for given category spec.
joke_for_category_f = (
    "tests/resources/storage/sample_flow/python/chucknorris_io/joke_for_category_rq.chk"
)

# execute command and get response
result = subprocess.check_output(
    [
        "chk",
        "http",
        "--result",
        "--no-format",
        joke_for_category_f,
        f"category={ a_category }",
    ]
)

# convert response to json
response = json.loads(result.rstrip())

# get response body
joke = response[0]["body"]

# display
print(
    "\n",
    f":: This joke {joke['id']} was created on {joke['created_at']} ::\n",
    f":: Permalink {joke['url']} ::\n",
    f"{joke['value']}\n",
    "\n",
)
