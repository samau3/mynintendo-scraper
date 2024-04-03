from helpers.index_of_common_strings import index_of_common_strings
from helpers.remove_trademark_symbols import remove_trademark_symbols

def remove_trademark_false_positives(differences_dictionary):
    cleaned_dict = differences_dictionary.copy()

    for difference in cleaned_dict:
        cleaned_dict[difference] = remove_trademark_symbols(cleaned_dict[difference])

    added_indices, removed_indices = index_of_common_strings(cleaned_dict["dictionary_item_added"], cleaned_dict["dictionary_item_removed"])

    for i in range(len(added_indices) - 1, -1, -1):
        differences_dictionary["dictionary_item_added"].pop(added_indices[i])
        if len(differences_dictionary["dictionary_item_added"]) == 0:
            del differences_dictionary["dictionary_item_added"]
    for i in range(len(removed_indices) - 1, -1, -1):
        differences_dictionary["dictionary_item_removed"].pop(removed_indices[i])
        if len(differences_dictionary["dictionary_item_removed"]) == 0:
            del differences_dictionary["dictionary_item_removed"]

    return differences_dictionary