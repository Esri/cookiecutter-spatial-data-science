# Copyright {% now 'utc', '%Y' %} Esri
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

.PHONY: data clean docs docserve env jupyter test black

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = {{ cookiecutter.project_name }}
ENV = $(PROJECT_DIR)/env

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Make Dataset
data:
	conda run --no-capture-output -p "$(ENV)" python scripts/make_data.py

## Delete all compiled Python files
clean:
	find . -path "./env" -prune -o -type f -name "*.py[co]" -delete
	find . -path "./env" -prune -o -type d -name "__pycache__" -delete

## Build the docs
docs:
	conda run --no-capture-output -p "$(ENV)" mkdocs build -f ./docsrc/mkdocs.yml

## MkDocs live documentation server
docserve:
	conda run --no-capture-output -p "$(ENV)" mkdocs serve -f ./docsrc/mkdocs.yml

## Build the local environment from the environment file
env:
	conda env create -p "$(ENV)" -f environment.yml
	conda run --no-capture-output -p "$(ENV)" pip install -e .

## Initialize SpecKit in the project
speckit:
	specify init --here

## Run jupyter without having to explicitly activate the environment
jupyter:
	conda run --no-capture-output -p "$(ENV)" jupyter lab

## Run all tests in module
test:
	conda run --no-capture-output -p "$(ENV)" python -m pytest

## Black formatting
black:
	conda run --no-capture-output -p "$(ENV)" python -m black /src

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
