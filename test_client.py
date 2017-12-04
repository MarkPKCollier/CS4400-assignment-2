import requests

# r = requests.get('http://127.0.0.1:5000/?git_url=https://github.com/rubik/argon.git&max_workers=4&data_parallelisation_strategy=commits&work_distribution_strategy=work_stealing')
# r = requests.get('http://127.0.0.1:5000/?git_url=https://github.com/rubik/argon.git&max_workers=4&data_parallelisation_strategy=commits&work_distribution_strategy=work_pushing')

# r = requests.get('http://127.0.0.1:5000/?git_url=https://github.com/rubik/argon.git&max_workers=4&data_parallelisation_strategy=commits&work_distribution_strategy=work_stealing')
r = requests.get('http://127.0.0.1:5000/?git_url=https://github.com/MarkPKCollier/CS4400-assignment-2.git&max_workers=4&data_parallelisation_strategy=commits&work_distribution_strategy=work_pushing')

print r.content