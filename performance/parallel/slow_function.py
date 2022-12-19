import math
import sys
import argparse
import multiprocessing

import numpy as np

DASK_RUNNING = False

def slow_function(start: float) -> float:
    res = 0
    for i in range(int(math.pow(start, 7))):
        res += math.atan(i) * math.atan(i)
    return res


def get_sample():
    data = {'value': np.random.random(500) + 5}
    return data


def run_default():
    import pandas as pd

    sample = pd.DataFrame(get_sample())
    sample['results'] = sample['value'].apply(slow_function)
    print("Default results:\n", sample.tail(5))


def run_multiprocessing():
    import pandas as pd

    sample = pd.DataFrame(get_sample())
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(slow_function, sample['value'])
    sample['results'] = results
    print("Multiprocessing results:\n", sample.tail(5))


def run_joblib():
    import pandas as pd
    from joblib import Parallel, delayed

    sample = pd.DataFrame(get_sample())
    results = Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(slow_function)(i) for i in sample['value']
            )
    sample['results'] = results
    print("joblib results:\n", sample.tail(5))


def run_dask():
    import pandas as pd
    import dask.dataframe as dd

    global DASK_RUNNING

    if not DASK_RUNNING:
        from dask.distributed import Client, LocalCluster
        cluster = LocalCluster()  # Launches a scheduler and workers locally
        client = Client(cluster)  # Connect to distributed cluster and override default
        print(f"Started cluster at {cluster.dashboard_link}")
        DASK_RUNNING = True

    sample = pd.DataFrame(get_sample())
    
    dask_sample = dd.from_pandas(sample, npartitions=multiprocessing.cpu_count())
    dask_sample['results'] = dask_sample['value'].apply(slow_function, meta=('value', 'float64')).compute()

    print("Dask results:\n", dask_sample.tail(5))



def run_modin():
    global DASK_RUNNING
    
    import os

    os.environ["MODIN_ENGINE"] = "dask"  # Modin will use Dask

    if not DASK_RUNNING:
        from dask.distributed import Client, LocalCluster
        cluster = LocalCluster()  # Launches a scheduler and workers locally
        client = Client(cluster)  # Connect to distributed cluster and override default
        print(f"Started cluster at {cluster.dashboard_link}")
        DASK_RUNNING = True

    import modin.pandas as pd
    sample = pd.DataFrame(get_sample())
    sample['results'] = sample['value'].apply(slow_function)
    print("Modin results:\n", sample.tail(5))


def run_swifter():
    global DASK_RUNNING
    
    import os

    if not DASK_RUNNING:
        from dask.distributed import Client, LocalCluster
        cluster = LocalCluster()  # Launches a scheduler and workers locally
        client = Client(cluster)  # Connect to distributed cluster and override default
        print(f"Started cluster at {cluster.dashboard_link}")
        DASK_RUNNING = True

    import pandas as pd
    import swifter

    sample = pd.DataFrame(get_sample())
    sample['results'] = sample['value'].swifter.apply(slow_function)
    print("Swifter results:\n", sample.tail(5))


def run_pandarallel():
    from pandarallel import pandarallel

    pandarallel.initialize()

    import pandas as pd
    sample = pd.DataFrame(get_sample())
    sample['results'] = sample['value'].parallel_apply(slow_function)
    print("Pandarallel results:\n", sample.tail(5))


def run_pyspark():

    import pyspark.pandas as ps

    sample = ps.DataFrame(get_sample())
    sample['results'] = sample['value'].apply(slow_function)
    print("PySpark results:\n", sample.tail(5))


def main():
    parser = argparse.ArgumentParser("slow_function")
    parser.add_argument("type", choices=["default",
                                         "multiprocessing",
                                         "joblib",
                                         "dask",
                                         "modin",
                                         "swifter",
                                         "pandarallel",
                                         "pyspark"])
   
    args = parser.parse_args()

    if args.type == "default":
        run_default()
    elif args.type == "multiprocessing":
        run_multiprocessing()
    elif args.type == "joblib":
        run_joblib()
    elif args.type == "dask":
        run_dask()
    elif args.type == "modin":
        run_modin()
    elif args.type == "swifter":
        run_swifter()
    elif args.type == "pandarallel":
        run_pandarallel()
    elif args.type == "pyspark":
        run_pyspark()
    else:
        print(f"{args.type} is not supported")
        sys.exit(1)

if __name__ == '__main__':
    main()

