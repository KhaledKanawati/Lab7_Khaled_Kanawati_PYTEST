def capital_case(value):
    if not isinstance(value, str):
        raise TypeError("Please provide a string argument")
    return value.capitalize()
