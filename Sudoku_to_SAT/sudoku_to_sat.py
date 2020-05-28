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





# functions that returns true if the input for the sudoku is ok; else returns false
def check_input(n, rows_per_block, columns_per_block):
    # check for negative values
    if n <= 0 or rows_per_block <= 0 or columns_per_block <= 0:
        print "\nError in the input file: The sizes in the first line must be positive.\n"
        return False
    # check for invalid block size values
    elif n != rows_per_block * columns_per_block:
        print "\nError in the input file: The product of the lengths of the sides of the block have \
                 to be equal to the dimension of the grid, that is: n = rows_per_block * columns_per_block.\n"
        return False

    # everything is ok
    return True




# function that returns the input from the file in a meaningful way
def parse_input(input_file_name = "input_sudoku.txt"):

    # open the input file in order to parse it
    input_file = open(input_file_name, "r")


    # get the important sizes from the first line of the input file
    first_line = [int(x) for x in input_file.readline().split()]
    # check for errors
    if len(first_line) != 3:
        print "\nError in the input file: The first line must contain n (dimension of grid), and the size of blocks (3 5 for 3x5).\n"
        # close the file
        input_file.close()
        # abort
        sys.exit(1)


    # get the correct values
    n, rows_per_block, columns_per_block = first_line
    if check_input(n, rows_per_block, columns_per_block) == False:
        # close the file
        input_file.close()
        # abort
        sys.exit(1)


    # get the available symbols from the second line of the input file
    symbols = [x for x in input_file.readline().split()]
    # check for errors
    if len(symbols) != n:
        print "\nError in the input file: The second line has to contain as many symbols as the dimension of the grid (n).\n"
        # close the file
        input_file.close()
        # abort
        sys.exit(1)



    # dictionary to store the values of the cells; it's keys are tuples of the form (row, column)
    cell_values = {}


    # read the n lines of the sudoku puzzle
    for i in range(1, n + 1):

        # read the next row (line)
        line = input_file.readline()
        # check for errors
        if len(line) / 2 != n + n/columns_per_block - 1:
            print "\nError in the input file: The file lines must have the specific format. For example: \"5 - - | - 2 - | 4 - 3\" for 9x9 Sudokus with 3x3 blocks.\n"
            # close the file
            input_file.close()
            # abort
            sys.exit(1)

        # position of the next symbol inside the string "line" above
        position = 0
        # read the values from the columns
        for j in range(1, n + 1):

            # if we have finished the block, then the input file has a '|', so skip it
            if (position - columns_per_block * 2) % (2 * (columns_per_block + 1)) == 0 and columns_per_block > 1:
                position = position + 2

            # if we read a dash (empty cell), increment the position and proceed
            if line[position] == '-':
                position = position + 2
                continue
            # check for errors
            elif line[position] not in symbols:
                # print relevant message
                print "\nError in cell (%d, %d): symbol %s is not in the symbol list provided above.\n" % (i, j, line[position])
                # close the file
                input_file.close()
                # abort
                sys.exit(1)

            # store the value since it's valid
            cell_values[(i, j)] = line[position]
            # increment the position of the next symbol to be read
            position = position + 2


        # after a block finishes, we have a line of just dashes (---), so skip it
        if i % rows_per_block == 0 and i < n and rows_per_block > 1:
            line = input_file.readline()

    # make sure that the file has finished
    line = input_file.readline()
    if line != "":
        # print relevant message
        print "\nError, input file should end after the Sudoku. Fix the input file according the correct format.\n"
        # close the file
        input_file.close()
        # abort
        sys.exit(1)


    # close the input file because we don't need it anymore
    input_file.close()

    # return the information parsed
    return [n, rows_per_block, columns_per_block, symbols, cell_values]





# function that generates the variables of the problem, which are: cell_has_value(i, j, v) for i,j \in {1, .., n} and v \in symbols
def gen_vars(n, symbols):

    # dictionary with all the variables
    varMap = {}

    # iterate through all the rows
    for i in range(n):
        # iterate through all the columns
        for j in range(n):
            # iterate through all the symbols
            for v in symbols:
                # create the variable
                var = "cell_has_value([%d, %d], %c)" % (i + 1, j + 1, v)
                # store in the dictionary it's corresponding number
                varMap[var] = gvi(var)

    # return the dictionary
    return varMap




# function that generates the 5 set of constraints for the sudoku puzzle
def gen_contraints(variables, n, rows_per_block, columns_per_block, symbols):

    # list with the clauses (constraints)
    clauses = []

    # length of list of symbols (which is equal to the dimension of the grid)
    len_symbols = len(symbols)


    # set 1: every cell must have at least one value (symbol)
    for i in range(n):
        for j in range(n):
            disjunction = []
            for v in symbols:
                literal = "cell_has_value([%d, %d], %c)" % (i + 1, j + 1, v)
                disjunction.append(variables[literal])

            clauses.append(disjunction)


    # set 2: every cell cannot have 2 values
    for i in range(n):
        for j in range(n):
            for v1 in range(len_symbols):
                literal1 = "cell_has_value([%d, %d], %c)" % (i + 1, j + 1, symbols[v1])
                for v2 in range(v1 + 1, len_symbols):
                    literal2 = "cell_has_value([%d, %d], %c)" % (i + 1, j + 1, symbols[v2])
                    clauses.append([-variables[literal1], -variables[literal2]])



    # set 3: every row must contain all symbols once <=> no 2 cells in the same row can have the same symbol
    for i in range(n):
        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                for v in symbols:
                    literal1 = "cell_has_value([%d, %d], %c)" % (i + 1, j1 + 1, v)
                    literal2 = "cell_has_value([%d, %d], %c)" % (i + 1, j2 + 1, v)
                    clauses.append([-variables[literal1], -variables[literal2]])



    # set 4: every column must contain all symbols once <=> no 2 cells in the same column can have the same symbol
    for j in range(n):
        for i1 in range(n):
            for i2 in range(i1 + 1, n):
                for v in symbols:
                    literal1 = "cell_has_value([%d, %d], %c)" % (i1 + 1, j + 1, v)
                    literal2 = "cell_has_value([%d, %d], %c)" % (i1 + 1, j + 1, v)
                    clauses.append([-variables[literal1], -variables[literal2]])


    # set 5: every block must contain all symbols once <=> no 2 cells in the same block can have the same symbol (if blocks exist)
    


    print len(clauses)
    # return all the clauses (constraints)
    return clauses




# main functiom
if __name__ == '__main__':

    # make sure that the solver is legit
    if not (os.path.isfile(solver) and os.access(solver, os.X_OK)):
        print "\nSet the path to solver correctly on line 2 of this file (%s).\n" % sys.argv[0]
        sys.exit(1)

    # read the input file
    input = parse_input("input_sudoku.txt")

    # assign the input to the correct variables
    n = input[0]
    rows_per_block = input[1]
    columns_per_block = input[2]
    symbols = input[3]
    cell_values = input[4]

    print n
    print rows_per_block
    print columns_per_block
    print symbols
    print cell_values

    variables = gen_vars(n, symbols)
    constraints = gen_contraints(variables, n, rows_per_block, columns_per_block, symbols)
    # print variables
