import random


# Exercise 1
# https://www.fuzzingbook.org/html/Intro_Testing.html#Exercise-1:-Testing-Shellsort
def shellsort(elems):
    sorted_elems = elems.copy()
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]
    for gap in gaps:
        for i in range(gap, len(sorted_elems)):
            temp = sorted_elems[i]
            j = i
            while j >= gap and sorted_elems[j - gap] > temp:
                sorted_elems[j] = sorted_elems[j - gap]
                j -= gap
            sorted_elems[j] = temp

    return sorted_elems


random_length = random.sample(range(1, 11), 10)
for length in random_length:
    test_case = random.sample(range(length + 1), length)
    assert sorted(test_case) == shellsort(test_case)
