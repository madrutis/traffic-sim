#!/bin/bash

# make a virtual environment
python3 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install the requirements
pip install -r requirements.txt

#Good to go!