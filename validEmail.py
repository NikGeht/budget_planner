import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
# Define a function for
# for validating an Email
 
 
def check(email):
 
    # pass the regular expression
    # and the string in search() method
    if(re.match(regex, email)):
        return True
 
    else:
        return False