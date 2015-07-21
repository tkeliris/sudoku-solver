# sudoku-solver
Sudoku solver

My implementation of a sudoku solver in Python (tested on Python 2.7).
The solver propagates cell values according to basic sudoku rules. This is enough to solve easy/intermediate puzzles. For harder puzzles recursive brute forcing is applied, by selecting the values with the least possible values for better performance.

2 "easy" and 4 "hard" problems are included in the repo.

Inspiration by Peter Norvig's [Solving Every Sudoku Puzzle](http://norvig.com/sudoku.html)

Released under an MIT license