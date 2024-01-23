# The generated python files in the folder remotivelabs/broker/generated/sync contain an incorrect import statement
# For example the file remotivelabs/broker/generated/sync/traffic_api_pb2.py contains
#   import common_pb2 as common__pb2
#
# However, it should contain
#   from . import common_pb2 as common__pb2
#
# This script goes through all the python files in the folder and does the replacement based on the regex pattern
# `regex_string` defined below.

import re
import glob

files = glob.glob("remotivelabs/broker/generated/sync/*.py")
files = files + glob.glob("remotivelabs/broker/generated/sync/*.pyi")

regex_string = r"^import \w+_pb2"
substitute_string = "from . \\g<0>"

# You can manually specify the number of replacements by changing the 4th argument
for file in files:
    stream = open(file, "rt")
    contents = stream.read()
    result = re.sub(regex_string, substitute_string, contents, 0, re.MULTILINE)
    stream.close()
    stream = open(file, "wt")
    stream.write(result)
    stream.close()
