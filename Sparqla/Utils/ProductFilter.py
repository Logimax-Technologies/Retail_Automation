def match_default_items(input_data):
    """
    Compares input data against a default list of special products.
    Returns a list of items that match the defaults.
    """
    # Define the default list as per your requirement
    defaults = ["GUNDU 22KT", "GOLD BAR 999", "LOOSE DIAMOND"]
    
    # Handle single string input by converting to list
    if isinstance(input_data, str):
        # If it's a pipe separated string (common in this project), split it
        if "|" in input_data:
            input_list = [i.strip() for i in input_data.split("|")]
        else:
            input_list = [input_data.strip()]
    elif isinstance(input_data, list):
        input_list = [str(i).strip() for i in input_data]
    else:
        return []
    
    # Filter items that exist in the defaults list
    matches = [item for item in input_list if item in defaults]
    
    return matches

if __name__ == "__main__":
    # Test cases
    test_input = "GUNDU 22KT | GOLD CHAIN | LOOSE DIAMOND"
    print(f"Input: {test_input}")
    print(f"Matches: {match_default_items(test_input)}")
