# simple stack based (RPN) calculator
# ERP Nov 2011

class StackOperation
 def doAdd( stack )
  stack.push( stack.pop + stack.pop)
 end
end

so = StackOperation.new

# get a string
print "> "
user_input = gets() 

# split it into an array
myarray = user_input.split

stack = Array.new

# elements into the array as either integers or strings
myarray.each { |element| 
	if(element =~ /^[0-9]/ ) then stack.push(element.to_i)   
	elsif( element == "+" ) then 
		so.doAdd( stack)
	elsif( element == "-" ) then
		temp = stack.pop
		stack.push( stack.pop - temp )
	elsif( element == "*" ) then
		stack.push( stack.pop * stack.pop )
	elsif( element == "/" ) then
		temp = stack.pop
		stack.push( stack.pop / temp )
	else
		puts "Unknown word: " + element
		break
	end
	}

puts stack

