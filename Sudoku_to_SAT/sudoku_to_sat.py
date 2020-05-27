# relative path to the solver; change here if you I send you only this file
solver = "../../../build/cadical"

import sys
from subprocess import Popen
from subprocess import PIPE
import re
import random
import os


# global variable to define the "corresponding number" of a clause
gbi = 0
# the corresponding string of a clause represented by a number
varToStr = ["invalid"]




# function to print a clause
def printClause(cl):
    print map(lambda x: "%s%s" % (x < 0 and eval("'-'") or eval ("''"), varToStr[abs(x)]) , cl)



# function to increment global counter, update list with strings and return the new value of the counter dbi
def gvi(name):
    global gbi
    global varToStr
    gbi += 1
    varToStr.append(name)
    return gbi


# function that returns the input from the file in a meaningful way
def parse_input(input_file_name = "input_sudoku.txt"):

    # open the input file in order to parse it
    input_file = open(input_file_name, "r")

    # get the important sizes from the first line of the input file
    n, rows_per_block, columns_per_block = [int(x) for x in input_file.readline().split()]
    # get the available symbols from the second line of the input file
    symbols = [x for x in input_file.readline().split()]
    # append the dash symbol

    print n, rows_per_block, columns_per_block
    print symbols

    # dictionary to store the values of the cells; it's keys are tuples of the form (row, column)
    cell_values = {}

    # read the n lines of the sudoku puzzle
    for i in range(1, n + 1):

        # read the next row (line)
        line = input_file.readline()

        # position of the next symbol inside the string "line" above
        position = 0
        # read the values from the columns
        for j in range(1, n + 1):

            # if we have finished the block, then the input file has a '|', so skip it
            if line[position] == '|':
                position = position + 2

            # if we read a dash (empty cell), increment the position and procced
            if line[position] == '-':
                position = position + 2
                continue
            # check for errors
            elif line[position] not in symbols:
                # print relevant message
                print "Error in cell (%d, %d): symbol %s is not in the symbol list provided above." % (i, j, line[position])
                # close the file
                input_file.close()
                # abort
                sys.exit(1)

            # store the value
            cell_values[(i, j)] = line[position]
            # increment the position of the next symbol to be read
            position = position + 2


        # after a block finishes, we have a line of just dashes (---), so skip it
        if i % rows_per_block == 0:
            line = input_file.readline()

    print cell_values



    # close the input file because we don't need it anymore
    input_file.close()











# main functiom
if __name__ == '__main__':

    # make sure that the solver is legit
    if not (os.path.isfile(solver) and os.access(solver, os.X_OK)):
        print "\nSet the path to solver correctly on line 2 of this file (%s).\n" % sys.argv[0]
        sys.exit(1)

    parse_input()
