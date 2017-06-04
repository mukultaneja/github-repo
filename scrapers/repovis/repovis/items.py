# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import os
import logging
from datetime import datetime as dt
import scrapy
import pandas as pd
from odo import odo
from sqlalchemy import create_engine


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

    def get_st_point(self):
        '''
        Function
        '''
        repo_id = None
        try:
            with open('st_point.txt') as st_point:
                repo_id = st_point.readline()
        except IOError:
            return None

        return int(repo_id)

    def set_st_point(self, repo_id):
        '''
        Function
        '''
        with open('st_point.txt', 'w') as st_point:
            st_point.write(repo_id)

    def process_response(self, response):
        '''
        Function
        '''
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

        try:
            owners.drop('Unnamed: 0', inplace=True, axis=1)
            repos.drop('Unnamed: 0', inplace=True, axis=1)
        except ValueError:
            pass

        self.store_public_repos(repos, owners)


    def store_public_repos(self, repos, owners):
        '''
        Function
        '''
        if len(owners) > 0:
            odo(owners, ENGINE_STRING + '::owners')
        if len(repos) > 0:
            odo(repos, ENGINE_STRING + '::repos')

        last_repo_record = RepovisItem.connection.execute(
            "SELECT max(id) from repos")
        last_owner_record = RepovisItem.connection.execute(
            "SELECT max(id) from owners")
        last_repo_id = [row[0] for row in last_repo_record][0]
        last_owner_id = [row[0] for row in last_owner_record][0]

        log_repo_id = 'records in repos: {}'.format(last_repo_id)
        log_owner_id = 'records in owners: {}'.format(last_owner_id)

        logging.info(log_repo_id)
        logging.info(log_owner_id)


    def store_languages(self, response, repo_id):
        '''
        Function
        '''
        meta = pd.DataFrame([response])
        meta = meta.T
        meta = meta.reset_index()
        meta.columns = ['language', 'value']
        meta['repo_id'] = repo_id
        odo(meta, ENGINE_STRING + '::languages')

    def store_forks(self, forks, repo_id):
        '''
        Function
        '''
        meta = pd.DataFrame({'repo_id': [repo_id],
                             'forks': [forks]})

        odo(meta, ENGINE_STRING + '::forks')

    def store_stargazers(self, stargazers, repo_id):
        '''
        Function
        '''
        meta = pd.DataFrame({'repo_id': [repo_id],
                             'stargazers': [stargazers]})

        odo(meta, ENGINE_STRING + '::stargazers')

    def store_contributors(self, contributors, repo_id):
        '''
        Function
        '''
        meta = pd.DataFrame({'repo_id': [repo_id],
                             'contributors': [contributors]})

        odo(meta, ENGINE_STRING + '::contributors')

    def store_meta_data(self, key, res, repo_id):
        '''
        Function
        '''
        if key == 'forks':
            self.store_forks(res, repo_id)
        elif key == 'languages':
            self.store_languages(res, repo_id)
        elif key == 'stargazers':
            self.store_stargazers(res, repo_id)
        else:
            self.store_contributors(res, repo_id)
