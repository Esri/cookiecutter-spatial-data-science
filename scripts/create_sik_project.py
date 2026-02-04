"""Shortcut to quickly create a new SIK project with standard structure."""
import logging
import shutil
import subprocess
from pathlib import Path
import sys

from cookiecutter.main import cookiecutter

# script constants
PROJECT_LOCATION = Path("D:/scratch")

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

# create the full path to the project location
project_path = PROJECT_LOCATION / CONTEXT["project_name"]

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

if __name__ == "__main__":
    # ensure the project location exists
    if not PROJECT_LOCATION.exists():
        raise FileNotFoundError(f"The project location (where to create the new project) does not "
                                f"exist: {PROJECT_LOCATION}")

    # remove any existing project at the location
    if project_path.exists():
        logger.info(f"The project already exists; removing existing project at: {project_path}")
        shutil.rmtree(PROJECT_LOCATION)
        logger.debug(f'Removed existing project.')
    else:
        logger.debug(f'No existing project found at: {project_path}. Nothing to remove.')

    # path to the cookiecutter template
    template_path = Path(__file__).parent.parent

    logger.info(f'Creating new SIK project using cookiecutter template located at: {template_path}')

    # create the sik-project using cookiecutter
    cookiecutter(
        template=str(template_path),
        no_input=True,
        extra_context=CONTEXT,
        output_dir=str(PROJECT_LOCATION)
    )

    logger.info('SIK project creation complete.')

    # create the environment
    logger.debug('Starting Conda environment creation.')

    subprocess.run("make env", cwd=project_path, shell=True, check=True)

    logger.info('Conda environment creation complete.')

    # build the documentation
    logger.debug('Starting MkDocs documentation build.')

    subprocess.run("make docs", cwd=project_path, shell=True, check=True)

    logger.info('MkDocs documentation build complete.')
