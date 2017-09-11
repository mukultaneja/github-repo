
import os
import pandas as pd
from odo import odo


def get_engine_string():
    '''
    Function
    '''
    db_string = os.path.abspath('db/repos.db')
    engine_string = 'sqlite:///' + db_string

    return engine_string


def get_repos():
    '''
    Function
    '''
    engine_string = get_engine_string()
    repos = odo(engine_string + '::repos', pd.DataFrame)
    meta = odo(engine_string + '::languages', pd.DataFrame)
    data = pd.merge(repos, meta, left_on=['id'], right_on=['repo_id'])
    data = data[['name', 'full_name', 'language', 'value']]
    data = data.groupby(['language']).sum()
    data.sort_values(by=['value'], ascending=False, inplace=True)
    data = data.reset_index()

    return data.to_json(orient='records')
