import re

def is_number(phone):
    regex = re.match(r'^(\d|\-|\ |\.){9,15}$', phone)
    if regex is None:
        return False
    return True