# The generated python files in the folder remotivelabs/broker/generated/sync contain an incorrect import statement
# For example the file remotivelabs/broker/generated/sync/traffic_api_pb2.py contains
#   import common_pb2 as common__pb2
#
# However, it should contain
#   from . import common_pb2 as common__pb2
#
# This script goes through all the python files in the folder and does the replacement based on the regex pattern
# `regex_string` defined below.

import glob
import re

files = glob.glob("remotivelabs/broker/generated/sync/*.py")
files = files + glob.glob("remotivelabs/broker/generated/sync/*.pyi")

REGEX_STRING = r"^import \w+_pb2"
SUBSTITUTE_STRING = "from . \\g<0>"

# You can manually specify the number of replacements by changing the 4th argument
for file in files:
    with open(file, encoding="utf-8") as stream:
        contents = stream.read()
        result = re.sub(REGEX_STRING, SUBSTITUTE_STRING, contents, count=0, flags=re.MULTILINE)

    with open(file, encoding="utf-8", mode="wt") as stream:
        stream.write(result)
