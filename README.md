**Table of contents:**

[[_TOC_]]

avazu-ctr-prediction
===============
Kaggle competition Click-Through Rate Prediction (Avazu)

# Getting started 
In order to run the project, you will need an isolated environment. We recommend using [conda](https://docs.conda.io/en/latest/) but feel free to use whichever you prefer. 
If you haven't install conda yet, please follow the instruction bellow, and then create the project environment. 

To install conda, follow [these instructions](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

## Makefile
We use the makefile to abstract all the different commands available for the project.
They are self documented. Just run `make` in the root directory to get a list of them.

## Create Environment
From the root directory: 

1. `make create_environment`
2. `conda activate avazu-ctr-prediction`
3. `make requirements`

## Update pinned-dependencies
In order to keep our builds stable across environments and over time, we use a tool called `pip-compile` (from [Pip-tools](https://github.com/jazzband/pip-tools) ) to automatically pin the dependencies along with the sub-dependencies.

To use it: 
- Pin the top level dependencies in “requirements.in” (you don't have to specify a version if you don't need to).
- Run:
```shell script
pip-compile --no-emit-index-url requirements.in
```
This will look at all the packages in `requirements.in` and automatically generate a `requirements.txt` with everything needed.

**Note:** The `--no-emit-index-url` avoid to commit our custom python package repository URL and its password to git.

- If you want to update automatically to the latest version of the packages, add the `-U` flag: 
```shell script
pip-compile -U --no-emit-index-url requirements.in
```

## Build the package
From the root directory:
 
1. Auto-increment the version in `setup.py` by running:  
`make bump_version` (or `make bump_version environment=prod` for non dev version) 
2. Run `make build`

You can now import it with: 

```python
import avazu-ctr-prediction
```

## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.in   <- The requirements file for pinning the requirements
    │
    ├── requirements.txt   <- The requirements file for reproducing the builds environment, e.g.
    │                         generated with `pip-compile --no-emit-index-url requirements.in`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    │
    ├── .bumpversion.cfg   <- configuration for the versioning auto-increment module
    │
    ├── avazu-ctr-prediction
    │   ├── __init__.py    <- Make a Python module
    │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    |   │   └── build_features.py
    │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │      └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io





