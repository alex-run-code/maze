import random


class Maze:

    # Constructor
    def __init__(self, map):
        self.cases = []
        self.items = []
        self.empty_cases = []
        self.wall_case = []
        self.start_case = []
        self.finish_case = []
        self.load_map(map)

        # Generate items, then delete their case from item_cases
        # so the next one doesnt overlap
        self.item_cases = self.empty_cases.copy()
        self.item_cases.remove(
            [self.finish_case[0][0], self.finish_case[0][1]-1])
        self.needle = random.choice(self.item_cases)
        self.item_cases.remove(self.needle)
        self.tube = random.choice(self.item_cases)
        self.item_cases.remove(self.tube)
        self.ether = random.choice(self.item_cases)
        self.item_cases.remove(self.ether)
        self.syringe = random.choice(self.item_cases)

    # Storing cases in self.cases
    def load_map(self, filename):
        with open(filename, "r") as my_file:
            for line in my_file.readlines():
                my_list = line.split()
                self.cases.append(my_list)
            for i_line, line in enumerate(self.cases):
                for i, case in enumerate(line):
                    if "vide" == case:
                        self.empty_cases.append([i, i_line])
                    if "mur" == case:
                        self.wall_case.append([i, i_line])
                    if "depart" == case:
                        self.start_case.append([i, i_line])
                    if "arrivee" == case:
                        self.finish_case.append([i, i_line])

    # Return type of the case whose coordinates are x,y
    def get_type(self, x, y):
        try:
            self.cases[x][y]
        except IndexError:
            return("mur")
        else:
            return(self.cases[y][x])
