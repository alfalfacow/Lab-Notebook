# Environments and Installation

## Table of Contents

1: What are Conda and Mamba?

2: Installing Conda and Mamba
* 2.1: Conda
* 2.2: Mamba (specifically Micromamba)

3: Creating and Using an environment
* 3.1: Create
* 3.2: Activate
* 3.3: Install
* 3.4: Deactivate
* 3.5: Other Useful Commands

4: Sharing an environment
* 4.1: Exporting
* 4.2: Recreating

## 1: What are Conda and Mamba?
Conda and Mamba are commonly used "Package and Environment Managers"; both are used to create isolated "environments" for Python and R programming.

What exactly does this mean? When you want to run a specific software or package, you always have to install the necessary dependencies as well as the package itself. The main advantage of these environments is isolation: you can download packages without disturbing your main files, you can download older versions of packages without error or mixups, and you can create a separate environment for different projects or packages. In addition, once created, these environments are only "activated" upon command, meaning that they won't interfere with regular use if inactive. Environments also support reproducibility of code and analysis.

The difference bewteen Conda and Mamba is mainly that Mamba is known for being faster due to its running on C++. Both work well! Many sources recommend Mamba over Conda due to speed, but many tutorials online will download packages using conda; know that both are great and are often interchangeable.

## 2: Installing Conda and Mamba
### 2.1: Conda
To download Conda, you can use the wget command to download the file directly from the internet ([this link](https://repo.anaconda.com/miniconda/), if you are curious)[.](https://github.com/rxinnn/Lab_toolkit/blob/main/1_Introductory_Material/3_Conda.md) Once logged in to the supercomputer account via ssh, change to the home directory (using the cd command, stands for change directory) and download the file listed below in the code chunk (using the wget command). This will download the .sh file, which is the conda installer. To execute the installer, we will use the bash command.

```
cd /home/your_username
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
Follow the directions and prompts after running the installation! Make sure to say YES to everything, especially the step about "conda init" (which will initialize conda and allow it to run smoothly).

```
The message will look like below: 
Do you wish to update your shell profile to automatically initialize conda?
This will activate conda on startup and change the command prompt when activated.
If you'd prefer that conda's base environment not be activated on startup,
   run the following command when conda is activated:

conda config --set auto_activate_base false

Note: You can undo this later by running `conda init --reverse $SHELL`

Proceed with initialization? [yes|no]
(TYPE YES HERE AND CLICK ENTER)
```

### 2.2: Mamba (specifically Micromamba)
Like Conda, Mamba is an environment/package manager. A specific "subtype" of the Mamba tool is called Micromamba, defined as a ["tiny"](https://research.it.iastate.edu/micromamba-usage-guide) and ["more compact"](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) version of the mamba package manager. Some forums online recommend mamba over conda for speed, and [micromamba over mamba](https://discourse.pangeo.io/t/mamba-mature-enough/3154/2), so we will focus on downloading micromamba.

To install Micromamba, use the following code on the command line/Termius
```
"${SHELL}" <(curl -L micro.mamba.pm)
```
It will give you a series of prompts! 
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100  3059  100  3059    0     0   2891      0  0:00:01  0:00:01 --:--:--  2891
Micromamba binary folder? [~/.local/bin] (Can just click enter)
Init shell (bash)? [Y/n] (Answer Y)
Configure conda-forge? [Y/n] (Answer Y)
Prefix location? [~/micromamba] /home/your_username/miniconda
Running `shell init`, which:
 - modifies RC file: "/home/akao1/.bashrc"
 - generates config for root prefix: "/home/akao1/miniconda"
 - sets mamba executable to: "/home/akao1/.local/bin/micromamba"
The following has been added in your "/home/akao1/.bashrc" file

# >>> mamba initialize >>>
# !! Contents within this block are managed by 'micromamba shell init' !!
export MAMBA_EXE='/home/akao1/.local/bin/micromamba';
export MAMBA_ROOT_PREFIX='/home/akao1/miniconda';
__mamba_setup="$("$MAMBA_EXE" shell hook --shell bash --root-prefix "$MAMBA_ROOT_PREFIX" 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__mamba_setup"
else
    alias micromamba="$MAMBA_EXE"  # Fallback on help from micromamba activate
fi
unset __mamba_setup
# <<< mamba initialize <<<
```
Lastly, after installation and initialization following the prompts, it will tell you to reset the shell:

```
# The prompt that shows up following installation is below:
# Please restart your shell to activate micromamba or run the following:\n
  source ~/.bashrc (or ~/.zshrc, ~/.xonshrc, ~/.config/fish/config.fish, ...)
# The code for resetting the shell is in the below box on github
```
```
source ~/.bashrc
```

If you recall, both conda and micromamba require "initialization" during the installation process. This initialization adds information about conda and mamba to something called the [".bashrc"](https://www.digitalocean.com/community/tutorials/bashrc-file-in-linux) file. The link above describes the .bashrc file as "a shell script that the Bash shell runs whenever it starts interactively. In simple terms, every time you open a new terminal window, Bash reads and executes the commands inside this file. That makes it the ideal place for your personal Linux environment configuration." 

Since this file is read every time you open a new terminal window, conda/mamba commands are now automatically always available once you open any terminal window!


## 3: Creating and Using an environment

### 3.1: Create
The syntax for creating an environment is practically the same for both conda and mamba! You will notice that to run conda or micromamba commands, the general format is: conda/micromamba + command name + command specifications. There are three main commands for environment creation you should know: create, activate, and install. Other downstream commands to know include: deactivate, env list, and list[.](https://www.montana.edu/uit/rci/tempest/getting-started-online/rstudio-custom-r/index.html)
```
#For everything in the brackets, replace with actual information of interest
conda create --name <ENV_NAME> #most simple
conda create --name <ENV_NAME> <PACKAGE>=<VERSION> <PACKAGE> <PACKAGE> #create the environment, and download 3 packages as specified
conda create -n <ENV_NAME> python=<name_of_Python_version> #for python, example version: 3.10, note that specfiying version is optional
conda create -n <name_of_environment> r-base=<name_of_R_version> #for R studio, example version: 4.2.3, note that specfiying version is optional

#literally the same except (micro)mamba instead of conda!
micromamba create --name <ENV_NAME> #most simple
micromamba create --name <ENV_NAME> <PACKAGE>=<VERSION> <PACKAGE> <PACKAGE> #create the environment, and download 3 packages as specified
micromamba create -n <ENV_NAME> python=<name_of_Python_version> #for python
micromamba create -n <name_of_environment> r-base=<name_of_R_version> #for R studio
```
Note: for creating environments with R studio, it is recommended to use micromamba due to the faster and lighter nature compared to conda, as described above. The first time I tried this with conda, it kept failing.

### 3.2: Activate
To activate a created environment, simply use:
```
conda activate <ENV_NAME>
micromamba activate <ENV_NAME>
```
You will notice the environment name show up on the tab where you type in commands on the terminal! That is an indication that your environment has been successfully activated. All packages and commands within this environment are now ready to be run :)

### 3.3: Install
While you can specify many packages during the "create" command, sometimes you will want to install additional packages into the environment following creation. This is done using the "install" command.
```
conda install <PACKAGE>=<VERSION> <PACKAGE>=<VERSION> <PACKAGE>=<VERSION> #this installs multiple packages in the currently activated conda environment (activate command)
conda install <PACKAGE>=<VERSION> <PACKAGE>=<VERSION> --name <ENV_NAME> #this installs packages in the specified environment that may or may not be currently activated!

#mamba equivalents:
conda install <PACKAGE>=<VERSION> <PACKAGE>=<VERSION> <PACKAGE>=<VERSION> #this installs multiple packages in the currently activated conda environment (activate command)
conda install <PACKAGE>=<VERSION> <PACKAGE>=<VERSION> --name <ENV_NAME> #this installs packages in the specified environment that may or may not be currently activated!

#Python dependencies: some may require you to use the pip command to install, you will likely see this in installation guides for different packages
pip install <python_package>
pip install cell2location #example of real life package

```
Note from [documentation](https://www.anaconda.com/docs/getting-started/working-with-conda/packages/using-r-language) to keep in mind: "When using conda to install R packages, add r- before the regular package name. For instance, to install rbokeh, use conda install r-rbokeh. To install rJava, use conda install r-rjava."

### 3.4: Deactivate
Finally, to deactivate the environment after you are done running commands on the terminal, simply use the deactivate command
```
conda deactivate

#or if using micromamba environment
micromamba deactivate
```
### 3.5: Other useful commands
```
conda env list #displays list of all environments made within conda manager
conda list #displays all packages within currently active conda environment

micromamba env list #displays list of all environments made within micromamba manager
micromamba list #displays all packages within currently active micromamba environment
```

## 4: Sharing an environment
After creating an environment and filling it with your custom packages and dependencies, you may want to share this with others (such as lab mates) for reproducibility! According to the [documentation](https://www.anaconda.com/docs/getting-started/working-with-conda/environments), you may do this by exporting your environment as a .yml file.

### 4.1: Exporting
To export your environment as a .yml file, simple use the following commands:
```
conda activate <ENV_NAME> #activate environment you want to export
conda env export > environment.yml #or you can specify any name for the .yml file

micromamba activate <ENV_NAME>
conda env export > environment.yml
```
The .yml file will be found in your current working directory.

### 4.2: Recreating
To use a .yml file to recreate the environment on your own computer, use the following command:
```
conda env create --file environment.yml
```
The environment.yml file should be in the same directory as your current directory so you are able to access it!

That's all for environments; please let me know if any of the code doesn't work, is outdated, or if there are any factual errors!


## References/Additional Resources
* [Conda Documentation](https://www.anaconda.com/docs/getting-started/working-with-conda/main)
* [Mamba/Micromamba Documentation](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html)
* [Mamba github](https://github.com/mamba-org/micromamba-releases)
* [Conda vs Mamba reading 1](https://iamdamilare13.medium.com/mamba-vs-conda-know-the-differences-and-similarities-be3ae94d2542)
* [Conda vs Mamba reading 2](https://statistics.berkeley.edu/computing/conda)
* [Conda vs Mamba reading 3](https://www.dataschool.io/conda-vs-anaconda-vs-miniconda/)
* [Yale conda guide](https://docs.ycrc.yale.edu/clusters-at-yale/guides/conda/) (slightly different than Expanse system so might not be applicable)
* [Arizona State mamba guide](https://research.it.iastate.edu/micromamba-usage-guide)
* [Iowa State mamba guide](https://research.it.iastate.edu/micromamba-usage-guide)
* [Montana State R studio in micromamba guide](https://research.it.iastate.edu/micromamba-usage-guide)
* Probably outdated [Biostars forum](https://www.biostars.org/p/450316/?__cf_chl_f_tk=LgZTwFTU3L2no4SKLhDIMWWVaPC7PK8cdf.ijI4aLV4-1782799542-1.0.1.1-xPucZ9mNDMrxYIixX7aKFwkLmXRD6YjoOAVQj5tMqSA) about downloading R using conda/mamba
