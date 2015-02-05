#!/usr/bin/env python
#coding:utf-8

import copy

ROW = "ABCDEFGHI";
COL = "123456789";

# utility function to print each sudoku
def printSudoku(sudoku):
	print "-----------------"
	for i in ROW:
		for j in COL:
			print sudoku[i + j],
		print ""	

# Reading of sudoku list from file
try:
    f = open("sudokus.txt", "r")
    sudokuList = f.read()
    f.close()
except:
	print "Error in reading the sudoku file."
	exit()

# Define remove inconsistent value function
def remove_inconsistent_value(constraint, domain):
	removed = False
	if len(domain[constraint[1]]) == 1:
		for value in domain[constraint[0]]:
			if value == domain[constraint[1]][0]:
				domain[constraint[0]].remove(value)
				removed = True
	return removed

def AC_3(sudoku):

	domain = {}

	# Create Domain = {coordinate (ex: "A5") : possible value list (ex: [1,2,3,4,5,6,7,8,9])}
	for coord in sudoku:
		if sudoku[coord] == 0:
			domain[coord] = [1,2,3,4,5,6,7,8,9]
		else:
		 	domain[coord] = [sudoku[coord]]
	# print domain

	# Create Queue, and put the arc 
	queue = []
	for coord in sudoku:

		# Create arc for a row in sudoku
		for row in ROW:
			if row != coord[0]:
				queue.append([coord, row + coord[1]])


		# Create arc for a colume in sudoku
		for col in COL:
			if col != coord[1]:
				queue.append([coord, coord[0] + col])

		# Now create arc for a box

		row_map = {"A":0,"B":0,"C":0,"D":1,"E":1,"F":1,"G":2,"H":2,"I":2}
		col_map = {"1":0,"2":0,"3":0,"4":1,"5":1,"6":1,"7":2,"8":2,"9":2}

		row_box = row_map[coord[0]]
		col_box = col_map[coord[1]]

		for i in range(3):
			for j in range(3):
				if coord[0] != ROW[row_box*3 + i] and coord[1] !=  COL[col_box*3 + j]:
					queue.append([coord, ROW[row_box*3 + i] + COL[col_box*3 + j]])

	while len(queue) != 0:

		constraint = queue.pop()
		if remove_inconsistent_value(constraint,domain):
			# print "Update this" , constraint[0]
			coord = constraint[0]
			# Create arc for a row in sudoku
			for row in ROW:
				if row != coord[0]:
					queue.append([row + coord[1], coord])

			# Create arc for a colume in sudoku
			for col in COL:
				if col != coord[1]:
					queue.append([coord[0] + col, coord])

			# Now create arc for a box

			row_map = {"A":0,"B":0,"C":0,"D":1,"E":1,"F":1,"G":2,"H":2,"I":2}
			col_map = {"1":0,"2":0,"3":0,"4":1,"5":1,"6":1,"7":2,"8":2,"9":2}

			row_box = row_map[coord[0]]
			col_box = col_map[coord[1]]

			for i in range(3):
				for j in range(3):
					if coord[0] != ROW[row_box*3 + i] and coord[1] !=  COL[col_box*3 + j]:
						queue.append([ROW[row_box*3 + i] + COL[col_box*3 + j], coord])

	return domain

def recursive_backtracking(domain, assignment,level):

	complete = True

	for variable in assignment:
		if assignment[variable] == [0]:
			complete = False
			# print "Not complete"
			break

	if complete == True:
		return assignment

	# Implement minimum remaining value heuristic
	min_variable = None
	min_value = 10

	for variable in domain:


		# If the length is less the min_value, and the that place is unassignment
		if len(domain[variable]) < min_value and assignment[variable] == [0]:
			min_variable = variable
			min_value = len(domain[variable])



	# For every possible value in 
	for value in domain[min_variable]:

		# Create a new domain
		new_domain = copy.deepcopy(domain)

		# Assign value to that variable, and reduce domain
		new_domain[min_variable] = [value]

		# Perform forward checking for the row, column, and box, remove inconsistent value
		# Remove the same value in the same column
		for row in ROW:
			if row != min_variable[0] and value in domain[row + min_variable[1]]:
				new_domain[row + min_variable[1]].remove(value)

		# Remove the same value in the same row
		for col in COL:
			if col != min_variable[1] and value in domain[min_variable[0] + col]:
				new_domain[min_variable[0] + col] .remove(value)

		# Remove the same value in the same box
		row_map = {"A":0,"B":0,"C":0,"D":1,"E":1,"F":1,"G":2,"H":2,"I":2}
		col_map = {"1":0,"2":0,"3":0,"4":1,"5":1,"6":1,"7":2,"8":2,"9":2}

		row_box = row_map[min_variable[0]]
		col_box = col_map[min_variable[1]]

		for i in range(3):
			for j in range(3):
				if min_variable != (ROW[row_box*3 + i] + COL[col_box*3 + j]) and value in new_domain[ROW[row_box*3 + i] + COL[col_box*3 + j]]:
					new_domain[ROW[row_box*3 + i] + COL[col_box*3 + j]].remove(value)
		
		consistent = True

		# If the assign will cause no space for other variable, return false
		for variable in new_domain:
			if len(new_domain[variable]) == 0:
				consistent = False

		if consistent == True:
			new_assignment = copy.deepcopy(assignment)
			new_assignment[min_variable] = [value]

			result = recursive_backtracking(new_domain, new_assignment, level + 1)

			if result != False:
				return result
	return False



# Now Solving question 5 & 6

num_ac3_solved = 0

for line in sudokuList.split("\n"):

	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

	# Perform AC-3 algorithm
	result = AC_3(sudoku)

	# Check if we have unique number for every variable, if so, the puzzle is solved

	solved = True
	for variable in result:
		if len(result[variable]) != 1:
			solved = False

	if solved == True:
		num_ac3_solved += 1
		print "-----------------"
		for row in range(9):
			for col in range(9):
				print result[ROW[row]+COL[col]][0] ,
			print ""

print "Number solved by AC3: " , num_ac3_solved


for line in sudokuList.split("\n"):

	try:
		f = open("sudokus.txt","r")
		sudokuList = f.read()
	except:
		print "Error in reading the sudoku file."
		exit()

	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

	domain = AC_3(sudoku)
	assignment = {}

	# Create Domain = {coordinate (ex: "A5") : possible value list (ex: [1,2,3,4,5,6,7,8,9])}
	for coord in sudoku:
		if sudoku[coord] == 0:
			assignment[coord] = [0]
		else:
			assignment[coord] = [sudoku[coord]]

	result = recursive_backtracking(domain, assignment, 0)
	
	print "-----------------"
	for row in range(9):
		for col in range(9):
			print result[ROW[row]+COL[col]][0] ,
		print ""


	f = open("output.txt", "a")
	f.write("-----------------\n")
	for row in range(9):
		for col in range(9):
			f.write(str(result[ROW[row]+COL[col]][0]))
			if col != 9:
				f.write(" ")
		f.write("\n")
	f.close()










