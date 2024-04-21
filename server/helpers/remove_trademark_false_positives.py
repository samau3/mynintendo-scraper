from helpers.index_of_common_strings import index_of_common_strings
from helpers.remove_trademark_symbols import remove_trademark_symbols


def remove_trademark_false_positives(differences_dictionary):
    """
    Removes trademark false positives from a dictionary of differences.

    This function removes false positives caused by changes in item names due to the presence
    or absence of trademark symbols. It utilizes helper functions to remove trademark symbols 
    and find indices of common strings between lists.

    Parameters:
        differences_dictionary (dict): A dictionary containing differences between two versions 
                                       of a dataset.

    Returns:
        dict: A modified dictionary with trademark false positives removed.

    Example:
        >>> differences = {
        ...     "dictionary_item_added": ["Apple™", "Banana", "Orange™"],
        ...     "dictionary_item_removed": ["Apple", "Banana™", "Kiwi"]
        ... }
        >>> remove_trademark_false_positives(differences)
        {'dictionary_item_added': ['Orange'], 'dictionary_item_removed': ['Kiwi']}
    """
    cleaned_dict = differences_dictionary.copy()

    # Remove trademark symbols from items in the dictionary
    for difference in cleaned_dict:
        cleaned_dict[difference] = remove_trademark_symbols(
            cleaned_dict[difference])

    # Find indices of common strings between added and removed items
    added_indices, removed_indices = index_of_common_strings(
        cleaned_dict.get("dictionary_item_added", []), cleaned_dict.get("dictionary_item_removed", []))
    
    # If no indices are found for either added or removed items, return the original dictionary
    if not added_indices or not removed_indices:
        return differences_dictionary

    # Remove common items from added and removed lists
    for i in range(len(added_indices) - 1, -1, -1):
        differences_dictionary["dictionary_item_added"].pop(added_indices[i])
        if len(differences_dictionary["dictionary_item_added"]) == 0:
            del differences_dictionary["dictionary_item_added"]
    for i in range(len(removed_indices) - 1, -1, -1):
        differences_dictionary["dictionary_item_removed"].pop(
            removed_indices[i])
        if len(differences_dictionary["dictionary_item_removed"]) == 0:
            del differences_dictionary["dictionary_item_removed"]

    return differences_dictionary
