
import json
import logging
import re
from logging.handlers import RotatingFileHandler
import scrapy
from repovis.items import RepovisItem


def create_logger():
    '''
    Function
    '''
    logger = logging.getLogger("Rotating Log")
    if not len(logger.handlers):
        formatter = logging.Formatter(
            '%(asctime)s, %(levelname)s, %(message)s')
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler('logs/scrapers.logs', maxBytes=1024000,
                                      backupCount=5)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


class FetchPublicRepo(scrapy.Spider):
    '''
    Class
    '''
    name = 'fetchpublicrepo'
    visitem = RepovisItem()
    logger = create_logger()

    def build_url(self, url, repo_id):
        '''
        Function
        '''
        if url is None:
            url = 'https://api.github.com/repositories?since={}&'
        url += 'access_token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

        return url.format(repo_id)

    def start_requests(self):
        '''
        Function
        '''
        repo_id = FetchPublicRepo.visitem.get_st_point()
        repo_id = 1 if repo_id is None else repo_id
        url = self.build_url(url=None, repo_id=repo_id)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        Function
        '''
        process_response = FetchPublicRepo.visitem.process_response
        json_response = json.loads(response.text)
        json_response = sorted(json_response, key=lambda row: row['id'])
        link_url = re.search('\?since=\w+', response.headers['Link']).group(0)
        next_repo_id = int(link_url.split('=')[1])
        FetchPublicRepo.visitem.set_st_point('{}'.format(next_repo_id))
        process_response(json_response)
        logstr = None
        for row in json_response:
            repo_id = row['id']
            next_urls = {}
            next_urls['forks'] = row['forks_url']
            # next_urls['collaborators'] = row['collaborators_url']
            next_urls['languages'] = row['languages_url']
            next_urls['contributors'] = row['contributors_url']
            next_urls['stargazers'] = row['stargazers_url']

            # logging response status
            logstr = 'repo id = {}, URL = {}, Status = {}'.format(
                repo_id, row['html_url'], response.status)
            FetchPublicRepo.logger.info(logstr)

            # fetch all the meta data related to specific repo
            for key, url in next_urls.iteritems():
                url = self.build_url(url=url + '?', repo_id=repo_id)
                yield scrapy.Request(url=url,
                                     callback=self.parse_next_url,
                                     meta={'repo_id': repo_id,
                                           'key': key})


    def parse_next_url(self, response):
        '''
        Function
        '''
        repo_id = response.meta.get('repo_id')
        key = response.meta.get('key')
        store_meta_data = FetchPublicRepo.visitem.store_meta_data
        res = None
        if response.status == 200:
            res = json.loads(response.text) if key == 'languages' else len(
                json.loads(response.text))
        else:
            res = {} if key == 'languages' else 0

        # logging response status
        logstr = 'repo id = {}, URL = {}, Status = {}'.format(
            repo_id, response.url, response.status)
        FetchPublicRepo.logger.info(logstr)

        store_meta_data(key, res, repo_id)
