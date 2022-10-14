import hashlib


## nohack ##
# please don't hack me
# 1. hashing password
# 2. filtering strings


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def filter_string(string):
    filter_list = [">","<","-","%","$","/"]
    for x in filter_list:
        string = string.replace(x, "")
    return string
