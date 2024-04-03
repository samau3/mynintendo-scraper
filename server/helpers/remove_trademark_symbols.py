import re

def remove_trademark_symbols(input_list):
    cleaned_list = []
    for string in input_list:
        # Using re.sub() to remove trademark symbols from each string in the list
        cleaned_string = re.sub(r'™', '', string)
        cleaned_list.append(cleaned_string)
    return cleaned_list
