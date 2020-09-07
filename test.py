import json
with open('test.json') as f:
    y = json.load(f)

print(y['data'][0][0]['MoTa'])