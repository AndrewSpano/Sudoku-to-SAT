# Sudoku to CNF converter (for SAT solvers)

This repository contains a python script that translates a Sudoku puzzle (with arbitrary grid size) to CNF clauses for the SAT solver CaDiCaL, runs the solver and prints the solutionf if it exists; else it prints that the problem is unsatisfiable.

In order to run this script, [CaDiCaL](http://fmv.jku.at/cadical/) has to be installed and compiled.

## How to compile

Get the sources, and go to the directory containing the zipped file.
```shell
$ tar Jxf cadical-1.0.3-cb89cbf.tar.xz
$ cd cadical-1.0.3-cb89cbf
$ mkdir build; cd build
$ ../configure
$ make
```

Now take note of the path of the executable, because we will need it:
```shell
$ pwd
````


## How to setup the script for your machine

Go to the [sudoku_to_sat.py](Sudoku_to_SAT/sudoku_to_sat.py) python script and change the second line to match the path of the CaDiCaL SAT solver in your machine.



## How to run the script

Be in the [directory](Sudoku_to_SAT) that contains [sudoku_to_sat.py](Sudoku_to_SAT/sudoku_to_sat.py), and run the command
```shell
$ python sudoku_to_sat.py <input_file>
```

where <input_file> is the file containing the Sudoku puzzle that you want to solve (more on the input file below).  
For example, to use the puzzles already provided in this repository, you can run
```shell
$ python sudoku_to_sat.py Examples/input_sudoku.txt
```
and the solution will be printed in stdout.



## How to write input files (Sudokus)

1. The first line of the input file must contain 3 integers separated by a space:  
<pre>                    Grid size n, rows per block r and columns per block c. </pre>
2. The second line contains all the n symbols that should be used to solve the Sudoku, separated by a space each.
3. Third line is empty.
4. From the fourth line and on, only the Sudoku puzzle should exist. Each line contains n cells. The cells who do not have a value, are represented with a dash ”-”. Those who have a value, are represented by it. Each cell is separated by a space. When a block ends (due to advancing in columns), then the character ”∣” should be put to indicate the boundaries of the block, and then proceed normally. When a block ends due to advancing in rows, a line of just dashes is placed again to indicate the boundaries of the block.  


For example, for the ordinary 9x9 Sudoku (n = 9) with 3x3 boxes (r = c = 3), the first 2 lines should be like this.
<pre>
9 3 3
1 2 3 4 5 6 7 8 9
</pre>  
You can also take a look directly at the [file](Sudoku_to_SAT/Examples/input_sudoku.txt) to see how to describe the Sudoku.



## Implementation

The basic idea of the script can be described in the steps below:  
1. Read and parse input from a file.
2. Convert the problem to CNF clauses.
3. Write the CNF clauses in a file, in a format so that CaDiCaL understands them.
4. Feed the file to CaDiCaL.
5. Read the output of CaDiCaL to see if a solution exists. If it exists, print it; else print that the problem is unsatisfiable.


You can take a look at the [report](Sudoku_to_SAT/report.pdf) I have written for implementation details and for matters regarding the logic/complexity of the conversion.

