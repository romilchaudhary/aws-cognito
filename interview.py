# https://www.interviewbit.com/django-interview-questions/
# https://mindmajix.com/django-interview-questions
# https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react

import json
import sys

s = "130"
print(len(s)//2)
k = [s[~i] for i in range(len(s))]
for i in k:
	print(i)
out = [s[i] == s[~i] for i in range(len(s)//2)]
print(out)

# Using "Enumerate" to traverse through a list instead of "range".
# "defaultdict" - which will provide default values to the keys.
# "izip" is better than "zip" performance wise:


# Can we use string as key in dictionary Python?
# The dictionary webstersDict used strings as keys in the dictionary, but dictionary keys can be any immutable data type (numbers, strings, tuples etc). Dictionary values can be just about anything (int, lists, functions, strings, etc).

# How is dictionary stored in memory?
# The dictionary is stored in memory in the form of a hash table with an ordered array of ranges and their corresponding values. This storage method works the same way as hashed and allows using date/time (arbitrary numeric type) ranges in addition to the key.

test_string = '{"Nikhil" : 1, "Akshat" : 2, "Akash" : 3}'
print(type(eval(test_string)))
print(json.loads(test_string))
res = json.loads(test_string)
print(sys.getsizeof(res))


# Is it bad to use a dict in Python?
# Not bad; given how often dictionaries are used in Python, it�s good to know that they don�t normally consume that much memory. What if I add something to the dict?

# How does memory management work in Python generators?
# Because strings are immutable, every time you add an element to a string, Python creates a new string and a new address. This means that new memory needs to be allocated each time the string is altered. Generators allow you to create a function that returns one item at a time rather than all the items at once.