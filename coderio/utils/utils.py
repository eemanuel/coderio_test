def get_value(dictionary, key_path_list):
    """
    Pass a dictionary and list with strings.
    It returns the value by following the 'key path' of the list in the dictionary.
    """

    try:
        first_key = key_path_list[0]
    except IndexError:
        return dictionary
    try:
        first_value = dictionary[first_key]
    except KeyError:
        return
    key_path_list_without_first = key_path_list[1:]
    return get_value(dictionary=first_value, key_path_list=key_path_list_without_first)


def farenheit_to_celsius(farenheit):
    """
    Pass a temperature in farenheit (should be int or str).
    It returns the celsius temperarture equivalent.
    """

    if isinstance(farenheit, str):
        farenheit = int(farenheit)
    celsius = (farenheit - 32) * 0.55555  # formula
    return round(celsius)
