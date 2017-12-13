# CS4400-assignment-2

A RESTful service to compute the cyclomatic complexity of a code repository using a distributed system.

## Usage

The application can be run by cloning the repo and installing the requirements.txt file, please note that you must have MPI installed.

Make sure you have python, git and pip installed.

```
git clone https://github.com/MarkPKCollier/CS4400-assignment-2.git
pip install -r requirements.txt
python api.py --port_num=8080
```

If you wish to run a batch of experiments you can run:

```
python run_experiments.py
```

you can also just make a GET request like so:

```
http://127.0.0.1:5000/?git_url=https://github.com/tensorflow/haskell.git&max_workers=4&data_parallelisation_strategy=commits&work_distribution_strategy=work_stealing
```

## Implementation details

My implementation provides a RESTful API which exposes a simple endpoint to call with a code repository's url. You may also specify a data parallelisation strategy from ['files', 'commits'], a work distribution strategy [work_stealing', 'work_pushing'] and the maximum number of workers you wish to spin up.

To distribute the work across the nodes in the distributed system I implement and compare the **master-slave work stealing pattern** and the **master-slave work pushing pattern**.

The problem is **massively parallel** with simple parallelisation across commits and files within a single commit. I experiment with two data parallelisation strategies. The data is can be parallelised along the files in a commit or along the commits in a repo. I compare these two means to parallise the data by directing the master to give out chunks of work in the form of **single files from a commit** or **single commits in a repo**.

The Message Passing Interface is used to enable point-to-point communication between the workers and the master.

## Results

## Libraries

I use the [Python Flask library](http://flask.pocoo.org/) to implement a lightweight RESTful service.

I use the [Argon](https://github.com/rubik/argon) library to compute the cyclomatic complexity of Haskell source files.

I use the [MPI for Python library](https://mpi4py.readthedocs.io) to distribute the workload accross nodes in the distributed system using the Message Passing Interface specification. You must have MPI installed for this.
