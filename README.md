# BioRxivCurator

BioRxiv article curation batch scripts using Altmetric score.

## Requirements and Installation

### Raspberry Pi

I recommend using `setup.sh` script to set up your environment on Raspbian OS.
This script automatically create python environment and install sqlite3 client app.

```bash
$ sudo bash ./src/setup.py
```

I tested this script on Raspberry Pi 3 ModelB (Raspbian Stretch with Desktop).
The following show what to do in this script.

#### Installing python modules

```bash
$ pip install feedparser
$ pip install pyyaml
$ pip install slackclient
$ pip install tweepy
```

#### Installing sqlite3 client app(Option)

If you want to see stored data from a GUI, I recommend you to install sqlite3 client app named DB Browser for SQLite.

```bash
$ sudo apt-get install sqlitebrowser
```

## Preparation of slack and twitter access token

`./src/production.yaml` are needed to run BioRxivCurator.
The values of slack_token, slack_channel, twitter_consumer_key, twitter_consumer_secret, twitter_access_token and twitter_access_token_secret is replaced with yours.

```
rss_categories: ['genomics', 'bioinformatics']
slack_token: 'xxxxxxxx'
slack_channel: '@xxxxxxx'
twitter_consumer_key: xxxxxxxx
twitter_consumer_secret: xxxxxxxx
twitter_access_token: xxxxxxxx
twitter_access_token_secret: xxxxxxxx
```

## Basic Usage

Run BioRxivCurator following the main script.

```
$ python ./src/startup.sh
```
