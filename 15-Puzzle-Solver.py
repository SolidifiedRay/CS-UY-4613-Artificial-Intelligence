from copy import deepcopy
from collections import deque

class FifteenPuzzlesSolver:
    def __init__(self):
        self.initial_state = []
        self.goal_state = []
        self.path=[]
        self.f =[]

    def read_input_file(self):
        #print("Type the input file name: (example: input1.txt)")
        #inputFile = input()
        f = open("input1.txt", "r")
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

        print(self.initial_state)
        print(self.goal_state)

    def find_index(self, num):
        # return the goal state number index
        for r in range(4):
            for c in range(4):
                if self.goal_state[r][c] == num:
                    return [r, c]

    def heuristic(self, puzz):
        # Manhattan Distance
        distance = 0
        for r in range(4):
            for c in range(4):
                if puzz[r][c] != self.goal_state[r][c]:
                    goal = self.find_index(puzz[r][c])
                    distance += abs(r-goal[0]) + abs(c-goal[1])
        return distance

    def moves(self, puzz):
        # return all possible outcome
        output = []
        row = 0
        col = 0

        #find zero index
        for r in range(3):
            for c in range(3):
                if puzz[r][c] == "0":
                    row = r
                    col = c

        # if not repeat, move up
        if row != 3:
            puzz[row][col], puzz[row + 1][col] = puzz[row + 1][col], puzz[row][col]
            up = deepcopy(puzz)
            output.append(up)
            puzz[row][col], puzz[row + 1][col] = puzz[row + 1][col], puzz[row][col]

        # if not repeat, move down
        if row != 0:
            puzz[row][col], puzz[row - 1][col] = puzz[row - 1][col], puzz[row][col]
            down = deepcopy(puzz)
            output.append(down)
            puzz[row][col], puzz[row - 1][col] = puzz[row - 1][col], puzz[row][col]

        # if not reapeat, move left
        if col != 3:
            puzz[row][col], puzz[row][col + 1] = puzz[row][col + 1], puzz[row][col]
            left = deepcopy(puzz)
            output.append(left)
            puzz[row][col], puzz[row][col + 1] = puzz[row][col + 1], puzz[row][col]

        # if not repeat, move right
        if col != 0:
            puzz[row][col], puzz[row][col - 1] = puzz[row][col - 1], puzz[row][col]
            right = deepcopy(puzz)
            output.append(right)
            puzz[row][col], puzz[row][col - 1] = puzz[row][col - 1], puzz[row][col]
        '''
        # print all possible outcome
        for i in output:
            for j in range(len(i)):
                print(i[j])
        '''
        return output

    def astar_search(self, initial, goal):
        front = deque()
        expanded = []
        expanded_nodes = 0
        front.append([self.heuristic(self.initial_state),self.initial_state])
        while front:




solver = FifteenPuzzlesSolver()
solver.read_input_file()
solver.astar_search()
