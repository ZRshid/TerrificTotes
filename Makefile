#################################################################################
#
# Makefile to build the project
#
#################################################################################

PROJECT_NAME = TerrificTotes
REGION = eu-west-2
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}/python/
SHELL := /bin/bash
PROFILE = default
PIP := pip
PIP := pip

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PYTHON_INTERPRETER) -m venv venv; \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install --upgrade pip)
	$(call execute_in_env, $(PIP) install -r ./requirements.dev.txt)
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################################################
# Build / Run
## Run the security test (bandit + safety)
security-test:
	$(call execute_in_env, bandit -lll  ./python/*/*/*.py) 

## Run the black code check
run-black:
	$(call execute_in_env, black  ./python/*/*/*.py ) 
## Run the unit tests
unit-test:
	$(echo PYTHONPATH)
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -vv)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=python/src/ --cov=python/utils)

## Run all checks
run-checks: security-test run-black unit-test check-coverage



terraform-layers-requirements:
	@echo ${WD}/terraform/package/python
##$(call execute_in_env, $(PIP) install requests -t ${WD}/terraform/package/python)