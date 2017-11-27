import argparse
from mpi4py import MPI
from subprocess import call
import utils
import os

parser = argparse.ArgumentParser()
parser.add_argument('--git_url', type=str)
args = parser.parse_args()
git_url = args.git_url

comm = MPI.COMM_WORLD
num_proc = comm.Get_size()
rank = comm.Get_rank()

repo_dest = os.path.abspath('./repos/' + git_url.split('/')[-1].replace('.git', '') + str(rank))
call(['git clone {0} {1}'.format(git_url, repo_dest)], shell=True)

if rank == 0: # manager
    res = {}
    commits = utils.get_all_files_in_repo(repo_dest, '.hs')
    work_packets = [(commit_id, f) for commit_id, files in commits.iteritems() for f in files]
    num_files = len(work_packets)
    work_counter = 0
    while True:
        rank, work_res = comm.recv(tag=1)
        res.update(work_res)
        if len(res) == num_files:
            for i in range(1, num_proc):
                comm.send((None, None), dest=i, tag=2)
            break
        else:
            if work_counter >= (num_files - 1):
                work = None
                for i, commit in enumerate(commits):
                    for f in commit:
                        if (i, f) not in res:
                            work = (i, f)
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
        commit_id, file_name = comm.recv(source=0, tag=2)
        if commit_id is None:
            break
        else:
            res = {}
            complexity = utils.compute_complexity(repo_dest, commit_id, file_name)
            res[(commit_id, file_name)] = complexity
            comm.send((rank, res), dest=0, tag=1)

call(['rm -rf {0}'.format(repo_dest)], shell=True)

