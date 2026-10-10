#!/bin/bash
set -e
echo "racoogent build env setup..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
python3 --version
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Done. source venv/bin/activate"
