
import subprocess
import os

DIR = '/home/mac/Work/Mac/github-repo/scrapers/repovis/repovis'
SCRAPY = '/home/mac/anaconda2/bin/scrapy'
DIRNAME = os.path.dirname(__file__)
SPIDER = os.path.join(DIRNAME, 'spiders/fetch_repo_spider.py')

os.chdir(DIR)

subprocess.Popen(SCRAPY + ' runspider ' + SPIDER, shell=True)
