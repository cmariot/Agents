#!/bin/sh

# You must source this script to activate the virtualenv in your shell.
# source env.sh


ENV_NAME=.venv
BLUE='\033[0;34m'
NC='\033[0m'


PYTHON=python3.11

# Create a virtualenv based on the ENV_NAME variable.
$PYTHON -m venv $ENV_NAME
echo "${BLUE}${ENV_NAME} virtual environment has been created.${NC}"
echo

# Activate the virtualenv.
source $ENV_NAME/bin/activate
echo "${BLUE}The virtual environment is activated.${NC}"
echo

# Install the requirements in the virtualenv.
echo "${BLUE}Installing the requirements...${NC}"
$PYTHON -m pip install --upgrade pip

if [ $? -ne 0 ]; then
    echo "${BLUE}Pip installation failed.${NC}"
    exit 1
fi

$PYTHON -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "${BLUE}Installation failed. Please check the requirements.${NC}"
    exit 1
fi

echo

# Show the installed packages.
echo "${BLUE}Installed packages:${NC}"
$PYTHON -m pip freeze
echo

echo "${BLUE}Running the program...${NC}"

if [ -f ./srcs/main.py ]; then
    $PYTHON ./srcs/main.py
else
    echo "${BLUE}Error: main.py not found.${NC}"
    exit 1
fi
