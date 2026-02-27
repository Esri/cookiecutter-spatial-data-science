"""
Configuration loader for the project.

Reads settings from YAML configuration files in the ``config/`` directory using
a singleton pattern so the files are parsed once and reused across modules.

The YAML config supports *environment-specific* sections (``dev``, ``test``,
``prod``).  Change the :pydata:`ENVIRONMENT` constant below — or set the
``PROJECT_ENV`` environment variable — to switch environments.

Usage::

    from {{cookiecutter.support_library}}.config import config, secrets, ENVIRONMENT

    # dot-notation access
    log_level = config.logging.level

    # dict-style access
    input_path = config["data"]["input"]

    # secrets (loaded from config/secrets.yml)
    gis_url = secrets.esri.gis_url

    # check current environment
    print(f"Running in {ENVIRONMENT} mode")
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterator, Literal

import yaml

# ---------------------------------------------------------------------------
# Project root – three levels up from this file
# (src/{{cookiecutter.support_library}}/config.py -> project/)
# ---------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR: Path = PROJECT_ROOT / "config"

# Default file names
_CONFIG_FILE: str = "config.yml"
_SECRETS_FILE: str = "secrets.yml"

# ---------------------------------------------------------------------------
# Active environment — change this value or set the PROJECT_ENV env var
# to switch between  dev | test | prod
# ---------------------------------------------------------------------------
ENVIRONMENT: str = os.environ.get("PROJECT_ENV", "dev")
_VALID_ENVIRONMENTS = {"dev", "test", "prod"}


# ---------------------------------------------------------------------------
# ConfigNode – recursive, attribute-accessible wrapper around a dict
# ---------------------------------------------------------------------------
class ConfigNode:
    """Immutable, attribute-accessible wrapper around nested dictionaries.

    Supports both dot-notation (``cfg.logging.level``) and dict-style
    (``cfg["logging"]["level"]``) access for convenience.
    """

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        data = data or {}
        for key, value in data.items():
            if isinstance(value, dict):
                value = ConfigNode(value)
            # store on the instance __dict__ so attribute access works
            object.__setattr__(self, key, value)

    # dict-style access -------------------------------------------------------
    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__)

    # convenience --------------------------------------------------------------
    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for *key* if present, else *default*."""
        return self.__dict__.get(key, default)

    def to_dict(self) -> dict[str, Any]:
        """Recursively convert back to a plain dictionary."""
        out: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            out[key] = value.to_dict() if isinstance(value, ConfigNode) else value
        return out

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_dict()!r})"


# ---------------------------------------------------------------------------
# Loader helpers
# ---------------------------------------------------------------------------
def _load_yaml(path: Path) -> dict[str, Any]:
    """Read a YAML file and return its contents as a dictionary."""
    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise TypeError(
            f"Expected a YAML mapping at the top level of {path}, "
            f"got {type(data).__name__}"
        )
    return data


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge *override* into *base* (non-destructive copy)."""
    merged = base.copy()
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(
    config_path: Path | str | None = None,
    environment: Literal["dev", "test", "prod"] | None = None,
) -> ConfigNode:
    """Load the main project configuration for a given environment.

    Top-level keys (e.g. ``project``) are always loaded.  Then the
    environment-specific section (``environments.<env>``) is deep-merged on
    top, so environment values override any shared defaults.

    Parameters
    ----------
    config_path : Path or str, optional
        Explicit path to a YAML file.  Defaults to ``config/config.yml``
        relative to the project root.
    environment : str, optional
        One of ``dev``, ``test``, or ``prod``.  Defaults to the module-level
        :pydata:`ENVIRONMENT` constant.

    Returns
    -------
    ConfigNode
        A recursively accessible configuration object.
    """
    env = environment or ENVIRONMENT
    if env not in _VALID_ENVIRONMENTS:
        raise ValueError(
            f"Invalid environment '{env}'. "
            f"Must be one of: {', '.join(sorted(_VALID_ENVIRONMENTS))}"
        )

    path = Path(config_path) if config_path else CONFIG_DIR / _CONFIG_FILE
    raw = _load_yaml(path)

    # pull out the environments block and the active env section
    environments = raw.pop("environments", {})
    env_settings = environments.get(env, {})

    # deep-merge environment-specific settings onto the shared base
    merged = _deep_merge(raw, env_settings)
    return ConfigNode(merged)


def load_secrets(
    secrets_path: Path | str | None = None,
) -> ConfigNode:
    """Load project secrets.

    Parameters
    ----------
    secrets_path : Path or str, optional
        Explicit path to a YAML file.  Defaults to ``config/secrets.yml``
        relative to the project root.

    Returns
    -------
    ConfigNode
        A recursively accessible secrets object.

    Raises
    ------
    FileNotFoundError
        If the secrets file does not exist. Copy
        ``config/secrets_template.yml`` to ``config/secrets.yml`` and
        fill in your values.
    """
    path = Path(secrets_path) if secrets_path else CONFIG_DIR / _SECRETS_FILE
    return ConfigNode(_load_yaml(path))


# ---------------------------------------------------------------------------
# Module-level singletons – parsed once on first import
# ---------------------------------------------------------------------------
config: ConfigNode = load_config()

try:
    secrets: ConfigNode = load_secrets()
except FileNotFoundError:
    # secrets.yml is optional; warn but do not crash on import
    import warnings

    warnings.warn(
        "config/secrets.yml not found. Copy config/secrets_template.yml "
        "to config/secrets.yml and fill in your credentials.",
        stacklevel=2,
    )
    secrets = ConfigNode()

# ---------------------------------------------------------------------------
# Convenience aliases so that existing imports still work.
# ---------------------------------------------------------------------------
LOG_LEVEL: str = config.get("logging", ConfigNode()).get("level", "DEBUG")
INPUT_DATA: str = config.get("data", ConfigNode()).get("input", "")
OUTPUT_DATA: str = config.get("data", ConfigNode()).get("output", "")
