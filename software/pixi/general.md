
# Instructions for using pixi at PDC
Pixi is a fast, modern, and reproducible package management tool for developers of all backgrounds.

- Pixi helps developers manage dependencies and environments across languages (Python, C++, R, Rust, etc.) — similar to Conda or Poetry, but faster and more reproducible.
- It’s built in Rust and optimized for quick installs and environment creation.
- Uses a lockfile to ensure that the exact same package versions are installed on any machine.
- Built on top of the Conda ecosystem, so it can use packages from Conda, Conda-Forge, and other compatible repositories.
- Works seamlessly on Linux, macOS, and Windows.

More information is available at https://pixi.sh/

## How to use pixi

pixi is available as a module and can be loaded by `ml pixi`
Within pixi provided by PDC, you can either use the global environment or create
your own local environment.

### How to use the global environment.

A lot of software is directly available for you after loading the pixi module regardless of which folder you are currently in.

You can use...
```
$ pixi global list
```
...to get a list of all installed and, by PDC, maintained packages.
You can run them by simply typing
their executable.
Example:
```
$ pixi global list
Global environments as specified in '/cfs/klemming/pdc/software/dardel/other/pixi/0.55.0/manifests/pixi-global.toml'
└── nano: 8.6 
    └─ exposes: nano, rnano
$ nano
```

As you do not have write permission in the globally installed version of pixi, if there are any software or
updates you would like to use, please contact us.

## How to use the local environment

One of the strength in pixi is that you can create several environment as they are needed for
your projects.
using ...
```
$ pixi init [name]
```
...creates the folder [name] and an environment within it. Just goto that folder and install the software you need.
You can then use `pixi add [software]`and `pixi run [executable]` to install and run said software.

Example:
```
$ cd [name]
$ pixi init [name]
$ pixi add gromacs
  Added gromacs >=2025.3,<2026
$ pixi run gmx
```
If that software is not needed anymore use `pixi remove [software]`

The beauty of pixi is that you can create as many environments as needed.

Running the command `pixi update` will then update ALL the software you have in that environment.

## Creating your own global environment

In case you would like to maintain your own global environment in pixi, you need to install pixi from scratch in your own $HOME folder.
This can be achieved using command...

```
export PIXI_NO_PATH_UPDATE=1`
curl -fsSL https://pixi.sh/install.sh | bash
# Following 2 lines can be added to your .bashrc
export PIXI_HOME=./pixi
export $PATH=$PATH:$PIXI_HOME/bin
```
