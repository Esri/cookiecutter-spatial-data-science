---
title: Configuration
---
# Configuration

This project uses **YAML configuration files** in the `config/` directory to manage
settings across different environments. This approach keeps configuration separate
from code, making it easy to adjust behavior without modifying Python source files.

## File Layout

```text
config/
├── config.yml              # Main project settings (committed to version control)
├── secrets_template.yml    # Template for credentials (committed)
└── secrets.yml             # Your actual credentials (git-ignored, create from template)
```

## Main Configuration — `config.yml`

The configuration file has two parts:

1. **Shared settings** — always loaded regardless of environment (e.g. `project`).
2. **Environment-specific sections** — under the `environments` key. Add, rename,
   or remove environments by editing this block — no Python changes required.

```yaml
project:
  name: "my-project"
  title: "My Project"
  description: "A short description."

environments:

  dev:
    logging:
      level: DEBUG
    data:
      input: "data/raw/input_data.csv"
      output: "data/processed/processed.gdb/output_data"

  test:
    logging:
      level: INFO
    data:
      input: "data/raw/input_data.csv"
      output: "data/processed/processed.gdb/output_data"

  prod:
    logging:
      level: WARNING
    data:
      input: "data/raw/input_data.csv"
      output: "data/processed/processed.gdb/output_data"
```

When the configuration is loaded, the active environment's section is **deep-merged**
onto the shared settings, so you only need to specify what differs per environment.

!!! tip "Custom environments"
    The available environments are **introspected** from the keys under
    `environments` in `config.yml`. To add a `staging` environment, simply add
    a `staging:` block — the config loader will recognise it automatically.

## Secrets — `secrets.yml`

Credentials and API keys live in a separate file that is **never committed** to
version control.

1. Copy `secrets_template.yml` to `secrets.yml`.
2. Fill in your actual values.

```yaml
esri:
  gis_url: "https://arcgis.com"
  gis_profile: "my_profile"
```

!!! warning
    `secrets.yml` is listed in `.gitignore`. **Never commit real credentials.**

## Switching Environments

The active environment defaults to **`dev`**. There are two ways to switch:

### Option 1 — Environment Variable

Set the `PROJECT_ENV` variable before running any script or notebook:

=== "PowerShell"

    ```powershell
    $env:PROJECT_ENV = "prod"
    python -m scripts.make_data
    ```

=== "Bash / macOS"

    ```bash
    export PROJECT_ENV=prod
    python -m scripts.make_data
    ```

### Option 2 — Edit the Constant

Open `src/{{ cookiecutter.support_library }}/config.py` and change the default value:

```python
ENVIRONMENT: str = os.environ.get("PROJECT_ENV", "dev")  # change "dev" → "test" or "prod"
```

## Using Configuration in Python

### In Scripts

```python
from {{ cookiecutter.support_library }}.config import config, secrets, ENVIRONMENT

# dot-notation access
log_level = config.logging.level
input_path = config.data.input

# dict-style access
output_path = config["data"]["output"]

# secrets
gis_url = secrets.esri.gis_url

# check current environment
print(f"Running in {ENVIRONMENT} mode")
```

Legacy-style imports also work for backward compatibility:

```python
from {{ cookiecutter.support_library }}.config import LOG_LEVEL, INPUT_DATA, OUTPUT_DATA
```

### In Notebooks

```python
import yaml
from pathlib import Path

config_path = Path.cwd().parent / "config" / "config.yml"
with open(config_path, encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

# access the dev environment settings
env = cfg["environments"]["dev"]
print(env["logging"]["level"])
```

Or import the config module directly:

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path.cwd().parent / "src"))

from {{ cookiecutter.support_library }}.config import config
print(config.logging.level)
```

## API Reference

::: {{ cookiecutter.support_library }}.config
    options:
      show_root_heading: true
      members:
        - ENVIRONMENT
        - ConfigNode
        - get_available_environments
        - load_config
        - load_secrets
