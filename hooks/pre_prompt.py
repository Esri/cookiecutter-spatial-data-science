"""Runs prior to project generation."""
import json
import logging
from pathlib import Path
import shutil
import subprocess

# set up logging - tying into cookiecutter logging
logger = logging.getLogger('cookiecutter.hooks.pre_prompt')
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    gh_username = ""
    
    # Check if gh CLI is installed
    if not shutil.which("gh"):
        logger.info("GitHub CLI (gh) not found. Skipping GitHub username detection.")
        logger.info("You can install it from: https://cli.github.com/")
    else:
        logger.info("Checking GitHub CLI authentication...")
        
        # try to retrieve git username
        try:
            # get the auth dictionary from gh cli with a timeout for faster failure
            gh_auth_dict = subprocess.run(
                ["gh", "api", "user"], 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=5  # 5 second timeout to fail fast
            )

            # extract the username from the auth dictionary
            gh_username = json.loads(gh_auth_dict.stdout).get("login", "").strip()

        except subprocess.TimeoutExpired:
            logger.warning("GitHub CLI request timed out. Skipping username detection.")
        except subprocess.CalledProcessError as e:
            logger.warning("GitHub CLI authentication failed. You may need to run 'gh auth login'.")
            logger.debug(f"Error details: {e.stderr if e.stderr else 'No error output'}")
        except json.JSONDecodeError:
            logger.warning("Failed to parse GitHub CLI response. Skipping username detection.")
        except Exception as e:
            logger.debug(f"Unexpected error retrieving GitHub username: {e}")

    # log the retrieved username
    if gh_username:
        logger.info(f"Retrieved GitHub username from GH CLI: {gh_username}")
    else:
        logger.info("No GitHub username retrieved. You'll be prompted to enter it manually.")

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
