# test out the write word
# bounce a bit back and forth on port 2

# shift right
: rshift 2 * ;

# left shift
: lshift 2 / ;

# write TOS to port two
: write_2 2 swap write ;

# start with the LSB set
1

7 begin swap dup write_2 rshift swap 1 - dup ?0 until drop

7 begin swap dup write_2 lshift swap 1 - dup ?0 until drop write_2



