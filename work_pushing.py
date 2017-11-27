import argparse
from mpi4py import MPI
from subprocess import check_output
import utils
import os

parser = argparse.ArgumentParser()
parser.add_argument('--git_url', type=str)
parser.add_argument('--data_parallelisation_strategy', type=str)
args = parser.parse_args()
git_url = args.git_url
data_parallelisation_strategy = args.data_parallelisation_strategy

comm = MPI.COMM_WORLD
num_proc = comm.Get_size()
rank = comm.Get_rank()

repo_dest = os.path.abspath('./repos/' + git_url.split('/')[-1].replace('.git', '') + str(rank))
check_output('git clone {0} {1}'.format(git_url, repo_dest), shell=True)

if rank == 0: # manager
    res = {}
    commits = utils.get_all_files_in_repo(repo_dest, '.hs')
    if data_parallelisation_strategy == 'files':
        work_packets = [(commit_id, [f]) for commit_id, files in commits.iteritems() for f in files]
        num_files = num_work_packets = len(work_packets)
    else:
        work_packets = commits.items()
        num_work_packets = len(work_packets)
        num_files = sum(map(len, commits.values()))

    worker_packets = [[] for _ in range(num_proc-1)]
    for i, packet in enumerate(work_packets):
        worker_packets[i % (num_proc-1)].append(packet)

    for i, packets in enumerate(worker_packets):
        comm.send(packets, dest=i+1, tag=0)

    for i in range(1, num_proc):
        work_res = comm.recv(source=i, tag=1)
        res.update(work_res)

    print sum(res.values())

else: # worker
    packets = comm.recv(source=0, tag=0)
    res = {}
    for commit_id, file_names in packets:
        partial_res = utils.compute_complexity(repo_dest, commit_id, file_names)
        res.update(partial_res)

    comm.send(res, dest=0, tag=1)

check_output(['rm -rf {0}'.format(repo_dest)], shell=True)

