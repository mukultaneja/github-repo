
import json
import time
import scrapy
from repovis.items import RepovisItem


class FetchPublicRepo(scrapy.Spider):
    '''
    Class
    '''
    name = 'fetchpublicrepo'
    visitem = RepovisItem()

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
        repo_id = FetchPublicRepo.visitem.get_last_id()
        repo_id = 1 if repo_id is None else repo_id
        url = self.build_url(url=None, repo_id=repo_id)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        Function
        '''
        process_response = FetchPublicRepo.visitem.process_response
        json_response = json.loads(response.text)
        max_id = process_response(json_response)
        for row in json_response:
            repo_id = row['id']
            next_urls = {}
            next_urls['forks'] = row['forks_url']
            # next_urls['collaborators'] = row['collaborators_url']
            next_urls['languages'] = row['languages_url']
            next_urls['contributors'] = row['contributors_url']
            next_urls['stargazers'] = row['stargazers_url']
            for key, url in next_urls.iteritems():
                url = self.build_url(url=url + '?', repo_id=repo_id)
                yield scrapy.Request(url=url,
                                     callback=self.parse_next_url,
                                     meta={'repo_id': repo_id,
                                           'key': key})

        url = self.build_url(url=None, repo_id=max_id)
        time.sleep(360)
        yield scrapy.Request(url=url, callback=self.parse)


    def parse_next_url(self, response):
        '''
        Function
        '''
        repo_id = response.meta.get('repo_id')
        key = response.meta.get('key')
        if key == 'forks':
            store_repo_forks = FetchPublicRepo.visitem.store_repo_forks
            store_repo_forks(len(json.loads(response.text)), repo_id)
        elif key == 'languages':
            store_repo_languages = FetchPublicRepo.visitem.store_repo_languages
            store_repo_languages(json.loads(response.text), repo_id)
        elif key == 'stargazers':
            store_repo_stargazers = FetchPublicRepo.visitem.store_repo_stargazers
            store_repo_stargazers(len(json.loads(response.text)), repo_id)
        else:
            store_repo_contributors = FetchPublicRepo.visitem.store_repo_contributors
            store_repo_contributors(len(json.loads(response.text)), repo_id)
