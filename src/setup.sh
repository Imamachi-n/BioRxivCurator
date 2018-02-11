#!/bin/bash
sudo curl -sSL https://repo.continuum.io/miniconda/Miniconda-3.16.0-Linux-armv7l.sh -o /tmp/miniconda.sh
bash /tmp/miniconda.sh -bfp /home/pi/miniconda3
sudo rm -rf /tmp/miniconda.sh
echo 'export PATH="/home/pi/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
conda install -y python=2
conda update conda
pip install feedparser
pip install pyyaml
pip install slackclient
pip install tweepy

# Install sqlite3 client app
sudo apt-get install sqlitebrowser