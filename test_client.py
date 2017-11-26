import requests

r = requests.get('http://127.0.0.1:5000/?git_url=https://github.com/rubik/argon.git&max_workers=4')
print r
print r.content