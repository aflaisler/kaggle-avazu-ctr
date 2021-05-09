.PHONY: clean data lint requirements
SHELL := /usr/bin/env bash

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = aws-c4-bdap-ds-development
PROFILE = aws-c4-bdap-ds
REGION =  eu-west-1
PROJECT_NAME = avazu_ctr_prediction
PYTHON_INTERPRETER = $(shell which python)
VERSION := $(shell $(PYTHON_INTERPRETER) setup.py --version)

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Update requirements.txt with the required packages needed by the project (requirements.in)
update_requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip-tools
	pip-compile --no-emit-index-url requirements.in

## Update the packages to their latest available versions and pin them
update_dependencies:
	$(PYTHON_INTERPRETER) -m pip install -U pip-tools
	pip-compile -U --no-emit-index-url requirements.in

## Delete all compiled Python files
clean:
	rm -rf dist
	rm -rf build
	rm -rf tests/.cache
	rm -rf .pytest_cache
	rm -rf avazu_ctr_prediction/*.egg-info
	rm -rf *.egg-info
	rm -rf .eggs
	find . -name *.log -type f -delete
	find . -name *.pyc -type f -delete
	find . -name *__pycache__ -delete
	find . -type f -name "*.py[co]" -delete
	find . -type f -name .pytest_cache -delete

## Lint using black
lint:
	black avazu_ctr_prediction

## Run unit tests only
run_unit_tests:
	$(PYTHON_INTERPRETER) -m pytest -m "not integration" --cov=avazu_ctr_prediction --tb=short --disable-warnings

## Run all tests
run_all_tests:
	$(PYTHON_INTERPRETER) -m pytest --cov=avazu_ctr_prediction --tb=short --disable-warnings

## Build python package
build: clean lint
	$(PYTHON_INTERPRETER) setup.py bdist_wheel --universal

## Auto increment the version of the package (args: environment, ie: make bump_version environment=prod)
bump_version:
ifeq (prod,$(environment))
	bumpversion --tag release
else
	bumpversion patch
endif

## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python=3.8 -y
else
	conda create --name $(PROJECT_NAME) python=2.7
endif
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already installed.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## add kernel to Jupyter
add_kernel:
	conda install ipykernel -y && $(PYTHON_INTERPRETER) -m ipykernel install --user --name=$(PROJECT_NAME)
	@echo ">>> New env created and kernel installed within Jupyter. Activate with: conda activate $(PROJECT_NAME)"

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

## Initialise the git repository
init_git:
	@echo -n "Have you created an empty repository with the name $(PROJECT_NAME) on https://gitlab.channel4.com/datascience? [y/N] " && read ans && [ $${ans:-N} = y ]
	if [ -d ".git" ]; then echo "ERROR: git has already been initialised." && exit 1; fi
	git init
	git remote add origin git@gitlab.channel4.com:datascience/$(PROJECT_NAME).git
	git add .
	git commit -m "Initial commit"
	git push -u origin master


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
