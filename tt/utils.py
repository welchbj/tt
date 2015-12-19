def without_spaces(the_str):
    return "".join(the_str.split())

def listwise_to_str(the_list):
    return list(map(str, the_list))

def str_replace_range(the_string, start, end, replace_string):
    # replace
    return the_string[:start] + replace_string + the_string[(end+1):]