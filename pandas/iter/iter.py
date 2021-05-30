#!/usr/bin/env python

import doctest
import argparse
from datetime import datetime, timedelta
from dataclasses import dataclass

import perfplot 

import pandas as pd
import numpy as np
from faker import Faker

from iter import score_cython

fake = Faker()

@dataclass
class Customer:
    first_name: str
    last_name: str
    start_date: datetime
    end_date: datetime
    city: str
    state: str
    zipcode: str
    balance: int


def score_customer(customer:Customer) -> str:
    """Give a customer a credit score.
    >>> score_customer(Customer("Joe", "Smith", datetime(2020, 1, 1), datetime(2023,1,1), "Chicago", "Illinois", 66666, -5))
    'F'
    >>> score_customer(Customer("Joe", "Smith", datetime(2020, 1, 1), datetime(2023,1,1), "Chicago", "Illinois", 66666, 50))
    'C'
    >>> score_customer(Customer("Joe", "Smith", datetime(2021, 1, 1), datetime(2023,1,1), "Chicago", "Illinois", 66666, 50))
    'D'
    >>> score_customer(Customer("Joe", "Smith", datetime(2021, 1, 1), datetime(2023,1,1), "Chicago", "Illinois", 66666, 150))
    'C'
    >>> score_customer(Customer("Joe", "Smith", datetime(2021, 1, 1), datetime(2023,1,1), "Chicago", "Illinois", 66666, 250))
    'B'
    >>> score_customer(Customer("Joe", "Smith", datetime(2021, 1, 1), datetime(2023,1,1), "Chicago", "Illinois", 66666, 350))
    'B'
    >>> score_customer(Customer("Joe", "Smith", datetime(2021, 1, 1), datetime(2023,1,1), "Santa Fe", "California", 88888, 350))
    'A'
    >>> score_customer(Customer("Joe", "Smith", datetime(2020, 1, 1), datetime(2023,1,1), "Santa Fe", "California", 88888, 50))
    'C'
    """
    if customer.balance < 0:
        return 'F'
    if customer.balance > 500:
        return 'A'
    # legacy vs. non-legacy
    if customer.start_date > datetime(2020, 1, 1):
        if customer.balance < 100:
            return 'D'
        elif customer.balance < 200:
            return 'C'
        elif customer.balance < 300:
            return 'B'
        else:
            if customer.state in ['Illinois', 'Indiana']:
                return 'B'
            else:
                return 'A'
    else:
        if customer.balance < 100:
            return 'C'
        else:
            return 'A'

def vectorized_score(df):
    return np.select([df['balance'] < 0,
                      df['balance'] > 500, # technically not needed, would fall through
                      ((df['start_date'] > datetime(2020,1,1)) &
                       (df['balance'] < 100)),
                      ((df['start_date'] > datetime(2020,1,1)) &
                       (df['balance'] >= 100) &
                       (df['balance'] < 200)),
                      ((df['start_date'] > datetime(2020,1,1)) &
                       (df['balance'] >= 200) &
                       (df['balance'] < 300)),
                      ((df['start_date'] > datetime(2020,1,1)) &
                       (df['balance'] >= 300) &
                       df['state'].isin(['Illinois', 'Indiana'])),
                      ((df['start_date'] >= datetime(2020,1,1)) &
                       (df['balance'] < 100)),
                     ], # conditions
                     ['F',
                      'A',
                      'D',
                      'C',
                      'B',
                      'B',
                      'C'], # choices
                     'A') # default score

def score_customer_attributes(balance:int, start_date:datetime, state:str) -> str:
    if balance < 0:
        return 'F'
    if balance > 500:
        return 'A'
    # legacy vs. non-legacy
    if start_date > datetime(2020, 1, 1):
        if balance < 100:
            return 'D'
        elif balance < 200:
            return 'C'
        elif balance < 300:
            return 'B'
        else:
            if state in ['Illinois', 'Indiana']:
                return 'B'
            else:
                return 'A'
    else:
        if balance < 100:
            return 'C'
        else:
            return 'A'

def vec(df):
    df['score'] = vectorized_score(df)
    return df['score']

def list_comp(df):
    df['score'] = [score_customer_attributes(*a) for a in zip(df['balance'], df['start_date'], df['state'])]
    return df['score']

def apply(df):
    df['score'] = df.apply(score_customer, axis=1)
    return df['score']

def iterrows(df):
    df['score'] = [score_customer(r[1]) for r in df.iterrows()] 
    return df['score']

def itertuples(df):
    df['score'] = [score_customer(t) for t in df.itertuples()] 
    return df['score']

def cython_iter(df):
    df['score'] = score_cython(df)
    return df['score']

def iloc_iter(df):
    df['score'] = [score_customer(df.iloc[i]) for i in range(len(df))]
    return df['score']

def make_dataframe(n):
    today = datetime.now()
    next_month = today + timedelta(days=30)
    df = pd.DataFrame([[fake.first_name(), fake.last_name(),
                        fake.date_this_decade(), fake.date_between_dates(today, next_month),
                        fake.city(), fake.state(), fake.zipcode(), fake.random_int(-100,1000)]
                      for r in range(n)],
                      columns=['first_name', 'last_name', 'start_date', 'end_date', 'city', 'state', 'zipcode', 'balance'])
    
    
    df['start_date'] = pd.to_datetime(df['start_date']) # convert to datetimes
    df['end_date'] = pd.to_datetime(df['end_date'])
    return df

def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-t', '--test', action='store_true', help='run unit test')
    argp.add_argument('-v', '--verify', action='store_true', help='verify equality of methods')

    args = argp.parse_args()

    kernels = [vec, list_comp, apply, iterrows, itertuples, cython_iter, iloc_iter]

    if args.test:
        print(doctest.testmod())
    elif args.verify:
        df = make_dataframe(100)
        v = kernels[0](df)
        for k in kernels[1:]:
            assert (v == k(df)).all(), f"{k.__name__} doesn't match"
    else:
       perfplot.show(
               setup=lambda n: make_dataframe(n),
               kernels=kernels,
               labels=[str(k.__name__) for k in kernels],
               n_range=[2**k for k in range(16)],
               xlabel='N',
               logx=True,
               logy=True,
               equality_check=False
               )

if __name__ == '__main__':
    main()
