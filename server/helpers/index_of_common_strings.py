def index_of_common_strings(list1, list2):
    list1_indices = []
    list2_indices = []
    for idx, item in enumerate(list1):  # Iterate over a copy of list1 to avoid modifying it while iterating
        if item in list2:
            list1_indices.append(idx)
            list2_indices.append(list2.index(item))
    return list1_indices, list2_indices