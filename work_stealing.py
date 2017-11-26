import argparse
from mpi4py import MPI

parser = argparse.ArgumentParser()
parser.add_argument('--git_url', type=str)
args = parser.parse_args()

comm = MPI.COMM_WORLD
num_proc = comm.Get_size()
rank = comm.Get_rank()

def compute_complexity(commit, file_name):
    return 1

if rank == 0: # manager
    res = {}
    commits = [('a.hs', 'b.hs'), ('a.hs', 'b.hs', 'c.hs'), ('b.hs', 'c.hs', 'd.hs', 'e.hs')]
    num_files = sum(map(len, commits))
    work_packets = [(i, f) for i, commit in enumerate(commits) for f in commit]
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
    print res

else: # worker
    comm.send((rank, {}), dest=0, tag=1) # ready for work
    while True:
        commit_id, file_name = comm.recv(source=0, tag=2)
        if commit_id is None:
            break
        else:
            res = {}
            complexity = compute_complexity(commit_id, file_name)
            res[(commit_id, file_name)] = complexity
            comm.send((rank, res), dest=0, tag=1)

