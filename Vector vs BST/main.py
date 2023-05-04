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
    Measures the run time of a function for different sizes of input and stores the results in a dictionary.
    :param datastructure: Data structure to measure
    :param dataset: Dictionary mapping size of input to list of run times 
    """
    
    start = 0
    end = 0
    random.seed(0)
    n = 10
    while end - start < 3:
        # Increase size of input
        n = n*10
        # Generate random array of size n
        arr = [random.randint(0, n) for _ in range(n)]
        
        if dataset.get(n) == None:
            dataset[n] = []
        # Measure run time if data structure is a multiset
        if type(datastructure) == sortedlist.SortedList:
            start = time.time()
            for i in arr:
                datastructure.add(i)
            end = time.time()
            # Store run time
            dataset[n].append((end - start)/n)

        # Measure run time if data structure is a vector
        else:
            start = time.time()
            for i in arr:
                # Run binary search to find index to insert element
                left = 0
                right = len(datastructure) - 1
                mid = 0
                while left <= right:
                    mid = (left + right) // 2
                    if datastructure[mid] < i:
                        left = mid + 1
                    elif datastructure[mid] > i:
                        right = mid - 1
                    else:
                        break
                # Insert element
                datastructure.insert(mid, i)
            end = time.time()
            # Store run time
            dataset[n].append((end - start)/n)


    print(type(datastructure),"  n: ",n)
            

if __name__ == "__main__":
    # Data structures
    multiset = sortedlist.SortedList()
    vector = []

    # Dictionary mapping size of input to list of run times
    vector_times = {}
    multiset_times = {}

    for i in range(10):
        # Measure run times
        measure_times(vector, vector_times)
        measure_times(multiset, multiset_times)

        # Reset data structures
        vector = []
        multiset = sortedlist.SortedList()

    # Plot results
    df = pd.DataFrame.from_dict(vector_times, orient='index')
    df = df.transpose()
    df = df.melt(var_name='n', value_name='time')
    df['n'] = df['n'].astype(int)
    df['time'] = df['time'].astype(float)
    sns.lineplot(x='n', y='time', data=df)
    plt.title('Vector with Binary Search Insertion Time')
    plt.ylabel('Time (s)')
    plt.savefig('vector_insertion.png')
    plt.clf()

    df = pd.DataFrame.from_dict(multiset_times, orient='index')
    df = df.transpose()
    df = df.melt(var_name='n', value_name='time')
    df['n'] = df['n'].astype(int)
    df['time'] = df['time'].astype(float)
    sns.lineplot(x='n', y='time', data=df)
    plt.title('Binary Search Tree Insertion Time ')
    plt.savefig('bst_insertion.png')
    plt.clf()
