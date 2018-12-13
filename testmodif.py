import random
import pygame
from pygame.locals import *


class Maze:

    # CONSTRUCTEUR # # #
    def __init__(self):
        self.cases = []
        self.items = []
        self.empty_cases = []
        self.wall_case = []
        self.start_case = []
        self.finish_case = []

        self.load_map("Maze.txt")

        #  Generate items, and store them in self.items
        self.needle = random.choice(self.empty_cases)
        self.tube = random.choice(self.empty_cases)
        self.ether = random.choice(self.empty_cases)

        #  if two items are on the same case, we generate them again
        #  TODO: regenerer uniquement l'objet qui se trouve sur un autre - utiliser del
        while self.tube == self.needle or self.tube == self.ether or self.ether == self.needle:
            self.needle = random.choice(self.empty_cases)
            self.tube = random.choice(self.empty_cases)
            self.ether = random.choice(self.empty_cases)

    # Storing cases in self.cases

    def load_map(self, filename):
        with open(filename, "r") as my_file:
            for line in my_file.readlines():
                my_list = line.split()
                self.cases.append(my_list)
            for line in self.cases:
                i = 0
                i_line = self.cases.index(line)
                for case in line:
                    if "vide" == case:
                        self.empty_cases.append([i, i_line])
                    if "mur" == case:
                        self.wall_case.append([i, i_line])
                    if "depart" == case:
                        self.start_case.append([i, i_line])
                    if "arrivee" == case:
                        self.finish_case.append([i, i_line])
                    i += 1

    # # #  INTERFACE GRAPHIQUE # # # # # # # # # # # # # # # # # # # # # # # #
    # TODO: faire classe IG

    def graphic_interface(self):

        pygame.init()

        case_size = 40
        window = pygame.display.set_mode((15*case_size, 16*case_size))

        def display_cases(self):

            #  loading and display of empty cases
            # TODO: charger les cases une seule fois dans une méthode
            #  de chargement
            self.img_empty_case = pygame.image.load(
                "case-vide-40.png").convert()
            self.img_empty_case = pygame.transform.scale(
                self.img_empty_case, (case_size, case_size))

            #  loading and display of wall cases
            self.img_case_mur = pygame.image.load("case-mur-40.png").convert()
            self.img_case_mur = pygame.transform.scale(
                self.img_case_mur, (case_size, case_size))

            #  loading and display of start
            self.img_start_case = pygame.image.load(
                "case-depart-40.png").convert()
            self.img_start_case = pygame.transform.scale(
                self.img_start_case, (case_size, case_size))

            #  loading and display of finish
            self.img_finish_case = pygame.image.load(
                "case-arrivee-40.png").convert()
            self.img_finish_case = pygame.transform.scale(
                self.img_finish_case, (case_size, case_size))

            y = 0
            for line in self.cases:
                x = 0
                for case in line:
                    if case == "vide":
                        window.blit(self.img_empty_case,
                                    (x*case_size, y*case_size))
                    if case == "mur":
                        window.blit(self.img_case_mur,
                                    (x*case_size, y*case_size))
                    if case == "depart":
                        window.blit(self.img_start_case,
                                    (x*case_size, y*case_size))
                    if case == "arrivee":
                        window.blit(self.img_finish_case,
                                    (x*case_size, y*case_size))
                    x += 1
                y += 1

        #  loading and display of items
        self.collected_items = []  # list of collected items
        self.img_ether = pygame.image.load("ether-40.png")
        self.img_ether = pygame.transform.scale(
            self.img_ether, (case_size, case_size))
        self.img_ether.set_colorkey((255, 255, 255))
        self.img_needle = pygame.image.load("needle-40.png")
        self.img_needle = pygame.transform.scale(
            self.img_needle, (case_size, case_size))
        self.img_needle.set_colorkey((255, 255, 255))
        self.img_tube = pygame.image.load("tube-40.png")
        self.img_tube = pygame.transform.scale(
            self.img_tube, (case_size, case_size))
        self.img_tube.set_colorkey((255, 255, 255))
        pos_img_ether_x = case_size*(self.ether[0])
        pos_img_ether_y = case_size*(self.ether[1])
        pos_img_needle_x = case_size*(self.needle[0])
        pos_img_needle_y = case_size*(self.needle[1])
        pos_img_tube_x = case_size*(self.tube[0])
        pos_img_tube_y = case_size*(self.tube[1])
        position_ether = self.img_ether.get_rect(
            topleft=(pos_img_ether_x, pos_img_ether_y))
        position_needle = self.img_needle.get_rect(
            topleft=(pos_img_needle_x, pos_img_needle_y))
        position_tube = self.img_tube.get_rect(
            topleft=(pos_img_tube_x, pos_img_tube_y))
        window.blit(self.img_ether, position_ether)
        window.blit(self.img_needle, position_needle)
        window.blit(self.img_tube, position_tube)

        #  loading and display of warden
        self.img_warden = pygame.image.load("gardien-40.png").convert()
        self.img_warden = pygame.transform.scale(
            self.img_warden, (case_size, case_size))
        self.img_warden.set_colorkey((255, 255, 255))
        position_warden = self.img_warden.get_rect(topleft=(
            self.finish_case[0][0]*case_size, (self.finish_case[0][1]-1)*case_size))
        window.blit(self.img_warden, position_warden)
        warden_coordinates = [position_warden[0] /
                              case_size, position_warden[1]/case_size]

        # we make sure that item doesnt appear on warden
        while self.needle == warden_coordinates or self.tube == warden_coordinates or self.ether == warden_coordinates:
            self.needle = random.choice(self.empty_cases)
            self.tube = random.choice(self.empty_cases)
            self.ether = random.choice(self.empty_cases)
        else:
            self.items.extend([self.needle, self.tube, self.ether])

        #  loading and display of character
        self.img_char = pygame.image.load("MacGyver-40.png").convert()
        self.img_char.set_colorkey((255, 255, 255))
        self.img_char = pygame.transform.scale(
            self.img_char, (case_size, case_size))
        position_char = self.img_char.get_rect(
            topleft=(self.start_case[0][0]*case_size, self.start_case[0][1]*case_size))
        window.blit(self.img_char, position_char)
        # refreshing of screen
        pygame.display.flip()

        # if key is maintained, the action repeats
        pygame.key.set_repeat(30, 100)

        # loop
        continue_game = 1
        while continue_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    continue_game = 0
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        if Maze.get_type(self, int(position_char[0]/case_size), int(position_char[1]/case_size)+1) == "mur":
                            print("mur , {},{}".format(
                                int(position_char[0]/case_size), int(position_char[1]/case_size)+1))
                        else:
                            position_char = position_char.move(0, case_size)
                    if event.key == K_UP:
                        if Maze.get_type(self, int(position_char[0]/case_size), int(position_char[1]/case_size)-1) == "mur":
                            print("mur , {},{}".format(
                                int(position_char[0]/case_size), int(position_char[1]/case_size)-1))
                        else:
                            position_char = position_char.move(0, -case_size)
                    if event.key == K_LEFT:
                        if Maze.get_type(self, int(position_char[0]/case_size)-1, int(position_char[1]/case_size)) == "mur":
                            print("mur , {},{}".format(
                                int(position_char[0]/case_size)-1, int(position_char[1]/case_size)))
                        else:
                            position_char = position_char.move(-case_size, 0)
                    if event.key == K_RIGHT:
                        if Maze.get_type(self, int(position_char[0]/case_size)+1, int(position_char[1]/case_size)) == "mur":
                            print("mur , {},{}".format(
                                int(position_char[0]/case_size)+1, int(position_char[1]/case_size)))
                        else:
                            position_char = position_char.move(case_size, 0)

                # if play walk on item, he collects it
                if position_char == position_ether:
                    position_ether = self.img_ether.get_rect(
                        topleft=(case_size*14, case_size*15))
                    self.collected_items.append("ether")
                    print("collecté: {}".format(self.collected_items))
                if position_char == position_needle:
                    position_needle = self.img_needle.get_rect(
                        topleft=(case_size*13, case_size*15))
                    self.collected_items.append("needle")
                    print("collecté: {}".format(self.collected_items))
                if position_char == position_tube:
                    position_tube = self.img_tube.get_rect(
                        topleft=(case_size*12, case_size*15))
                    self.collected_items.append("tube")
                    print("collecté: {}".format(self.collected_items))

                # if play meet warden
                if (position_char[0]/case_size, position_char[1]/case_size) == (position_warden[0]/case_size - 1, position_warden[1]/case_size):
                    if "ether" in self.collected_items and "needle" in self.collected_items and "tube" in self.collected_items:
                        position_warden = position_warden.move(0, -case_size)
                        print("items collectés: {}".format(
                            self.collected_items))
                        print("vous pouvez passer")
                    else:
                        continue_game = 0
                        game_won = 0

                # if play get to finish
                if (position_char[0]/case_size, position_char[1]/case_size) == (self.finish_case[0][0], self.finish_case[0][1]):
                    game_won = 1
                    continue_game = 0

            # recollage
            display_cases(self)
            window.blit(self.img_ether, position_ether)
            window.blit(self.img_needle, position_needle)
            window.blit(self.img_tube, position_tube)
            window.blit(self.img_warden, position_warden)
            window.blit(self.img_char, position_char)

            # rafraichissement
            pygame.display.flip()

        endofgame = 1
        while endofgame:
            for event in pygame.event.get():
                if event.type == QUIT:
                    endofgame = 0
            # if continue_game = 0
            self.endofgame = pygame.image.load("fin.png").convert()
            self.victory = pygame.image.load("victoire.png").convert()
            display_cases(self)
            window.blit(self.img_ether, position_ether)
            window.blit(self.img_needle, position_needle)
            window.blit(self.img_tube, position_tube)
            window.blit(self.img_warden, position_warden)
            window.blit(self.img_char, position_char)
            if game_won == 1:
                window.blit(self.victory, (pygame.Surface.get_width(
                    window)/2, pygame.Surface.get_width(window)/2))
            else:
                window.blit(self.endofgame, (pygame.Surface.get_width(
                    window)/2, pygame.Surface.get_width(window)/2))

            # refreshing
            pygame.display.flip()

    # # #  FONCTIONS # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Return type of the case whose coordinates are x,y

    def get_type(self, x, y):
        try:
            self.cases[x][y]
        except IndexError:
            return("mur")
        else:
            return(self.cases[y][x])

    # Return items stored in self.items as a list of coordinates [x,y]
    def get_items(self):
        return(self.items)

    # Return type and coordinates of case "c"
    def get_coord_c(self, c):
        my_list_case_c = []
        for line in self.cases:
            i = 0
            for case in line:
                if c == case:
                        #  print("case *{}* in position ({},{}) ".format(c, i, self.cases.index(line) )) #  c = case, return type and coordinates of c
                    my_list_case_c.append([i, self.cases.index(line)])
                    i += 1
                else:
                    i += 1
        return(my_list_case_c)

    def get_wall_case(self):
        return(self.wall_case)


laby = Maze()
print(laby.graphic_interface())
