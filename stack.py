# simple stack based (RPN) calculator
# originally written in ruby by ERP Nov 2011
# converted to python and extended by ERP May 2013

import re

class StackOperation:
    def doAdd( self, stack ):
        stack.append( int(stack.pop()) + int(stack.pop()))
    
    def doSubtract( self, stack):
        temp = int(stack.pop())
        stack.append( int(stack.pop()) - temp)
    
    def doMultiply( self, stack):
        stack.append( int(stack.pop()) * int(stack.pop()))

    def doDivide( self, stack):
        temp = int(stack.pop())
        stack.append( int(stack.pop()) / temp)

    def doPop( self, stack):
        print int(stack.pop())

    def doDuplicate( self, stack):
        temp = int(stack.pop())
        stack.append( temp)
        stack.append( temp)

    def doUntil( self, data, cmd):
        temp = int(data.pop() )
        if temp != 0:
            # end the loop
            cmd.pop()
            return -1
        else:
            # go back to the latest 'begin'
            return cmd.pop()

    def startLoop( self, cmd, index):
        # mark the beginning of a loop
        cmd.append( index)

    def doTestZero( self, stack):
        temp = int( stack.pop() )
        stack.append( temp) # we leave the tested value on the stack
        if temp == 0:
            stack.append( 1)
        else:
            stack.append( 0)

so = StackOperation()

# get a string
#user_input = raw_input( '> ') 
user_input = "10 begin 1 - dup . ?0 until"

# split it into an array
myarray = user_input.split()

dataStack = []
cmdStack = []

# elements into the array as either integers or strings
PC = 0
while PC < len(myarray):
    #print "DEBUG: PC = ", PC
    element = myarray[PC]
    if( re.compile(r"^[0123456789]+").search(element) ):
        dataStack.append( int(element) )   
    elif( element == "+" ): 
        so.doAdd( dataStack)
    elif( element == "-" ):
        so.doSubtract( dataStack)
    elif( element == "*" ):
        so.doMultiply( dataStack)
    elif( element == "/" ):
        so.doDivide( dataStack)
    elif( element == "." ):
        so.doPop( dataStack)
    elif( element == "dup" ):
        so.doDuplicate( dataStack)
    elif( element == 'begin' ):
        so.startLoop( cmdStack, PC)
    elif( element == 'until' ):
        ret = so.doUntil( dataStack, cmdStack)
        if ret != -1:
            PC = ret
            continue
        # otherwise just increment PC like usual
    elif( element == '?0' ):
        so.doTestZero( dataStack)
    else:
        print "Unknown word: " + element
        break
    PC += 1

print dataStack

