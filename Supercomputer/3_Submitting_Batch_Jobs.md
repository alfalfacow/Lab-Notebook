# Environments and Installation

## Table of Contents

1: Login vs Compute nodes

2: Jobs and Schedulers
* 2.1: Jobs
* 2.2: Schedulers

3: Anatomy of a Batch Job
* 3.1: Header
* 3.2: Environment setup (Conda/Micromamba)

4: Submitting a Batch Job

## 1: Login vs Compute nodes
As described in section 1, Expanse is a cluster of computers (nodes). There are two types of nodes: **login** and **compute**. When we connect to our supercomputer accounts via ssh, we are accessing the login node. This is described as the "lobby" of the cluster, where we can add, edit, and manipulate files. The compute nodes are where the intensive and heavy computations are made.

What is the relationship between these two types of nodes? We log into the login node; from there, we submit "jobs" (instructions to run intensive computations) to the compute node. You should NEVER run computationally intensive jobs on the login node!!

## 2: Jobs and Schedulers
### 2.1: Jobs
Jobs are how computations and "instructions" are sent to the compute nodes in an HPC system. In our case, the specific type of job we will be using is called a **"batch job"**. Essentially, instructions are sent as a script from the login node to the compute node, and all the computations are done remotely, separate from our own computer. This means that we do not need to keep our computer open or running while the script completes (a major advantage for scripts that take hours to run!) In addition, the job continues to run even if we quit the terminal/Termius because it has been sent to the compute node :)

There are other types of jobs (such as "interactive jobs"), but we will be focusing on batch jobs for now.

### 2.2: Schedulers
HPC cluster resources are shared among MANY individuals, scholars, and researchers. As such, there may be many people requesting resources and submitting batch jobs at the same time. Thus, **schedulers** are required to handle the orderly organization and execution of different jobs.

There are several different types of schedulers, but for the Expanse HPC cluster the scheduler is called SLURM (Simple Linux Utility for Resource Management). SLURM manages the job queue and allocates memory/resources to different jobs. Another example of a scheduler is Sun Grid Engine (SGE), although we don't really need to know that. Knowing what scheduler we have is important because the syntax for batch jobs and resource requests is different.

## 3: Anatomy of a Batch Job
SLURM batch jobs are submitted in the form of a plain text file (.txt, .sh, .sl, .job, etc.). This file requires very specific syntax for telling the compute node exactly what to do (including resource requests, environment initialization, and the actual commands/computations to be run).

Here is a link to an example document/template with the proper batch job heading and format: [click here](https://docs.google.com/document/d/1zPe-o6Lg4T1DdZSLBxcUbOc4Nkr5nwozAY92RcC7Xl8/edit?tab=t.0)

### 3.1: Header
You will notice that the first line is "#!/bin/bash" and that the header section includes many lines beginning with #SBATCH. 

The first line is known as the "interpreter directory" (aka the "shebang"), and it gives information on what application to use to run the script within the batch job. The "#!" represents "interpretor directory", and "/bin/bash" says that the bash shell is the application that will run the script.

The next few lines begin with #SBATCH, which are read directly by SLURM (the scheduler). These lines define the resources requested (such as memory, number of cores, etc) and general job management (time limit, etc). 

```
#Example batch job header! Find more details/annotations in the linked document
#!/bin/bash
#SBATCH --job-name=my_project
#SBATCH --output=output.txt
#SBATCH -p shared 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --export=ALL
#SBATCH -t 48:00:00
#SBATCH --mail-user=alkao@ucsd.edu
#SBATCH --mail-type=all
#SBATCH -A CSD670
#SBATCH --mem=64G

```

You will notice that these headers define the resources requested (# of nodes (--nodes), # of tasks per node (--ntasks-per-node), # cpus per task (--cpus-per-task), time reqeusted (-t), memory (--mem)), as well as job management (job name (--job-name), output file (--output), email address (--mail-user)). 

The output file will list the output of all the commands within the script. It will also document any errors, and is this very important for debugging errors that may arise. This file will be saved to the directory in which you submit the job (see next section on sbatch!).

For more details on what each command in the header means, feel free to check out the example document linked above or the [official sbatch documentation](https://slurm.schedmd.com/sbatch.html)

### 3.2: Environment setup (Conda/Micromamba)
Environment set up for [conda](https://github.com/conda/conda/issues/7980) and [mamba](https://research.it.iastate.edu/micromamba-usage-guide) require very specific commands within the bash script. While conda/mamba may be configured on the login node (the terminal interface after logging in via ssh), this is not true for batch jobs sent to the compute node. Thus, we need to explicitly initialize conda/mamba and the environment of interest within our batch job. This is done directly following the initial header as described above.
```
#conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate my_env

#micromamba
eval "$(micromamba shell hook --shell=bash)"
micromamba activate my_env
```

After the header and environment setup, the rest of the script consists of the commands and computations you want to run on the compute node! This will depend on the specific package or software you want to run, and there will be separate documentation for every package.

## 4: Submitting a batch job
Once you set up a batch job file (text file), it is very easy to submit it! Move or copy the batch job file into your current directory after logging into your supercomputer account. This can be done very easily using the SFTP tab in Termius. Then, use the sbatch command to send the batch job file to the Expanse compute nodes!
```
cd /directory/with/the/text/file
sbatch batch_job_name.txt
```
Tada! If no errors arise, your batch job has been successfully submitted to the supercomputer and will be running without any further action on your end. The output will be something like
```
submitted batch job 12345678
```

Additional commands that are useful to know:
* scancel: cancels/terminates a submitted batch job
```
scancel 12345678 #put the batch job number that was assigned after submitting the batch job
```
* squeue: view job status
```
squeue 12345678 #shows specific job id submitted
squeue -u $USER #shows all jobs submitted by you
```

## References and Readings
* [UIowa Login vs Compute nodes](https://iowabiostat.github.io/hpc/4.html)
* [UPenn HPC basics](https://ekatsevi.github.io/statistical-computing/hpc-basics.html)
* [SBATCH Slurm documentation](https://slurm.schedmd.com/sbatch.html) (includes more info on sbatch commands)
* [UAB Slurm Batch Job script](https://docs.rc.uab.edu/cheaha/slurm/submitting_jobs/)
* [JHU Slurm script tutorial](https://www.arch.jhu.edu/short-tutorial-how-to-create-a-slurm-script/)
* [Batch Jobs + Scripting guide](https://curc.readthedocs.io/en/latest/running-jobs/batch-jobs.html)
* [Conda setup in batch job](https://github.com/conda/conda/issues/7980)
* [Micromamba setup in batch job](https://research.it.iastate.edu/micromamba-usage-guide)
* [Micromamba documentation + shell hook](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)
