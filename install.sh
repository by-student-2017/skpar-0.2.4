#!/bin/bash

sudo apt update
sudo apt install -y git python3 python3-setuptools python3-pip
pip3 install deap
sudo python3 setup.py install

