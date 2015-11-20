import sys
import json


for line  in sys.stdin:
    try:
        jp = json.loads(line)
    except:
        continue
    print jp["url"].encode("gbk")