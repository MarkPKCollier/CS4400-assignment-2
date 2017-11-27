from flask import Flask
from flask import request
from flask import jsonify
from subprocess import call, check_output
from git import Repo

app = Flask(__name__)

@app.route("/")
def api():
    git_url = request.args.get('git_url')
    max_workers = request.args.get('max_workers')
    complexity = check_output(['mpiexec -n {0} python work_stealing.py --git_url={1}'.format(int(max_workers)+1, git_url)], shell=True)
    return jsonify({
        'git_url': git_url,
        'complexity': int(complexity.strip()) if isinstance(complexity, str) else complexity
        })

if __name__ == "__main__":
    app.run()