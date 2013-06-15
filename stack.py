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
    #dstack.append( temp) # we leave the tested value on the stack
    if temp == 0:
        dstack.append( 1)
    else:
        dstack.append( 0)
    return pc+1

def doPeek( ds, cs, pc):
    doDuplicate( ds, cs, pc)
    doPop(ds, cs, pc)
    return pc+1

def doRotate( ds, cs, pc):
    # c b a -- b a c
    a = int(ds.pop())
    b = int(ds.pop())
    c = int(ds.pop())
    ds.append(b)
    ds.append(a)
    ds.append(c)
    return pc+1

def doSwap( ds, cs, pc):
    a = int(ds.pop())
    b = int(ds.pop())
    ds.append(a)
    ds.append(b)
    return pc+1

def doOver( ds, cs, pc):
    temp = int(ds[-2])
    ds.append( temp)
    return pc+1

#if an argument was given, treat it like a source file and parse it
if len(sys.argv) > 1:
    f = open(sys.argv[1], 'r')
    res = ""
    for line in f.readlines():
        if line[0] != '#':
            res += line
    myarray = res.split()
else:
    myarray = []

dataStack = []
cmdStack = []

mapping = {'+': doAdd, '-': doSubtract, '*': doMultiply, '/': doDivide,     \
    '.': doPop, 'dup': doDuplicate, 'begin': startLoop, '?0': doTestZero,   \
    'drop': doDrop, 'endl': doEndline, 'until': doUntil, 'peek': doPeek,    \
    'rot': doRotate, 'swap': doSwap, 'over': doOver }


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
            #myarray[PC:PC+1] = mapping[element].split()
            (addr, inst) = mapping[element].split()
            if inst == 'jmp':
                cmdStack.append(PC+1)
                PC = int(addr)
        else:
            print "Unhandled definition type for word '", element, "'"
            PC += 1 # skip the unhandled definition type
    elif element == ':':
        defStart = PC
        newWord = myarray[PC+1] # let's hope its valid...
        newDef = []
        defPtr = PC+2 # the first word in the definition body
        while myarray[defPtr] != ';':
            #newDef.append(myarray[defPtr])
            defPtr += 1
        newDef.append(str(defStart+2))
        newDef.append("jmp")
        mapping[newWord] = ' '.join(newDef)
        #print "DEBUG: new def! ->" + newWord + "<--->" + str(newDef)
        PC = defPtr + 1
    elif element == ';':
        PC = int(cmdStack.pop())    # this is the same as 'until' isn't it?
    elif element == 'if':
        temp = dataStack.pop()
        if temp != 0:
            PC += 1
        else:
            # skip over the true block until you find an 'else', and set PC to the instruction after the 'else'
            ptr = PC
            while myarray[ptr] != 'else':
                ptr += 1
            PC = ptr + 1
    elif element == 'else':
        # skip over the false block until you find a 'fi', and set PC to inst after that
        ptr = PC
        while myarray[ptr] != 'fi':
            ptr += 1
        PC = ptr + 1
    elif element == 'fi':
        # we'll encounter this after doing the false block, so just ignore it
        PC += 1
    else:
        print "Unknown word: " + element
        break

print "done"
if len(dataStack) > 0:
    print "Data Stack: ", dataStack
if len(cmdStack) > 0:
    print "Command Stack: ", cmdStack
#print "Dicitonary: ", mapping.keys()
