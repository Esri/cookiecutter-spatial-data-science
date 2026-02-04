"""Test cookiecutter spatial data science project generation using the sik-project example."""
import importlib.util
import logging
from pathlib import Path
import subprocess
import sys

# define context for generating the sik-project example
CONTEXT = {
    "project_name": "sik-project",
    "project_title": "Sik Project",
    "author_name": "One Rad Dude",
    "description": "One sik project by one rad dude.",
    "open_source_license": "Apache 2.0",
    "create_github_repo": "no",
}
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
LOG_LEVEL = logging.DEBUG

# configure logging
logger = logging.getLogger(Path(__file__).stem)

# create console handler
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(LOG_LEVEL)
formatter = logging.Formatter(LOG_FORMAT)
stream_handler.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(stream_handler)
logger.setLevel(LOG_LEVEL)


def test_sik_project(cookies):
    # generate project using cookiecutter with context defined above
    result = cookies.bake(extra_context=CONTEXT)

    # basic validation...did the project generate?
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.isdir()

    # create a list of assets to check for
    required_assets = [
        "LICENSE",
    ]

    # arcpy is available, add arcgis assets to check for
    if importlib.util.find_spec("arcpy") is not None:
        required_assets = required_assets + [
            "arcgis",
            "arcgis/sik-project.pyt"
        ]

    # check for required assets
    for asset_suffix in required_assets:
        asset_path = result.project / asset_suffix
        assert asset_path.exists(), f"Required asset '{asset_suffix}' is missing."

    # create the environment
    logger.debug('Starting Conda environment creation.')
    subprocess.run("make env", cwd=result.project, shell=True, check=True)
    logger.info('Conda environment creation complete.')

        # build the documentation
    logger.debug('Starting MkDocs documentation build.')
    subprocess.run("make docs", cwd=result.project, shell=True, check=True)
    logger.info('MkDocs documentation build complete.')
