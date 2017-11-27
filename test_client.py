import requests

# r = requests.get('http://127.0.0.1:5000/?git_url=https://github.com/rubik/argon.git&max_workers=4&data_parallelisation_strategy=commits&work_distribution_strategy=work_stealing')
r = requests.get('http://127.0.0.1:5000/?git_url=https://github.com/rubik/argon.git&max_workers=4&data_parallelisation_strategy=commits&work_distribution_strategy=work_pushing')

print r.content