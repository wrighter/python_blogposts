import pandas as pd
import numpy as np

import logging

from faker import Faker

fake = Faker()

@profile
def function_with_issues(df):
    logging.debug(f'called with {df}') 
    def _get_first_name(n):
        return n.split()[0]
    def _get_last_name(n):
        return ' '.join(n.split()[1:])
    
    df['first'] = df['name'].apply(_get_first_name)
    df['last'] = df['name'].apply(_get_last_name)
    
    return df


if __name__ == '__main__':
        df = pd.DataFrame([(fake.name(), fake.phone_number()) for _ in range(1000)], columns=['name', 'phone'])
        function_with_issues(df)
