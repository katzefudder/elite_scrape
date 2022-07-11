[![Scrape Eliteprospects for team rosters](https://github.com/katzefudder/elite_scrape/actions/workflows/run_spiders.yml/badge.svg)](https://github.com/katzefudder/elite_scrape/actions/workflows/run_spiders.yml)

# Scrape using Python and scrapy

## Use virtual environment
python3 -m venv venv
source ./venv/bin/activate

## Install requirements
venv/bin/pip3 install -r requirements.txt

## run scrapy spider
scrapy runspider elitescrape/spiders/spider_del.py
