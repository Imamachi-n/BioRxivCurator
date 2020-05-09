"biorxivWatch" is a python-based tool for filtering biorxiv RSS feed and sending notification to SNS (Twitter, slack). 
Filtering based on...
- Altmetric score
- field (biorxiv-based)
- Keywords
- Authors

Developing/testing environment: 
- Python3.7 on Win10
- slack app


From the original repository (BiorxivCurator, https://github.com/Imamachi-n/BioRxivCurator)
-----------------------------------------------------------------------------------------
# BioRxivCurator

BioRxiv article curation batch scripts using Altmetrics data.  
Altmetrics data is provided by Altmetric.com, a research metrics company who track and collect the online conversations around millions of scholarly outputs.
Further information about how the Altmetric Attention Score is calculated is available [here](https://www.altmetric.com/about-altmetrics/the-donut-and-score/).

## Sample Twitter bot

The following twitter account is a sample bot for tweeting curated BioRxiv articles using Altmetrics data.  
https://twitter.com/BioRxivCurator

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
rss_categories is set to several categories. Check adaptive categories for BioRxiv RSS feed.  
https://www.biorxiv.org/alertsrss

The values of slack_token, slack_channel, twitter_consumer_key, twitter_consumer_secret, twitter_access_token and twitter_access_token_secret are replaced with yours.

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

-----------------------------------------------------------------------------------------
