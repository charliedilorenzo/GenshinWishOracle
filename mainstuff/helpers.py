def add_dictionary_entries(list_of_dicts: list[dict[int, float]]) -> dict[int, float]:
    # assumes that the dictionary have the same keys
    new_dict = {key: 0 for key in list_of_dicts[0]}
    for dict in list_of_dicts:
        for key in list_of_dicts[0]:
            new_dict[key] += dict[key]
    return new_dict


def multiply_dictionary_entries(dictionary: dict[int, float], factor: float) -> dict[int, float]:
    # assumes that the dictionary have the same keys
    new_dict = {}
    for key in dictionary:
        new_dict[key] = factor*dictionary[key]
    return new_dict


def upgrade_dictionary(dictionary: dict[int, float]) -> dict[int, float]:
    # for a dictionary assumed to have keys that are ascending integers starting at 0
    # returns a new dictionary that the value for every key moved up to that key+1 except the final entry which is the previous key's value plus its current
    new_dict = {}
    temp1 = dictionary[0]
    for i in range(1, len(dictionary)-1):
        temp2 = dictionary[i]
        new_dict[i] = temp1
        temp1 = temp2
    new_dict[i+1] = temp1+dictionary[i+1]
    new_dict[0] = 0
    return new_dict