# `fractopo` inputs to `porepy` and `OpenGeoSys`

## Adding `fractopo` to your `OpenGeosys-porepy` pip or conda installation

This section explains how to install the `fractopo` package after you have set
up your environment for `OpenGeoSys` and `porepy` using either `pip` or `conda`, as
described in the main `README.md`.

For more information, see the official repository:
<https://github.com/nialov/fractopo>

## Using `pip` (use this if you had WSL installed and you used pip to install OpenGeoSys)

If you are using a virtual environment, activate it first (if not
already activated). You will need to find the directory where you
created it during OpenGeoSys installation. It might be your
home directory or a project directory. To activate:

``` bash
source .venv/bin/activate
```

If the above command succeeds, then install `fractopo`:

``` bash
pip install fractopo
```

## Using `conda` (you can try this if you are using only Windows without WSL)

First, activate your `conda` environment (for example,
`opengeosys-porepy`):

``` bash
conda activate opengeosys-porepy
```

Then install `fractopo` using `conda`:

``` bash
conda install -c conda-forge fractopo
```

## Verifying the installation

After installing, you can verify that `fractopo` is installed correctly
by running:

``` bash
python3 -c "import fractopo"
```

If no errors are shown, the installation was successful.

## Get code

You need to clone this repository to your machine to run a script and notebook
that are provided. Using `git` is the easiest method. It is always installed in
WSL environments.

~~~bash
git clone https://github.com/nialov/dfn-modelling-workshop-for-nuclear-waste-repositories-2025.git
~~~

Then change directory to `dfn-modelling-workshop-for-nuclear-waste-repositories-2025/fractopo_to_porepy_and_opengeosys/`:

~~~bash
cd dfn-modelling-workshop-for-nuclear-waste-repositories-2025/fractopo_to_porepy_and_opengeosys/
~~~

If you now list the contents of the directory using `ls` command, you should
see, e.g., `generate_fracture_parameters.py` file.

~~~bash
ls
~~~

## Explanation of code

The script, `generate_fracture_parameters.py`, uses mapped
two-dimensional fracture traces (`data/og1_clipped_traces.geojson`),
some of which have associated structural geological measurements (dip
and dip direction) taken in the field. Fractures are assigned to
pre-determined sets and their orientations are estimated. The main
purpose is to generate an initial 3D fracture network for use in
`OpenGeoSys` and `porepy` through the generation of a
`fracture_params.json` file.

## Usage

Run the script in this directory, `generate_fracture_parameters.py`:

~~~bash
python3 ./generate_fracture_parameters.py
~~~

See `./outputs/` directory for generated `fracture_params.json` and other
outputs.

Use `fracture_params.json` as input in `OpenGeoSys` notebook and use the
`domain_size` value in `domain.json` to specify domain size. These
are automatically used in the `./DFNbyPorePy_to_OGS_fractopo_inputs.ipynb`
notebook in this directory.

Start jupyter lab in `fractopo_to_porepy_and_opengeosys` directory:

~~~bash
jupyter lab
~~~

Open `DFNbyPorePy_to_OGS_fractopo_inputs.ipynb` from the side panel,
and run it. You can see the start of the notebook on how the
`fracture_params.json` and `domain.json` files are used.
