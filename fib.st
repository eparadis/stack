: dup2 over over ;
: calc_fib dup2 + rot drop ;

0 1 10 begin rot rot calc_fib peek rot peek endl 1 - ?0 until drop

