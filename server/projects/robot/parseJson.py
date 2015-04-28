import sys
import json


for line  in sys.stdin:
    jp = json.loads(line)
    print jp["url"]