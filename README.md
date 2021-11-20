[![Scrape Eliteprospects for team rosters](https://github.com/katzefudder/elite_scrape/actions/workflows/scrape_elite.yml/badge.svg)](https://github.com/katzefudder/elite_scrape/actions/workflows/scrape_elite.yml)

# Scrape using Python and scrapy

## Use virtual environment
python3 -m venv venv
source ./venv/bin/activate

## Install scrapy
venv/bin/pip3 install scrapy

## scrape URL to extract roster
scrapy shell https://www.eliteprospects.com/team/677/esv-kaufbeuren

## run scrapy spider
scrapy runspider elitescrape/elitescrape/spiders/teams_del2.py
