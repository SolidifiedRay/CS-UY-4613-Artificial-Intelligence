from copy import deepcopy
# Author: Yuanrui Chen

class FutoshikiSolver:
	def __init__(self):
		self.board = []  # in a CSP problem, this is "X", the set of variables
		self.inequal_horizontal = []  # in a CSP problem, this is "C", the set of constraints
		self.inequal_vertical = []  # in a CSP problem, this is "C", the set of constraints
		self.domain = []  # in a CSP problem, this is "D", the set of domain
		self.already_assign = []   # store the index of the cells that is already assign

	def read_input_file(self):
		# read the input and store them into array
		print("Type the input file name: (example: input1.txt)")
		inputFile = input()
		f = open(inputFile, "r")
		for i in range(17):
			if i < 5:
				self.board.append(f.readline().strip("\n").split(" "))
			elif i > 5 and i < 11:
				self.inequal_horizontal.append(f.readline().strip("\n").split(" "))
			elif i > 11 and i < 16:
				self.inequal_vertical.append(f.readline().strip("\n").split(" "))
			else:
				f.readline()
		f.close()
		self.check_input()

	def check_input(self):
	# the input file in the nyu class contain unexpected spaces, removing those spaces in this function
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				if (not (self.board[r][c].isdigit())):
					del self.board[r][c]
		for r in range(len(self.inequal_horizontal)):
			for c in range(len(self.inequal_horizontal[r])):
				if (not (self.inequal_horizontal[r][c].isdigit() or self.inequal_horizontal[r][c]==">"
						 or self.inequal_horizontal[r][c]=="<")):
					del self.inequal_horizontal[r][c]
		for r in range(len(self.inequal_vertical)):
			for c in range(len(self.inequal_vertical[r])):
				if (not (self.inequal_vertical[r][c].isdigit() or self.inequal_vertical[r][c]=="^"
						 or self.inequal_vertical[r][c]=="v")):
					del self.inequal_vertical[r][c]

	def initiate_domain(self):
		# initiate the domain of all the empties cells for later forward checking
		for row in range(5):
			self.domain.append([[], [], [], [], []])
			for col in range(5):
				if self.board[row][col] == "0":
					self.domain[row][col] = ["1", "2", "3", "4", "5"]
				else:
					self.domain[row][col] = [self.board[row][col]]
					self.already_assign.append([row, col])

	def reduce_inequal_domian(self, num, row, col, sign):
		# reduce the domain because of the inequal sign constraint
		if sign == "bigger":
			# remove all the domain value that is bigger than the number
			for i in range(len(self.domain[row][col])-1,0,-1):
				if self.domain[row][col][i] < num:
					self.domain[row][col] = self.domain[row][col][0:i+1]
					return
		if sign == "smaller":
			# remove all the domain value that is smaller than the number
			for i in range(len(self.domain[row][col])):
				if self.domain[row][col][i] > num:
					self.domain[row][col] = self.domain[row][col][i:]
					return

	def update_domain(self, row, col):
		# update neighbors'domain value after assignment
		# if the domain of a cell is empty, stop the program:
		if len(self.domain[row][col]) == 0:
			return False
		num = self.board[row][col]
		# each row and col cannot have repeated number
		for c in range(len(self.board[row])):
			if c != col:
				try:
					self.domain[row][c].remove(num)
				except:
					pass
		for r in range(len(self.board)):
			if r != row:
				try:
					self.domain[r][col].remove(num)
				except:
					pass
		# Adjacent number should satisfy the inequality
		# check for upper inequality
		if row > 0:
			if self.inequal_vertical[row-1][col] == "^":
				self.reduce_inequal_domian(self.board[row][col], row-1, col, "bigger")
			elif self.inequal_vertical[row-1][col] == "v":
				self.reduce_inequal_domian(self.board[row][col], row-1, col, "smaller")
		# check for lower inequality
		if row < 4:
			if self.inequal_vertical[row][col] == "^":
				self.reduce_inequal_domian(self.board[row][col], row+1, col, "smaller")
			elif self.inequal_vertical[row][col] == "v":
				self.reduce_inequal_domian(self.board[row][col], row+1, col, "bigger")
		# check for left inequality
		if col > 0:
			if self.inequal_horizontal[row][col-1] == "<":
				self.reduce_inequal_domian(self.board[row][col], row, col-1, "bigger")
			elif self.inequal_horizontal[row][col-1] == ">":
				self.reduce_inequal_domian(self.board[row][col], row, col-1, "smaller")
		# check for right inequality
		if col < 4:
			if self.inequal_horizontal[row][col] == "<":
				self.reduce_inequal_domian(self.board[row][col], row, col+1, "smaller")
			elif self.inequal_horizontal[row][col] == ">":
				self.reduce_inequal_domian(self.board[row][col], row, col+1, "bigger")

	def forward_checking(self):
		# first, use Forward Checking to reduce the domain of empty cells,
		# based on the values of cells that already have a number
		for i in range(len(self.already_assign)):
			row = self.already_assign[i][0]
			col = self.already_assign[i][1]
			self.update_domain(row, col)
		#  If an empty cell has only one value left in its
		# domain after domain reduction, repeat Forward Checking on the cell’s neighbors, and so on
		empty_cell = []
		for r in range(len(self.domain)):
			for c in range(len(self.domain[r])):
				if len(self.domain[r][c]) == 1 and [r, c] not in self.already_assign:
					empty_cell.append([r, c])
		while(len(empty_cell)!=0):
			cell = empty_cell[0]
			empty_cell = empty_cell[1:]
			self.update_domain(cell[0], cell[1])
			for r in range(len(self.domain)):
				for c in range(len(self.domain[r])):
					if len(self.domain[r][c]) == 1 and [r, c] not in self.already_assign:
						empty_cell.append([r, c])

	def find_most_constrained_variable(self):
		# return a list of the index of the most constrained variable
		# most constrained = least legal states = smallest domain size
		most_constrained = []
		min = 99999999
		for r in range(len(self.domain)):
			for c in range(len(self.domain[r])):
				if len(self.domain[r][c]) < min and ([r, c] not in self.already_assign):
					min = len(self.domain[r][c])
		for r in range(len(self.domain)):
			for c in range(len(self.domain[r])):
				if len(self.domain[r][c]) == min and ([r, c] not in self.already_assign):
					most_constrained.append([r, c])
		return most_constrained

	def find_unassigned_neighbors(self, row, col):
		# return the number of unassigned neighbors of a cell
		count = 0
		# count the unassigned neighbors in the same row
		for c in range(len(self.domain)):
			if c != col and ([row, c] not in self.already_assign):
				count += 1
		# count the unassigned neighbors in the same col
		for r in range(len(self.domain[row])):
			if r != row and ([r, col] not in self.already_assign):
				count += 1
		return count

	def find_most_constraining_variable(self, most_constrained):
		# return a list of index of most constraining variable
		# most constraining = cells have the most number of unassigned neighbor
		most_constraining = []
		cells = most_constrained
		neighbor = [] # this list store the number of unassigned neighbor
		for cell in cells:
			neighbor.append(self.find_unassigned_neighbors(cell[0], cell[1]))
		max = 0
		for count in neighbor:
			if count > max:
				max = count
		for i in range(len(neighbor)):
			if neighbor[i] == max:
				most_constraining.append(cells[i])
		return most_constraining

	def select_unassigned_variable(self):
		# return the index of unassigned variable based on most constrained and most constraining function
		select = self.find_most_constrained_variable()
		if len(select) > 1:
			select = self.find_most_constraining_variable(select)
		return select[0]

	def is_consistent(self, domain, row, col):
		#check if the domain value is consistent in the assignment
		num = domain
		# each row and col cannot have repeated number
		for c in range(len(self.board[row])):
			if c != col and self.board[row][c] == num:
				return False

		for r in range(len(self.board)):
			if r != row and self.board[r][col] == num:
				return False

		# Adjacent number should satisfy the inequality
		# check for upper inequality
		if row > 0:
			if self.inequal_vertical[row - 1][col] == "^":
				if self.board[row-1][col] != "0" and self.board[row-1][col] > domain:
					return False
			elif self.inequal_vertical[row - 1][col] == "v":
				if self.board[row-1][col] != "0" and self.board[row-1][col] < domain:
					return False
		# check for lower inequality
		if row < 4:
			if self.inequal_vertical[row][col] == "^":
				if self.board[row+1][col] != "0" and self.board[row+1][col] < domain:
					return False
			elif self.inequal_vertical[row][col] == "v":
				if self.board[row+1][col] != "0" and self.board[row+1][col] > domain:
					return False
		# check for left inequality
		if col > 0:
			if self.inequal_horizontal[row][col - 1] == "<":
				if self.board[row][col-1] != "0" and self.board[row][col-1] > domain:
					return False
			elif self.inequal_horizontal[row][col - 1] == ">":
				if self.board[row][col-1] != "0" and self.board[row][col-1] < domain:
					return False
		# check for right inequality
		if col < 4:
			if self.inequal_horizontal[row][col] == "<":
				if self.board[row][col+1] != "0" and self.board[row][col+1] < domain:
					return False
			elif self.inequal_horizontal[row][col] == ">":
				if self.board[row][col+1] != "0" and self.board[row][col+1] > domain:
					return False

		return True

	def backtrack(self):
		# use backtrack to solve the puzzle
		if len(self.already_assign) == 25:
			# if assginment is complete then return assignment
			return True
		else:
			# var <- SELECT-UNASSIGNED-VARIABLE(csp)
			assign = self.select_unassigned_variable()
			row = assign[0]
			col = assign[1]
			# for each value in ORDER-DOMAIN-VALUES (var, assignment, csp) do
			for domain in self.domain[row][col]:
				if self.is_consistent(domain, row, col):
					# if value is consistent with assignment, add value to assignment
					temp_domain = deepcopy(self.domain)
					temp_board_value = self.board[row][col]
					temp_already_assign = deepcopy(self.already_assign)
					self.board[row][col] = domain
					self.domain[row][col] = [self.board[row][col]]
					self.update_domain(row, col)
					self.already_assign.append([row, col])
					if(not self.backtrack()):
						self.domain = temp_domain
						self.board[row][col] = temp_board_value
						self.already_assign = temp_already_assign
					else:
						return True
			return False

	def display_board(self):
		# display the board, for debug purpose
		for row in self.board:
			print(row)
		print()

	def solve(self):
		self.read_input_file()
		self.initiate_domain()  # assign empty cells' domain
		self.forward_checking()  # reduce the domain before backtrack
		self.backtrack()   # solve the puzzle
		# write the result in output.txt and print the result
		f = open("output.txt", 'w')
		for r in range(5):
			line = ""
			for c in range(5):
				line += self.board[r][c] + " "
			print(line)
			f.write(line)
			f.write("\n")
		f.close()

if __name__ == '__main__':
	solver = FutoshikiSolver()
	solver.solve()