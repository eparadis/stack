# Notes on this crazy language
"I swear it isn't Forth" (tm)

## TODONE
+ impliment new word definitions by jumping to the actual definition 
+ impliment 'if' without 'else'
+ add 'else/fi'
+ write some more test cases, like calculating pi or something
+ should 'if' leave something on the data stack -- no, and it turned out to be ?0
+ add some way to add inline comments: first char of line is '#'
+ non-parsed comments in .st files! (simply ignore in initial file load)
+ parse several files passed as command line arguments
+ write command which could write to file handles or digital port
+ source files with "#include whatever.st" but watch out; the order in which the get included can be non-obvious...

## TODO
- fix dumb parsing bugs (negative number literals, words like '2dup')
- anonymous words aka blocks (what use case does this make easier?)
- proper test cases: stack.py honors special comment line that specifies expected resultant data stack
- impliment direct PC and CmdStack manipulation, the rewrite everything to use those primatives
- data input analog to 'write'
- come up with a way to do interrupts and multitasking ('IRQ' and 'yield' special words?)
- create the idea of a thread, with its own stack contexts

## Possible syntax for jumps:
1 jmp 0 1 . endl
1 1 - jz 

: gosub pc pushcs ;
: return pc popcs ;
: jrel pc + pushpc poppc ;
1 jrel skipped target

: skip 4 pc + popDS2pc ; asdf qwert
  0    1 2  3 4          5    6
skip nop target


## Brainstorming conditional syntax
### a lot of stuff is left on the stack (unlike Forth ... )
    valA valB                                                ( -- A B )
              comparison                                     ( A B -- A B BOOL)
                         if true_block else false_block fi   ( A B BOOL -- A B IF_RESULT )

new words could be defined by using jump points
'word word word : newWord def1 def2 def3 ; word word newWord word'
- definition of new word stores pointer to def1 ( 'newWordDict[newWord] = addr(def1)' )
- when neWord is encountered in use, push PC onto control stack, 'PC = NWD[newWord]'
- when ';' is encountered, pop CS to PC

## Fundamental/atomic operations for control
it seems like the fundamental operations here are
- push a value onto the control stack  (from where?)
- get the value of the PC (and put it where?)
- soem sort of conditional around the top of the control stack
- parsing up through the program to match a word (like ; then else fi etc)

## uses for threading
- poll a keyboard for keypresses
- perform routine tasks on a given time period, such as sampling a thermometer
how do these threads share data?
are the threads pre-emptive?

## threading notes
- each thread has its own DS, CS, and PC
- all threads share the same instruction space (both definitions and program)
- IPC occurs by writing to special queue ports using "write" and "read"
- how do threads signal each other? status flag for each thread. polled by other
    threads with "3 tstat"
- timesharing: permissive hand offs? single-word round-robin? execution time
    limited?
- each thread's word should be atomic, so a thread can be started or stopped at any
    time
- 


