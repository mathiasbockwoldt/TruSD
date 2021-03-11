# TruSD

**Tr**ajectories **u**nder **S**election and **D**rift is an implementation of a method that co-infers selection coefficients and genetic drift from allele trajectories using a maximum-likelihood framework.

If you find the software useful in your research please cite this package.


## Installation

TruSD needs Python 3.6 or newer. Python 2 is *not* supported!

Currently, the best way to install TruSD is to use a virtual environment and
install TruSD from source.

To setup a virtual environment, go to some folder where you want to have your
virtual environment. This could be your home folder. The following command will
create the virtual environment in the folder `trusd_env`. You can call the
environment something else, but then you have to adapt the name also in the
examples further below.

```sh
python3 -m venv trusd_env
```

This will take some seconds. After that, you can activate the environment:

```sh
source trusd_env/bin/activate
```

Your command line prompt should change to reflect the activated environment.
Now, you can install TruSD into that environment. You can also install other
packages that you might think are useful for your work. Make sure that pip is
uprade to the latest version (first line in the following).

```sh
pip install --upgrade pip
git clone https://github.com/mathiasbockwoldt/TruSD.git
cd TruSD
pip3 install -e .
```

If you want to leave the environment again, simple run `deactivate` in your shell.


## Update

In the TruSD folder run:

```sh
git pull
```


## Running TruSD

If you installed TruSD in a virtual environment, you have to activate it, before
you can run TruSD. The command line prompt should show you, whether it is active.

```sh
source trusd_env/bin/activate
```

Please note, that you are not in the right path, you will have to give the full
path:

```sh
source /path/to/trusd_env/bin/activate
```

Now you should be able to run TruSD and, for example, get some help.

```sh
trusd --help
```

You can also import the `trusd` module from your Python 3 script:

```python
import trusd
help(trusd) # gives package content
```

You can start an example run with

```sh
python3 min_working_example.py
```

To get out of the virtual environment, simply run `deactivate` in your shell.

If you want to run TruSD from a virtual environment on a cluster, please
make the step `source /path/to/trusd_env/bin/activate` part of your job script.
