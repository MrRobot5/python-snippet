import os

for filename in os.listdir('/tmp'):
    # print filename
    if not filename.endswith('json'):
        # os.remove('/tmp/' + filename)
        if not os.path.isdir('/tmp/' + filename):
            print(filename)

