from flask import Flask
from flask import request
import work_stealing
app = Flask(__name__)

@app.route("/")
def api():
    git_url = request.args.get('git_url')
    max_workers = request.args.get('max_workers')
    return git_url

if __name__ == "__main__":
    app.run()