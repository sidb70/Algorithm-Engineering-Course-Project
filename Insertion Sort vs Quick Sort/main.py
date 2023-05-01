import time
import random
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def quicksort(data):
    """
    https://github.com/sidb70/CSE-331/blob/main/Projects/Project%204%20Sorting%20algorithms/solution.py
    Sorts a list in place using quicksort
    :param data: Data to sort
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
def measure_times(function,sizes):
    """
    Measures the run time of a function for different sizes of input
    :param function: Function to measure
    :param sizes: Dictionary mapping size of input to list of run times
    """
     # 
    random.seed(0)
    for size in sizes.keys():
        arr = [random.randint(0, 1000) for _ in range(size)]
        start = time.time()
        function(arr)
        end = time.time()
        sizes[size].append((end - start)/size)
if __name__ == '__main__':
    # Create a dictionary mapping n to a list of run times for each algorithm
    quicksort_runtimes = {5: [],10:[],15:[],20:[],30:[], 40:[], 50: [],100:[],200:[]}
    insertion_sort_runtimes ={5: [],10:[],15:[],20:[],30:[],40:[], 50: [],100:[],200:[]}
    
    # Populate each algorithm's dictionary with 20 run time tests for each n value
    for i in range(20):
        measure_times(quicksort,quicksort_runtimes)
        measure_times(insertion_sort,insertion_sort_runtimes)
     
    # Master list of data to plot
    data = []
    # Loop over the n values and run times for quicksort
    for n, times in quicksort_runtimes.items():
        for time in times:
            data.append({'Algorithm': 'Quick Sort', 'n': n, 'Time per element': time})
    # Loop over the n values and run times for insertion sort
    for n, times in insertion_sort_runtimes.items():
        for time in times:
            data.append({'Algorithm': 'Insertion Sort', 'n': n, 'Time per element': time})

    # Create a pandas DataFrame from the list of data
    df = pd.DataFrame(data)
    # Create a seaborn swarmplot
    sns.swarmplot(x='n', y='Time per element', hue='Algorithm', data=df,size=1)
    plt.legend(title='Algorithm', loc='upper left')
    plt.xlabel('n')
    plt.ylabel('Run Time per element (microseconds)')
    plt.title('Comparison of Insertion Sort and Quick Sort Run Times')
    plt.show()