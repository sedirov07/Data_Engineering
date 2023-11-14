def statistical_characteristics(arr, key):
    sumary = 0
    maximum = arr[0][key]
    minimum = arr[0][key]
    nums = []
    moda_dict = dict()
    length = len(arr)
    for el in arr:
        num = el[key]
        nums.append(num)
        sumary += num
        maximum = max(maximum, num)
        minimum = min(minimum, num)
        moda_dict[el[key]] = moda_dict.get(el[key], 0) + 1
    average = sumary / length

    moda = max(moda_dict, key=moda_dict.get)

    if length % 2 == 1:
        median = nums[length // 2]
    else:
        median = (nums[length // 2 - 1] + nums[length // 2]) / 2

    return {
        'sumary': sumary,
        'maximum': maximum,
        'minimum': minimum,
        'average': average,
        'median': median,
        'moda': moda
    }


def frequency_of_occurrence(arr, key):
    frequency_of_labels = {}
    for el in arr:
        frequency_of_labels[el[key]] = frequency_of_labels.get(el[key], 0) + 1

    sorted_frequency = dict(sorted(frequency_of_labels.items(), key=lambda x: x[1], reverse=True))

    return sorted_frequency
