# `fractopo` inputs to `porepy` and `OpenGeoSys`

## Explanation of code

The script, `generate_fracture_parameters.py`, uses mapped
two-dimensional fracture traces (`data/og1_clipped_traces.geojson`),
some of which have associated structural geological measurements (dip
and dip direction) taken in the field. Fractures are assigned to
pre-determined sets and their orientations are estimated. The main
purpose is to generate an initial 3D fracture network for use in
`OpenGeoSys` and `porepy` through the generation of a
`fracture_params.json` file.

## Adding `fractopo` to your `OpenGeosys-porepy` pip or conda installation

This section explains how to install the `fractopo` package after you have set
up your environment for `OpenGeoSys` and `porepy` using either `pip` or `conda`, as
described in the main `README.md`.

For more information, see the official repository:
<https://github.com/nialov/fractopo>

## Using `pip`

If you are using a virtual environment, activate it first (if not
already activated):

``` bash
source .venv/bin/activate
```

Then install `fractopo`:

``` bash
pip install fractopo
```

## Using `conda`

First, activate your `conda` environment (for example,
`opengeosys-porepy`):

``` bash
conda activate opengeosys-porepy
```

Then install `fractopo` using `pip`:

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

## Usage

Run `generate_fracture_parameters.py`:

~~~bash
python3 ./generate_fracture_parameters.py
~~~

See `./outputs/` directory for generated `fracture_params.json` and other
outputs.

Use `fracture_params.json` as input in `OpenGeoSys` notebook and use the
`domain_size` value in `domain.json` to specify domain size.
