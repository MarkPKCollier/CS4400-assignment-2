import matplotlib
matplotlib.use('macosx')
import matplotlib.pyplot as plt
import numpy as np
import requests

# SERVER_ADDR = 'http://127.0.0.1:5000'
SERVER_ADDR = 'http://localhost:8000'
# REPO = 'https://github.com/rubik/argon.git'
REPO = 'https://github.com/MarkPKCollier/CS4400-assignment-2.git'
MAX_WORKERS = 8
workers = [2 ** i for i in range(int(np.log2(MAX_WORKERS) + 1))]

times = {}

for data_parallelisation_strategy in ['files', 'commits']:
  for work_distribution_strategy in ['work_stealing', 'work_pushing']:
    times[(data_parallelisation_strategy, work_distribution_strategy)] = []
    for num_workers in workers:
        r = requests.get('{0}/?git_url={1}&max_workers={2}&data_parallelisation_strategy={3}&work_distribution_strategy={4}'.format(SERVER_ADDR, REPO, num_workers, data_parallelisation_strategy, work_distribution_strategy))
        res = r.json()

        times[(data_parallelisation_strategy, work_distribution_strategy)].append(res['time_taken'])

max_time = max(map(max, times.values()))
min_time = min(map(min, times.values()))

plt.plot(workers, times[('files', 'work_stealing')], 'r-', label='files | work stealing')
plt.plot(workers, times[('files', 'work_pushing')], 'g-', label='files | work pushing')
plt.plot(workers, times[('commits', 'work_stealing')], 'b-', label='commits | work stealing')
plt.plot(workers, times[('commits', 'work_pushing')], 'm-', label='commits | work pushing')
plt.axis([0, MAX_WORKERS + 1, 0, 1.1 * max_time])
plt.xlabel('Num workers')
plt.ylabel('Time (seconds)')
plt.legend(loc=1, title='Data parallelisation | Work distribution')
plt.title('Argon repo execution times - Macneill - Num cores = 8')
# plt.show()
plt.savefig('images/argon_macneill.png')