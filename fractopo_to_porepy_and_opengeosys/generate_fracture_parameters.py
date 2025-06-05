import json
from pathlib import Path
from typing import Annotated, Any

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import typer
from fractopo import Network
from fractopo.general import read_geofile, save_fig

APP = typer.Typer()

# File paths for input and output data
TRACES_PATH: Path = Path("data/og1_clipped_traces.geojson")
AREA_PATH: Path = Path("data/og1_area_with_dip_data.geojson")
OUTPUT_DIR: Path = Path("outputs/fractopo_to_porepy_and_opengeosys/")

# Azimuth set definitions and labels
AZIMUTH_SETS: tuple[tuple[int, int], ...] = ((160, 25), (30, 60), (120, 150))
AZIMUTH_SET_LABELS: tuple[str, ...] = ("1", "2", "3")
AZIMUTH_SET_LABEL_FALLBACK_ORIENTATION = {
    # Set 1 does not have DIP and DIP_DIR data collected so fallback to values set here
    AZIMUTH_SET_LABELS[0]: (85.0, 90.0),
}


def _classify_dip(dip: Any) -> str:
    """
    Classify the dip value into one of four classes:
    - "vertical" for 80 <= dip <= 90
    - "subvertical" for 60 <= dip < 80
    - "other" for 0 <= dip < 60
    - "missing" for NaN or invalid values
    """
    try:
        if np.isnan(dip):
            return "missing"
    except TypeError:
        # dip is None or not a number
        return "missing"
    if 80 <= dip <= 90:
        return "vertical"
    elif 60 <= dip < 80:
        return "subvertical"
    elif 0 <= dip < 60:
        return "other"
    else:
        return "missing"


def visualize_input_data(traces_gdf, area_gdf, output_path) -> None:
    # Fail if DIP column is not present
    if "DIP" not in traces_gdf.columns:
        raise RuntimeError(
            "ERROR: The 'DIP' column is missing from the traces file. "
            "Please ensure the input GeoJSON contains a 'DIP' column."
        )

    # Convert DIP column to numeric
    traces_gdf["DIP"] = pd.to_numeric(traces_gdf["DIP"], errors="coerce")

    # Classify DIP values
    traces_gdf["dip_class"] = traces_gdf["DIP"].apply(_classify_dip)

    # Define colors for each class
    class_colors: dict[str, str] = {
        "vertical": "#e41a1c",  # red
        "subvertical": "#377eb8",  # blue
        "other": "#4daf4a",  # green
        "missing": "#999999",  # gray
    }

    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    area_gdf.plot(ax=ax, facecolor="none", edgecolor="black", linewidth=2, label="Area")

    # Plot each class separately for legend and color control
    for dip_class, color in class_colors.items():
        subset = traces_gdf[traces_gdf["dip_class"] == dip_class]
        if not subset.empty:
            subset.plot(ax=ax, color=color, linewidth=1, label=dip_class.capitalize())

    # Custom legend
    patches: list[mpatches.Patch] = [
        mpatches.Patch(color=color, label=label.capitalize())
        for label, color in class_colors.items()
    ]
    area_patch = mpatches.Patch(
        edgecolor="black", facecolor="none", label="Area", linewidth=2
    )
    handles = patches + [area_patch]
    ax.legend(handles=handles, loc="best")

    ax.set_title("OG1 clipped traces and area with dip data (colored by DIP data)")
    plt.tight_layout()

    # Save the figure instead of showing it
    plt.savefig(output_path, dpi=300)
    plt.close(fig)


@APP.command()
def main(
    add_only_known_fractures: Annotated[
        bool, typer.Option(help="Only add fractures with known dip and dip direction")
    ] = False,
    max_fractures: Annotated[
        int, typer.Option(help="Maximum number of fractures to add")
    ] = 100,
) -> None:
    """
    Generate fracture parameters from trace and area GeoJSON files.
    Optionally only include fractures with known dip/dip direction.
    """
    # Read traces and area from geojson files
    traces_gdf: gpd.GeoDataFrame = read_geofile(TRACES_PATH)
    area_gdf: gpd.GeoDataFrame = read_geofile(AREA_PATH)

    # Create a Fractopo Network for analysis
    network: Network = Network(
        trace_gdf=traces_gdf,
        area_gdf=area_gdf,
        azimuth_set_ranges=AZIMUTH_SETS,
        azimuth_set_names=AZIMUTH_SET_LABELS,
        truncate_traces=True,
    )

    # Collect mean orientations for each defined fracture set
    set_mean_orientations: dict[str, tuple[float, float]] = {}
    for set_label in AZIMUTH_SET_LABELS:
        set_data: pd.DataFrame = network.trace_data._line_gdf.loc[
            network.trace_data.azimuth_set_array == set_label
        ].copy()

        # Convert DIP and DIP_DIR to numeric, ignore non-numeric
        set_data["DIP"] = pd.to_numeric(set_data["DIP"], errors="coerce")
        set_data["DIP_DIR"] = pd.to_numeric(set_data["DIP_DIR"], errors="coerce")
        average_dip: float = np.nanmean(set_data["DIP"])
        average_dip_dir: float = np.nanmean(set_data["DIP_DIR"])

        # Fallback values if no valid data
        if np.isnan(average_dip):
            average_dip = AZIMUTH_SET_LABEL_FALLBACK_ORIENTATION[set_label][0]
        if np.isnan(average_dip_dir):
            average_dip_dir = AZIMUTH_SET_LABEL_FALLBACK_ORIENTATION[set_label][1]

        set_mean_orientations[set_label] = (average_dip, average_dip_dir)

    rng: np.random.Generator = np.random.default_rng(12345)

    area_gdf_bounds: np.ndarray = area_gdf.total_bounds
    x_diff: float = area_gdf_bounds[2] - area_gdf_bounds[0]

    fracture_params: list[dict[str, Any]] = []
    # Sample up to max_fractures from the trace data
    for _, row in network.trace_data._line_gdf.sample(max_fractures).iterrows():
        # Center of fracture from trace geometry
        center = row["geometry"].centroid

        # Radius based on half the trace length
        radius: float = row["geometry"].length / 2

        dip: float = pd.to_numeric(row["DIP"], errors="coerce")
        dip_dir: float = pd.to_numeric(row["DIP_DIR"], errors="coerce")

        # Only use classified fractures
        row_azimuth_set: str = row["azimuth_set"]
        if row_azimuth_set not in AZIMUTH_SET_LABELS:
            continue

        # Handle missing dip/dip_dir
        if np.isnan(dip):
            if add_only_known_fractures:
                continue
            dip = rng.normal(set_mean_orientations[row_azimuth_set][0], 5)
        if np.isnan(dip_dir):
            if add_only_known_fractures:
                continue
            dip_dir = rng.normal(set_mean_orientations[row_azimuth_set][1], 10)

        # Ensure dip and strike are within valid bounds
        strike: float = dip_dir - 90
        if dip > 90:
            dip = 180 - dip
            strike = strike + 180
        if dip < 0:
            dip = -dip
            strike = strike + 180
        if strike < 0:
            strike = strike + 360
        if strike > 360:
            strike = strike - 360
        assert 0 <= dip <= 90
        assert 0 <= strike <= 360

        x, y = center.coords[0]

        # Transform to local coordinate system
        x = x - area_gdf_bounds[0]
        y = y - area_gdf_bounds[1]

        # Set z coordinate randomly within the rectangle
        z: float = rng.uniform(0, x_diff)

        for value in (x, y, z):
            assert value >= 0.0

        # Convert strike and dip to radians
        strike_rad: float = np.deg2rad(strike)
        dip_rad: float = np.deg2rad(dip)

        # Use .item() if available, else use the value directly
        # i.e. convert from numpy value to python
        strike_angle = strike_rad.item() if hasattr(strike_rad, "item") else strike_rad
        dip_angle = dip_rad.item() if hasattr(dip_rad, "item") else dip_rad

        fracture: dict[str, Any] = {
            "center": [
                x.item() if hasattr(x, "item") else x,
                y.item() if hasattr(y, "item") else y,
                z,
            ],
            "major_axis": radius,
            "minor_axis": radius,
            "major_axis_angle": 0.0,
            "strike_angle": strike_angle,
            "dip_angle": dip_angle,
        }
        fracture_params.append(fracture)

    # Write fractures to JSON file
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.joinpath("fracture_params.json").write_text(
        json.dumps(fracture_params, indent=4)
    )

    # Write domain info to another JSON file
    OUTPUT_DIR.joinpath("domain.json").write_text(
        json.dumps(
            {
                "domain_size": x_diff.item() if hasattr(x_diff, "item") else x_diff,
            }
        )
    )

    visualize_input_data(
        traces_gdf=traces_gdf,
        area_gdf=area_gdf,
        output_path=OUTPUT_DIR.joinpath("og1_traces_and_area.png"),
    )


if __name__ == "__main__":
    APP()
