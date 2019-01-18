import random
import pygame
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT


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

        #  Generate items, then delete their case from item_cases so the next one doesnt overlap
        self.item_cases = self.empty_cases.copy()  # List of collected items
        self.item_cases.remove([self.finish_case[0][0], self.finish_case[0][1]-1])  # Removing warden case
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
            for line in self.cases:
                i = 0
                i_line = self.cases.index(line) #TODO
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
                    my_list_case_c.append([i, self.cases.index(line)])
                    i += 1
                else: #TODO
                    i += 1
        return(my_list_case_c)

    def get_wall_case(self):
        return(self.wall_case)


class Graphics:

    def __init__(self, maze):
        pygame.init()
        self.case_size = 40
        self.window = pygame.display.set_mode((15*self.case_size, 16*self.case_size))
        self.collected_items = []
        self.maze = maze

        # Loading of cases' images
        self.img_empty_case = pygame.image.load("images/case-vide-40.png").convert() #TODO, #utiliser OS path join
        self.img_empty_case = pygame.transform.scale(
            self.img_empty_case, (self.case_size, self.case_size))
        self.img_case_wall = pygame.image.load("images/case-mur-40.png").convert()
        self.img_case_wall = pygame.transform.scale(
            self.img_case_wall, (self.case_size, self.case_size))
        self.img_start_case = pygame.image.load("images/case-depart-40.png").convert()
        self.img_start_case = pygame.transform.scale(
            self.img_start_case, (self.case_size, self.case_size))
        self.img_finish_case = pygame.image.load("images/case-arrivee-40.png").convert()
        self.img_finish_case = pygame.transform.scale(
            self.img_finish_case, (self.case_size, self.case_size))

        # Loading of items' images
        self.img_ether = pygame.image.load("images/ether-40.png").convert()
        self.img_ether = pygame.transform.scale(
            self.img_ether, (self.case_size, self.case_size))
        self.img_ether.set_colorkey((255, 255, 255))
        self.img_needle = pygame.image.load("images/needle-40.png")
        self.img_needle = pygame.transform.scale(
            self.img_needle, (self.case_size, self.case_size))
        self.img_needle.set_colorkey((255, 255, 255))
        self.img_tube = pygame.image.load("images/tube-40.png")
        self.img_tube = pygame.transform.scale(
            self.img_tube, (self.case_size, self.case_size))
        self.img_tube.set_colorkey((255, 255, 255))
        self.img_syringe = pygame.image.load("images/syringe-40.png")
        self.img_syringe = pygame.transform.scale(
            self.img_syringe, (self.case_size, self.case_size))
        self.img_syringe.set_colorkey((255, 255, 255))

        # Loading of character, warden, victory and endofgame images
        self.img_warden = pygame.image.load("images/gardien-40.png").convert()
        self.img_warden = pygame.transform.scale(
            self.img_warden, (self.case_size, self.case_size))
        self.img_warden.set_colorkey((255, 255, 255))
        self.position_warden = self.img_warden.get_rect(topleft=(
            self.maze.finish_case[0][0]*self.case_size, (self.maze.finish_case[0][1]-1)*self.case_size))
        self.img_char = pygame.image.load("images/macgyver-40.png").convert()
        self.img_char.set_colorkey((255, 255, 255))
        self.img_char = pygame.transform.scale(
            self.img_char, (self.case_size, self.case_size))
        self.position_char = self.img_char.get_rect(
            topleft=(self.maze.start_case[0][0]*self.case_size, self.maze.start_case[0][1]*self.case_size))
        self.endofgame = pygame.image.load("images/fin.png").convert()
        self.victory = pygame.image.load("images/victoire.png").convert()

        # Defining items positions
        pos_img_ether_x = self.case_size*(self.maze.ether[0]) #TODO créer classe objet
        pos_img_ether_y = self.case_size*(self.maze.ether[1])
        pos_img_needle_x = self.case_size*(self.maze.needle[0])
        pos_img_needle_y = self.case_size*(self.maze.needle[1])
        pos_img_tube_x = self.case_size*(self.maze.tube[0])
        pos_img_tube_y = self.case_size*(self.maze.tube[1])
        pos_img_syringe_x = self.case_size*(self.maze.syringe[0])
        pos_img_syringe_y = self.case_size*(self.maze.syringe[1])
        self.position_ether = self.img_ether.get_rect(
            topleft=(pos_img_ether_x, pos_img_ether_y))
        self.position_needle = self.img_needle.get_rect(
            topleft=(pos_img_needle_x, pos_img_needle_y))
        self.position_tube = self.img_tube.get_rect(
            topleft=(pos_img_tube_x, pos_img_tube_y))
        self.position_syringe = self.img_syringe.get_rect(
            topleft=(pos_img_syringe_x, pos_img_syringe_y))

    # Bliting images of the cases
    def display_cases(self):

        y = 0
        for line in self.maze.cases:
            x = 0
            for case in line:
                if case == "vide":
                    self.window.blit(self.img_empty_case,
                                (x*self.case_size, y*self.case_size))
                if case == "mur":
                    self.window.blit(self.img_case_wall,
                                (x*self.case_size, y*self.case_size))
                if case == "depart":
                    self.window.blit(self.img_start_case,
                                (x*self.case_size, y*self.case_size))
                if case == "arrivee":
                    self.window.blit(self.img_finish_case,
                                (x*self.case_size, y*self.case_size))
                x += 1
            y += 1

        # Bliting items, char and warden images, and refreshing
        self.window.blit(self.img_ether, self.position_ether)
        self.window.blit(self.img_needle, self.position_needle)
        self.window.blit(self.img_tube, self.position_tube)
        self.window.blit(self.img_syringe, self.position_syringe)
        self.window.blit(self.img_warden, self.position_warden)
        self.window.blit(self.img_char, self.position_char)
        pygame.display.flip()

    def main_loop(self):

        self.display_cases()

        # If key is maintained, the action repeats
        pygame.key.set_repeat(30, 100)

        continue_game = 1
        while continue_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    continue_game = 0
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        if self.maze.get_type(int(self.position_char[0]/self.case_size), int(self.position_char[1]/self.case_size)+1) == "mur":
                            print("mur , {},{}".format(
                                int(self.position_char[0]/self.case_size), int(self.position_char[1]/self.case_size)+1))
                        else:
                            self.position_char = self.position_char.move(0, self.case_size)
                    if event.key == K_UP:
                        if self.maze.get_type(int(self.position_char[0]/self.case_size), int(self.position_char[1]/self.case_size)-1) == "mur":
                            print("mur , {},{}".format(
                                int(self.position_char[0]/self.case_size), int(self.position_char[1]/self.case_size)-1))
                        else:
                            self.position_char = self.position_char.move(0, -self.case_size)
                    if event.key == K_LEFT:
                        if self.maze.get_type(int(self.position_char[0]/self.case_size)-1, int(self.position_char[1]/self.case_size)) == "mur":
                            print("mur , {},{}".format(
                                int(self.position_char[0]/self.case_size)-1, int(self.position_char[1]/self.case_size)))
                        else:
                            self.position_char = self.position_char.move(-self.case_size, 0)
                    if event.key == K_RIGHT:
                        if self.maze.get_type(int(self.position_char[0]/self.case_size)+1, int(self.position_char[1]/self.case_size)) == "mur":
                            print("mur , {},{}".format(
                                int(self.position_char[0]/self.case_size)+1, int(self.position_char[1]/self.case_size)))
                        else:
                            self.position_char = self.position_char.move(self.case_size, 0)

                # If play walk on item, he collects it
                if self.position_char == self.position_ether:
                    self.position_ether = self.img_ether.get_rect(
                        topleft=(self.case_size*14, self.case_size*15))
                    self.collected_items.append("ether")
                    print("collecté: {}".format(self.collected_items))
                if self.position_char == self.position_needle:
                    self.position_needle = self.img_needle.get_rect(
                        topleft=(self.case_size*13, self.case_size*15))
                    self.collected_items.append("needle")
                    print("collecté: {}".format(self.collected_items))
                if self.position_char == self.position_tube:
                    self.position_tube = self.img_tube.get_rect(
                        topleft=(self.case_size*12, self.case_size*15))
                    self.collected_items.append("tube")
                    print("collecté: {}".format(self.collected_items))
                if self.position_char == self.position_syringe:
                    self.position_syringe = self.img_syringe.get_rect(
                        topleft=(self.case_size*11, self.case_size*15))
                    self.collected_items.append("syringe")
                    print("collecté: {}".format(self.collected_items))

                # If play meet warden
                if (self.position_char[0]/self.case_size, self.position_char[1]/self.case_size) == (self.position_warden[0]/self.case_size - 1, self.position_warden[1]/self.case_size):
                    if "ether" in self.collected_items and "needle" in self.collected_items and "tube" in self.collected_items and "syringe" in self.collected_items:
                        self.position_warden = self.position_warden.move(0, -self.case_size)
                        print("items collectés: {}".format(
                            self.collected_items))
                        print("vous pouvez passer")
                    else:
                        continue_game = 0
                        game_won = 0

                # If play get to finish
                if (self.position_char[0]/self.case_size, self.position_char[1]/self.case_size) == (self.maze.finish_case[0][0], self.maze.finish_case[0][1]):
                    game_won = 1
                    continue_game = 0

            # Re-pasting cases
            self.display_cases()

        endofgame = 1
        while endofgame:
            for event in pygame.event.get():
                if event.type == QUIT:
                    endofgame = 0
                if continue_game == 0:
                    self.display_cases()
                    if game_won == 1:
                        self.window.blit(self.victory, (pygame.Surface.get_width(
                            self.window)/2, pygame.Surface.get_width(self.window)/2))
                    else:
                        self.window.blit(self.endofgame, (pygame.Surface.get_width(
                            self.window)/2, pygame.Surface.get_width(self.window)/2))

                # Refreshing
                pygame.display.flip()


def main():
    laby = Maze("maze.txt")
    gui = Graphics(laby)
    gui.main_loop()


if __name__ == "__main__":
    main()
