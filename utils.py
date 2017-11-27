import os
from subprocess import check_output, call
import json

def compute_complexity(repo_dir, commit_id, file_name):
    if not file_name.endswith('.hs'):
        return 0
    output = check_output(['cd {0} && git checkout {1} && argon --json {2}'.format(repo_dir, commit_id, file_name)], shell=True)
    output = json.loads(output.strip())
    results = filter(lambda res: res.get('type') == 'result', output)
    all_blocks = []
    for result in results:
        all_blocks += result.get('blocks', [])
    return sum(map(lambda block: block['complexity'], all_blocks))

def get_dir_files_with_ext(root_dir, ext):
    res = []
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith(ext):
                fname = os.path.join(root, f).replace(root_dir if root_dir.endswith('/') else root_dir + '/', '')
                # fname = os.path.join(root, f).replace(root_dir, '')
                res.append(fname)
    return res

def get_commit_ids(repo_dir):
    output = check_output(["cd {0} && git log --pretty=format:'%H'".format(repo_dir)], shell=True)
    return output.split('\n')

def set_repo_to_commit_id(repo_dir, commit_id):
    call(["cd {0} && git checkout {1}".format(repo_dir, commit_id)], shell=True)

def get_all_files_in_repo(repo_dir, ext):
    res = {}
    commits = get_commit_ids(repo_dir)
    for commit_id in commits:
        set_repo_to_commit_id(repo_dir, commit_id)
        files = get_dir_files_with_ext(repo_dir, ext)
        res[commit_id] = files
    return res