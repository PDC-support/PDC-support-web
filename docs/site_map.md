# Quick start guide

* [Quick Start](basics/quickstart.md)
    * [Brief description](basics/quickstart.md#brief-description)
    * [How to log in](basics/quickstart.md#how-to-log-in)
    * [Storage](basics/quickstart.md#storage)
    * [Transfer of files](basics/quickstart.md#transfer-of-files)
    * [The Lmod module system](basics/quickstart.md#the-lmod-module-system)
    * [The Cray programming environment](basics/quickstart.md#the-cray-programming-environment)
    * [Build your first program](basics/quickstart.md#build-your-first-program)
    * [How to use EasyBuild](basics/quickstart.md#how-to-use-easybuild)
    * [Submit a batch job to the queue](basics/quickstart.md#submit-a-batch-job-to-the-queue)
    * [References](basics/quickstart.md#references)

# Introduction

* [Introduction](basics/introduction.md)
    * [Basic Information](basics/introduction.md#basic-information)
        * [Clusters, nodes, processors, and cores](basics/introduction.md#clusters-nodes-processors-and-cores)
        * [Deciding whether you need PDC for your work](basics/introduction.md#deciding-whether-you-need-pdc-for-your-work)
        * [Who may use PDC’s HPC services](basics/introduction.md#who-may-use-pdc-s-hpc-services)
        * [Account and Time Allocation](basics/introduction.md#account-and-time-allocation)
        * [How much resources will be needed  corehours](basics/introduction.md#how-much-resources-will-be-needed-corehours)
    * [Clusters at PDC](basics/introduction.md#clusters-at-pdc)
    * [Basic Linux for new HPC users](basics/introduction.md#basic-linux-for-new-hpc-users)
        * [Using commands in the shell](basics/introduction.md#using-commands-in-the-shell)
        * [Useful Shell commands](basics/introduction.md#useful-shell-commands)
        * [Further information](basics/introduction.md#further-information)
    * [Glossary](basics/introduction.md#glossary)

# Requesting resources

* [Getting Access](getting_access/get_access.md)
    * [Getting compute time](getting_access/get_access.md#getting-compute-time)
    * [Apply for a new Time Allocation via NAISS](getting_access/get_access.md#apply-for-a-new-time-allocation-via-naiss)
    * [Joining an existing Time Allocation](getting_access/get_access.md#joining-an-existing-time-allocation)
    * [Check your existing Time Allocation](getting_access/get_access.md#check-your-existing-time-allocation)
    * [Applying for an account](getting_access/get_access.md#applying-for-an-account)
        * [Apply via a SUPR account](getting_access/get_access.md#apply-via-a-supr-account)
        * [Apply via PDC webpage](getting_access/get_access.md#apply-via-pdc-webpage)
        * [Request class access](getting_access/get_access.md#request-class-access)
* [Software Development Assistance](getting_access/dev_support.md)

# How to Login

* [How to log in with SSH keys](login/ssh_login.md)
    * [How SSH key pairs work](login/ssh_login.md#how-ssh-key-pairs-work)
    * [How to create SSH key pairs](login/ssh_login.md#how-to-create-ssh-key-pairs)
    * [Authentication process details](login/ssh_login.md#authentication-process-details)
    * [In the login portal](login/ssh_login.md#in-the-login-portal)
    * [Log in to PDC resources](login/ssh_login.md#log-in-to-pdc-resources)
    * [Users which do not have a SUPR account](login/ssh_login.md#users-who-do-not-have-a-supr-account)
    * [Configuring ssh keys and kerberos login](login/ssh_login.md#configuring-ssh-keys-and-kerberos-login)
    * [Debugging](login/ssh_login.md#debugging)
* [Generating SSH keys](login/ssh_keys.md)
    * [Linux](login/ssh_keys.md#linux)
    * [Windows](login/ssh_keys.md#windows)
    * [macOS](login/ssh_keys.md#macos)
* [How to log in with kerberos](login/kerberos_login.md)
    * [General information about Kerberos](login/kerberos_login.md#general-information-about-kerberos)
    * [Login nodes](login/kerberos_login.md#login-nodes)
    * [Step by step Login tutorial](login/kerberos_login.md#step-by-step-login-tutorial)
    * [Troubleshooting login problems](login/kerberos_login.md#troubleshooting-login-problems)
    * [How to configure kerberos](login/configuration.md)
    * [How to reset your password](login/reset_password.md)
* [Interactive HPC at PDC](login/interactive_hpc.md)
    * [How ThinLinc can help in my computation?](login/interactive_hpc.md#how-thinlinc-can-help-in-my-computation)
    * [Kerberos Authentication](login/interactive_hpc.md#kerberos-authentication)
    * [SSH key based authentication](login/interactive_hpc.md#ssh-key-based-authentication)
    * [Graphical application on Dardel](login/interactive_hpc.md#graphical-application-on-dardel)
    * [Launching Jupyter Lab and Jupyter Notebook](login/interactive_hpc.md#launching-jupyter-lab-and-jupyter-notebook)
    * [Disconnect or Logout](login/interactive_hpc.md#disconnect-or-logout)
	* [Mounting Dardel directories on your computer](login/mounting.md)

# How to Run Jobs

* [How to Run Jobs](run_jobs/job_scheduling.md)
    * [How jobs are scheduled](run_jobs/job_scheduling.md#how-jobs-are-scheduled)
    * [Dardel compute nodes](run_jobs/job_scheduling.md#dardel-compute-nodes)
    * [Dardel partitions](run_jobs/job_scheduling.md#dardel-partitions)
    * [How to submit jobs](run_jobs/queueing_jobs.md)
        * [Job scripts](run_jobs/job_scripts.md)
            * [Job script examples](run_jobs/job_scripts_dardel.md)
            * [Job arrays](run_jobs/job_arrays.md)
            * [Short jobs](run_jobs/short_jobs.md)
        * [Run interactively](run_jobs/run_interactively.md)
        * [Running on Dardel](run_jobs/run_interactively.md#running-on-dardel)
* [Job Statistics](run_jobs/job_statistics.md)
    * [Viewing information about account usage](run_jobs/job_statistics.md#viewing-information-about-account-usage)
    * [Specifying what information is shown on the PDC system usage page](run_jobs/job_statistics.md#specifying-what-information-is-shown-on-the-pdc-system-usage-page)
    * [To find information about a particular project account](run_jobs/job_statistics.md#to-find-information-about-a-particular-project-account)
    * [Displaying account usage information as a graph or table](run_jobs/job_statistics.md#displaying-account-usage-information-as-a-graph-or-table)
    * [Viewing usage information per day or per month](run_jobs/job_statistics.md#viewing-usage-information-per-day-or-per-month)
    * [Viewing usage information for specific PDC systems](run_jobs/job_statistics.md#viewing-usage-information-for-specific-pdc-systems)
    * [To clear all current selections](run_jobs/job_statistics.md#to-clear-all-current-selections)

# Data Management

* [Data Management](data_management/data_management.md)
    * [Where to store my data](data_management/data_management.md#where-to-store-my-data)
    * [PDC environmental variables](data_management/data_management.md#pdc-environmental-variables)
    * [Klemming](data_management/klemming.md)
        * [Performance considerations](data_management/klemming.md#performance-considerations)
        * [Managing access permissions](data_management/klemming.md#managing-access-permissions)
    * [Swestore](data_management/file_transfer_swestore-dcache.md)
        * [Swestore-dCache access from PDC transfer node](data_management/file_transfer_swestore-dcache.md#swestore-dcache-access-from-pdc-transfer-node)
        * [Security considerations when using rclone](data_management/file_transfer_swestore-dcache.md#security-considerations-when-using-rclone)
    * [File transfer](data_management/file_transfer.md)
        * [Some important consideration before using Swestore](data_management/file_transfer_swestore-dcache.md)
        * [Swestore-dCache access from PDC transfer node](data_management/file_transfer_swestore-dcache.md#swestore-dcache-access-from-pdc-transfer-node)
        * [Security considerations when using rclone](data_management/file_transfer_swestore-dcache.md#security-considerations-when-using-rclone)
        * [Using rclone to access OneDrive](data_management/rclone_onedrive.md)
        * [Nodes for file operations](data_management/data_management.md#nodes-for-file-operations)

# Software Development

* [Compilers and libraries](software_development/development.md)
    * [The Cray Programming Environment](software_development/development.md#the-cray-programming-environment)
    * [Compiler wrappers](software_development/development.md#compiler-wrappers)
    * [Cray scientific and math libraries](software_development/development.md#cray-scientific-and-math-libraries)
    * [Cray message passing toolkit](software_development/development.md#cray-message-passing-toolkit)
    * [Compiler and linker flags](software_development/development.md#compiler-and-linker-flags)
    * [Build examples](software_development/development.md#build-examples)
* [Building for AMD GPUs](software_development/development_gpu.md)
    * [The AMD ROCm development platform](software_development/development_gpu.md#the-amd-rocm-development-platform)
    * [Compiler and linker flags environment variables](software_development/development_gpu.md#compiler-and-linker-flags-environment-variables)
    * [Build and run examples](software_development/development_gpu.md#build-and-run-examples)
    * [References, general information](software_development/development_gpu.md#references-general-information)
* [Allinea Forge](software_development/development_allineaforge.md)
    * [ARM (Allinea) map](software_development/development_allineaforge.md#arm-allinea-map)
* [Downloadable example for compiling and submitting](software_development/development_example.md)
* [References](software_development/development_references.md)
* [Installing software using EasyBuild](software_development/easybuild.md)
    * [For local installations](software_development/easybuild.md#for-local-installations)
    * [How is EasyBuild configured](software_development/easybuild.md#how-is-easybuild-configured)
    * [How to install software using EasyBuild](software_development/easybuild.md#how-to-install-software-using-easybuild)
    * [dry-run installation of software](software_development/easybuild.md#dry-run-installation-of-software)
    * [How to search for software using EasyBuild](software_development/easybuild.md#how-to-search-for-software-using-easybuild)
    * [How install dependent software](software_development/easybuild.md#how-install-dependent-software)
    * [How to build easyconfig files](software_development/easybuild.md#how-to-build-easyconfig-files)
    * [Final results](software_development/easybuild.md#final-results)
* [Installing software using Spack](software_development/spack.md)
    * [Setting the environment](software_development/spack.md#setting-the-environment)
    * [Finding and listing available software](software_development/spack.md#finding-and-listing-available-software)
    * [Installing software using spack](software_development/spack.md)
    * [Installing non-downloadable software](software_development/spack.md#installing-non-downloadable-software)
    * [Garbage collection](software_development/spack.md#garbage-collection)
    * [How to execute your software](software_development/spack.md#how-to-execute-your-software)

# Industry

* [Practical information for industry projects](industry/industry.md)
    * [SCANIA](industry/scania.md)

# Courses

* [General instructions for PDC courses](courses/general.md)
* [Introduction to PDC](courses/pdcintro.md)
* [PDC Summer School](courses/summerschool.md)

# PDC Blog

* [PDC Blog](https://www.kth.se/blogs/pdc)

# Frequently Asked Questions  FAQ 

* [Frequently Asked Questions (FAQ)](faq/faq.md)
    * [Filesystem](faq/faq.md#filesystem)
    * [Kerberos](faq/faq.md#kerberos)
    * [Login](faq/faq.md#login)
    * [Running](faq/faq.md#running)
    * [Other](faq/faq.md#other)

# Contact Support

* [Contact Support](contact/contact_support.md)

# Available software

* [How to get information about installed softwares](applications/index.md)
* [How to use module to load different softwares into your environment](software/module.md)
    * [Cray Programming Environment](software/module.md#cray-programming-environment)
    * [What softwares are installed](software/module.md#what-softwares-are-installed)
    * [What softwares are present in my environment](software/module.md#what-softwares-are-present-in-my-environment)
    * [How to manage software into your environment](software/module.md#how-to-manage-software-into-your-environment)
    * [What parameters are set by a specific module](software/module.md#what-parameters-are-set-by-a-specific-module)
