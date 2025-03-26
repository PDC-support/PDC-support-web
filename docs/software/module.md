

# How to use module to load different softwares into your environment

Modules are used to load a specific software, and versions, into your
environment. In this manner we can uphold a pletora of different
softwares and different versions of softwares.

This documentation will primarily focus on using modules on **Dardel**
but many of the commands are also working on other clusters.

On Dardel we are using the **Lmod** module system and many softwares
can be loaded within different Cray Programming Environments.

## Cray Programming Environment

The software we have installed are are under different Cray Programming Environment (CPE)
This is reflected by using the module **PDC** which by default loads the latest CPE
into your environment.

Therefore, right after login in a new session on Dardel, the listing of software will
show only a subset of all the programs and libraries that are installed on the
system. In order to view and access a larger set of programs and libraries,
you need to load one of the `PDC` modules.

```text
# Loads the most recent PDC module
ml PDC
# Loads a specific PDC module
ml PDC/23.12
```

where *23.12* is the most recent version as of May 2024.

## What softwares are installed

At PDC we install many softwares and to examine what softwares are
available for you. Both of these commands are case insentitive.

```text
module avail <SOFTWARE>
# For short
ml avail <SOFTWARE>
```

You can also use…

```text
module spider <SOFTWARE>
# For short
ml spider <SOFTWARE>
```

## What softwares are present in my environment

In order to list the softwares in your environment.

```text
module list
# For short
ml
```

## How to manage software into your environment

Softwares can be loaded into your environment if you have found which one
you prefer. Do remember that this command is case sensitive so you need to spell
<SOFTWARE> with the appropriate lowercase/uppercase letters.

```text
module load <SOFTWARE>[/<VERSION>]
# For short
ml <SOFTWARE>[/<VERSION>]
```

!!! ATTENTION

    In the old **module.tcl** on Cray environments you had to use *swap* for going from one compiler wrapper to the one you prefer. This is not needed on Dardel as it will be handled automatically using the *load* command.

To remove a software from your environment. Do remember that this command is case sensitive so you need to spell
<SOFTWARE> with the appropriate lowercase/uppercase letters.

```text
module unload <SOFTWARE>[/<VERSION>]
# For short
ml -<SOFTWARE>[/<VERSION>]
```

## What parameters are set by a specific module

To list what parameters, pathes, variables are set when loading a specific software.

```text
module show <SOFTWARE>[/<VERSION>]
# For short
ml show <SOFTWARE>[/<VERSION>]
```
