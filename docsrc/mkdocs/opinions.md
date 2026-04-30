---
title: Opinions
---
# Opinions

In software, calling a tool **opinionated** means it has decided how things *should*
be done and made those choices the path of least resistance. The opposite — an
*unopinionated* tool — gives you a blank canvas, every decision up to you, and the
freedom to spend your first week debating folder names.

Opinionated tools trade flexibility for momentum. You give up some "any way you want"
in exchange for "the way that usually works." If the defaults fit your work, you move
fast. If they don't, you can usually override them — but the *defaults* are deliberate.

Cookiecutter-Spatial-Data-Science is opinionated. Its structure reflects choices about
how to do collaborative spatial data science work. Those opinions started as the
[Cookiecutter-Data-Science](https://cookiecutter-data-science.drivendata.org/opinions/)
opinions from DrivenData Labs, then bent and grew to fit the realities of working with
ArcGIS Pro, file geodatabases, and Esri's Python ecosystem I have learned in 20 plus
years of working at Esri in various roles.

Take what helps. Skip what doesn't. Just do it consistently.

## Spatial analysis is a directed acyclic graph

The most important properties of a quality spatial analysis are **correctness** and
**reproducibility** — anyone should be able to re-run your work using only your code
and your raw data and land on the same results - maps, tables, and metrics.

The best way to ensure correctness is to test your code. The best way to ensure
reproducibility is to treat your analysis as a directed acyclic graph
([DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph)): each step is a node,
arrows go one way, no loops. Run the graph forwards to recreate any output, or trace
backwards from an output to see exactly what code and data produced it.

This is doubly important in spatial work, where it is far too easy to do the right
analysis in the wrong projection, or to reproject something twice without realising it.

## Raw data is immutable

Treating your analysis as a DAG means raw data is read-only. Read it, copy it,
transform it into new outputs — but never edit it in place. The default `data/` layout
makes this easy:

| Folder | Purpose |
|---|---|
| `data/raw/` | Your original, immutable inputs (often `raw.gdb`) |
| `data/external/` | Reference data from third parties — also immutable |
| `data/interim/` | Cached intermediate outputs (`interim.gdb`) |
| `data/processed/` | Final analytical products (`processed.gdb`) |

Some dos and _do nots_ that follow:

- ✅ Move the raw data through a documented pipeline, ideally invoked from
  `scripts/make_data.py`.
- ✅ Cache long-running intermediate steps to `interim/` so you don't have to recompute
  the universe to debug the last 5%.
- ✅ Make it possible (and ideally automated in `scripts/make_data.py`) for anyone to 
  reproduce your final products from `data/raw/` plus the code in `src/<package>/`.
- ⛔ Don't edit raw data — especially not in ArcGIS Pro's edit session, especially not
  manually, and *especially* not in Excel.
- ⛔ Don't overwrite a feature class in `raw.gdb` with a "fixed" version. Fix it in the
  pipeline.
- ⛔ Don't keep multiple versions of the same raw dataset side-by-side hoping you'll
  remember which is which. _You won't._

!!! warning "ArcGIS-specific traps"
    A file geodatabase is opaque from outside ArcGIS, which makes silent in-place edits
    tempting. Resist. If a feature class needs cleanup, do it as a documented step in
    the pipeline that reads from `raw.gdb` and writes to `interim.gdb` — not as a
    one-off edit you'll never remember making.

## Data should (mostly) stay out of source control

Because raw data is immutable, it doesn't need source control the way code does. The
generated `.gitignore` excludes the entire `data/` directory by default.

This matters more in spatial work than in plain-tabular data science, because file
geodatabases, lidar tiles, mosaic datasets, and large GeoTIFFs blow past Git's
practical limits very quickly. GitHub warns at 50 MB and rejects files over 100 MB,
and a single statewide parcel layer can pass that without trying.

Options for sharing larger spatial data:

- **ArcGIS Online / Enterprise**: publish the data as a hosted feature layer and pull
  it in your scripts via `arcgis.GIS` and a profile from `secrets.yml`.
- **Cloud object storage**: Amazon S3, Azure Blob Storage, Google Cloud Storage —
  all support GeoParquet, Cloud-Optimized GeoTIFF, and FlatGeobuf for cloud-native
  spatial workflows. [`cloudpathlib`](https://github.com/drivendataorg/cloudpathlib)
  and [`fsspec`](https://filesystem-spec.readthedocs.io/en/stable/) make these feel
  like local paths.
- **Git LFS** for moderately large files you genuinely need versioned alongside the
  code. (This is a bit of an anti-pattern for raw data, but it can be useful for 
  reference datasets that are small enough to be versioned but large enough to 
  break Git's limits.)
- **Small reference datasets** that rarely change (e.g. a study-area boundary in
  GeoJSON) are fine to commit directly.

## Tools for orchestrating DAGs

For most projects, `make` (with the bundled `Makefile` / `make.cmd`) is enough — it's
simple, declarative, and already wired up for `make env`, `make data`, `make docs`,
and friends.

If your pipeline grows beyond what `make` handles gracefully, reach for a Python
DAG orchestrator: [Snakemake](https://snakemake.readthedocs.io/),
[Prefect](https://github.com/PrefectHQ/prefect),
[Dagster](https://github.com/dagster-io/dagster) (a department favorite),
[Airflow](https://airflow.apache.org/), or
[Luigi](https://luigi.readthedocs.org/). Use what fits — the template doesn't ship one
because most spatial projects don't need it, and the wrong choice early adds drag for
years.

## Notebooks are for exploration; source files are for repetition

Jupyter notebooks are unbeatable for exploratory spatial analysis — quick reprojections,
inline maps, iterating on a buffer distance until something looks right. They are also
poor vehicles for reproducible analysis, because diffs of `.ipynb` JSON are
near-unreadable, merging is brutal, and they encourage copy-paste.

The rule of thumb: **once a notebook cell does something you'll do again, move it into
`src/<package>/`**.

Classic signs you've crossed that threshold:

- You're duplicating cells from an old notebook to start a new one.
- You're copy-pasting the same function between notebooks.
- You're defining classes inside a notebook.

Generated projects install the package in editable mode, so you can refactor a function
to `src/<package>/analysis.py` and immediately use it from a notebook:

```python
%load_ext autoreload
%autoreload 2

from <package>.analysis import buffer_and_summarize
```

A loose convention that helps when notebooks accumulate: use a numeric prefix, your
initials, and a short description — `0.3-jck-explore-buffer-distances.ipynb`. It costs
nothing and makes intent obvious six months later.

For notebooks that become part of the documentation (worked examples, methodology
write-ups), move them to `docsrc/mkdocs/notebooks/` so MkDocs picks them up.

## Keep modeling organised

Modeling pipelines vary too much to over-prescribe, so the `models/` directory is
deliberately light. What it *does* include is `models/emd/`, because in the ArcGIS
world deep-learning artifacts are bundled as
[Esri Model Definition (`.emd`) files](https://pro.arcgis.com/en/pro-app/latest/help/analysis/deep-learning/the-emd-file.htm)
that pair the model weights with the metadata ArcGIS Pro needs to apply them.

Whatever you train, document enough about each experiment to reproduce it later — at
minimum:

- the data version that went in (path, date, or hash),
- the code version that produced it (Git commit),
- the parameters and hyperparameters,
- the metrics that came out.

For small projects, a JSON or YAML file per run is plenty. For anything bigger, or for
team work, graduate to [MLflow](https://mlflow.org/) or whatever tooling your team has
standardised on.

## Build from the environment up

Reproducing an analysis starts with reproducing the environment that ran it — same
tools, same libraries, same versions. In Python this means picking and configuring an
environment manager.

This template uses **Conda**, for two non-negotiable reasons in the spatial world:

1. ArcPy is shipped through Conda and cannot be installed via pip.
2. Spatial dependencies (GDAL, GEOS, PROJ) are notoriously painful to compile from
   source. Conda packages them for you.

The recommended Conda installer is [Miniforge](https://github.com/conda-forge/miniforge)
when you're not using ArcGIS Pro, and the bundled ArcGIS Pro Python distribution when
you are.

`make env` builds a project-local environment in `./env`, isolated from your other
projects. If you need stronger reproducibility (pinning the full transitive dependency
tree), add [conda-lock](https://github.com/conda/conda-lock) on top.

## Keep secrets and configuration out of version control

You really don't want your ArcGIS Online token, your Postgres password, or your
client's API key on GitHub. Treat these as you would any other piece of leaked
credential — assume someone *will* find them.

The template's pattern is two YAML files in `config/`:

| File | Purpose | Committed? |
|---|---|---|
| `config.yml` | Non-sensitive settings (paths, log levels, environment overrides) | Yes |
| `secrets_template.yml` | Template showing the *shape* of secrets, with placeholder values | Yes |
| `secrets.yml` | Your real credentials — copy from the template and fill in | **No** (gitignored) |

In code, both are loaded via singletons that support dot- and dict-style access:

```python
from <package>.config import config, secrets

gis_url = secrets.esri.gis_url
log_level = config.logging.level
```

Active environment is controlled by the `PROJECT_ENV` environment variable (`dev`,
`test`, `prod`) so you can switch without editing code. See the
[Configuration](https://github.com/esri/cookiecutter-spatial-data-science/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/docsrc/mkdocs/configuration.md)
docs in the generated project for the full contract.

For ArcGIS Online / Enterprise specifically, prefer
[`arcgis.gis.GIS(profile=...)`](https://developers.arcgis.com/python/latest/guide/working-with-different-authentication-schemes/)
with a profile name stored in `secrets.yml` over embedding usernames and passwords
anywhere in code.

## Encourage adaptation from a consistent default

The template is meant to be a starting point, not a straitjacket. The right call is to
**be liberal in adapting the structure for your project, but conservative in changing
the default for everyone**.

Common adaptations:

- **Simplify** — small projects don't need every folder. If `models/` and `references/`
  stay empty for the life of a project, delete them.
- **Expand** — long-running projects often grow sub-packages under `src/<package>/`
  for related groups of code (e.g. `analysis/`, `viz/`, `io/`), or sub-folders under
  `notebooks/` separating exploratory work from polished reports.
- **Re-organise** — when `notebooks/` gets crowded on a long project, a top-level
  `research/` folder with sub-folders per experiment (each with its own notebooks and
  optionally its own Makefile) keeps things navigable.

If you find yourself making the same change on every project, that's a signal worth
sharing — open an
[issue](https://github.com/esri/cookiecutter-spatial-data-science/issues) on the
template repo.

## In Short

The structure exists so you can stop thinking about structure and start thinking about
the analysis. Treat the data as immutable, treat the analysis as a graph, and keep the
parts that change (notebooks, exploration) separate from the parts that need to be
trustworthy (source code, tests, documentation). Adapt freely. Just be consistent.
