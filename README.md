# CS4400-assignment-2

A RESTful service to compute the cyclomatic complexity of a code repository using a distributed system.

## Implementation details

My implementation provides a RESTful API which exposes a simple endpoint to call with a code repository's url.

To distribute the work across the nodes in the distributed system I implement and compare the **master-slave work stealing pattern**, **master-slave work pushing pattern**.

The Message Passing Interface is used to enable nodes to enable point-to-point communication within the cluster.

The problem is **massively parallel** with simple parallelisation across commits and files within a single commit.

### Libraries

I use the [Python Flask library](http://flask.pocoo.org/) to implement a lightweight RESTful service.

I use the [Argon](https://github.com/rubik/argon) library to compute the cyclomatic complexity of Haskell source files.

I use the [MPI for Python library](https://mpi4py.readthedocs.io) to distribute the workload accross nodes in the distributed system using the Message Passing Interface specification.

## Results

