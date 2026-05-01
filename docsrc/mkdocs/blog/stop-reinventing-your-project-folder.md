---
title: Stop Reinventing Your Project Folder
date: 2026-04-30
---

# Stop Reinventing Your Project Folder

*An overview of Cookiecutter-Spatial-Data-Science for Esri Professional Services coders.*

If you have ever opened an old project folder and asked yourself, *"do I run
`clean_data.py` first, or `evaluate_data.py`?"* — or worse, *"is `make_figures_v2_FINAL.py`
actually the final one?"* — this post is for you.

## The problem we all share

Professional Services work moves fast. We jump between customers, ArcGIS Pro versions,
ArcPy, the ArcGIS API for Python, notebooks, the occasional rogue Excel file, and the
ever-present pressure to *just deliver something*. Every project starts the same way:
a fresh empty folder and a quiet little argument with yourself about where the data
should go, where the scripts should go, and whether this is the project where you
finally write tests.

That argument is expensive. It costs you time at the start of every engagement, it
costs your teammates time when they pick up your work, and it costs *future-you* time
when you come back to a project six months later with no memory of where anything
lives.

## What Cookiecutter-Spatial-Data-Science is

[Cookiecutter-Spatial-Data-Science](https://github.com/esri/cookiecutter-spatial-data-science)
is a project template — you run one command and you get a fully scaffolded project
with all of the boring decisions already made:

```cmd
cookiecutter https://github.com/esri/cookiecutter-spatial-data-science
```

Answer a handful of prompts, and out the other side comes a project with:

- a pre-configured **ArcGIS Pro** project (`.aprx`), traditional toolbox, and Python
  toolbox,
- a **Conda** environment definition wired up to a one-line `make env` build,
- a `data/` tree split into `raw/`, `interim/`, `processed/`, and `external/` —
  gitignored by default,
- a `src/<your_package>/` Python package, installed in editable mode so your notebooks
  can `import` it immediately,
- YAML-based **config and secrets** (with `secrets.yml` already gitignored — because
  of course it is),
- **PyTest** scaffolding with reusable spatial fixtures,
- **MkDocs** documentation ready to publish,
- and an `AGENTS.md` file so Copilot, Claude, and Cursor have a fighting chance of
  being useful on day one.

It is opinionated, in the good sense — it has decided how things should be done so you
don't have to. The defaults are the path of least resistance, and they are deliberate
choices [learned the hard way over many years](origins.md) of Esri project work.

## Why structure matters (even when you're working alone)

There is a tempting myth that structure is something you adopt when a *team* gets
involved — that solo work can stay loose. It cannot. Or rather, it can, but you will
pay for it later.

Spatial data science is two activities at once:

1. **Messy creative exploration** — quick reprojections, eyeballing a buffer distance,
   trying a third clustering algorithm because the second one looked weird.
2. **Reproducible delivery** — the analysis someone (often you) needs to re-run next
   quarter when the data refreshes or the customer asks "what if?"

Trying to impose structure mid-exploration kills the creativity. Trying to add structure
*after* you have already landed on results is, in practice, nearly impossible. A
template solves this by giving you the structure up front: explore freely inside it,
and the reproducible scaffolding is already there when you need it.

The win shows up in concrete ways:

- **For collaboration:** a teammate (or a handoff team) can clone your repo, run
  `make env`, and know exactly where the data, code, notebooks, and tests live without
  reading a wiki.
- **For yourself:** when you return to a project months later, the folder layout *is*
  the documentation. `notebooks/` is exploration. `src/<package>/` is reusable. `data/raw/`
  is immutable. `scripts/make_data.py` is the pipeline. You do not have to remember.
- **For the customer:** consistent project shape means consistent deliverables. They
  get the same quality bar from every Esri engagement, not "whatever convention the
  consultant happened to like."

## The opinions, in one paragraph

Treat your analysis as a [DAG](opinions.md#spatial-analysis-is-a-directed-acyclic-graph).
Treat raw data as immutable. Keep big spatial data out of Git (use ArcGIS Online or 
S3/Azure Blob). Use notebooks to explore and source files to repeat — when a
notebook cell does something you will do again, it belongs in `src/<package>/`. Use
Conda for environments because ArcPy and GDAL/GEOS/PROJ leave you no realistic choice.
Keep secrets in `config/secrets.yml` and out of source control. Adapt the structure
freely for any one project, but be conservative about changing the defaults for
everyone.

That's it. None of it is novel. All of it is easier when the template has already wired
it up for you.

## Who it's for

Honestly, all of us — beginner to expert.

- **If you're newer to Python or data science**, the template is a tour of best
  practices in concrete form. The folder names, the `Makefile`, the test scaffolding,
  the config pattern — these are the conventions you would otherwise have to assemble
  from a dozen blog posts.
- **If you're an experienced developer**, the template eliminates the tedious 20% of
  every new project so you can spend that time on the analysis instead. You can
  override anything that doesn't fit — the defaults are a starting point, not a
  cage.
- **If you live in ArcGIS Pro**, the `arcgis/` directory ships with a real `.aprx`,
  a `.tbx`, and a `.pyt` already in place. No more "step one: open Pro and create a
  project."

## How to try it

1. Make sure you have Conda (the one bundled with ArcGIS Pro is fine) and Git.
2. Create a small environment with Cookiecutter installed (`conda create -n ck --clone arcgispro-py3 -y && conda activate ck`,
   then `conda install -c conda-forge cookiecutter`).
3. `cd` to wherever you want your new project to live and run:

   ```cmd
   cookiecutter https://github.com/esri/cookiecutter-spatial-data-science
   ```

4. Answer the prompts. You'll get a fully initialized Git repo with sensible defaults.
5. `cd` into the new project, run `make env`, activate `./env`, and start working.

Full setup instructions, including a short walkthrough video, live on the
[Getting Started](getting_started.md) page.

## In short

Stop reinventing your project folder on every engagement. Adopt a consistent shape so
the messy parts of your work can stay messy and the deliverable parts stay deliverable
— for your teammates, your customers, and the version of you who has to revisit this
project a year from now.

Try it on your next project. If something doesn't fit, [open an issue](https://github.com/esri/cookiecutter-spatial-data-science/issues)
or a PR — it's an Esri-maintained, community-shaped template, and the next improvement
might as well be yours.
