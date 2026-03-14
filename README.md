# debris-landlab

Landlab-focused workspace for postfire topographic evolution experiments and DEM differencing.

This repo has been stripped of ML training and data-pipeline code. It is for:
- loading ASCII DEMs,
- running linear/nonlinear Landlab experiments,
- comparing modeled elevation change with LiDAR DEM differences,
- exporting results to GeoTIFF and Zarr.

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
