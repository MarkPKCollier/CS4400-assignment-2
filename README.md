# CS4400-assignment-2

A RESTful service to compute the cyclomatic complexity of a code repository using a distributed system.

Also first time using Haskell.

## Implementation details

My implementation provides a RESTful API which exposes a simple endpoint to call with a code repository.

I follow the **master-slave work stealing pattern** to distribute the work across the nodes in the distributed system.

The problem is **massively parallel** with simple parallelisation across commits and files within a single commit.

### Libraries

I use the [Haskell Servant](http://haskell-servant.readthedocs.io/en/stable/index.html) library to implement a RESTful service.

I use the [Argon](https://github.com/rubik/argon) library to compute the cyclomatic complexity of Haskell source files.

I use the [Haskell Cloud Platform](http://haskell-distributed.github.io/) to distribute the workload accross nodes in the distributed system.