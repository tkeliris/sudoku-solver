# sudoku-solver
Sudoku solver

My implementation of a sudoku solver in Python (tested on Python 2.7).
The solver propagates cell values according to basic sudoku rules. This is enough to solve easy/intermediate puzzles. For harder puzzles recursive brute forcing is applied, by selecting the values with the least possible values for better performance.

2 "easy" and 4 "hard" problems are included in the repo.

Inspiration by Peter Norvig's [Solving Every Sudoku Puzzle](http://norvig.com/sudoku.html)

Released under an MIT license

Copyright (c) 2015 Anastasis Keliris


Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.