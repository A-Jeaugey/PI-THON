#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import os  # Module pour interagir avec le système d'exploitation (chemins de fichier, etc.)
import pygame  # Bibliothèque Pygame pour la gestion de la fenêtre, de l'affichage et des événements

pygame.init()  # Initialise les modules internes de Pygame
pygame.display.set_caption("- THON")  # Définition du titre de la fenêtre
pygame.display.set_icon(pygame.image.load("data/logo.png"))  # Définition de l'icône, qui est juste le symbole pi, mais qui avec le titre forme le nom du projet
POLICE = os.path.join("data", "Iosevka_fixed.ttf")  # Chemin vers la police personnalisée
ecran_information = pygame.display.Info()  # Objet contenant des informations sur l'écran (résolution, etc.)
largeur_ecran, hauteur_ecran = 1000, 800  # Dimensions par défaut de la fenêtre en mode fenêtré
plein_ecran_etat = True  # Booléen indiquant si on est en mode plein écran (True) ou non (False)

BLANC = (255, 255, 255)  # Définition de la couleur blanche en RGB
NOIR = (0, 0, 0)  # Couleur noire
ROUGE = (255, 0, 0)  # Couleur rouge
VERT = (0, 255, 0)  # Couleur verte
BLEU = (119, 181, 254)  # Couleur bleue clair
GRIS = (100, 100, 100)  # Couleur gris moyen
GRIS_CLAIR = (150, 150, 150)  # Couleur gris clair
GRIS_FONCE = (56, 56, 56)  # Couleur gris foncé
NOIR_MENU = (50, 48, 48)

ecran = pygame.display.set_mode((ecran_information.current_w, ecran_information.current_h), pygame.FULLSCREEN)  # Création de la fenêtre Pygame avec les dimensions spécifiées
police = pygame.font.Font(POLICE, 45)  # Chargement de la police taille 45

placement_croix_fermer = pygame.Rect(ecran.get_width() - 50, 0, 50, 50)  # Rectangle pour placer la croix de fermeture en haut à droite
placement_bouton_menu = pygame.Rect(ecran.get_width() - 132, 8, 50, 50)  # Rectangle pour le bouton de retour au menu
placement_plein_ecran = pygame.Rect(ecran.get_width() - 100, 10, 35, 35)  # Rectangle pour le bouton "F" (plein écran)

rectangles_barre_laterale = []  # Liste des rectangles cliquables dans la barre latérale
groupe_selectionne = None  # Retient le groupe sélectionné (ou None si aucun)

def menu_principal():
    """
    Gère l'affichage et la logique du menu principal (écran d'accueil).
    Paramètres: Aucun
    Retourne: Le nom d'une méthode (str) si l'utilisateur en choisit une, sinon None si la fenêtre se ferme.
    """
    from utils import afficher_texte_dynamique  # Import local d'une fonction qui gère l'affichage dynamique de textes. L'import local évite un import circulaire
    global groupe_selectionne  # Indique qu'on modifie ces variables globales dans la fonction
    police_titre = pygame.font.SysFont(POLICE, largeur_ecran // 5, italic=True)  # Police pour le titre, taille dépendant de la largeur de l'écran
    police_texte = pygame.font.Font(POLICE, largeur_ecran // 38)  # Police pour le texte courant, taille dépendant de la largeur de l'écran

    rectangles_scrollables = {
        "intro": pygame.Rect(largeur_ecran * 0.04, ecran.get_height() // 4 if plein_ecran_etat else ecran.get_height() // 3.5,  ecran.get_width() // 1.42 if plein_ecran_etat else ecran.get_width() // 1.55, ecran.get_width() // 6 if plein_ecran_etat else ecran.get_width() // 4),
        "groupes": pygame.Rect(largeur_ecran * 0.04, ecran.get_height() // 1.6,  ecran.get_width() // 1.42 if plein_ecran_etat else ecran.get_width() // 1.55, ecran.get_width() // 6 if plein_ecran_etat else ecran.get_width() // 4),
    }

    texte_intro = (
            "π est une constante mathématique représentant le rapport entre la circonférence "
            "d'un cercle et son diamètre. Il est irrationnel et apparaît dans de nombreuses "
            "branches des mathématiques et des sciences. Les premières approximations de π "
            "remontent à l'Antiquité avec Archimède, mais aujourd'hui, nous disposons de nombreuses "
            "méthodes pour le calculer avec une précision extrême."
        )
    
    textes_groupes = (
        "Nous avons classés les méthodes d'estimations de pi selon différents groupes : ",
        "- Méthodes géométriques : ", 
        "Approches basées sur des polygones et l'intégration.",
        "- Séries et suites mathématiques : ", 
        "Utilisation de séries infinies pour approcher π.",
        "- Algorithmes et haute précision : ", 
        "Algorithmes optimisés pour un grand nombre de décimales.",
        "- Méthodes stochastiques : ", 
        "Simulations probabilistes pour estimer π.",
        "- Physiques et dynamiques : ", 
        "Approches basées sur des phénomènes physiques réels.",
        " "
    )

    scroll_positions = {"intro": 0, "groupes": 0}

    while True:  # Boucle principale d'exécution du menu
        ecran.fill(GRIS_FONCE)  # Efface l'écran en le remplissant de blanc

        rectangles_scrollables = {
        "intro": pygame.Rect(largeur_ecran * 0.04, ecran.get_height() // 4 if plein_ecran_etat else ecran.get_height() // 3.5,  ecran.get_width() // 1.42 if plein_ecran_etat else ecran.get_width() // 1.55, ecran.get_width() // 6 if plein_ecran_etat else ecran.get_width() // 4),
        "groupes": pygame.Rect(largeur_ecran * 0.04, ecran.get_height() // 1.6,  ecran.get_width() // 1.42 if plein_ecran_etat else ecran.get_width() // 1.55, ecran.get_width() // 6 if plein_ecran_etat else ecran.get_width() // 4),
        }

        titre = police_titre.render("π - thon", True, BLANC)  # Crée une surface de texte (titre) "PI-THON" en rouge
        rectangle_titre = pygame.Rect(ecran.get_width() // 4 - 20 if plein_ecran_etat else ecran.get_width() // 10 - 20, 40, titre.get_width() + 30, titre.get_height() + 15) # Crée un rectangle sur laquel sera placé le titre
        pygame.draw.rect(ecran, GRIS, rectangle_titre, border_radius=40) # Affiche ce rectangle
        ecran.blit(titre, (ecran.get_width() // 4 if plein_ecran_etat else ecran.get_width() // 10, 50))  # Affiche le titre centré horizontalement, décalé verticalement selon molette_position

        rectangles = barre_laterale(groupe_selectionne)  # Dessine la barre latérale et récupère ses zones cliquables

        pygame.draw.rect(ecran, ROUGE, placement_plein_ecran, 7)  # Trace un rectangle rouge autour du bouton plein écran
        police_lettre_f = pygame.font.Font(POLICE, 25)  # Police pour la lettre "F"
        lettre_f_plein_ecran = police_lettre_f.render("F", True, ROUGE)  # Surface texte "F" en rouge
        ecran.blit(lettre_f_plein_ecran, (placement_plein_ecran[0] + 11, placement_plein_ecran[1] + 2))  # Positionne la lettre "F" dans le rectangle du bouton plein écran
        
        souris_x, souris_y = pygame.mouse.get_pos() # Récupère les coordonnées de la souris
        rectangle_actif = None # Variable indiquant le rectangle actif

        for key, rectangle in rectangles_scrollables.items():
            if rectangle.collidepoint(souris_x, souris_y):
                rectangle_actif = key # Si la souris survole un rectangle, il devient le rectangle actif

        for key, rectangle in rectangles_scrollables.items():
            pygame.draw.rect(ecran, GRIS_CLAIR, rectangle, border_radius=20)  # Dessine les rectangles

            # Appliquer le clipping pour empêcher le texte de dépasser le rectangle
            ecran.set_clip(rectangle)

            # Affichage du texte
            if key == "groupes":  # Affichage avec scroll pour les groupes
                y_position = rectangle.y + 10 - scroll_positions[key] # Position verticale
                hauteur_total_groupes = 0  # Pour calculer la hauteur totale du texte

                for i in range(0, len(textes_groupes), 2): # Affiche le texte ligne par ligne, une ligne sur deux en rouge
                    hauteur_titre = afficher_texte_dynamique(ecran, textes_groupes[i], rectangle.x + 10, y_position, 15, rectangle.width - 40, police_texte, BLANC, False)
                    y_position += hauteur_titre + 20 # Rajoute un espace
                    hauteur_description = afficher_texte_dynamique(ecran, textes_groupes[i+1], rectangle.x + 10, y_position, 15, rectangle.width - 40, police_texte, ROUGE, False)
                    y_position += hauteur_description + 5  # Ajoute l'espacement entre groupes
                    hauteur_total_groupes += hauteur_titre + hauteur_description + 25

                hauteur_texte = hauteur_total_groupes  # On utilise cette hauteur pour le scroll

            elif key == "intro":  # Affichage de l'intro avec scroll
                hauteur_texte = afficher_texte_dynamique(ecran, texte_intro, rectangle.x + 10, rectangle.y + 10 - scroll_positions[key], 15, rectangle.width - 40, police_texte, BLANC, False)

            # Ajout de la barre de défilement
            hauteur_max_scroll = max(0, hauteur_texte + 50 - rectangle.height)

            if hauteur_max_scroll > 0:  # Afficher la barre seulement si le texte dépasse
                hauteur_barre = max(20, (rectangle.height - 40) * rectangle.height // hauteur_texte)  # Facteur de réduction (-40 pour éviter les coins arrondis)
                position_barre = rectangle.y + 20 + (rectangle.height - 40 - hauteur_barre) * (scroll_positions[key] / hauteur_max_scroll)  # Décalage pour éviter les coins
                
                # Dessiner la barre directement sur l'écran avec un léger décalage vers l'intérieur
                pygame.draw.rect(ecran, GRIS, (rectangle.right - 15, position_barre, 5, hauteur_barre), border_radius=2)
            
            ecran.set_clip(None) # Supprime le clipping après affichage

        croix_fermer()  # Dessine la croix de fermeture en haut à droite
        pygame.display.update()  # Met à jour l'affichage

        for evenement in pygame.event.get():  # Parcourt la liste des événements Pygame
            if evenement.type == pygame.QUIT:  # Vérifie si l'utilisateur ferme la fenêtre
                pygame.quit()  # Ferme les modules Pygame
                exit()  # Quitte complètement le programme Python
            if evenement.type == pygame.MOUSEBUTTONDOWN and placement_plein_ecran.collidepoint(evenement.pos) and evenement.button == 1 or evenement.type == pygame.KEYDOWN and evenement.key in (pygame.K_f, pygame.K_F11):  # Vérifie clic sur le bouton plein écran OU touche F/F11
                plein_ecran()  # Bascule l'affichage en plein écran ou mode fenêtré
            
            if evenement.type == pygame.MOUSEBUTTONDOWN:  # Gestion des événements de la souris (molette et clics)
                if rectangle_actif:
                    # Recalculer la hauteur à chaque scroll
                    if rectangle_actif == "groupes":
                        hauteur_texte = hauteur_total_groupes
                    else:
                        hauteur_texte = afficher_texte_dynamique(ecran, texte_intro, 0, 0, 15, rectangles_scrollables[rectangle_actif].width - 20, police_texte, BLANC, False)
                    
                    # Recalcule la hauteur max
                    hauteur_max_scroll = max(0, (hauteur_texte + police_texte.get_height() + 25) - rectangles_scrollables[rectangle_actif].height)

                    # Désactiver le scroll si tout le texte est visible
                    if hauteur_texte + police_texte.get_height() + 5 <= rectangles_scrollables[rectangle_actif].height:
                        hauteur_max_scroll = 0
                        scroll_positions[rectangle_actif] = 0

                    if evenement.button == 4:  # Molette haut
                        scroll_positions[rectangle_actif] = max(0, scroll_positions[rectangle_actif] - 20)
                    elif evenement.button == 5:  # Molette bas
                        scroll_positions[rectangle_actif] = min(hauteur_max_scroll, scroll_positions[rectangle_actif] + 20)

                if evenement.button == 1:  # Clic gauche de la souris
                    if placement_croix_fermer.collidepoint(evenement.pos):  # Vérifie si on a cliqué sur la croix de fermeture
                        pygame.quit()  # Ferme Pygame
                        exit()  # Quitte Python
                    for rectangle, action in rectangles:  # Parcourt la liste des boutons/rectangles de la barre latérale
                        if rectangle.collidepoint(evenement.pos):  # Vérifie si un rectangle est cliqué
                            if action == "menu":  # Bouton "menu"
                                groupe_selectionne = None  # On repasse à la liste générale des groupes
                            elif action in [1, 2, 3, 4, 5, 6]:  # Sélection d'un groupe par numéro
                                groupe_selectionne = action
                            else:  # Dans le cas où action est une chaîne correspondant à une méthode
                                groupe_selectionne = None
                                return action  # On retourne le nom de la méthode choisie et on quitte la fonction menu_principal


def barre_laterale(groupe_selectionne=None):
    """
    Affiche la barre latérale (liste de groupes ou de méthodes) et renvoie les zones cliquables.
    Paramètres: groupe_selectionne (int ou None)
    Retourne: Une liste de tuples (rectangle, action) représentant chaque bouton.
    """
    from utils import afficher_texte_dynamique  # Fonction d'affichage de texte dynamique. import local évitant un import circulaire
    largeur_barre = ecran.get_width() // 4  # Calcule la largeur de la barre en fonction de la taille actuelle de la fenêtre
    hauteur_ecran = ecran.get_height()  # Hauteur de la fenêtre
    position_x_gauche = ecran.get_width() - largeur_barre - 20  # Point de départ horizontal de la barre (côté droit)

    espace_haut_bas = hauteur_ecran // 15  # Marge en haut et en bas de la barre
    hauteur_barre_laterale = hauteur_ecran - 2 * espace_haut_bas  # Espace vertical total disponible pour la barre latérale
    espace_premier_dernier_rectangle = hauteur_barre_laterale // 20  # Espace réservé au-dessus du premier rectangle et en-dessous du dernier

    facteur_espacement = 1.1  # Facteur pour espacer verticalement les rectangles dans la barre

    pygame.draw.rect(ecran, NOIR_MENU, (position_x_gauche, espace_haut_bas, largeur_barre + 20, hauteur_barre_laterale), border_top_left_radius=30, border_bottom_left_radius=30)  # Dessine un grand rectangle gris arrondi représentant la barre

    groupes = {  # Dictionnaire associant un numéro de groupe à un tuple (nom, [liste de méthodes])
        1: ("Méthodes géométriques", ["Archimède", "Approximation par intégration"]),
        2: ("Séries et suites mathématiques", ["Leibniz", "Nilakantha", "Machin", "Ramanujan"]),
        3: ("Algorithmes et haute précision", ["Gauss-Legendre", "Borwein", "Chudnovsky"]),
        4: ("Méthodes stochastiques", ["Monte Carlo", "Buffon"]),
        5: ("Physiques et dynamiques", ["Collisions", "Pendule"]),
    }

    rectangles_barre_laterale = []  # Liste pour stocker chaque (rectangle, action)

    if groupe_selectionne is None:  # Si aucun groupe n'est sélectionné, on affiche la liste de tous les groupes
        compteur = 0  # Sert à calculer l'offset vertical
        for numero_groupe in groupes:  # Parcourt chaque groupe
            nombre_sections = len(groupes)  # Nombre total de groupes
            hauteur_rectangle = (hauteur_barre_laterale - 2 * espace_premier_dernier_rectangle) / (facteur_espacement * nombre_sections)  # Calcule la hauteur de chaque rectangle
            taille_police = max(20, int(hauteur_rectangle // 4))  # Taille de la police, on pose un minimum de 20
            police_rectangle = pygame.font.Font(POLICE, int(taille_police))  # Police pour afficher le nom du groupe

            nom_groupe = groupes[numero_groupe][0]  # Récupère le nom du groupe
            position_y = espace_haut_bas + espace_premier_dernier_rectangle + compteur * facteur_espacement * hauteur_rectangle  # Calcule la position verticale
            rectangle = pygame.Rect(position_x_gauche + 11, position_y, largeur_barre, hauteur_rectangle)  # Crée le rectangle associé à ce groupe

            pygame.draw.rect(ecran, GRIS_CLAIR if compteur % 2 == 0 else GRIS_FONCE, rectangle, border_radius=20)  # Dessine le rectangle avec une couleur alternée
            afficher_texte_dynamique(ecran, nom_groupe, position_x_gauche + 20, position_y + 10, 5, largeur_barre - 20, police_rectangle, BLANC, True, hauteur_rectangle)  # Affiche le nom du groupe

            rectangles_barre_laterale.append((rectangle, numero_groupe))  # Stocke le couple (rectangle, action) = numéro de groupe
            compteur += 1  # Incrémente pour passer au groupe suivant
    else:  # Si un groupe est sélectionné, on affiche les méthodes liées à ce groupe
        compteur = 0
        for methode in groupes[groupe_selectionne][1]:  # Parcourt la liste de méthodes du groupe sélectionné
            nombre_sections = len(groupes[groupe_selectionne][1])  # Nombre de méthodes dans ce groupe
            hauteur_rectangle = min((2.8 * espace_premier_dernier_rectangle), (hauteur_barre_laterale - 2 * espace_premier_dernier_rectangle) / (facteur_espacement * nombre_sections))  # Hauteur contraintée pour ne pas dépasser
            taille_police = max(20, int(hauteur_rectangle // 4))  # Taille de la police pour afficher la méthode
            police_rectangle = pygame.font.Font(POLICE, int(taille_police)) # Police spécifique à l'affichage de la méthode

            position_y = espace_haut_bas + espace_premier_dernier_rectangle + compteur * facteur_espacement * hauteur_rectangle  # Calcule la position verticale du rectangle
            rectangle = pygame.Rect(position_x_gauche + 11, position_y, largeur_barre, hauteur_rectangle)  # Crée le rectangle pour cette méthode

            pygame.draw.rect(ecran, GRIS_CLAIR if compteur % 2 == 0 else GRIS_FONCE, rectangle, border_radius=20)  # Dessine le rectangle avec une couleur alternée
            afficher_texte_dynamique(ecran, methode, position_x_gauche + 20, position_y + 10, 5, largeur_barre - 20, police_rectangle, BLANC, True, hauteur_rectangle)  # Affiche le nom de la méthode

            rectangles_barre_laterale.append((rectangle, methode))  # Stocke le tuple (rectangle, nom de la méthode)
            compteur += 1 # Incrémente pour passer à la méthode suivante

        position_bas_dernier_rectangle = position_y + hauteur_rectangle  # Calcule la position de la base du dernier rectangle dessiné
        espace_restante = (espace_haut_bas + hauteur_barre_laterale) - position_bas_dernier_rectangle  # Espace vide restant dans la barre
        position_y_retour = position_bas_dernier_rectangle + espace_restante // 2 - 17  # Position verticale du bouton "Retour"
        rectangle_retour = pygame.Rect(position_x_gauche - 50 + largeur_barre // 2, position_y_retour, 100, 35)  # Rectangle pour le bouton "Retour"

        pygame.draw.rect(ecran, ROUGE, rectangle_retour, border_radius=50)  # Dessine un rectangle rouge pour le bouton "Retour"
        police_retour = pygame.font.Font(POLICE, 28)  # Police pour le texte du bouton "Retour"
        texte_retour = police_retour.render("Retour", True, BLANC)  # Surface texte "Retour" en blanc
        texte_rect_retour = texte_retour.get_rect(center=(position_x_gauche + largeur_barre // 2, position_y_retour + 17))  # Centre le texte "Retour"
        ecran.blit(texte_retour, texte_rect_retour)  # Dessine le texte sur l'écran
        rectangles_barre_laterale.append((rectangle_retour, "retour"))  # Stocke (rectangle_retour, "retour") pour le gestionnaire d'événements

    return rectangles_barre_laterale  # Renvoie la liste finale des rectangles cliquables et leur action associée


def croix_fermer():
    """
    Affiche un "X" à l'emplacement prévu pour fermer la fenêtre.
    Paramètres: Aucun
    Retourne: Rien
    """
    croix = police.render("X", True, ROUGE)  # Crée la surface texte "X" en rouge
    ecran.blit(croix, placement_croix_fermer)  # Positionne ("blit") le "X" dans le rectangle placement_croix_fermer


def bouton_menu():
    """
    Affiche "menu" en rouge
    Paramètres: Aucun
    Retourne: Rien
    """
    texte_menu =  pygame.font.Font(POLICE, 30).render("menu", True, ROUGE)  # Surface texte "<" en rouge
    ecran.blit(texte_menu, placement_bouton_menu)  # Positionne le texte


def plein_ecran():
    """
    Bascule entre mode plein écran et mode fenêtré, et met à jour les positions des boutons.
    Paramètres: Aucun
    Retourne: Rien
    """
    global placement_croix_fermer, placement_bouton_menu, placement_plein_ecran
    global ecran, plein_ecran_etat, largeur_ecran, hauteur_ecran
    if plein_ecran_etat:  # Si l'application est déjà en plein écran
        ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))  # On repasse en mode fenêtré aux dimensions initiales
        plein_ecran_etat = False  # Met le booléen correspondant au plein écran à False
    else:  # Si on n'est pas en plein écran, on y passe
        ecran = pygame.display.set_mode((ecran_information.current_w, ecran_information.current_h), pygame.FULLSCREEN)  # Adapte la fenêtre à la résolution courante
        plein_ecran_etat = True  # Met le booléen à True
    placement_croix_fermer = pygame.Rect(ecran.get_width() - 50, 0, 50, 50)  # Met à jour la zone de la croix de fermeture en fonction de la nouvelle taille
    placement_bouton_menu = pygame.Rect(ecran.get_width() - 132, 8, 50, 50)  # Met à jour la zone du bouton de retour au menu
    placement_plein_ecran = pygame.Rect(ecran.get_width() - 100, 10, 35, 35)  # Met à jour la zone du bouton plein écran "F"


def bouton_informations():
    """
    Affiche un carré rouge avec un "?" blanc dans le coin inférieur droit.
    Paramètres: Aucun
    Retourne: Rien
    """
    pygame.draw.circle(ecran, ROUGE, (ecran.get_width() - 180, 28), 20)  # Dessine un rond rouge
    informations = pygame.font.Font(POLICE, 30).render("?", True, BLANC)  # Surface texte "?" en blanc
    # Calcule la position pour centrer le "?" dans le carré et l'afficher
    ecran.blit(informations, (ecran.get_width() - 180 - informations.get_width() // 2, 28 - informations.get_height() // 2))
