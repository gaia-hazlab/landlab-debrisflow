# landlab_debrisflow

Repository for debris-flow, landslide probability, and landscape evolution notebook workflows built around Landlab.

## Current State

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

## Environment

Create the Conda environment with:

```bash
conda env create -f environment.yml
conda activate landlab_debrisflow
```
