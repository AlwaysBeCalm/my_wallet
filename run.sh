#!/bin/bash

location=$PWD

last_pip=$(find venv/bin/ -maxdepth 1 -name 'pip*' | sort | tail -1)

python3 -m venv "$location"/venv

source "$location"/venv/bin/activate

"$location"/venv/bin/pip install --upgrade pip

"$location"/venv/bin/pip3 install --upgrade pip

"$location"/"$last_pip" install --upgrade pip

"$location"/venv/bin/pip install -r "$location"/requirements.txt

"$location"/venv/bin/pip3 install -r "$location"/requirements.txt

"$location"/"$last_pip" install -r "$location"/requirements.txt

"$location"/venv/bin/python3 "$location"/src/main.py

rm "$location"/run*