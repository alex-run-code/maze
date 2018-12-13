#CREATION DU LABYRINTHE 
#générer des cases


#GENERATION DES OBJETS
#Les objets peuvent apparaitre au hasard sur n'importe quel case non-mur qui n'est ni l'arrivée ni le départ

#DEPLACEMENT DU JOUEUR
#le joueur commence au départ
#si le joueur veut se déplacer vers une case mur, il ne peut pas
#si le joueur se déplace vers une case non mur, il se positionne effectivement sur cette case
#si le joueur se déplace sur la case arrivée avec tout les objets, il gagne. Sinon, il meurt.
#si le joueur se déplace sur une case objet, il ramasse cet objet

import random
import pygame
from pygame.locals import *

class Labyrinthe:

   ### CONSTRUCTEUR #####################################################################################################

    def __init__(self):
        self.cases = []
        self.objets = []
        self.cases_vides = []
        self.cases_mur = []
        self.case_depart = []
        self.case_arrivee = []

        self.load_map("Labyrinthe.txt")

        #On génère les objets et on les stock dans la liste self.objets
        self.aiguille = random.choice(self.cases_vides)
        self.tube = random.choice(self.cases_vides)
        self.ether = random.choice(self.cases_vides)

        #tant que deux objets sont sur la meme case, on les génère de nouveau
        #TODO: regenerer uniquement l'objet qui se trouve sur un autre - utiliser del 
        while self.tube == self.aiguille or self.tube == self.ether or self.ether == self.aiguille:
            self.aiguille = random.choice(self.cases_vides)
            self.tube = random.choice(self.cases_vides)
            self.ether = random.choice(self.cases_vides)



    #On stock les cases dans la liste self.cases
    def load_map(self,filename):
        with open(filename,"r") as fichier:
            for ligne in fichier.readlines():
                liste = ligne.split()
                self.cases.append(liste)
            for ligne in self.cases:
                i = 0
                i_line = self.cases.index(ligne)
                for case in ligne:
                    if "vide" == case:
                        self.cases_vides.append([i,i_line]) 
                    if "mur" == case:
                        self.cases_mur.append([i,i_line])
                    if "depart" == case:
                        self.case_depart.append([i,i_line])
                    if "arrivee" == case:
                        self.case_arrivee.append([i,i_line])
                    i += 1
        

    ### INTERFACE GRAPHIQUE ###############################################################################################
    #TODO: faire classe IG 
    def interface_graphique(self):
    
        pygame.init()

        taille_case = 40
        fenetre = pygame.display.set_mode((15*taille_case,16*taille_case))
 
        def afficher_cases(self):

            # chargement et affichage des cases vides
            #TODO: charger les cases une seule fois dans une méthode de chargement
            self.img_case_vide = pygame.image.load("case-vide-40.png").convert()
            self.img_case_vide = pygame.transform.scale(self.img_case_vide, (taille_case, taille_case))

            # chargement et affichage des cases mur
            self.img_case_mur= pygame.image.load("case-mur-40.png").convert()
            self.img_case_mur = pygame.transform.scale(self.img_case_mur, (taille_case, taille_case))
 
            # chargement et affichage du départ
            self.img_case_depart = pygame.image.load("case-depart-40.png").convert()
            self.img_case_depart = pygame.transform.scale(self.img_case_depart, (taille_case, taille_case))
  
            # chargement et affichage de l'arrivée
            self.img_case_arrivee = pygame.image.load("case-arrivee-40.png").convert()
            self.img_case_arrivee = pygame.transform.scale(self.img_case_arrivee, (taille_case, taille_case))

            y = 0
            for ligne in self.cases:
                x = 0
                for case in ligne:
                    if case == "vide":
                        fenetre.blit(self.img_case_vide, (x*taille_case, y*taille_case))
                    if case == "mur":
                        fenetre.blit(self.img_case_mur, (x*taille_case, y*taille_case))
                    if case == "depart":
                        fenetre.blit(self.img_case_depart, (x*taille_case, y*taille_case))
                    if case == "arrivee":
                        fenetre.blit(self.img_case_arrivee, (x*taille_case, y*taille_case))
                    x += 1
                y += 1




        # chargement et affichage des objets
        self.objets_collectes = [] #liste des objets collectés
        self.img_ether = pygame.image.load("ether-40.png")
        self.img_ether = pygame.transform.scale(self.img_ether, (taille_case, taille_case))
        self.img_ether.set_colorkey((255,255,255))
        self.img_aiguille = pygame.image.load("aiguille-40.png")
        self.img_aiguille = pygame.transform.scale(self.img_aiguille, (taille_case, taille_case))
        self.img_aiguille.set_colorkey((255,255,255))
        self.img_tube = pygame.image.load("tube-40.png")
        self.img_tube = pygame.transform.scale(self.img_tube, (taille_case, taille_case))
        self.img_tube.set_colorkey((255,255,255))
        pos_img_ether_x = taille_case*(self.ether[0])
        pos_img_ether_y = taille_case*(self.ether[1])
        pos_img_aiguille_x = taille_case*(self.aiguille[0])
        pos_img_aiguille_y = taille_case*(self.aiguille[1])
        pos_img_tube_x = taille_case*(self.tube[0])
        pos_img_tube_y = taille_case*(self.tube[1])
        position_ether = self.img_ether.get_rect(topleft=(pos_img_ether_x,pos_img_ether_y))
        position_aiguille = self.img_aiguille.get_rect(topleft=(pos_img_aiguille_x,pos_img_aiguille_y))
        position_tube = self.img_tube.get_rect(topleft=(pos_img_tube_x,pos_img_tube_y))
        fenetre.blit(self.img_ether, position_ether)
        fenetre.blit(self.img_aiguille, position_aiguille)
        fenetre.blit(self.img_tube, position_tube)

        # chargement et affichage du gardien
        self.img_gardien = pygame.image.load("gardien-40.png").convert()
        self.img_gardien = pygame.transform.scale(self.img_gardien, (taille_case, taille_case))
        self.img_gardien.set_colorkey((255,255,255))
        position_gardien = self.img_gardien.get_rect(topleft=(self.case_arrivee[0][0]*taille_case,(self.case_arrivee[0][1]-1)*taille_case))
        fenetre.blit(self.img_gardien, position_gardien)
        coordonnee_gardien = [position_gardien[0]/taille_case,position_gardien[1]/taille_case]
        
        #on s'assure que l'objet n'apparait pas sur le gardien
        while self.aiguille == coordonnee_gardien or self.tube == coordonnee_gardien or self.ether == coordonnee_gardien:
            self.aiguille = random.choice(self.cases_vides)
            self.tube = random.choice(self.cases_vides)
            self.ether = random.choice(self.cases_vides)
        else:
            self.objets.extend([self.aiguille, self.tube, self.ether])
            
        # chargement et affichage du personnage
        self.img_perso = pygame.image.load("MacGyver-40.png").convert()
        self.img_perso.set_colorkey((255,255,255))
        self.img_perso = pygame.transform.scale(self.img_perso, (taille_case, taille_case))
        position_perso = self.img_perso.get_rect(topleft=(self.case_depart[0][0]*taille_case,self.case_depart[0][1]*taille_case))
        fenetre.blit(self.img_perso, position_perso)
        #rafraîchissement de l'écran
        pygame.display.flip()

        #si la touche reste enfoncée, l'action se répète.
        pygame.key.set_repeat(30,100)

        #boucle
        continuer = 1
        while continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    continuer = 0
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        if Labyrinthe.get_type(self,int(position_perso[0]/taille_case),int(position_perso[1]/taille_case)+1) == "mur":
                            print("mur , {},{}".format(int(position_perso[0]/taille_case),int(position_perso[1]/taille_case)+1))
                        else:
                            position_perso = position_perso.move(0,taille_case)
                    if event.key == K_UP:
                        if Labyrinthe.get_type(self,int(position_perso[0]/taille_case),int(position_perso[1]/taille_case)-1) == "mur":
                            print("mur , {},{}".format(int(position_perso[0]/taille_case),int(position_perso[1]/taille_case)-1))
                        else:
                            position_perso = position_perso.move(0,-taille_case)
                    if event.key == K_LEFT:
                        if Labyrinthe.get_type(self,int(position_perso[0]/taille_case)-1,int(position_perso[1]/taille_case)) == "mur":
                            print("mur , {},{}".format(int(position_perso[0]/taille_case)-1,int(position_perso[1]/taille_case)))
                        else:
                            position_perso = position_perso.move(-taille_case,0)
                    if event.key == K_RIGHT:
                        if Labyrinthe.get_type(self,int(position_perso[0]/taille_case)+1,int(position_perso[1]/taille_case)) == "mur":
                            print("mur , {},{}".format(int(position_perso[0]/taille_case)+1,int(position_perso[1]/taille_case)))
                        else:
                            position_perso = position_perso.move(taille_case,0)

                #si le joueur marche sur l'objet, il le collecte
                if position_perso == position_ether:
                    position_ether = self.img_ether.get_rect(topleft=(taille_case*14,taille_case*15))
                    self.objets_collectes.append("ether")
                    print("collecté: {}".format(self.objets_collectes))
                if position_perso == position_aiguille:
                    position_aiguille = self.img_aiguille.get_rect(topleft=(taille_case*13,taille_case*15))
                    self.objets_collectes.append("aiguille")
                    print("collecté: {}".format(self.objets_collectes))
                if position_perso == position_tube:
                    position_tube = self.img_tube.get_rect(topleft=(taille_case*12,taille_case*15))
                    self.objets_collectes.append("tube")
                    print("collecté: {}".format(self.objets_collectes))

                #si le joueur rencontre le gardien
                if (position_perso[0]/taille_case,position_perso[1]/taille_case) == (position_gardien[0]/taille_case - 1,position_gardien[1]/taille_case):
                    if "ether" in self.objets_collectes and "aiguille" in self.objets_collectes and "tube" in self.objets_collectes:
                        position_gardien = position_gardien.move(0,-taille_case)
                        print("Objets collectés: {}".format(self.objets_collectes))
                        print("vous pouvez passer")
                    else:
                        continuer = 0
                        partie_gagnee = 0

                #si le joueur arrive sur la case arrivée
                if (position_perso[0]/taille_case,position_perso[1]/taille_case) == (self.case_arrivee[0][0],self.case_arrivee[0][1]):
                    partie_gagnee = 1
                    continuer = 0
           


            #recollage
            afficher_cases(self)
            fenetre.blit(self.img_ether, position_ether)
            fenetre.blit(self.img_aiguille, position_aiguille)
            fenetre.blit(self.img_tube, position_tube)
            fenetre.blit(self.img_gardien, position_gardien)
            fenetre.blit(self.img_perso, position_perso)
            
            
            #rafraichissement
            pygame.display.flip()

        findugame = 1
        while findugame:
            for event in pygame.event.get():
                if event.type == QUIT:
                    findugame = 0
            #Si continuer = 0
            self.findugame = pygame.image.load("fin.png").convert()
            self.victoire = pygame.image.load("victoire.png").convert()
            afficher_cases(self)
            fenetre.blit(self.img_ether, position_ether)
            fenetre.blit(self.img_aiguille, position_aiguille)
            fenetre.blit(self.img_tube, position_tube)
            fenetre.blit(self.img_gardien, position_gardien)
            fenetre.blit(self.img_perso, position_perso)
            if partie_gagnee == 1:
                fenetre.blit(self.victoire, (pygame.Surface.get_width(fenetre)/2, pygame.Surface.get_width(fenetre)/2))
            else:
                fenetre.blit(self.findugame, (pygame.Surface.get_width(fenetre)/2, pygame.Surface.get_width(fenetre)/2))

            #rafraichissement
            pygame.display.flip()

    


    ### FONCTIONS ##################################################################################################

    #Renvoie le type de case dont les coordonnées sont x,y
    def get_type(self,x,y):
        try:
            self.cases[x][y]
        except IndexError:
            return("mur")
        else:
            return(self.cases[y][x])

    #Renvoie les objets stockés dans la liste self.objets sous formes de liste de coordonnées [x,y]
    def get_objets(self):
        return(self.objets)

    #Pacours les items "cases" des listes "ligne" de la liste "self.cases"
    #Si c = case, renvoie le type de c et ses coordonnées
    def get_coord_c(self,c): 
            liste_case_c = []
            for ligne in self.cases:
                i = 0
                for case in ligne:
                    if c == case:
                        # print("case *{}* à l'emplacement ({},{}) ".format(c, i, self.cases.index(ligne) )) # c = case, renvoie le type de c et ses coordonnées
                        liste_case_c.append([i,self.cases.index(ligne)])
                        i += 1
                    else:
                        i += 1
            return(liste_case_c)
            
    def get_cases_mur(self):
        return(self.cases_mur)


                    






laby = Labyrinthe()
print(laby.interface_graphique())





