# simple stack based (RPN) calculator
# originally written in ruby by ERP Nov 2011
# converted to python and extended by ERP May 2013

import re
import types

def doAdd( dstack, cstack, pc ):
    dstack.append( int(dstack.pop()) + int(dstack.pop()))
    
def doSubtract( dstack, cstack, pc):
    temp = int(dstack.pop())
    dstack.append( int(dstack.pop()) - temp)
    
def doMultiply( dstack, cstack, pc):
    dstack.append( int(dstack.pop()) * int(dstack.pop()))

def doDivide( dstack, cstack, pc):
    temp = int(dstack.pop())
    dstack.append( int(dstack.pop()) / temp)

def doPop( dstack, cstack, pc):
    print int(dstack.pop()),

def doDuplicate( dstack, cstack, pc):
    temp = int(dstack.pop())
    dstack.append( temp)
    dstack.append( temp)

def doUntil( data, cmd, pc):
    temp = int(data.pop() )
    if temp != 0:
        # end the loop
        cmd.pop()
        return -1
    else:
        # go back to the latest 'begin'
        return cmd.pop()

def startLoop( data, cmd, index):
    # mark the beginning of a loop
    cmd.append( index)

def doTestZero( dstack, cstack, pc):
    temp = int( dstack.pop() )
    dstack.append( temp) # we leave the tested value on the stack
    if temp == 0:
        dstack.append( 1)
    else:
        dstack.append( 0)

# get a string
#user_input = raw_input( '> ') 
#user_input = "10 begin 1 - dup . 4 begin 1 - dup . ?0 until . ?0 until"
user_input = "10 begin 1 - peek 4 begin 1 - peek ?0 until . ?0 until"

# split it into an array
myarray = user_input.split()

dataStack = []
cmdStack = []

mapping = {'+': doAdd, '-': doSubtract, '*': doMultiply, '/': doDivide,     \
    '.': doPop, 'dup': doDuplicate, 'begin': startLoop, '?0': doTestZero,   \
    'peek': 'dup .'}


# elements into the array as either integers or strings
PC = 0
while PC < len(myarray):
    #print "DEBUG: PC = ", PC
    element = myarray[PC]
    if( re.compile(r"^[0123456789]+").search(element) ):
        dataStack.append( int(element) )   
        PC += 1
    elif( element == 'until' ):
        ret = doUntil( dataStack, cmdStack, PC)
        if ret != -1:
            PC = ret
            continue
        # otherwise just increment PC like usual
        PC += 1
    elif element in mapping.keys():
        if type(mapping[element]) is types.FunctionType:
            mapping[element](dataStack, cmdStack, PC)
            PC += 1
        elif type(mapping[element]) is str:
            #print "DEBUG: expandng word", element
            myarray[PC:PC+1] = mapping[element].split()
            # don't change PC because we need to reparse whatever we just inserted
        else:
            print "Unhandled definition type for word '", element, "'"
            PC += 1 # skip the unhandled definition type
    else:
        print "Unknown word: " + element
        break

print "done"
print "Data Stack: ", dataStack
print "Command Stack: ", cmdStack
