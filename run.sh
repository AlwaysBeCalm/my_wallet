#!/bin/bash

loc=$PWD

python3 -m venv $loc/.venv

$loc/.venv/bin/pip install --upgrade pip

$loc/.venv/bin/pip3 install --upgrade pip

$loc/.venv/bin/pip3.7 install --upgrade pip

$loc/.venv/bin/pip install -r $loc/requirements.txt

$loc/.venv/bin/pip3 install -r $loc/requirements.txt

$loc/.venv/bin/pip3.7 install -r $loc/requirements.txt

$loc/.venv/bin/python3 $loc/src/main.py
