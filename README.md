# TruSD

**Tr**ajectories **u**nder **S**election and **D**rift is an implementation of a method that co-infers selection coefficients and genetic drift from allele trajectories using a maximum-likelihood framework.

If you find the software useful in your research please cite us:

> Mathias Bockwoldt, Charlie Sinclair, David Waxman, and Toni I. Gossmann: TruSD: A python package to co-estimate selection and drift from allele trajectories. In preparation.

## Installation

TruSD needs Python 3.5 or newer. Python 2 is *not* supported!

You should (after publication) be able to install from PyPI:

```sh
pip3 install trusd
```

You can also install it from source:

```sh
git clone https://github.com/mathiasbockwoldt/TruSD.git
cd TruSD
pip3 install -e .
```

If you **do not have root rights**, you can do a user specific install

```sh
git clone https://github.com/mathiasbockwoldt/TruSD.git
cd TruSD
pip3 install --user -e .
```

## Running TruSD

After installation, you should be able to run trusd from the command line:

```sh
trusd --help
```

You can also import the trusd module from your Python 3 script:

```python
import trusd
help(trusd) # gives package content
```
