import re


def remove_trademark_symbols(input_list):
    """
    Removes trademark symbols from each string in the input list.

    Parameters:
        input_list (list): A list of strings with or without trademark symbols.

    Returns:
        list: A new list with trademark symbols removed from each string.

    Example:
        >>> input_list = ["Apple™", "Banana", "Orange™"]
        >>> remove_trademark_symbols(input_list)
        ['Apple', 'Banana', 'Orange']
    """
    cleaned_list = []
    for string in input_list:
        # Using re.sub() to remove trademark symbols from each string in the list
        cleaned_string = re.sub(r"™", "", string)
        cleaned_list.append(cleaned_string)
    return cleaned_list
