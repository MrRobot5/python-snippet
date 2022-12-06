import time
import requests
from requests.adapters import HTTPAdapter


# https://www.cnblogs.com/gl1573/p/10129382.html

session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))

print(time.strftime('%Y-%m-%d %H:%M:%S'))
try:
    r = session.get('https://www.cnblogs.com/gl1573/p/10129382.html', timeout=5)
    print(r.text)
except requests.exceptions.RequestException as e:
    print(e)

print(time.strftime('%Y-%m-%d %H:%M:%S'))
