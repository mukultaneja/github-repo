
import subprocess
import os

DIR = '/home/mac/Work/Mac/github-repos/scrapers/repovis/repovis'
SCRAPY = '/home/mac/anaconda2/bin/scrapy'
DIRNAME = os.path.dirname(__file__)
SPIDER = os.path.join(
    DIRNAME, 'spiders/fetch_repo_spider.py -s JOBDIR=spider_states/repo_spider')

os.chdir(DIR)

subprocess.Popen(SCRAPY + ' runspider ' + SPIDER, shell=True)
