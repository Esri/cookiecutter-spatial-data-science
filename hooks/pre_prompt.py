"""Runs prior to project generation."""
import json
import logging
import os
import subprocess

# set up logging - tying into cookiecutter logging
logger = logging.getLogger('cookiecutter.hooks.pre_gen_project')
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":

    # try to retrieve git username
    try:

        # get the auth dictionary from gh cli
        gh_auth_dict = subprocess.run(["gh", "api", "user"], capture_output=True, text=True, check=True)

        # extract the username from the auth dictionary
        gh_username = json.loads(gh_auth_dict.stdout).get("login", None).strip()

    except:
        gh_username = None

    # log the retrieved username
    if gh_username:
        logger.info(f"Retrieved GitHub username from GH CLI: {gh_username}")
    else:
        logger.info("No GitHub username retrieved from GH CLI.")

    # set the github username in environment variable for use in cookiecutter
    os.environ['GITHUB_USERNAME'] = gh_username
