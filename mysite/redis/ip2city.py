import json

f = file('records.json')
rs = json.load(f)

for item in rs:
    name = item['bookingUserErp']
    if name == 'yangpan23':
        print item
