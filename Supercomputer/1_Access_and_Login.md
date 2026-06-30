# Supercomputer and HPC

## Table of Contents

1: What is an HPC?

2: HPC in the lab

3: Logging into your account!

## 1: What is HPC?
HPC stands for [High-performance computing](https://www.nvidia.com/en-us/glossary/high-performance-computing/). An HPC/supercomputing system is made up of many computers combined that work together to perform complex tasks. Some terminology to note:
* An HPC Cluster is a group/system of computers
* These computers are individually known as nodes
* Each node may have [CPU (Central Processing Unit) or GPU (Graphics Processing Unit)]([https://www.cdw.com/content/cdw/en/articles/hardware/cpu-vs-gpu.html](https://www.weka.io/learn/hpc/gpu-and-hpc-explained/)). 
* Each CPU and GPU have cores, which are essentially the processor of a CPU/GPU. CPU can have 2-64 cores, while GPU can have thousands. The more cores, the more processing power and thus the better the [performance and efficiency](https://www.cdw.com/content/cdw/en/articles/hardware/cpu-vs-gpu.html#5).
* General organization/hierarchy: Cluster -> Nodes (Computers) -> CPU/GPU -> cores

### More basic details on [CPU and GPU:]([https://www.cdw.com/content/cdw/en/articles/hardware/cpu-vs-gpu.html](https://www.weka.io/learn/hpc/gpu-and-hpc-explained/)).
CPU and GPU are both hardware components with different functionalities. CPUs are like the "brain" of the computer, running all the computations and RAM. GPUs were made to handle graphics and visual displays (as implied by the name), which are more complex operations. 

The difference between CPU and GPU is that CPU runs "serially" (one process after another), whereas GPU runs "in parallel" (multiple processes at the same time). When handling large amounts of data or heavy computations, GPU can be more efficient and is better able to handle certain operations.

## 2: HPC in the lab
Next generation sequencing (NGS) have given researchers the possibility of capturing the entirety of the human genome from a tissue sample, known as Whole Genome Sequencing. Oftentimes, the output files of these sequencing processes may be up to hundreds of gigabytes worth of data; regular computers will not be able to handle this. 

Many downstream analyses on WGS files will thus need to be run via a supercomputing/HPC cluster! We have the privilege of being right next to the San Diego Supercomputing Center (SDSC), located on campus at UCSD. The HPC cluster hosted at the SDSC is known as [Expanse](https://www.sdsc.edu/systems/expanse/index.html). In the past, the lab has used supercomputing resources to mine WGS genomic data for microbes and associations with clinical outcomes- analyses that require lots of computing resources that are only feasible with a supercomputer.

Access to supercomputing resources requires applications for resource "allocations". Only limited amounts are provided (rather than open access to resources) because of the computationally intensive nature of supercomputing services. They want to know that researchers have a goal in mind for supercomputing resources and are able to use these resources correctly and efficiently. So far, we only have CPU allocations.

## 3: Logging into your account
One of the lab leaders should have created an Expanse account for you after you joined the lab! This account is accessed via [ssh (Secure Shell)](https://hpc-wiki.info/hpc/SSH), which allows you to connect/login to a remote computer/server (in this case the supercomputing cluster) and execute commands there. There are two ways that I have tried for logging into this account and utilizing supercomputing resources: 1) Command Line and 2) Termius. Personally, I prefer Termius (more details below).

## Command Line
Once you open your command line (on mac, do command+space and type in terminal), use the following commands to log into your account

```
ssh (your username)@login.expanse.sdsc.edu
(Type in password after being prompted)
(Type in TOTP code after being prompted)
```
Use the ssh command, followed by your unique expanse address (should have been provided by lab leader) to begin the login process. It will prompt you for your account password. Then, it will ask you for a TOTP (Time-based One-Time Passwords) 2 factor authorization code. You should have set this up using an application such as Duo Mobile! You may find instructions under the "To Enroll" section of (the Expanse User Guide webpage)[https://www.sdsc.edu/systems/expanse/user_guide.html].

Tada! You are now connected to your Expanse supercomputer account and ready to start :)

## Termius (personally preferred, thanks Elizabeth!)
An alternative to the command line with additional convenient features is the Termius application. It is an ssh client that provides a more visual interface to logging into your Expanse account and manipulating/navigating files. [Termius](https://termius.com/education) is available for FREE as long as you have a Github Student Developer Pack (sign up with your UCSD email [here](https://education.github.com/pack)! You will need to send verification of your student identity such as an ID, transcript, etc.).

Below is what the homepage should look like. To access your supercomputer account via ssh, you want to set up a "new host" (circled in red)
![Alt text](https://github.com/alfalfacow/Spatial-Transcriptomics/blob/main/Images/Termius1.png)

After you click on "New Host", an interface will pop up on the right side of the application that allows you to input information. You will need to put the Expanse address, your username, and your password in the indicated fields. After that, everything should be set up! To connect to your supercomputer account, simple double click the newly created host under the "Hosts" section of the home screen. It will open up a separate tab with prompts for your password and TOTP code (same as Command Line). After successfully logging in, a terminal tab will be opened where you can fully access the supercomputer resources!
![Alt text](https://github.com/alfalfacow/Spatial-Transcriptomics/blob/main/Images/Termius2.png)

A very convenient feature of Termius not available with the command line is the SFTP tab (Secure File Transfer Protocol, or SSH File Transfer Protocol). It displays the files and folders on your native/personal computer on the left, and the files and folders on the remote computer (supercomputer that you are accessing via ssh) on the right. Note that to access the files and folders on the supercomputer you will need to separately connect via ssh by inputting your password and TOTP code. 
![Alt text](https://github.com/alfalfacow/Spatial-Transcriptomics/blob/main/Images/Termius3.png)

This feature allows you to drag, copy+paste, and manipulate files between both computers as you would while accessing the file explorer normally! It allows for easy visualization of the files and file structure in your systems. This is a major reason why I prefer Termius :)

![Alt text](https://github.com/alfalfacow/Spatial-Transcriptomics/blob/main/Images/Termius4.png)

I hope that these notes have taught you a bit more about supercomputers and how to log into your Expanse account!
