# simple stack based (RPN) calculator
# originally written in ruby by ERP Nov 2011
# converted to python and extended by ERP May 2013

import re
import types
import sys

def doAdd( dstack, cstack, pc ):
    dstack.append( int(dstack.pop()) + int(dstack.pop()))
    return pc+1

def doSubtract( dstack, cstack, pc):
    temp = int(dstack.pop())
    dstack.append( int(dstack.pop()) - temp)
    return pc+1

def doMultiply( dstack, cstack, pc):
    dstack.append( int(dstack.pop()) * int(dstack.pop()))
    return pc+1

def doDivide( dstack, cstack, pc):
    temp = int(dstack.pop())
    dstack.append( int(dstack.pop()) / temp)
    pc+1

def doPop( dstack, cstack, pc):
    print int(dstack.pop()),
    return pc+1

def doDuplicate( dstack, cstack, pc):
    temp = int(dstack.pop())
    dstack.append( temp)
    dstack.append( temp)
    return pc+1

def doDrop( dstack, cstack, pc):
    dstack.pop()
    return pc+1

def doEndline( dstack, cstack, pc):
    print
    return pc+1

def doUntil( data, cmd, pc):
    temp = int(data.pop() )
    if temp != 0:
        # end the loop
        cmd.pop()
        return pc+1
    else:
        # go back to the latest 'begin'
        return cmd.pop()

def startLoop( data, cmd, index):
    # mark the beginning of a loop
    cmd.append( index)
    return index+1

def doTestZero( dstack, cstack, pc):
    temp = int( dstack.pop() )
    dstack.append( temp) # we leave the tested value on the stack
    if temp == 0:
        dstack.append( 1)
    else:
        dstack.append( 0)
    return pc+1

# get a string
#user_input = raw_input( '> ') 
#user_input = "10 begin 1 - dup . 4 begin 1 - dup . ?0 until . ?0 until"
#user_input = "10 begin 1 - peek 4 begin 1 - peek ?0 until drop endl ?0 until drop"
#user_input = "1 peek : inc 1 + ; inc peek inc peek inc ."  # should output "1 2 3 4" with empty stacks

# split it into an array
#myarray = user_input.split()

#if an argument was given, treat it like a source file and parse it
if len(sys.argv) > 1:
    f = open(sys.argv[1], 'r')
    myarray = f.read().split()
else:
    myarray = []

dataStack = []
cmdStack = []

mapping = {'+': doAdd, '-': doSubtract, '*': doMultiply, '/': doDivide,     \
    '.': doPop, 'dup': doDuplicate, 'begin': startLoop, '?0': doTestZero,   \
    'peek': 'dup .', 'drop': doDrop, 'endl': doEndline, 'until': doUntil }


# elements into the array as either integers or strings
PC = 0
while PC < len(myarray):
    #print "DEBUG: PC = ", PC
    element = myarray[PC]
    if( re.compile(r"^[0123456789]+").search(element) ):
        dataStack.append( int(element) )   
        PC += 1
    elif element in mapping.keys():
        if type(mapping[element]) is types.FunctionType:
            PC = mapping[element](dataStack, cmdStack, PC)
        elif type(mapping[element]) is str:
            #print "DEBUG: expandng word", element
            myarray[PC:PC+1] = mapping[element].split()
            # don't change PC because we need to reparse whatever we just inserted
        else:
            print "Unhandled definition type for word '", element, "'"
            PC += 1 # skip the unhandled definition type
    elif element == ':':
        defStart = PC
        newWord = myarray[PC+1] # let's hope its valid...
        newDef = []
        defPtr = PC+2 # the first word in the definition body
        while myarray[defPtr] != ';':
            newDef.append(myarray[defPtr])
            defPtr += 1
        mapping[newWord] = ' '.join(newDef)
        #print "DEBUG: new def! ->" + newWord + "<--->" + str(newDef)
        PC = defPtr + 1
    else:
        print "Unknown word: " + element
        break

print "done"
print "Data Stack: ", dataStack
print "Command Stack: ", cmdStack
print "Dicitonary: ", mapping.keys()
