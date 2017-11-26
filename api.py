from flask import Flask
from flask import request
from subprocess import call, check_output
from git import Repo

app = Flask(__name__)

@app.route("/")
def api():
    git_url = request.args.get('git_url')
    repo_name = git_url.split('/')[-1].replace('.git', '')
    repo_dest = 'repos/' + repo_name
    max_workers = request.args.get('max_workers')
    call(['git clone {0} {1}'.format(git_url, repo_dest)], shell=True)
    complexity = check_output(['mpiexec -n {0} python work_stealing.py --repo_dir={1}'.format(int(max_workers)+1, repo_dest)], shell=True)
    return git_url, complexity

if __name__ == "__main__":
    app.run()