# debris-landlab

Landlab-focused workspace for postfire topographic evolution experiments and DEM differencing.

This repo has been stripped of ML training and data-pipeline code. It is for:
- loading ASCII DEMs,
- running linear/nonlinear Landlab experiments,
- comparing modeled elevation change with LiDAR DEM differences,
- exporting results to GeoTIFF and Zarr.

<<<<<<< HEAD
## Folder Layout

- `config/base.yaml`: shared workflow config for landslide, hillslope diffusion, and fluvial incision runs
- `config/scenarios/`: small YAML overrides for scenario-specific changes
- `config/landlab_experiments.yaml`: existing topographic experiment config kept for backward compatibility
- `notebook/`: Landlab notebooks
- `scripts/run_landlab_batch.py`: parallel CPU batch runner for independent Landlab runs
- `src/dem_difference.py`: pre/post DEM differencing utility
- `src/export_ascii_to_tif.py`: ASCII-to-GeoTIFF and Zarr export utility
- `src/workflow_config.py`: lightweight config merge and validation helper
- `src/reproject_and_resample.py`: reprojection/resampling helpers
=======
At this stage, the repository contains notebooks only to predict landslide probability and hillslope diffusion. 

## Structure

```text
landlab_debrisflow/
├── .github/
│   └── workflows/
├── config/
├── data/
├── experiments/
├── models/
├── notebooks/
│   ├── Landslide_PF_Bolt_Creek.ipynb
│   ├── Multi_model_Probability.ipynb
│   └── diffusion_and_fluvial_incision_2024.ipynb
├── scripts/
├── src/
├── tests/
├── .gitignore
├── environment.yml
└── README.md
```

## Notebook Inventory

- `notebooks/Landslide_PF_Bolt_Creek.ipynb`: Bolt Creek landslide probability and runout workflow.
- `notebooks/Multi_model_Probability.ipynb`: multi-model landslide probability workflow.
- `notebooks/diffusion_and_fluvial_incision_2024.ipynb`: Landlab diffusion and fluvial incision example.

## Expected Local Inputs

Some notebooks reference local raster inputs and helper modules that are not currently tracked in this repository. Keep them at the project root so the notebooks can import and open them consistently.

- Raster inputs such as `Stehekin_10m.asc` and `landlab_ascii/*.asc`
- Helper modules such as `potential_evapotranspiration_field.py`, `potential_evapotranspiration_field_OFFICIAL.py`, `radiation.py`, `radiation_field_OFFICIAL.py`, and `soil_moisture_dynamics.py`
>>>>>>> gaia/main

## Environment

Conda:

```bash
conda env create -f environment.yml
conda activate debris-landlab
```

Pip:

```bash
pip install -r requirements.txt
```

## Run Batch Experiments

```bash
python scripts/run_landlab_batch.py \
  --dem-path /mnt/c/Users/amehedi/Downloads/nsf_rapid/asc/BoltCreek_USGS_1m_DEM_Reference_A.asc \
  --n-runs 4 \
  --max-workers 4 \
  --total-t 10 \
  --dt 1 \
  --out-dir experiments/landlab_batch
```

## Config

Use `config/base.yaml` for shared project settings and layer paths. Keep observed forcing in CSV and use small YAML overrides in `config/scenarios/` for scenario-specific changes.

Resolve a base config plus one or more scenario overrides with:

```bash
resolve-workflow-config \
  --base config/base.yaml \
  --override config/scenarios/cohesion_burnsev_reduction.yaml \
  --format yaml
```

The sample forcing table used by the landslide notebook is now stored in:

```text
data/forcing_daily.csv
```

Update `config/landlab_experiments.yaml` only if you are using the existing DEM evolution batch runner.

Current default ASC directory:

```yaml
paths:
  asc_dir: /mnt/c/Users/amehedi/Downloads/nsf_rapid/asc
```

## Export Raster Products

Convert all ASC rasters in a directory to GeoTIFF and bundle them into one Zarr store:

```bash
export-raster-products \
  --output-dir data \
  --overwrite \
  --crs EPSG:32610 \
  --zarr-store experiments/outputs/layers.zarr
```
