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
python run_experiments.py --max_workers=8 --repo=https://github.com/tensorflow/haskell.git --server_addr=http://127.0.0.1:8080
```

the above command will take a while to run as it will run a set of experiments, if you just want to run a single experiment you can also just make a GET request like so:

```
http://127.0.0.1:8080/?git_url=https://github.com/tensorflow/haskell.git&max_workers=4&data_parallelisation_strategy=commits&work_distribution_strategy=work_stealing
```

## API

Below is the API specification for the RESTful cyclomatic complexity server.

* **URL**

  /

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `git_url=[string]`

   `max_workers=[int]`

   `data_parallelisation_strategy=[files | commits]`

   `work_distribution_strategy=[work_pushing | work_stealing]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ git_url : https://github.com/rubik/argon.git,
    data_parallelisation_strategy : files,
    complexity : 1250,
    time_taken : 102.3 }`

* **Sample Call:**

  http://127.0.0.1:5000/?git_url=https://github.com/rubik/argon.git&max_workers=4&data_parallelisation_strategy=commits&work_distribution_strategy=work_stealing

## Implementation details

My implementation provides a RESTful API which exposes a simple endpoint to call with a code repository's url. You may also specify a data parallelisation strategy from ['files', 'commits'], a work distribution strategy [work_stealing', 'work_pushing'] and the maximum number of workers you wish to spin up.

I computed the cyclomatic complexity of the user provided repo using [Argon](https://github.com/rubik/argon). Thus the computed cyclomatic complexity is of Haskell (.hs) files only.

I know you said in class that undergraduates were only required to implement one parallelisation strategy, but I have decided to compare the work pushing and work stealing approach and two data distributions strategies to go the extra mile.

## Work & data distribution

To distribute the work across the nodes in the distributed system I implement and compare the **master-slave work stealing pattern** and the **master-slave work pushing pattern**.

The problem is **massively parallel** with simple parallelisation across commits and files within a single commit. I experiment with two data parallelisation strategies. The data is can be parallelised along the files in a commit or along the commits in a repo. I compare these two means to parallise the data by directing the master to give out chunks of work in the form of **single files from a commit** or **single commits in a repo**.

In particular each worker maintains a local copy of the repository which it attains by cloning the repo at initialization. The time to clone the repo i.e. the data distribution time **is** included in the measured execution time in the experiments below.

The master nodes distributes the work by sending (commit id, file id) pairs to the workers in the case of the file data parallelisation strategy and just commit ids in the case of the commit data parallelisation strategy. Thus files are not sent accross the network in point-to-point communication, only ids which are relatively small in size are sent, this reduces network traffic.

### Work pushing 

For work pushing, the master node must divide up the work in advance. The key to ensuring work pushing performs well is the ability to evenly divide up the work.

If there are N nodes and W work packets, a naive approach is to give the first worker the first W/N packets. But the distribution pattern I implement is to give the first worker all packets with id mod N = 1 and so on.

This ensures that if the amount of work per packet is related to the packet id, which is very likely given that commits with increasing ids likely have more files, then the work is still evenly distributed using the mod arithmetic approach.

## Point-to-point communication

The Message Passing Interface is used to enable point-to-point communication between the workers and the master.

MPI is designed to provide efficient large scale point-to-point and grouped communication between nodes in a distributed system. It provides an abstraction of message passing style communication channels between processes in a distributed system. The actual placement of these processes on hardware and implementation of the communication channel is abstracted from the user. MPI programs are known to scale well to thousands of nodes.

## Results

I ran experiments with [1,2,4,8] workers and all 4 pairs of work distribution, data distribution strategies.

I measured the cyclomatic complexity of the [Tensorflow Haskell repo](https://github.com/tensorflow/haskell) and the [Argon repo](https://github.com/rubik/argon) itself. These repos have 165 commits and 119 commits respectively and single threaded execution times are approximately 430 seconds and 235 seconds respectively. So there is plenty of opportunity for parallel speedup and substantial benefit from it.

I run these experiments on my available computational resources, a Macbook Air with 4 cores.

I have measured the execution time of these experiments and computed the parallel speedup as the serial execution time/parallel execution time. Below are the results:

![Argon Repo Execution Times on Macbook Air](https://raw.githubusercontent.com/MarkPKCollier/CS4400-assignment-2/master/images/argon_mac.png)

![Argon Repo Parallel Speedup on Macbook Air](https://raw.githubusercontent.com/MarkPKCollier/CS4400-assignment-2/master/images/argon_mac_speedup.png)

![Tensorflow Haskell Repo Execution Times on Macbook Air](https://raw.githubusercontent.com/MarkPKCollier/CS4400-assignment-2/master/images/tensorflow_haskell_mac.png)

![Tensorflow Haskell Repo Parallel Speedup on Macbook Air](https://raw.githubusercontent.com/MarkPKCollier/CS4400-assignment-2/master/images/tensorflow_haskell_mac_speedup.png)

## Analysis

Interestingly we see little difference in the execution times between the 4 work distribution, data distribution pairs.

Intuitively I expected that work pushing with commit based data distribution to be the most efficient means to parallelize the task. Dividing the work evenly seemed relatively easy (as I describe above) so the advantage that work stealing gives in terms of evenly distributing the work should be minimized and the communication overhead of work stealing is reduced.

The disparity between the communication overhead of the work stealing and work pushing approach may be hightened if the distributed system was run on an underlying architecture where communication was across a network rather than local. I would expect the work pushing approach to have more of an advantage over work stealing in this setting as the communication overhead of work stealing would be increased.

The work pushing approach does show a sustained but small advantage over the work stealing approach in my experiments. I see little difference between parallelizing the data/distributing the work by commits or by file.

As anticipated we see linear speedup up to 4 workers, when the underlying architecture has 4 cores. Beyond that additional workers add no parallelization as that are just being swapped in and out by OS and are not in fact running in parallel.

Of course the problem isn't perfectly parallel and parallelizing the computation leads to some overhead relative to serial execution (mostly due to communication). This is why we see a parallel speedup less than 4 for 4 workers.

## Libraries

I use the [Python Flask library](http://flask.pocoo.org/) to implement a lightweight RESTful service.

I use the [Argon](https://github.com/rubik/argon) library to compute the cyclomatic complexity of Haskell source files.

I use the [MPI for Python library](https://mpi4py.readthedocs.io) to distribute the workload accross nodes in the distributed system using the Message Passing Interface specification. You must have MPI installed for this.
