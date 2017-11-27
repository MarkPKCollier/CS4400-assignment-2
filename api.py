from flask import Flask
from flask import request
from flask import jsonify
from subprocess import check_output
import time
from git import Repo

app = Flask(__name__)

@app.route("/")
def api():
    git_url = request.args.get('git_url')
    max_workers = request.args.get('max_workers')
    work_distribution_strategy = request.args.get('work_distribution_strategy')
    start_time = time.time()
    complexity = check_output(['mpiexec -n {0} python work_stealing.py --git_url={1} --work_distribution_strategy={2}'.format(int(max_workers)+1, git_url, work_distribution_strategy)], shell=True)
    return jsonify({
        'git_url': git_url,
        'work_distribution_strategy': work_distribution_strategy,
        'complexity': int(complexity.strip()) if isinstance(complexity, str) else complexity,
        'time_taken': time.time() - start_time
        })

if __name__ == "__main__":
    app.run()