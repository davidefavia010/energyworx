import re


def check_short(shortcode):
    # re.search returns None if no position in the string matches the pattern
    # pattern to search for any character other then . a-z 0-9
    pattern = r'[^\_A-Za-z\d]'
    if re.search(pattern, shortcode) or len(shortcode) != 6:
        # Character other then . a-z 0-9 was found
        return False
    return True


def check_short2(db_row):
    if db_row is None:
        return False
    return True
