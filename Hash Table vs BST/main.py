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
    while end - start < 3:
        # Generate random array of size n
        arr = [random.randint(0, n) for _ in range(n)]
        
        if dataset.get(n) == None:
            dataset[n] = []
        
        # Measure run time if data structure is a dictionary
        if type(datastructure) == dict:
            start = time.time()
            for i in arr:
                datastructure[i] = i
            end = time.time()
            dataset[n].append((end - start) / n) # Average time per element
        # Measure run time if data structure is a sorted list
        else:
            start = time.time()
            for i in arr:
                datastructure.add(i)
            end = time.time()
            dataset[n].append((end - start) / n)
        # Increase size of input
        n = n*10
    print(type(datastructure),"  n: ",n)
            

if __name__ == "__main__":
    # Data structures
    hashtable = {}
    multiset = sortedlist.SortedList()

    # Dictionary mapping size of input to list of run times
    hashtable_times = {}
    multiset_times = {}

    for i in range(10):
        # Measure run times
        measure_times(hashtable, hashtable_times)
        measure_times(multiset, multiset_times)

        # Reset data structures
        hashtable = {}
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
