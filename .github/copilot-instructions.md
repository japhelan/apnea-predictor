# Sleep Apnea Predictor - AI Agent Instructions

## Project Overview

This is a machine learning project predicting sleep apnea using the STAGES (Stanford Technology, Analytics and Genomics in Sleep) dataset from the National Sleep Research Resource. The project follows a structured data science workflow with emphasis on exploratory analysis and feature engineering.

## Architecture & Data Flow

### Core Data Pipeline

1. **Raw Data**: STAGES dataset files in `data/stages/` (manually acquired from NSRR)
2. **Data Preparation**: `notebooks/data_prep.ipynb` → processes raw data into domain-specific subsets
3. **Feature Engineering**: `notebooks/feature_engineering.ipynb` → transforms subsets into ML-ready features
4. **Processed Data Storage**:
   - `data/processed/raw_subsets/` - domain-specific cleaned datasets (.pkl files)
   - `data/processed/post_engineering/` - ML-ready feature sets

### Key Data Subsets

The project organizes data into domain-specific subsets stored as pickle files:

- `demographics_subset_raw.pkl` - demographic features with work/school schedules
- `general_health_lifestyle_subset_raw.pkl` - lifestyle and survey data
- `medical_history_subset_raw.pkl` - medical conditions and treatments
- `sleep_questionnaires_part_1_subset_raw.pkl` & `part_2` - sleep-related surveys
- `sleep_treatment_subset_raw.pkl` - sleep disorder treatments

## Development Workflow

### Environment Setup

Use conda environment from `environment.yml`:

```bash
conda env create -f environment.yml
conda activate /Users/jack/Repos/apnea-predictor/.conda
```

### Notebook Execution Order

1. Run `data_prep.ipynb` first to create raw subsets from STAGES data
2. Then run `feature_engineering.ipynb` to create ML-ready features
3. Both notebooks have preserved outputs - check execution state before running

### Data Handling Patterns

```python
# Standard imports used throughout
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Standard pandas settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
```

## Project-Specific Conventions

### Data Processing Standards

- **Multi-level column indexing**: Use `utils.data_utils.add_multi_index()` for display names
- **Missing data threshold**: Columns with >80% missing values are excluded from analysis
- **Data validation**: Always run `utils.data_utils.check_duplicates()` and `inspect_structure()`
- **Pickle storage**: Save processed subsets as `.pkl` files for faster loading

### Feature Engineering Guidelines

- **Time-based features**: Combine work/school start times into unified `day_start_time` features
- **Survey consolidation**: Extract individual survey instruments (FSS, GAD-7, PHQ-9, NOSE) as separate feature groups
- **Bias prevention**: Exclude demographic features that could introduce ethical bias (race, ethnicity, language proficiency)
- **Domain expertise**: Apply sleep medicine knowledge - BMI, work schedules, and medical history are key predictors

### Code Organization

- **Utilities**: `utils/data_utils.py` contains reusable functions for data inspection and processing
- **Documentation**: Update `docs/feature_engineering.md` with detailed notes about feature decisions
- **Version tracking**: Document major changes in feature sets and reasoning

## Key Files & Dependencies

### Critical Files

- `environment.yml` - Complete conda environment with scientific computing stack
- `data/stages/datasets/stages-harmonized-dataset-0.3.0.csv` - Main dataset (user must acquire)
- `utils/data_utils.py` - Core utility functions for data processing
- `docs/project_roadmap.md` - High-level project phases and milestones

### External Dependencies

- STAGES dataset requires personal acquisition from NSRR at https://sleepdata.org/datasets/stages
- Project follows ethical research practices with proper acknowledgments in README.md

## Debugging & Analysis Tips

- **Memory efficiency**: Use pickle files instead of re-processing CSV data repeatedly
- **Feature selection**: Document reasoning in markdown cells and `feature_engineering.md`
- **Data quality**: High missing value percentages are expected - this is real-world medical data
- **Domain knowledge**: Sleep apnea prediction benefits from understanding circadian rhythms, BMI correlations, and comorbidity patterns
