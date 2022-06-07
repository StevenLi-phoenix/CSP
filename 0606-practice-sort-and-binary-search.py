import random

from base import *  # 之前展示给您的我之前写的代码

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x  # pass and cause no error
    im.add("tqdm not found, use default", False)


# 尝试偷懒的写法
def org_sort_1(array: list) -> list:
    """
    build-in sorted
    :param array: list
    :return: list(sorted)
    """
    # log
    log.info("build-in list sort")
    return sorted(array)  # sort procedure : 就这一行


def org_sort_2(array: list) -> list:
    """
    build-in list sort
    :param array: list
    :return: list(sorted)
    """
    # log
    log.info("build-in list sort")
    array.sort()  # hhhhhhh
    return array


# 学习了一下不同的排序算法的时间复杂度
# https://www.programiz.com/dsa/sorting-algorithm

def bubbleSort(array: list) -> list:
    # Bubble sort
    """
    冒泡排序
    :param array: list
    :return: list(sorted)
    """
    """
    Bubble Sort Complexity
    Time Complexity	 
    Best	O(n)
    Worst	O(n**2)
    Average	O(n**2)
    Space Complexity	O(1)
    Stability	Yes
    """
    # log
    log.info("Bubble Sort")
    for i in range(len(array)):
        for j in range(0, len(array) - i - 1):
            # compare two adjacent elements
            # change > to < to sort in descending order
            if array[j] > array[j + 1]:
                # swapping elements if elements
                # are not in the intended order
                temp = array[j]
                array[j] = array[j + 1]
                array[j + 1] = temp
    return array


def bubbleSort_OPT(array: list) -> list:
    # Optimized Bubble sort
    """
    冒泡排序优化
    :param array: list
    :return: list(sorted)
    """
    """
    Optimized Bubble Sort Complexity
    smilar to Bubble Sort, but requires only several swaps which is not sgnificantly in terms of time complexity.
    """
    # log
    log.info("Optimized Bubble Sort")
    # loop through each element of array
    for i in range(len(array)):

        # keep track of swapping
        swapped = False

        # loop to compare array elements
        for j in range(0, len(array) - i - 1):

            # compare two adjacent elements
            # change > to < to sort in descending order
            if array[j] > array[j + 1]:
                # swapping occurs if elements
                # are not in the intended order
                temp = array[j]
                array[j] = array[j + 1]
                array[j + 1] = temp

                swapped = True

        # no swapping means the array is already sorted
        # so no need for further comparison
        if not swapped:
            break
    return array


# Selection sort in Python
def selectionSort(array: list) -> list:
    # Selection sort
    """
    选择排序
    :param array: list
    :return: list(sorted)
    """
    """
    Selection Sort Complexity
    Time Complexity	 
    Best	O(n**2)
    Worst	O(n**2)
    Average	O(n**2)
    Space Complexity	O(1)
    Stability	No
    """
    # log
    log.info("Selection Sort")
    size = len(array)
    for step in range(size):
        min_idx = step

        for i in range(step + 1, size):

            # to sort in descending order, change > to < in this line
            # select the minimum element in each loop
            if array[i] < array[min_idx]:
                min_idx = i

        # put min at the correct position
        (array[step], array[min_idx]) = (array[min_idx], array[step])
    return array


# Insertion sort in Python
def insertionSort(array: list) -> list:
    # Insertion sort
    """
    插入排序
    :param array: list
    :return: list(sorted)
    """
    """
    Insertion Sort Complexity
    Time Complexity	 
    Best	O(n)
    Worst	O(n**2)
    Average	O(n**2)
    Space Complexity	O(1)
    Stability	Yes
    """
    # log
    log.info("Insertion Sort")
    for step in range(1, len(array)):
        key = array[step]
        j = step - 1

        # Compare key with each element on the left of it until an element smaller than it is found
        # For descending order, change key<array[j] to key>array[j].
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j = j - 1

        # Place key at after the element just smaller than it.
        array[j + 1] = key
    return array


def mergeSort(array: list) -> list:
    # MergeSort
    """
    归并排序
    :param array: list
    :return: list(sorted)
    """
    """
    Merge Sort Complexity
    Time Complexity	 
    Best	O(n*log n)
    Worst	O(n*log n)
    Average	O(n*log n)
    Space Complexity	O(n)
    Stability	Yes
    """
    # log
    log.info("Merge Sort")
    if len(array) > 1:

        #  r is the point where the array is divided into two subarrays
        r = len(array) // 2
        L = array[:r]
        M = array[r:]

        # Sort the two halves
        mergeSort(L)
        mergeSort(M)

        i = j = k = 0

        # Until we reach either end of either L or M, pick larger among
        # elements L and M and place them in the correct position at A[p..r]
        while i < len(L) and j < len(M):
            if L[i] < M[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = M[j]
                j += 1
            k += 1

        # When we run out of elements in either L or M,
        # pick up the remaining elements and put in A[p..r]
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1

        while j < len(M):
            array[k] = M[j]
            j += 1
            k += 1
    return array


def quickSort_ENTRANCE(array: list) -> list:
    # Quick sort in Python
    """
    快速排序
    :param array: list
    :return: list(sorted)
    """
    """
    Quicksort Complexity
    Time Complexity	 
    Best	O(n*log n)
    Worst	O(n**2)
    Average	O(n*log n)
    Space Complexity	O(log n)
    Stability	No - 时间和归并排序相同，空间复杂度为O(log n)较低，所以在硬件条件有限下，比如超大数据集，可以使用快速排序。
    """
    # log
    log.info("Quick sort")

    # function to find the partition position
    def partition(array_PAR, low, high):

        # choose the rightmost element as pivot
        pivot = array_PAR[high]

        # pointer for greater element
        i = low - 1

        # traverse through all elements
        # compare each element with pivot
        for j in range(low, high):
            if array_PAR[j] <= pivot:
                # if element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1

                # swapping element at i with element at j
                (array_PAR[i], array_PAR[j]) = (array_PAR[j], array_PAR[i])

        # swap the pivot element with the greater element specified by i
        (array_PAR[i + 1], array_PAR[high]) = (array_PAR[high], array_PAR[i + 1])

        # return the position from where partition is done
        return i + 1

    # function to perform quicksort
    def quickSort(array_QS, low, high):
        if low < high:
            # find pivot element such that
            # element smaller than pivot are on the left
            # element greater than pivot are on the right
            pi = partition(array_QS, low, high)

            # recursive call on the left of pivot
            array_QS = quickSort(array_QS, low, pi - 1)

            # recursive call on the right of pivot
            array_QS = quickSort(array_QS, pi + 1, high)
        return array_QS

    return quickSort(array, 0, len(array) - 1)


def countingSort(array: list) -> list:
    # Counting sort
    """
    计数排序
    :param array: list
    :return: list(sorted)
    """
    """
    Complexity
    Time Complexity	 
    Best	O(n+k)
    Worst	O(n+k)
    Average	O(n+k)
    Space Complexity	O(max) # the space complexity is a big trouble
    Stability	Yes
    """
    # log
    log.info("countingSort")
    size = len(array)
    output = [0] * size

    # Initialize count array
    count = [0] * 10

    # Store the count of each elements in count array
    for i in range(0, size):
        count[array[i]] += 1

    # Store the cummulative count
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Find the index of each element of the original array in count array
    # place the elements in output array
    i = size - 1
    while i >= 0:
        output[count[array[i]] - 1] = array[i]
        count[array[i]] -= 1
        i -= 1

    # Copy the sorted elements into original array
    for i in range(0, size):
        array[i] = output[i]

    return array


# Radix Sort
# https://www.geeksforgeeks.org/radix-sort/
# Not writing this code, just reference
# This algorithm is based on counting sort
# because this algorithm works on digit by digit, it is better to use counting sort in python.
"""
Radix Sort Algorithm:
radixSort(array)
  d <- maximum number of digits in the largest element
  create d buckets of size 0-9
  for i <- 0 to d
    sort the elements according to ith place digits using countingSort

countingSort(array, d)
  max <- find largest element among dth place elements
  initialize count array with all zeros
  for j <- 0 to size
    find the total count of each unique digit in dth place of elements and
    store the count at jth index in count array
  for i <- 1 to max
    find the cumulative sum and store it in count array itself
  for j <- size down to 1
    restore the elements to array
    decrease count of each element restored by 1
"""
"""
Radix Sort Complexity
Time Complexity	 
Best	O(n+k)
Worst	O(n+k)
Average	O(n+k)
Space Complexity	O(max)
Stability	Yes
"""


def bucketSort(array: list) -> list:
    # Bucket Sort
    """
    桶排序
    :param array: list
    :return: list(sorted)
    """
    """
    Bucket Sort Complexity
    Time Complexity	 
    Best	O(n+k)
    Worst	O(n2)
    Average	O(n)
    Space Complexity	O(n+k)
    Stability	Yes
    """
    # log
    log.info("bucketSort")
    # re-arrange the array value to 0-1
    array_max = max(array)
    array = [i / array_max for i in array]

    bucket = []
    # Create empty buckets
    for i in range(len(array)):
        bucket.append([])

    # Insert elements into their respective buckets
    for j in array:
        index_b = int(10 * j)
        bucket[index_b].append(j)

    # Sort the elements of each bucket
    for i in range(len(array)):
        bucket[i] = sorted(bucket[i])

    # Get the sorted elements
    k = 0
    for i in range(len(array)):
        for j in range(len(bucket[i])):
            array[k] = bucket[i][j]
            k += 1
    return array


def heapSort_ENTRANCE(array: list) -> list:
    # Heap Sort
    """
    堆排序
    :param array: list
    :return: list(sorted)
    """
    """
    Heap Sort Complexity
    Time Complexity	 
    Best	O(nlog n)
    Worst	O(nlog n)
    Average	O(nlog n)
    Space Complexity	O(1)
    Stability	No
    """
    # log
    log.info("Heap Sort")

    def heapify(arr, n, i):
        # Find largest among root and children
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[i] < arr[l]:
            largest = l

        if r < n and arr[largest] < arr[r]:
            largest = r

        # If root is not largest, swap with largest and continue heapifying
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

        return arr

    def heapSort(arr):
        n = len(arr)

        # Build max heap
        for i in range(n // 2, -1, -1):
            arr = heapify(arr, n, i)

        for i in range(n - 1, 0, -1):
            # Swap
            arr[i], arr[0] = arr[0], arr[i]

            # Heapify root element
            arr = heapify(arr, i, 0)
        return arr

    return heapSort(array)


def shellSort(array: list) -> list:
    # Shell sort
    """
    希尔排序
    :param array: list
    :return: list(sorted)
    """
    """
    Shell Sort Complexity
    Time Complexity	 
    Best	O(nlog n)
    Worst	O(n**2)
    Average	O(nlog n)
    Space Complexity	O(1)
    Stability	No
    """
    # log
    log.info("Shell Sort")
    n = len(array)
    # Rearrange elements at each n/2, n/4, n/8, ... intervals
    interval = n // 2
    while interval > 0:
        for i in range(interval, n):
            temp = array[i]
            j = i
            while j >= interval and array[j - interval] > temp:
                array[j] = array[j - interval]
                j -= interval

            array[j] = temp
        interval //= 2
    return array


sort = lambda array: random.choice(
    [org_sort_1, org_sort_2, bubbleSort, selectionSort, insertionSort, mergeSort, quickSort_ENTRANCE, heapSort_ENTRANCE,
     shellSort])(array)



def binarySearch(arr, target):
    """
    二分查找
    :param arr: list
    :param target: int
    :return: index else -1
    """
    # log
    log.info("Binary Search")
    # arr = sort(arr)
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def val_sort(arr: list, sort: staticmethod) -> (str, str, str, bool):
    """
    验证数组排序
    :param sort: sort function
    :param arr: list
    :return: bool
    """
    try:
        sorted_arr = sort(arr)
    except Exception as e:
        return "error", arr, e, False
    for i in range(len(sorted_arr) - 1):
        if sorted_arr[i] > sorted_arr[i + 1]:
            return str(arr[:10])[:-1] + " ... " + str(arr[-10:])[1:], str(sorted_arr[:10])[:-1] + " ... " + str(
                sorted_arr[-10:])[1:], sort.__name__, False
    return str(arr[:10])[:-1] + " ... " + str(arr[-10:])[1:], str(sorted_arr[:10])[:-1] + " ... " + str(
        sorted_arr[-10:])[1:], sort.__name__, True


if __name__ == '__main__':
    arr_org = [random.randint(0, 10 ** 5) for _ in tqdm(range(10 ** 4))]
    random.shuffle(arr_org)
    sort_methods = [org_sort_1, org_sort_2, bubbleSort, selectionSort, insertionSort, mergeSort, quickSort_ENTRANCE,
                    heapSort_ENTRANCE, shellSort]
    for sort in tqdm(sort_methods):
        print(val_sort(arr_org.copy(), sort), autoFlush=False)
        pass
    print(bcolors.HEADER + str(arr_org) + bcolors.ENDC)
    flush()

    target = eval(input('Enter a number: '))
    arr_sorted = sorted(arr_org)  # some of the sort algorithms are not stable so use default sorted instead
    assert type(target) == int
    try:
        index = arr_sorted.index(target)
        print(f"GROUND TRUTH: 给定目标值{target}存在于数组{index}个")
    except ValueError:
        print(f"GROUND TRUTH: 给定目标值{target}不存在于数组中")

    index = binarySearch(arr_sorted, target)
    print(f"CALCULATION:  给定目标值{target}存在于数组{index}个" if index != -1 else f"CALCULATION:  给定目标值{target}不存在于数组中")
