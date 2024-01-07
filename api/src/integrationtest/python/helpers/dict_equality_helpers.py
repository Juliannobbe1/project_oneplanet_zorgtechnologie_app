def sort_dict_list(dict_list: list, sort_on: str) -> list:
    """
    Sorts a list of dictionaries based on 'sort_on' in ascending order.

    Parameters:
    - dict_list (list<dict>): List of dictionaries
    - sort_on (str): The key to sort on

    Returns:
    - list: Sorted list of dictionaries based on 'sort_on'.
    """

    # Sort the list of products based on the 'ID' key
    sorted_dict_list = sorted(dict_list, key=lambda x: x.get(sort_on, 0))

    return sorted_dict_list

def assert_dict_equality(actual_dict: dict, expected_dict: dict) -> bool:
    """
    Asserts the equality of two dict dictionaries.

    Parameters:
    - actual_dict (dict): The dictionary representing the actual dict.
    - expected_dict (dict): The dictionary representing the expected dict.

    Raises:
    - AssertionError: If any key in expected_dict is not present in actual_dict
                      or if the corresponding values are not equal.
    """

    for key, expected_value in expected_dict.items():
        if key not in actual_dict:
            raise AssertionError(f"Key '{key}' not found in actual_dict")

        actual_value = actual_dict[key]

        if actual_value != expected_value:
            raise AssertionError(f"Value mismatch for key '{key}': "
                                 f"Expected {expected_value}, but got {actual_value}")
        
    return True