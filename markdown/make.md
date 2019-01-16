---
title: Minimal makefiles
...

In this class, you will generally submit multiple files for each assignment
with an accompanying makefile to help us run them.
Makefiles are quite powerful and, while sometimes considered antequated compared to tools like ant, buildr, gradle, ivy, maven, and scons, it remains the workhorse of the GNU and Linux worlds.
You're welcome to [read a lot more](https://www.gnu.org/software/make/manual/) than this one summary if you wish.


The following is a base makefile for our course

````makefile
# set up how compilation will happen
CC = clang
CFLAGS = -g -O1
LDFLAGS = 

# define the set of files used
objects = foo.o bar.o



# default to building everything, running nothing
all: runner tester



# Create a runner target ...
runner: main.o $(objects)
    $(CC) $(LDFLAGS) $< -o $@

# ... and a target that runs it
run: runner
    ./runner



# Create a tester target ...
tester: tester.o $(objects)
    $(CC) $(LDFLAGS) $< -o $@

# ... and a target that runs it
test: tester
    ./tester

test: tester.o $(objects)
    $(CC) $(LDFLAGS) $< -o $@
    ./test



# genetic rule to build a .o from any .c
# see https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html
%.o: %.c
    $(CC) -c $(CFLAGS) $< -o $@



# something to remove files the makefile created
clean:
    rm -f run test main.o tester.o $(objects)

# mark a few targets as not producing files
.PHONEY: all run test clean 
````
