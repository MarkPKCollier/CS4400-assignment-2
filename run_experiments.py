import matplotlib
matplotlib.use('macosx')
import matplotlib.pyplot as plt
import numpy as np
import requests

SERVER_ADDR = 'http://127.0.0.1:8080'
# SERVER_ADDR = 'http://localhost:3000'
REPO = 'https://github.com/rubik/argon.git'
# REPO = 'https://github.com/tensorflow/haskell.git'
# REPO = 'https://github.com/MarkPKCollier/CS4400-assignment-2.git'
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

print times

plt.plot(workers, times[('files', 'work_stealing')], 'r-', label='files | work stealing')
plt.plot(workers, times[('files', 'work_pushing')], 'g-', label='files | work pushing')
plt.plot(workers, times[('commits', 'work_stealing')], 'b-', label='commits | work stealing')
plt.plot(workers, times[('commits', 'work_pushing')], 'm-', label='commits | work pushing')
plt.axis([0, MAX_WORKERS + 1, 0, 1.1 * max_time])
plt.xlabel('Num workers')
plt.ylabel('Time (seconds)')
plt.legend(loc=1, title='Data parallelisation | Work distribution')
plt.title('Argon repo execution times - Macbook Air - Num cores = 4')
# plt.show()
plt.savefig('images/argon_mac.png')

plt.clf()
plt.cla()
plt.close()

plt.plot(workers, map(lambda t: times[('files', 'work_stealing')][0] / t, times[('files', 'work_stealing')]), 'r-', label='files | work stealing')
plt.plot(workers, map(lambda t: times[('files', 'work_pushing')][0] / t, times[('files', 'work_pushing')]), 'g-', label='files | work pushing')
plt.plot(workers, map(lambda t: times[('commits', 'work_stealing')][0] / t, times[('commits', 'work_stealing')]), 'b-', label='commits | work stealing')
plt.plot(workers, map(lambda t: times[('commits', 'work_pushing')][0] / t, times[('commits', 'work_pushing')]), 'm-', label='commits | work pushing')
plt.axis([0, MAX_WORKERS + 1, 0, MAX_WORKERS])
plt.xlabel('Num workers')
plt.ylabel('Parallel Speedup')
plt.legend(loc=1, title='Data parallelisation | Work distribution')
plt.title('Argon repo parallel speedup - Macbook Air - Num cores = 4')
# plt.show()
plt.savefig('images/argon_mac_speedup.png')

