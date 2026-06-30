# Supercomputer and HPC

## Table of Contents

1: What is an HPC?

2: Accessing Resources

## 1: What is HPC?
HPC stands for [High-performance computing](https://www.nvidia.com/en-us/glossary/high-performance-computing/). An HPC/supercomputing system is made up of many computers combined that work together to perform complex tasks. Some terminology to note:
* An HPC Cluster is a group/system of computers
* These computers are individually known as nodes
* Each node may have [CPU (Central Processing Unit) or GPU (Graphics Processing Unit)]([https://www.cdw.com/content/cdw/en/articles/hardware/cpu-vs-gpu.html](https://www.weka.io/learn/hpc/gpu-and-hpc-explained/)). 
* Each CPU and GPU have cores, which are essentially the processor of a CPU/GPU. CPU can have 2-64 cores, while GPU can have thousands. The more cores, the more processing power and thus the better the [performance and efficiency](https://www.cdw.com/content/cdw/en/articles/hardware/cpu-vs-gpu.html#5).

### More basic details on [CPU and GPU:]([https://www.cdw.com/content/cdw/en/articles/hardware/cpu-vs-gpu.html](https://www.weka.io/learn/hpc/gpu-and-hpc-explained/)).
CPU and GPU are both hardware components with different functionalities. CPUs are like the "brain" of the computer, running all the computations and RAM. GPUs were made to handle graphics and visual displays (as implied by the name), which are more complex operations. The difference between CPU and GPU is that CPU runs "serially" (one process after another), whereas GPU runs "in parallel" (multiple processes at the same time). When handling large amounts of data or heavy computations, GPU can be more efficient and is better able to handle certain operations.

First, you will need to obtain a spatial transcriptomics dataset, either from a publically accessible dataset or one you generated yourself. An example is the [GSE281978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE281978) series from the Gene Expression Omnibus (GEO) for Head and Neck Cancer (HNSC). The dataset can be downloaded as a tar file at the bottom of the page.
