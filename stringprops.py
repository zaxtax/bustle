# TODO: define an API and convert Java code to Python

# Listing 5: Java code for all Properties acting on single Strings.
str.isEmpty()               # is empty?
str.length() == 1           # is single char?
str.length() <= 5           # is short string?
str.equals(lower)           # is lowercase?
str.equals(upper)           # is uppercase?
str.contains(" ")           # contains space?
str.contains(",")           # contains comma?
str.contains(".")           # contains period?
str.contains("-")           # contains dash?
str.contains("/")           # contains slash?
str.matches(". *\\d. *")    # contains digits?
str.matches("\\d+")         # only digits?
str.matches(". *[a-zA-Z]. * ") # contains letters?
str.matches("[a-zA-Z]+")    # only letters?

# Listing 6: Java code for all Properties acting on single Integers.
integer == 0                # is zero?
integer == 1                # is one?
integer == 2                # is two?
integer < 0                 # is negative?
0 < integer && integer <= 3 # is small integer?
3 < integer && integer <= 9 # is medium integer?
9 < integer                 # is large integer?

# Listing 7: Java code for all Properties acting on a String and the output String.
outputStr.contains(str)            # output contains input?
outputStr.startsWith(str)          # output starts with input?
outputStr.endsWith(str)            # output ends with input?
str.contains(outputStr)            # input contains output?
str.startsWith(outputStr)          # input starts with output?
str.endsWith(outputStr)            # input ends with output?
outputStrLower.contains(lower)     # output contains input ignoring case?
outputStrLower.startsWith(lower)   # output starts with input ignoring case?
outputStrLower.endsWith(lower)     # output ends with input ignoring case?
lower.contains(outputStrLower)     # input contains output ignoring case?
lower.startsWith(outputStrLower)   # input starts with output ignoring case?
lower.endsWith(outputStrLower)     # input ends with output ignoring case?
str.equals(outputStr)              # input equals output?
lower.equals(outputStrLower)       # input equals output ignoring case?
str.length() == outputStr.length() # input same length as output?
str.length() < outputStr.length()  # input shorter than output?
str.length() > outputStr.length()  # input longer than output?

# Listing 8: Java code for all Properties acting on an Integer and the output String.
integer < outputStr.length()                # is less than output length?
integer <= outputStr.length()               # is less or equal to output length?
integer == outputStr.length()               # is equal to output length?
integer >= outputStr.length()               # is greater or equal to output length?
integer > outputStr.length()                # is greater than output length?
Math.abs(integer - outputStr.length()) <= 1 # is very close to output length?
Math.abs(integer - outputStr.length()) <= 3 # is close to output length?
