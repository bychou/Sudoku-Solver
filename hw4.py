with open("sudokus.txt") as f:
	sudoku_line = f.readline()


sudoku = [[] for x in range(9)]

for row in range(9):
	for col in range(9):
		sudoku[row].append(sudoku_line[row*9 + col])

for row in sudoku:
	print row

for row in sudoku:



# def print_sudoku(sudoku):
# 	for row in range(9):
# 		for col in range(9):
# 			print sudoku[row * 9 + col] , 
# 		print ""

# def print_sudoku_1(sudoku):
# 	for row in range(3):
# 		for col in range(9):
# 			print sudoku[row * 9 + col] , 
# 		print ""
# print_sudoku(sudoku)
