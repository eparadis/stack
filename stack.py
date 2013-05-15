# simple stack based (RPN) calculator
# originally written in ruby by ERP Nov 2011
# converted to python ERP May 2013

import re

class StackOperation:
    def doAdd( self, stack ):
        stack.append( int(stack.pop()) + int(stack.pop()))

so = StackOperation()

# get a string
user_input = raw_input( '> ') 

# split it into an array
myarray = user_input.split()

stack = []

# elements into the array as either integers or strings
for element in myarray:
    if( re.compile(r"^[0123456789]+").search(element) ):
        stack.append( int(element) )   
    elif( element == "+" ): 
        so.doAdd( stack)
    elif( element == "-" ):
        temp = int(stack.pop())
        stack.append( stack.pop() - temp )
    elif( element == "*" ):
        stack.append( int(stack.pop()) * int(stack.pop()) )
    elif( element == "/" ):
        temp = int(stack.pop())
        stack.append( int(stack.pop()) / temp )
    else:
        print "Unknown word: " + element
        break

print stack
