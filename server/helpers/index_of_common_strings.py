def index_of_common_strings(list1, list2):
    """
    Finds the indices of common strings between two lists.

    Parameters:
        list1 (list): The first list of strings.
        list2 (list): The second list of strings.

    Returns:
        tuple: A tuple containing two lists. The first list contains the indices of common strings in list1,
               and the second list contains the corresponding indices of common strings in list2.

    Example:
        >>> list1 = ['apple', 'banana', 'orange']
        >>> list2 = ['kiwi', 'banana', 'orange']
        >>> index_of_common_strings(list1, list2)
        ([1, 2], [1, 2])
    """
    list1_indices = []
    list2_indices = []
    for idx, item in enumerate(list1):
        if item in list2:
            list1_indices.append(idx)
            list2_indices.append(list2.index(item))
    return list1_indices, list2_indices