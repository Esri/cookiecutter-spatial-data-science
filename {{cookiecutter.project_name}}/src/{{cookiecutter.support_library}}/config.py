"""
Configuration loader for the project.

Reads settings from YAML configuration files in the ``config/`` directory using
a singleton pattern so the files are parsed once and reused across modules.

The YAML config supports *environment-specific* sections defined under the
``environments`` key in ``config.yml``.  A special ``default`` sub-section
provides fallback values for any key that is not overridden in a named
environment.  The merge order is:

1. Top-level keys in ``config.yml``
2. ``environments.default`` (if present) — overrides top-level defaults
3. ``environments.<active-env>`` — overrides both of the above

Add, rename, or remove environments by editing that YAML block — no Python
changes required.  Set the ``ENVIRONMENT`` environment variable to force the
active environment, otherwise the ``environment`` key in ``config.yml`` is
used, and the function invocation parameter is used as a final fallback.

Usage::

    from {{cookiecutter.support_library}}.config import config, ENVIRONMENT

    # dot-notation access
    log_level = config.logging.level

    # dict-style access
    input_path = config["data"]["input"]

    # secrets are merged into config — no separate namespace
    gis_url = config.esri.gis_url

    # check current environment
    print(f"Running in {ENVIRONMENT} mode")
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Iterator

import yaml

from .utils._logging import get_logger

# implement module-level logging
logger = get_logger(__name__, level="DEBUG", add_stream_handler=False)

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
# Active environment override from process environment.
# If unset, the loaders fall back to ``environment`` in config.yml,
# then to the invocation parameter, then to ``dev``.
# ---------------------------------------------------------------------------
ENVIRONMENT: str | None = os.environ.get("ENVIRONMENT")


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


def _resolve_environment(
    config_data: dict[str, Any] | None,
    invocation_environment: str | None,
) -> str:
    """Resolve the active environment using project precedence rules."""
    config_environment = None
    if isinstance(config_data, dict):
        config_environment = config_data.get("environment")
    return ENVIRONMENT or config_environment or invocation_environment or "dev"


def get_available_environments(
    config_path: Path | str | None = None,
) -> list[str]:
    """Return the named environment keys defined in ``config.yml``.

    The reserved ``default`` key is excluded from the result because it is a
    fallback section, not a selectable environment.

    Parameters
    ----------
    config_path : Path or str, optional
        Explicit path to a YAML file.  Defaults to ``config/config.yml``.

    Returns
    -------
    list[str]
        Sorted list of environment keys found under the ``environments``
        section, excluding ``default`` (e.g. ``["dev", "prod", "test"]``).
    """
    path = Path(config_path) if config_path else CONFIG_DIR / _CONFIG_FILE
    raw = _load_yaml(path)
    return sorted(
        k for k in raw.get("environments", {}).keys() if k != "default"
    )


def load_config(
    config_path: Path | str | None = None,
    environment: str | None = None,
) -> ConfigNode:
    """Load the main project configuration for a given environment.

    Configuration is built up in three layers:

    1. **Top-level keys** (e.g. ``project``) — always included.
    2. **``environments.default``** — deep-merged on top of the top-level
       keys, providing shared fallback values for all environments.
    3. **``environments.<env>``** — deep-merged last, overriding both of the
       above with environment-specific values.

    Any key present in ``default`` but absent from the active environment
    section is inherited from ``default``.  Keys present in the active
    environment always win.

    Available environments are introspected from the ``environments`` key in
    ``config.yml`` (excluding the reserved ``default`` key) — add or remove
    named sections there to define your own.

    Parameters
    ----------
    config_path : Path or str, optional
        Explicit path to a YAML file.  Defaults to ``config/config.yml``
        relative to the project root.
    environment : str, optional
        Environment name passed at invocation time.
        Resolution order is: ``ENVIRONMENT`` environment variable,
        then top-level ``environment`` in ``config.yml``, then this parameter.

    Returns
    -------
    ConfigNode
        A recursively accessible configuration object.

    Raises
    ------
    ValueError
        If the requested environment is not defined in ``config.yml``.
    """
    path = Path(config_path) if config_path else CONFIG_DIR / _CONFIG_FILE
    raw = _load_yaml(path)
    env = _resolve_environment(raw, environment)

    # pull out the environments block and the active env section
    environments = raw.pop("environments", {})

    # extract the default section (if any) before validation
    # A key with only comments in YAML is parsed as None, so normalise to {}.
    default_settings = environments.pop("default", {}) or {}

    if env not in environments:
        available = ", ".join(sorted(environments.keys())) or "(none)"
        raise ValueError(
            f"Invalid environment '{env}'. "
            f"Available environments in config.yml: {available}"
        )

    # A comment-only environment block is parsed as None by PyYAML; treat as {}.
    env_settings = environments[env] or {}

    # three-way merge: top-level → default → env-specific
    merged = _deep_merge(raw, default_settings)
    merged = _deep_merge(merged, env_settings)
    return ConfigNode(merged)


def load_secrets(
    secrets_path: Path | str | None = None,
    environment: str | None = None,
) -> ConfigNode:
    """Load and resolve project secrets for the given environment.

    Applies the same three-layer merge used by :func:`load_config`:

    1. Top-level keys in ``secrets.yml``
    2. ``environments.default`` — shared fallback values shared across all
       environments.
    3. ``environments.<env>`` — environment-specific overrides applied last.

    The resolved secrets are deep-merged into the main ``config`` object so
    they are accessible as ``config.esri.gis_url`` — no separate namespace.

    Unlike :func:`load_config`, a missing environment section in
    ``secrets.yml`` is **not** an error: the file may legitimately omit
    environments that require no overrides beyond the ``default`` values.
    A debug message is emitted if the active environment is not found.

    Parameters
    ----------
    secrets_path : Path or str, optional
        Explicit path to a YAML file.  Defaults to ``config/secrets.yml``
        relative to the project root.
    environment : str, optional
        Environment name passed at invocation time.
        Resolution order is: ``ENVIRONMENT`` environment variable,
        then top-level ``environment`` in ``config.yml``, then this parameter.

    Returns
    -------
    ConfigNode
        A recursively accessible, environment-resolved secrets object.
        The result is merged into the main :pydata:`config` singleton —
        do not use it as a standalone secrets store.

    Raises
    ------
    FileNotFoundError
        If the secrets file does not exist. Copy
        ``config/secrets_template.yml`` to ``config/secrets.yml`` and
        fill in your values.
    """
    path = Path(secrets_path) if secrets_path else CONFIG_DIR / _SECRETS_FILE
    raw = _load_yaml(path)
    main_config_path = CONFIG_DIR / _CONFIG_FILE
    config_for_env = _load_yaml(main_config_path) if main_config_path.exists() else {}
    env = _resolve_environment(config_for_env, environment)

    environments = raw.pop("environments", {})
    # A key with only comments in YAML is parsed as None, so normalise to {}.
    default_settings = environments.pop("default", {}) or {}

    if env not in environments:
        logger.debug(
            "Environment '%s' not found in %s — using default secrets only.",
            env,
            path.name,
        )
    # A comment-only environment block is parsed as None by PyYAML; treat as {}.
    env_settings = environments.get(env) or {}

    # three-way merge: top-level → default → env-specific
    merged = _deep_merge(raw, default_settings)
    merged = _deep_merge(merged, env_settings)
    return ConfigNode(merged)


# ---------------------------------------------------------------------------
# Module-level singleton – parsed once on first import
# ---------------------------------------------------------------------------
_base_config: ConfigNode = load_config()

try:
    _secrets: ConfigNode = load_secrets()
    config: ConfigNode = ConfigNode(_deep_merge(_base_config.to_dict(), _secrets.to_dict()))
except FileNotFoundError:
    import warnings

    warnings.warn(
        "config/secrets.yml not found. Copy config/secrets_template.yml "
        "to config/secrets.yml and fill in your credentials. "
        "Secret keys will be absent from config until the file is created.",
        stacklevel=2,
    )
    config = _base_config
