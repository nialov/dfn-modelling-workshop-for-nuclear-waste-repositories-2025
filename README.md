# DFN Modelling Workshop for Nuclear Waste Repositories – 3rd – 5th of June 2025, RWTH Aachen University

Please make issues and pull requests here regarding the instructions and
problems, especially those who will hold hackathons and demo your software.

## Preliminary requirements

### WSL

It is recommended to have a Linux environment available for installation
of software. On Windows, you can enable and install Windows Subsystem
for Linux (WSL), see <https://learn.microsoft.com/en-us/windows/wsl/install>
for instructions. The default Ubuntu distribution is fine to use.

### Conda (use if you can not get WSL installed)

Installation of (some) software is also possible using `conda` on
Windows. See:
<https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html>.

To install `miniforge` using `winget`, if available:

~~~powershell
winget install CondaForge.Miniforge3 --source winget
~~~

### Google Colab

A Google account is require to access Google Colab
(<https://colab.research.google.com/>) which can be used as a cloud computing
platform for scientific (Python) applications. Using Colab circumvents the need
to install software on your own devices but might be limited in computing power,
storage and interactivity.

### Software development environment (SDE)

Interacting with code is best done in a code editor. Visual Studio Code
provides many features and plugins to help working with coding environments.
See <https://code.visualstudio.com/> for installation instructions.

## OpenGeoSys and porepy

`OpenGeoSys` can be installed on Windows natively. However, `porepy` cannot be.
Consequently, a WSL installation is recommended or installation in a `conda`
environment can be attempted.

-   <https://www.opengeosys.org/docs/userguide/basics/5-mins-ogs/>
-   <https://github.com/pmgbergen/porepy>

### Installation options

If attempting a native installation on Ubuntu (e.g. in WSL), you will need to
install some system packages for ``gmsh``, which is a dependency of
``porepy``, if they are not installed already.

~~~bash
sudo apt-get update
sudo apt-get install -y build-essential libglu1-mesa libxrender1 libxcursor1 libxft2 libxinerama1 ffmpeg libsm6 libxext6
~~~

#### pip (if you have WSL installed, follow this)

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

#### conda (if you have WSL installed, use the pip instructions above and skip this)

It is recommended to create a new `conda` environment for
`conda` installation.

~~~bash
conda env create -n opengeosys-porepy
~~~

~~~bash
# Install
conda install -c conda-forge -n opengeosys-porepy ogstools jupyterlab ogs
# Activate
conda activate opengeosys-porepy
# Install porepy (which is not available on conda-forge)
pip install git+https://github.com/pmgbergen/porepy.git@76d11493e7c62269d03406bd736e1ddded85b517
~~~

### Testing installation

After installing the required packages, you can run the following command to
perform an initial test that everything is set up correctly:

~~~bash
python3 -c "import ogstools; import porepy; import ogs"
~~~

### Material for Hackathon

-  <https://github.com/nagelt/DFN_OGS>

## GemPy

-   <https://www.gempy.org/>

### Installation options

#### Using Google Colab

The examples can be run in the cloud using Google Colab. Consequently, Only
a Google account is required to access Colab.

#### Local installation

-   See: <https://docs.gempy.org/installation.html#>

### Material

-  <https://github.com/cgre-aachen/egu25_gempy_workshop>

### Run using Binder

Just click link below to start an interactive notebook environment
provided by <https://mybinder.org>, however the environment can not completely
run the notebook.

-   <https://mybinder.org/v2/gh/nialov/gempy-notebook-repo-2025-06-04/2ad98b316e91be70be66a98cb4e5dac44d0d4eb6?urlpath=lab%2Ftree%2FModeling_exmple_EGU25.ipynb>
