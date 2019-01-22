import pygame
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT


class Graphics:

    def __init__(self, maze):
        pygame.init()
        self.case_size = 40
        self.window = pygame.display.set_mode(
            (15*self.case_size, 16*self.case_size))
        self.collected_items = []
        self.maze = maze

        # Loading of cases' images
        self.img_empty_case = self.load_image("images/case-vide-40.png")
        self.img_case_wall = self.load_image("images/case-mur-40.png")
        self.img_start_case = self.load_image("images/case-depart-40.png")
        self.img_finish_case = self.load_image("images/case-arrivee-40.png")

        # Loading of items' images
        self.img_ether = self.load_image("images/ether-40.png")
        self.img_needle = self.load_image("images/needle-40.png")
        self.img_tube = self.load_image("images/tube-40.png")
        self.img_syringe = self.load_image("images/syringe-40.png")

        # Loading of character, warden, victory and endofgame images
        self.img_warden = self.load_image("images/gardien-40.png")
        self.position_warden = self.img_warden.get_rect(topleft=(
            self.maze.finish_case[0][0]*self.case_size, (
                self.maze.finish_case[0][1]-1)*self.case_size))
        self.img_char = self.load_image("images/macgyver-40.png")
        self.position_char = self.img_char.get_rect(
            topleft=(self.maze.start_case[0][0]*self.case_size, (
                self.maze.start_case[0][1]*self.case_size)))
        self.endofgame = pygame.image.load("images/fin.png").convert()
        self.victory = pygame.image.load("images/victoire.png").convert()

        # Defining items positions
        self.position_ether = self.pos(self.img_ether, self.maze.ether)
        self.position_needle = self.pos(self.img_needle, self.maze.needle)
        self.position_tube = self.pos(self.img_tube, self.maze.tube)
        self.position_syringe = self.pos(self.img_syringe, self.maze.syringe)

    def pos(self, img_item, item):
        pos_item = img_item.get_rect(
         topleft=(self.case_size*(item[0]), self.case_size*(item[1])))
        return pos_item

    def load_image(self, path):
        image = pygame.image.load(path)
        converted_image = image.convert()
        scaled_image = pygame.transform.scale(
            converted_image, (self.case_size, self.case_size)
        )
        return scaled_image

    # Bliting images of the cases
    def display_cases(self):

        y = 0
        for line in self.maze.cases:
            x = 0
            for case in line:
                if case == "vide":
                    self.window.blit(self.img_empty_case, (
                                x*self.case_size, y*self.case_size))
                if case == "mur":
                    self.window.blit(self.img_case_wall, (
                                x*self.case_size, y*self.case_size))
                if case == "depart":
                    self.window.blit(self.img_start_case, (
                                x*self.case_size, y*self.case_size))
                if case == "arrivee":
                    self.window.blit(self.img_finish_case, (
                                x*self.case_size, y*self.case_size))
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

        continue_game = True

        while continue_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    continue_game = False
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        if self.maze.get_type(
                            int(self.position_char[0]/self.case_size), (
                             int(self.position_char[1]/self.case_size)+1)) == \
                             "mur":
                                pass
                        else:
                            self.position_char = self.position_char.move(
                                0, self.case_size)
                    if event.key == K_UP:
                        if self.maze.get_type(
                            int(self.position_char[0]/self.case_size), (
                             int(self.position_char[1]/self.case_size)-1)) == \
                             "mur":
                            pass
                        else:
                            self.position_char = self.position_char.move(
                                0, -self.case_size)
                    if event.key == K_LEFT:
                        if self.maze.get_type(
                            int(self.position_char[0]/self.case_size)-1, (
                             int(self.position_char[1]/self.case_size))) == \
                             "mur":
                            pass
                        else:
                            self.position_char = self.position_char.move(
                                -self.case_size, 0)
                    if event.key == K_RIGHT:
                        if self.maze.get_type(
                            int(self.position_char[0]/self.case_size)+1, (
                             int(self.position_char[1]/self.case_size))) == \
                             "mur":
                            pass
                        else:
                            self.position_char = self.position_char.move(
                                self.case_size, 0)

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
                if (self.position_char[0]/self.case_size, (
                    self.position_char[1]/self.case_size)) == \
                    (self.position_warden[0]/self.case_size - 1, (
                        self.position_warden[1]/self.case_size)):
                    if "ether" in self.collected_items \
                     and "needle" in self.collected_items \
                     and "tube" in self.collected_items \
                     and "syringe" in self.collected_items:
                        self.position_warden = \
                         self.position_warden.move(0, -self.case_size)
                    else:
                        continue_game = False
                        game_won = False

                # If play get to finish
                if (self.position_char[0]/self.case_size, (
                    self.position_char[1]/self.case_size)) == (
                     self.maze.finish_case[0][0], self.maze.finish_case[0][1]):
                    game_won = True
                    continue_game = False

            # Re-pasting cases
            self.display_cases()

        endofgame = True
        while endofgame:
            for event in pygame.event.get():
                if event.type == QUIT:
                    endofgame = False
                if continue_game is False:
                    self.display_cases()
                    if game_won is True:
                        self.window.blit(self.victory, (
                            pygame.Surface.get_width(
                                self.window)/2, pygame.Surface.get_width(
                                    self.window)/2))
                    else:
                        self.window.blit(self.endofgame, (
                            pygame.Surface.get_width(
                                self.window)/2, pygame.Surface.get_width(
                                    self.window)/2))

                # Refreshing
                pygame.display.flip()
