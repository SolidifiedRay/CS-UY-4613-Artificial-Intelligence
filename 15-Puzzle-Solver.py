from copy import deepcopy
# Author: Yuanrui Chen yc3346

class Node:
    def __init__(self, puzz):
        self.state = puzz
        self.parent = None
        self.child = []
        self.move = ""
        self.g = 0
        self.h = 0

    def display(self):
        #for debug
        print("state:")
        for i in range(4):
            print(self.state[i])
        print("parent:")
        if self.parent:
            for i in range(4):
                print(self.parent.state[i])
        print("children:")
        for i in range(len(self.child)):
            print(self.child[i].state)
        print("move: ", self.move)
        print("g: ", self.g)
        print("h: ", self.h)

class FifteenPuzzlesSolver:
    def __init__(self):
        self.initial_state = []   # store the initial position of the puzzle
        self.goal_state = []  # store  the goal state of the puzzle
        self.expanded = []  # store the expanded node
        self.front = []  # store tree node
        self.viewed_state = []  # store the state of the node to avoid repeating state
        self.front_state = []  # store the state of the tree node in the front

    def read_input_file(self):
        # read the input
        print("Type the input file name: (example: input1.txt)")
        inputFile = input()
        f = open(inputFile, "r")
        for i in range(9):
            if i < 4:
                self.initial_state.append(f.readline().strip("\n").split(" "))
            elif i > 4:
                self.goal_state.append(f.readline().strip("\n").split(" "))
            else:
                f.readline()
        # to make sure the format is correct
        for r in range(len(self.initial_state)):
            for c in range(len(self.initial_state[r])):
                if (not (self.initial_state[r][c].isdigit())):
                    del self.initial_state[r][c]
        for r in range(len(self.goal_state)):
            for c in range(len(self.goal_state[r])):
                if (not (self.goal_state[r][c].isdigit())):
                    del self.goal_state[r][c]
        f.close()

    def find_index(self, num):
        # return the number index in goal state
        for r in range(4):
            for c in range(4):
                if self.goal_state[r][c] == num:
                    return [r, c]

    def heuristic(self, puzz):
        # Manhattan Distance
        distance = 0
        for r in range(4):
            for c in range(4):
                if puzz[r][c] != self.goal_state[r][c] and puzz[r][c] != "0":
                    goal = self.find_index(puzz[r][c])
                    distance += (abs(r-goal[0]) + abs(c-goal[1]))
        return distance

    def expand(self, node):
        #expand the node and add the expanded nodes to their parent node
        self.expanded.append(node)
        self.viewed_state.append(node.state)
        self.front.remove(node)
        self.front_state.remove(node.state)

        cost = node.g + 1
        output = []
        puzz = deepcopy(node.state)

        #find zero index
        row = 0
        col = 0
        for r in range(4):
            for c in range(4):
                if puzz[r][c] == "0":
                    row = r
                    col = c

        # if not reapeat, move left
        if col != 3:
            puzz[row][col], puzz[row][col + 1] = puzz[row][col + 1], puzz[row][col]
            left = deepcopy(puzz)
            if left not in self.viewed_state:
                # create new node and add it to the front
                left_node = Node(left)
                left_node.parent = node
                left_node.move = "L"
                left_node.g = cost
                left_node.h = self.heuristic(left)
                output.append(left_node)
                self.front.append(left_node)
                self.front_state.append(left)
            puzz[row][col], puzz[row][col + 1] = puzz[row][col + 1], puzz[row][col]

        # if not repeat, move right
        if col != 0:
            puzz[row][col], puzz[row][col - 1] = puzz[row][col - 1], puzz[row][col]
            right = deepcopy(puzz)
            if right not in self.viewed_state:
                # create new node and add it to the front
                right_node = Node(right)
                right_node.parent = node
                right_node.move = "R"
                right_node.g = cost
                right_node.h = self.heuristic(right)
                output.append(right_node)
                self.front.append(right_node)
                self.front_state.append(right)
            puzz[row][col], puzz[row][col - 1] = puzz[row][col - 1], puzz[row][col]

        # if not repeat, move up
        if row != 3:
            puzz[row][col], puzz[row + 1][col] = puzz[row + 1][col], puzz[row][col]
            up = deepcopy(puzz)
            if up not in self.viewed_state:
                # create new node and add it to the front
                up_node = Node(up)
                up_node.parent = node
                up_node.move = "U"
                up_node.g = cost
                up_node.h = self.heuristic(up)
                output.append(up_node)
                self.front.append(up_node)
                self.front_state.append(up)
            puzz[row][col], puzz[row + 1][col] = puzz[row + 1][col], puzz[row][col]

        # if not repeat, move down
        if row != 0:
            puzz[row][col], puzz[row - 1][col] = puzz[row - 1][col], puzz[row][col]
            down = deepcopy(puzz)
            if down not in self.viewed_state:
                # create new node and add it to the front
                down_node = Node(down)
                down_node.parent = node
                down_node.move = "D"
                down_node.g = cost
                down_node.h = self.heuristic(down)
                output.append(down_node)
                self.front.append(down_node)
                self.front_state.append(down)
            puzz[row][col], puzz[row - 1][col] = puzz[row - 1][col], puzz[row][col]

        node.child = output

    def return_smallest_fn_index(self):
        # return the index of the node with the smallest f(n) value in the front
        index = 0
        smallest_f = 99999999
        for i in range(len(self.front)):
            f = self.front[i].g + self.front[i].h
            if f < smallest_f:
                smallest_f = f
        for i in range(len(self.front)):
            f = self.front[i].g + self.front[i].h
            if f == smallest_f:
                return i
        return index

    def astar_search(self, initial, goal):
        # A* search and return the goal node

        # the root node of the tree
        initial_node = Node(initial)
        initial_node.h = self.heuristic(initial)
        self.front.append(initial_node)
        self.front_state.append(initial)
        self.expand(initial_node)

        while goal not in self.front_state:
            self.expand(self.front[self.return_smallest_fn_index()])
            if goal in self.front_state:
                index = self.front_state.index(goal)
                goal_node = self.front[index]
                return goal_node


    def solve(self):
        # output the result
        goal_node = self.astar_search(self.initial_state, self.goal_state)
        f = open("output.txt", 'w')
        print("output: ")
        for r in range(4):
            line = ""
            for c in range(4):
                line += self.initial_state[r][c] + " "
            print(line)
            f.write(line)
            f.write("\n")
        print()
        f.write("\n")
        for r in range(4):
            line = ""
            for c in range(4):
                line += self.goal_state[r][c] + " "
            print(line)
            f.write(line)
            f.write("\n")
        print()
        f.write("\n")
        print(str(goal_node.g))
        f.write(str(goal_node.g))
        f.write("\n")
        print(str(len(self.expanded)+len(self.front)))
        f.write(str(len(self.expanded)+len(self.front)))
        f.write("\n")
        path = ""
        fn = ""
        node = goal_node
        while node.parent:
            path = node.move + " " + path
            fn = str(node.g + node.h) + " " +  fn
            node = node.parent
        print(path)
        f.write(path)
        print(fn)
        f.write("\n")
        f.write(fn)
        f.close()

if __name__ == '__main__':
    solver = FifteenPuzzlesSolver()
    solver.read_input_file()
    solver.solve()
