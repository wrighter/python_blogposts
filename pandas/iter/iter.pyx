import numpy as np
cimport numpy as np

import datetime

cutoff = datetime.datetime(2020, 1, 1)

def score_cython(df):
    """Note, this is not an optimized version, but is just
    a naive application of using cython to iterate through
    a DataFrame. As you can see in the results, this is
    not a reasonable way to solve this problem."""
    columns = dict(zip(df.columns,
        [x for x in range(len(df.columns))]))

    cdef Py_ssize_t i
    cdef np.ndarray[object, ndim=2] vals = df.values

    cdef Py_ssize_t balance = columns['balance']
    cdef Py_ssize_t start_date = columns['start_date']
    cdef Py_ssize_t state  = columns['state']

    out = []

    i = 0
    while i < df.shape[0]:
        r_balance = vals[i, balance]
        if r_balance < 0:
            out.append('F')
        elif r_balance > 500:
            out.append('A')
        else:
            r_start_date = vals[i, start_date]
            if r_start_date > cutoff:
                if r_balance < 100:
                    out.append('D')
                elif r_balance < 200:
                    out.append('C')
                elif r_balance < 300:
                    out.append('B')
                else:
                    r_state = vals[i, state]
                    if r_state in ['Illinois', 'Indiana']:
                        out.append('B')
                    else:
                        out.append('A')
            else:
                if r_balance < 100:
                    out.append('C')
                else:
                    out.append('A')
        i += 1

    return out

