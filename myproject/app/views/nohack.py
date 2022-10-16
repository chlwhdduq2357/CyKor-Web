import hashlib


## nohack ##
# please don't hack me
# 1. hashing password
# 2. filtering strings


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def filter_string(string):

    # return -1 if invalid character or string included

    invalid = False
    
    filter_char_list = [">","<","-","%","$","/","=","*","(",")","'",'"'," ","+","`",";","\\",".",","]
    filter_key_list = ["union","select","drop","update","from","where","join","substr"] 

    for x in filter_char_list:
        if x in string:
            invalid =  True
            break
    
    test_string = string.lower()

    for x in filter_key_list:
        if x in test_string:
            invalid = True
            break
    
    
    if invalid:
        return -1
    else:
        return string


def replace_string(string):


    # I don't think this is worth doing...
    # but this might prevent sql injection
    
    filter_replace_list = {
            "-" : "㇐", "|" : "⼁", "=" : "＝", "~" : "∼", ":" : "ː", ";": ";",
            "`":"'", "/" : "／", ",":"，", "(":"❨" , ")":"❩", "<" : "〈", ">":"〉", "*":"∗"

            }
    for x in list(filter_replace_list.keys()):
        if x in string:
            string = string.replace(x, filter_replace_list[x])

    return string


