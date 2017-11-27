import argparse
from mpi4py import MPI
from subprocess import check_output
import utils
import os

parser = argparse.ArgumentParser()
parser.add_argument('--git_url', type=str)
parser.add_argument('--work_distribution_strategy', type=str)
args = parser.parse_args()
git_url = args.git_url
work_distribution_strategy = args.work_distribution_strategy

comm = MPI.COMM_WORLD
num_proc = comm.Get_size()
rank = comm.Get_rank()

repo_dest = os.path.abspath('./repos/' + git_url.split('/')[-1].replace('.git', '') + str(rank))
check_output('git clone {0} {1}'.format(git_url, repo_dest), shell=True)

if rank == 0: # manager
    res = {}
    commits = utils.get_all_files_in_repo(repo_dest, '.hs')
    if work_distribution_strategy == 'files':
        work_packets = [(commit_id, [f]) for commit_id, files in commits.iteritems() for f in files]
        num_files = num_work_packets = len(work_packets)
    else:
        work_packets = commits.items()
        num_work_packets = len(work_packets)
        num_files = sum(map(len, commits.values()))
    
    work_counter = 0
    while True:
        rank, work_res = comm.recv(tag=1)
        res.update(work_res)
        if len(res) == num_files:
            for i in range(1, num_proc):
                comm.send((None, None), dest=i, tag=2)
            break
        else:
            if work_counter >= (num_work_packets - 1):
                work = None
                for commit_id, fnames in commits.iteritems():
                    for fname in fnames:
                        if (commit_id, fname) not in res:
                            work = (commit_id, [fname])
                            break
                    if work is not None:
                        break
            else:
                work = work_packets[work_counter]
            comm.send(work, dest=rank, tag=2)
            work_counter += 1
    print sum(res.values())

else: # worker
    comm.send((rank, {}), dest=0, tag=1) # ready for work
    while True:
        commit_id, file_names = comm.recv(source=0, tag=2)
        if commit_id is None:
            break
        else:
            res = utils.compute_complexity(repo_dest, commit_id, file_names)
            comm.send((rank, res), dest=0, tag=1)

check_output(['rm -rf {0}'.format(repo_dest)], shell=True)

