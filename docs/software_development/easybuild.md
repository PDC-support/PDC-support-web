

# Installing software using EasyBuild

EasyBuild is a software build and installation framework that allows you to manage
(scientific) software on High Performance Computing (HPC) systems in an efficient way.
EasyBuild is available on PDC clusters to facilitate the system wide installation
of software, or to install software in your home folder.
You can find more information about Easybuild at [https://easybuild.io/](https://easybuild.io/)
and all documentations for easybuild reside at [https://docs.easybuild.io/en/latest/](https://docs.easybuild.io/en/latest/)

There are two versions of EasyBuild installed. The **easybuild-prod**
module is only intended for users with privileged access to
PDC clusters. The **easybuild-user** module is intended for users to
make local installs within their home folders.

## For local installations

This module will facilitate the installation of the desired software
into your home folder and will build software and modules into
 *~/.local/easybuild/* by default.
If you would like to store your easybuild installation elsewhere please
set its environment variable prior of loading the **easybuild-user** module.
At this time this works only for easybuild/4.9.1 and PDC/23.12.

```default
export EB_USER_PREFIX=<MyPath>
```

To activate **easybuild-user**.

```default
ml PDC/23.12
ml easybuild-user/4.9.1
```

## How is EasyBuild configured

Easybuild module at PDC is configured to take advantage of existent local resources.

* Temporary files stored in  */tmp*
* EasyBuild searches for **easyconfig** recipes locally and
  has access to many recipes from various HPC centers.
* EasyBuild searches for **easyblocks** and
  has access to many recipes from various HPC centers.
* EasyBuild includes toolchains that are specific to the resources at hand

You can look up the current configuration of EasyBuild by…

```default
eb --show-config
```

## How to install software using EasyBuild

Files ending with **eb** are called **easyconfig** files and are used
as recipes for installation. In general their names have the format

```default
eb <software>-<version>-<toolchain>-<version>.eb
```

## dry run installation of software

Performing a dry-run is a handy procedure for testing the installation
of a software

```default
eb boost-1.83.0-cpeGNU-23.12.eb --dry-run
```

You can also use  *-x,–extended-dry-run* for more information.

## How to search for software using EasyBuild

The installation at PDC includes many **easyconfigs** that can be searched for
and use as a base for new easyconfig recipes. On Dardel git repositories of
easyconfigs can be found within the directory

```default
/pdc/software/eb_repo
```

The PDC-Software-stack is also hosted as a public git repository on
[https://github.com/PDC-support/PDC-SoftwareStack](https://github.com/PDC-support/PDC-SoftwareStack). In order to search
for easyconfigs for a specific program, use the command

```default
eb -S  <software>
```

where  *<software>* is the case insensitive name of the program that you would
like to install. For example, for a listing of available easyconfigs for the molecular
dynamics program GROMACS, use

```default
eb -S gromacs
CFGS1=/pdc/software/eb_repo/PDC-SoftwareStack/easybuild/easyconfigs/g
CFGS2=/pdc/software/eb_repo/CSCS-production/easybuild/easyconfigs/g/GROMACS
* $CFGS1/GROMACS-2020.5-cpeCray-21.09.eb
* $CFGS1/GROMACS-2021.3-cpeCray-21.09.eb
* $CFGS1/GROMACS-2021.3-cpeCray-21.11.eb
* $CFGS1/GROMACS-2022-beta1-cpeCray-21.09.eb
* $CFGS2/GROMACS-2018.6-CrayGNU-20.08-cuda-pat.eb
* $CFGS2/GROMACS-2018.6-CrayGNU-20.08-cuda.eb
...
```

Also you can directly install these softwares by just entering the
**easyconfig** name

## How install dependent software

In many cases a specific installation has many dependencies.
These dependencies can be automatically installed using easyconfigs that are available in robot paths

```default
eb boost-1.83.0-cpeGNU-23.12.eb --robot
```

To check what dependencies are missing

```default
eb boost-1.83.0-cpeGNU-23.12.eb --missing
```

## How to build easyconfig files

The **easyconfig** file is central for installing a software with EasyBuild.
This is a short tutorial on how to achieve that. More information can be found
at [https://docs.easybuild.io/en/latest/Writing_easyconfig_files.html](https://docs.easybuild.io/en/latest/Writing_easyconfig_files.html)

### Parameters

Parameters are good as variables to provide information for EasyBuild.
A full overview of all known easyconfig parameter can be acquired using

```default
eb --avail-easyconfig-params
```

More information can be found at
[https://docs.easybuild.io/en/latest/version-specific/easyconfig_parameters.html#vsd-avail-easyconfig-params](https://docs.easybuild.io/en/latest/version-specific/easyconfig_parameters.html#vsd-avail-easyconfig-params)

### Templates

A set of templates that can be used in easyconfig files and function as small commands.

```default
eb --avail-easyconfig-templates
```

More information can be found at
[https://docs.easybuild.io/en/latest/version-specific/easyconfig_templates.html#avail-easyconfig-templates](https://docs.easybuild.io/en/latest/version-specific/easyconfig_templates.html#avail-easyconfig-templates)

### Name

This specifies the name and version of the software. The created
module will be named accordingly.

```default
name = 'Blast+'
version = '2.12.0'
homepage = 'https://blast.ncbi.nlm.nih.gov/'
description = """Blast for searching sequences"""
```

### Toolchains

A toolchain provides information for EasyBuild about compilers libraries etc…
The idea is to compose and maintain a limited set of specific compiler toolchains.
At PDC we have several toolchains that should be used in case you would like to
parallelize your software

* cpeCray
* cpeGNU
* cpeAMD

In your **easyconfig** file you enter this information using the following command.

```default
toolchain = {'name': 'cpeGNU', 'version': '23.12'}
```

Remember that what toolchain should be used when building your software will
also have an impact on the dependencies your installation has.

For small software or supporting libraries it is not always important
that you use the cpeXXX toolchains but are happy with using whatever
system toolchain there is.

```default
toolchain = SYSTEM
```

### Sources

Specify where EasyBuild can download your source code.
Also look at *templates* described earlier for functions to
simplify this process.

```default
sources = [{
    'source_urls': ['https://example.com'],
    'filename': '%(name)s-%(version)s.tar.gz',
    'extract_cmd': "tar xf %s",  # Optional
}]
```

### Easyblock

An **easyblock** is a python code to address special procedure for the installation.
For example, adresses that you should first run *configure > make > make install* or *cmake > make > make install*

```default
easyblock = 'type'
```

Many EasyBlock are generic as to describe standard installation patterns.
Easyconfigs without an *easyblock* entry are specific and Easybuild will search for EasyBlocks named **EB_[software]**
in the local EasyBuild repository.

To find which **easyblock** are available for you…

```default
eb --list-easyblocks
```

See information about which generic **easyblock** are available at [https://docs.easybuild.io/en/latest/version-specific/generic_easyblocks.html](https://docs.easybuild.io/en/latest/version-specific/generic_easyblocks.html)

### Dependencies

Will be taken into consideration during the installation procedure if an **easyconfig** is found or if a module already exists

Ordinarily a dependency will follow whatever main application toolchain has been defined

```default
dependencies = [
    ('Software', 'version'),
]
```

If you, however, would like to build a specific dependency with the *SYSTEM*
toolchain, the format is as follows…

```default
dependencies = [
    ('Software', 'version', '', ('system', '')),
]
```

### Sanity check

Prior of finalizing the installation, EasyBuild performs a sanity check
to ensure that everything was installed correctly.

```default
sanity_check_paths = {
    'files': ['bin/reframe',
              'share/completions/file1',
              'share/completions/file2'],
    'dirs': ['bin', 'lib', 'share', 'tutorials']
}
sanity_check_commands = [
    'software --version',
    'software --help',
]
```

## Final results

After the installation is completed, EasyBuild will have built the software in question
and provided a module for it.
