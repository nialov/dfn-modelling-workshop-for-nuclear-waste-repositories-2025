# DFN Modelling Workshop for Nuclear Waste Repositories – 3rd – 5th of June 2025, RWTH Aachen University

## Preliminary requirements

### WSL

It is recommended to have a Linux environment available for installation
of software. On Windows, you can enable and install Windows Subsystem
for Linux (WSL), see <https://learn.microsoft.com/en-us/windows/wsl/install>
for instructions. The default Ubuntu distribution is fine.

### Conda

Installation of (some) software is also possible using `conda` on
Windows. See:
<https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html>.

To install `miniforge` using `winget`:

### Google Colab

A Google account is require to access Google Colab
(<https://colab.research.google.com/>) which can be used as a cloud computing
platform for scientific (Python) applications.

~~~powershell
winget install CondaForge.Miniforge3 --source winget
~~~

However, WSL is recommended.

## OpenGeoSys and porepy

-  <https://www.opengeosys.org/docs/userguide/basics/5-mins-ogs/>
-  <https://github.com/pmgbergen/porepy>

### Installation options

#### pip

It is recommended to create a virtual environment for `pip`
installation.

~~~bash
python3 -m venv .venv
~~~

~~~bash
.venv/bin/pip install 'ogstools[ogs]' jupyterlab git+https://github.com/pmgbergen/porepy.git@76d11493e7c62269d03406bd736e1ddded85b517
~~~

To activate environment:

~~~bash
source .venv/bin/activate
~~~

#### conda

It is recommended to create a new `conda` environment for
`conda` installation.

~~~bash
conda env create -n opengeosys-porepy
~~~

~~~bash
# Install
conda install -c conda-forge -n opengeosys-porepy ogstools jupyterlab
# Activate
conda activate opengeosys-porepy
# Install porepy (which is not available on conda-forge)
pip install git+https://github.com/pmgbergen/porepy.git@76d11493e7c62269d03406bd736e1ddded85b517
~~~

## GemPy

-   <https://www.gempy.org/>

### Installation options

#### Using Google Colab

The examples can be run in the cloud using Google Colab. Consequently, Only
a Google account is required to access Colab.

#### Local installation

-   See: <https://docs.gempy.org/installation.html#>
