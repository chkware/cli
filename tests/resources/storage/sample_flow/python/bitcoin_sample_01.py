# type: ignore

"""
This script contains sample code for calling an http spec. file
and use the results
"""

import subprocess
import json

file = "tests/resources/storage/sample_flow/python/bitcoin-usd.chk"
result = subprocess.check_output(["chk", "http", "--result", "--no-format", file])

output = json.loads(result.rstrip())
btc = output[0]['coin']
print(f"BTC price now ${ btc['price'] }")