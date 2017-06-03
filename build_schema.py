
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, ForeignKey


def main():
  '''
  Function: main
  '''
  if not os.path.exists('db/'):
    os.makedirs('db')
  engine = create_engine('sqlite:///db/repos.db')
  connection = engine.connect()
  metadata = MetaData()
  repos = Table('repos',
                metadata,
                Column('collaborators_url', String(500),
                       nullable=False, autoincrement=False),
                Column('contributors_url', String(500),
                       nullable=False, autoincrement=False),
                Column('stargazers_url', String(500),
                       nullable=False, autoincrement=False),
                Column('fork', Boolean, default=False, nullable=False,
                       autoincrement=False),
                Column('fork_url', String(500),
                       nullable=False, autoincrement=False),
                Column('full_name', String(100),
                       nullable=False, autoincrement=False),
                Column('html_url', String(500),
                       nullable=False, autoincrement=False),
                Column('description', String(2000),
                       nullable=True, autoincrement=False),
                Column('id', Integer, nullable=False),
                Column('languages_url', String(500),
                       nullable=False, autoincrement=False),
                Column('name', String(100), nullable=False,
                       autoincrement=False),
                Column('trees_url', String(500),
                       nullable=False, autoincrement=False),
                Column('scrapped_time', String(500),
                       nullable=False, autoincrement=False)
                )

  owners = Table('owners',
                 metadata,
                 Column('avatar_url', String(500),
                        nullable=False, autoincrement=False),
                 Column('events_url', String(500),
                        nullable=False, autoincrement=False),
                 Column('followers_url', String(500),
                        nullable=False, autoincrement=False),
                 Column('following_url', String(500),
                        nullable=False, autoincrement=False),
                 Column('gists_url', String(500),
                        nullable=False, autoincrement=False),
                 Column('gravatar_id', String(200),
                        nullable=True, autoincrement=False),
                 Column('html_url', String(500),
                        nullable=False, autoincrement=False),
                 Column('id', Integer, nullable=False),
                 Column('login', String(100),
                        nullable=False, autoincrement=False),
                 Column('organizations_url',
                        String(500), nullable=False, autoincrement=False),
                 Column('received_events_url',
                        String(500), nullable=False, autoincrement=False),
                 Column('repos_url', String(500),
                        nullable=False, autoincrement=False),
                 Column('site_admin',
                        Boolean, default=False, nullable=False,
                        autoincrement=False),
                 Column('starred_url',
                        String(500), nullable=False, autoincrement=False),
                 Column('subscriptions_url',
                        String(500), nullable=False, autoincrement=False),
                 Column('type',
                        String(500), nullable=False, autoincrement=False),
                 Column('url',
                        String(500), nullable=False, autoincrement=False),
                 Column('repo_id', Integer,
                        nullable=False, autoincrement=False),
                 )

  languages = Table('languages',
                    metadata,
                    Column('repo_id', Integer,
                           nullable=False),
                    Column('language', String(100),
                           nullable=False, autoincrement=False),
                    Column('value', Integer,
                           nullable=False, autoincrement=False),
                    )

  forks = Table('forks',
                metadata,
                Column('repo_id', Integer,
                       nullable=False),
                Column('forks', Integer,
                       nullable=False, autoincrement=False),
                )

  contributors = Table('contributors',
                       metadata,
                       Column('repo_id', Integer,
                              nullable=False),
                       Column('contributors', Integer,
                              nullable=False, autoincrement=False),
                       )

  stargazers = Table('stargazers',
                     metadata,
                     Column('repo_id', Integer,
                            nullable=False),
                     Column('stargazers', Integer,
                            nullable=False, autoincrement=False),
                     )

  metadata.create_all(engine)

if __name__ == '__main__':
  main()
