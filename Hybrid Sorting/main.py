import time
import random
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def quicksort_hybrid(data, k):
    """
    https://github.com/sidb70/CSE-331/blob/main/Projects/Project%204%20Sorting%20algorithms/solution.py
    Sorts a list in place using a hybrid of quicksort and insertion sort
    :param data: Data to sort
    :param k: Threshold for switching to insertion sort
    """

    def quicksort_inner(first, last):
        """
        Sorts portion of list at indices in interval [first, last] using quicksort
        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        if right - left < k:
            insertion_sort(data[left:right + 1])
            return
        
        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]
        # First and last elements are already on right side of pivot since they are sorted
        left += 1
        right -= 1

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1
            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1
        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)

def insertion_sort(arr):
    """
    In place implementation of insertion sort
    :param arr: List of integers
    :return: Sorted list of integers
    """
    for i in range(len(arr)):
        curr = arr[i]
        j = i
        while j > 0 and arr[j - 1] > curr:
            arr[j] = arr[j - 1]
            j -= 1
        arr[j] = curr  
def measure_hybrid_sort(k, runtimes):
    """
    Measures the run time of hybrid sort on lists of random integers of size n
    :param function: Function to measure
    :param sizes: Dictionary mapping size of input to list of run times
    """
     # 
    random.seed(0)
    for size in runtimes[k].keys():
        arr = [random.randint(0, 1000) for _ in range(size)]
        start = time.time()
        quicksort_hybrid(arr,k)
        end = time.time()
        runtimes[k][size].append((end - start)/size)
if __name__ == '__main__':
    hybrid_sort_runtimes = {}
    for i in range(5,21):
        hybrid_sort_runtimes[i*5] = {10:[],15:[],20:[],30:[], 40:[], 50: [],100:[],200:[]}
    for k in hybrid_sort_runtimes.keys():
        measure_hybrid_sort(k, hybrid_sort_runtimes)
        #print results for each k
        print("k = ", k)
        for size in hybrid_sort_runtimes[k].keys():
            print("n = ", size, "average time/element = ", sum(hybrid_sort_runtimes[k][size])/len(hybrid_sort_runtimes[k][size]))


    #plot results
    for k in hybrid_sort_runtimes.keys():
        for size in hybrid_sort_runtimes[k].keys():
            hybrid_sort_runtimes[k][size] = sum(hybrid_sort_runtimes[k][size])/len(hybrid_sort_runtimes[k][size])
    df = pd.DataFrame(hybrid_sort_runtimes)
    df = df.transpose()
    df = df.reset_index()
    df = df.melt(id_vars=['index'], value_vars=[10,15,20,30,40,50,100,200])
    df.columns = ['k', 'n', 'time/element']
    sns.lineplot(data=df, x='n', y='time/element', hue='k')
    plt.savefig('hybrid_sort.png')
    plt.show()

    


