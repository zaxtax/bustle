# TODO: define an API

import re

str = "dummy"
integer = 1
outputStr = "dummy"

# Listing 5: Java code for all Properties acting on single Strings.
str == ""                   # is empty?
len(str) == 1               # is single char?
len(str) <= 5               # is short string?
str.islower()               # is lowercase?
str.isupper()               # is uppercase?
" " in str                  # contains space?
"," in str                  # contains comma?
"." in str                  # contains period?
"-" in str                  # contains dash?
"/" in str                  # contains slash?
bool(re.search(r"\d", str))        # contains digits?
bool(re.match(r"\d+$", str))       # only digits?
bool(re.search(r"\d", str))        # contains digits?
bool(re.match(r"\d+$", str))       # only digits?
bool(re.search(r"[a-zA-Z]", str))  # contains letters?
bool(re.match(r"[a-zA-Z]+$", str)) # only letters?

# Listing 6: Java code for all Properties acting on single Integers.
integer == 0                # is zero?
integer == 1                # is one?
integer == 2                # is two?
integer < 0                 # is negative?
0 < integer and integer <= 3  # is small integer?
3 < integer and integer <= 9  # is medium integer?
9 < integer                 # is large integer?

# Listing 7: Java code for all Properties acting on a String and the output String.
str in outputStr                   # output contains input?
outputStr.startswith(str)          # output starts with input?
outputStr.endswith(str)            # output ends with input?
outputStr in str                   # input contains output?
str.startswith(outputStr)          # input starts with output?
str.endswith(outputStr)            # input ends with output?
str.lower() in outputStr.lower()   # output contains input ignoring case?
outputStr.lower().startswith(str.lower()) # output starts with input ignoring case?
outputStr.lower().endswith(str.lower())   # output ends with input ignoring case?
outputStr.lower() in str.lower()          # input contains output ignoring case?
str.lower().startswith(outputStr.lower())  # input starts with output ignoring case?
str.lower().endswith(outputStr.lower())    # input ends with output ignoring case?
str == outputStr                    # input equals output?
str.lower() == outputStr.lower()    # input equals output ignoring case?
len(str) == len(outputStr)          # input same length as output?
len(str) < len(outputStr)           # input shorter than output?
len(str) > len(outputStr)           # input longer than output?

# Listing 8: Java code for all Properties acting on an Integer and the output String.
integer < len(outputStr)           # is less than output length?
integer <= len(outputStr)          # is less or equal to output length?
integer == len(outputStr)          # is equal to output length?
integer >= len(outputStr)          # is greater or equal to output length?
integer > len(outputStr)           # is greater than output length?
abs(integer - len(outputStr)) <= 1 # is very close to output length?
abs(integer - len(outputStr)) <= 3 # is close to output length?
