"""
sortedcontainers.sortedlist source code:
https://grantjenks.com/docs/sortedcontainers/sortedlist.html
"""
import sortedcontainers.sortedlist as sortedlist
import time
import random
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def measure_times(datastructure, dataset):
    """
    Measures the run time of a function for different sizes of input
    :param datastructure: Data structure to measure
    :param dataset: Dictionary mapping size of input to list of run times
    """
    start = 0
    end = 0
    random.seed(0)
    n = 10
    while True:
        arr = [random.randint(0, n) for _ in range(n)]
        if dataset.get(n) == None:
            dataset[n] = []
        if type(datastructure) == dict:
            start = time.time()
            for i in arr:
                datastructure[i] = i
            end = time.time()
            dataset[n].append((end - start) / n) # Average time per element
        else:
            start = time.time()
            for i in arr:
                datastructure.add(i)
            end = time.time()
            dataset[n].append((end - start) / n)
        n = n**2
        if end - start >=3:
            print(type(datastructure),"  n: ",n)
            break
            
        # print result
        #print(type(datastructure),"  Data Set: ",dataset)

if __name__ == "__main__":
    hashtable = {}
    multiset = sortedlist.SortedList()

    hashtable_times = {}
    multiset_times = {}

    for i in range(10):
        measure_times(hashtable, hashtable_times)
        hashtable = {}
        measure_times(multiset, multiset_times)
        multiset = sortedlist.SortedList()

    # Plot results
    df = pd.DataFrame.from_dict(hashtable_times, orient='index')
    df = df.transpose()
    df = df.melt(var_name='n', value_name='time')
    df['n'] = df['n'].astype(int)
    df['time'] = df['time'].astype(float)
    sns.lineplot(x='n', y='time', data=df)
    plt.title('Hash Table Insertion Time')
    plt.savefig('ht.png')
    plt.clf()

    df = pd.DataFrame.from_dict(multiset_times, orient='index')
    df = df.transpose()
    df = df.melt(var_name='n', value_name='time')
    df['n'] = df['n'].astype(int)
    df['time'] = df['time'].astype(float)
    sns.lineplot(x='n', y='time', data=df)
    plt.title('Binary Search Tree Insertion Time ')
    plt.savefig('bt.png')
    plt.clf()
