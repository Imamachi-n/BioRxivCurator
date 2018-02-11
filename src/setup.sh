#!/bin/bash
curl -sSL https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -o /tmp/miniconda.sh
bash /tmp/miniconda.sh -bfp /usr/local
rm -rf /tmp/miniconda.sh
conda install -y python=2
conda update conda
conda config --add channels r
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
conda install feedparser
conda install sqlite3
conda install pyyaml
conda install slackclient
conda install tweepy
