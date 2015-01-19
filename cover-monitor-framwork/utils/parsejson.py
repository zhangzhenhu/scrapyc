import json
import sys

for line in sys.stdin:
    item = json.loads(line.strip())
    print item["url"]
    #print item["fromurl"]