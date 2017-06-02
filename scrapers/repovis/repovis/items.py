# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import os
import logging
import scrapy
import pandas as pd
from odo import odo
from sqlalchemy import create_engine
import datetime
from datetime import datetime as dt

logging.basicConfig(level=logging.DEBUG)

DB_PATH = os.path.abspath('../../../db/repos.db')
ENGINE_STRING = 'sqlite:///{}'.format(DB_PATH)
SCRAPPED_FORMAT = '%Y-%m-%d %H:%M:%S'


class RepovisItem(scrapy.Item):
    '''
    Class
    '''
    engine = create_engine(ENGINE_STRING)
    connection = engine.connect()

    def get_last_id(self):
        '''
        Function
        '''
        query = 'SELECT max(id) FROM repos'
        result = RepovisItem.connection.execute(query)
        return [row[0] for row in result][0]

    def process_response(self, response):
        '''
        Function
        '''
        response = sorted(response, key=lambda row: row['id'])
        response_length = len(response)
        owners = pd.DataFrame()
        repos = pd.DataFrame()
        for row in response:
            repo_id = row['id']
            repo_name = row['name']
            repo_fullname = row['full_name']
            repo_html_url = row['html_url']
            repo_description = row['description']
            repo_fork = row['fork']
            repo_fork_url = row['forks_url']
            repo_collaborators_url = row['collaborators_url']
            repo_languages_url = row['languages_url']
            repo_trees_url = row['trees_url']
            repo_contributors_url = row['contributors_url']
            repo_stargazers_url = row['stargazers_url']
            row_series = {'id': [repo_id],
                          'name': [repo_name],
                          'full_name': [repo_fullname],
                          'html_url': [repo_html_url],
                          'description': [repo_description],
                          'fork': [repo_fork],
                          'fork_url': [repo_fork_url],
                          'collaborators_url': [repo_collaborators_url],
                          'languages_url': [repo_languages_url],
                          'trees_url': [repo_trees_url],
                          'contributors_url': [repo_contributors_url],
                          'stargazers_url': [repo_stargazers_url],
                          'scrapped_time': [dt.strftime(dt.now(),
                                                        SCRAPPED_FORMAT)]}
            repo = pd.DataFrame.from_dict(row_series)
            owner = pd.DataFrame([row['owner']])
            owner['repo_id'] = row['id']
            repos = repos.append(repo, ignore_index=True)
            owners = owners.append(owner, ignore_index=True)

        owners.fillna(' ')
        repos.fillna(' ')

        self.store_public_repos(repos, owners)

        return response[response_length - 1]['id']

    def store_public_repos(self, repos, owners):
        '''
        Function
        '''
        try:
            owners.drop('Unnamed: 0', inplace=True, axis=1)
            repos.drop('Unnamed: 0', inplace=True, axis=1)
        except ValueError:
            pass

        if len(owners) > 0 and len(repos) > 0:
            odo(owners, ENGINE_STRING + '::owners')
            odo(repos, ENGINE_STRING + '::repos')

        last_repo_record = RepovisItem.connection.execute(
            "SELECT max(id) from repos")
        last_owner_record = RepovisItem.connection.execute(
            "SELECT max(id) from owners")
        last_repo_id = [row[0] for row in last_repo_record][0]
        last_owner_id = [row[0] for row in last_owner_record][0]

        logging.info('records in repos: {}'.format(last_repo_id))
        logging.info('records in owners: {}'.format(last_owner_id))

        self.store_records(last_repo_id, last_owner_id)

    def store_records(self, last_repo_id, last_owner_id):
        '''
        Function
        '''
        if os.path.isfile('reports.csv'):
            reports = pd.read_csv('reports.csv', index_col=False)
            try:
                reports.drop('Unnamed: 0', inplace=True, axis=1)
            except ValueError:
                pass
            temp = pd.DataFrame({'repo_id': [last_repo_id],
                                 'owner_id': [last_owner_id]})
            reports = reports.append(temp, ignore_index=True)
        else:
            reports = pd.DataFrame({'repo_id': [last_repo_id],
                                    'owner_id': [last_owner_id]})
        reports.to_csv('reports.csv')

    def store_repo_languages(self, response, repo_id):
        '''
        Function
        '''
        meta = pd.DataFrame([response])
        meta = meta.T
        meta = meta.reset_index()
        meta.columns = ['language', 'value']
        meta['repo_id'] = repo_id
        odo(meta, ENGINE_STRING + '::languages')

    def store_repo_forks(self, forks, repo_id):
        '''
        Function
        '''
        meta = pd.DataFrame({'repo_id': [repo_id],
                             'forks': [forks]})

        odo(meta, ENGINE_STRING + '::forks')

    def store_repo_stargazers(self, stargazers, repo_id):
        '''
        Function
        '''
        meta = pd.DataFrame({'repo_id': [repo_id],
                             'stargazers': [stargazers]})

        odo(meta, ENGINE_STRING + '::stargazers')

    def store_repo_contributors(self, contributors, repo_id):
        '''
        Function
        '''
        meta = pd.DataFrame({'repo_id': [repo_id],
                             'contributors': [contributors]})

        odo(meta, ENGINE_STRING + '::contributors')
