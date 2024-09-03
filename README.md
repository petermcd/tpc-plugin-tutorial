# TPC Plugin Tutorial

This repository is to accompany this [medium article](https://medium.com/p/a241a24c9cfb)

The aim of the article is to show how a plugin that utilizing the custom Terminal Plugin Controller (TPC)
platform for the CyberArk application.

This repository is not intended to be a complete application, but rather demonstrate how to one can be created
and is intended to be built upon.

## Installation

This plugin can be installed using PIP using the following steps:

On Windows (please read part two of the series to see how to install this for use with PSM)
```
# Create a virtual environment
python2.11 -m venv .venv
. .venv/Scripta/Activate.exe

# Update pip
.python.exe -m pip install pip

# Install the package
pip install git+https://github.com/petermcd/tpc-plugin-tutorial.git
```

On Linux/Mac (for development)
```
# Create a virtual environment
python2.11 -m venv .venv
. .venv/Scripta/Activate.exe

# Update pip
.python.exe -m pip install pip

# Install the package
pip install git+https://github.com/petermcd/tpc-plugin-tutorial.git[test]
```

## TODO

* Update code so that type: ignore statements can be removed.
