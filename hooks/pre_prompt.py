"""Runs prior to project generation."""
import json
import logging
from pathlib import Path
import subprocess

# set up logging - tying into cookiecutter logging
logger = logging.getLogger('cookiecutter.hooks.pre_prompt')
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    # try to retrieve git username
    try:

        # get the auth dictionary from gh cli
        gh_auth_dict = subprocess.run(["gh", "api", "user"], capture_output=True, text=True, check=True)

        # extract the username from the auth dictionary
        gh_username = json.loads(gh_auth_dict.stdout).get("login", "").strip()

    except:
        gh_username = ""

    # log the retrieved username
    if gh_username:
        logger.info(f"Retrieved GitHub username from GH CLI: {gh_username}")
    else:
        logger.info("No GitHub username retrieved from GH CLI.")

    # get the path to the current cookiecutter context file
    template_root = Path.cwd()
    context_file = template_root / "cookiecutter.json"

    # load the existing cookiecutter context
    with open(context_file, "r", encoding="utf-8") as f:
        context = json.load(f)

    # Set the cookiecutter context
    context["github_username"] = gh_username

    # save the updated context back to the context file
    with open(context_file, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=4)

    logger.debug("Updated cookiecutter context with GitHub username.")
