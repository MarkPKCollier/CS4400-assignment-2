import os
from subprocess import check_output
import json

def compute_complexity(commit, file_name):
    output = check_output(['argon --json {0}'.format(file_name)], shell=True)
    output = json.loads(output.strip())
    results = filter(lambda res: res.get('type') == 'result', output)
    all_blocks = []
    for result in results:
        all_blocks += result.get('blocks', [])
    return sum(map(lambda block: block['complexity'], all_blocks))

def get_files_with_ext(root_dir, ext):
    res = []
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith(ext):
                res.append(os.path.join(root, f))
    return res