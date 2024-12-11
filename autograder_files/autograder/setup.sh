#!/usr/bin/env bash

apt-get update && apt-get install -y --no-install-recommends apt-utils

apt-get install -y python3 python3-pip python3-dev

pip3 install -r /autograder/source/requirements.txt

mkdir results

touch results/results.json
