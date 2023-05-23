import re

def is_string_numbers(regex):
    match = re.match(r"^\d+$", regex)
    return match is not None

def is_string_letters(regex):
    match = re.match(r"^[a-zA-Z]+(?: [a-zA-Z]+)*(?: [a-zA-Z]+)*$", regex)
    return match is not None

def is_string_alphanumeric(regex):
    match = re.match(r"^\w+$", regex)
    return match is not None

def is_address(regex):
    match = re.match(r"^(\d+)\s+(.+?)$", regex)
    return match is not None

def regex_filter(value):

    if is_string_numbers(str(value)) is True and len(str(value)) < 6:
        (where_clause := f"account_id = '{value}'")
        print(where_clause)
        print("Account Query")

    elif is_string_letters(str(value)) is True:
        searched_name = value.upper()
        (where_clause := f"owner_name LIKE '%{searched_name}%'")
        print(where_clause)
        print("Owner Name Query")

    elif is_string_alphanumeric(str(value)) is True:
        value = value[:8] + "-" + value[8:]
        (where_clause := f"map_taxlot LIKE '%{value}%'")
        print(where_clause)
        print("Map Taxlot Query")

    elif is_address(str(value)) is True:
        situs = value.upper()
        (where_clause := f"situs_address LIKE '%{situs}%'")
        print(where_clause)
        print("Address Query")

    else:
        print('search error -- #http redirect??')

    return where_clause