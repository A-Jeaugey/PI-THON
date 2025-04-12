#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import random  # Permet de générer des nombres aléatoires
import pygame  # Bibliothèque pour la gestion de la fenêtre graphique et des événements
import pygame_textinput  # Permet la saisie de texte dans pygame
from affichage import ecran, POLICE, BLANC, NOIR, BLEU, ROUGE, VERT, croix_fermer, bouton_menu, bouton_informations, ecran_information  # Objets/constantes d'affichage
from utils import temps_ecoule, gestionnaire_evenements, afficher_texte_dynamique, souligner_texte # Fonctions utilitaires (gestion d'événements, temps, etc.)

def information_monte_carlo():
    """
    Fonction qui gère l'affichage d'informations sur Monte-Carlo
    parametres:
        Aucun
    retourne:
        True si l'utilisateur clique dans la fenêtre pour continuer, False s'il clique sur le bouton menu.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Obtient la taille de la fenêtre
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police adaptée au titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 39)  # Police adaptée au texte courant

    # Titres et textes explicatifs
    texte_titre = "Méthode de Monte-Carlo"
    texte_description = (
        "La méthode de Monte-Carlo permet d'estimer π en générant aléatoirement des points dans un carré "
        "contenant un cercle inscrit. Le rapport entre les points à l'intérieur du cercle et le nombre total "
        "de points donne une approximation de π."
    )
    texte_formule = (
        "La formule utilisée est :",
        "π ≈ 4 × (nombre de points dans le cercle) / (nombre total de points)."
    )
    texte_visualisation = (
        "Visualisation :",
        "• Dans cette implémentation, les points sont colorés en verts s'ils sont dans le cercle, et en rouge sinon.",
        "• l'entrée de points par seconde permet de contrôler la vitesse de génération des points.",
        "• le bouton 'Activer le mode rapide' permet de passer à une version plus performante de la méthode sans affichage. ",
        "• La version rapide permet de générer une grande quantitée de points d'un coup, mais cela montre aussi que cette méthode n'est "
        "pas vraiment efficace même avec un grand nombre d'itérations dans l'expérience"
    )

    while True:  # Boucle d'affichage
        ecran.fill(NOIR)  # Remplit l'écran de noir
        # Préparation du titre
        titre_rendu = police_titre.render(texte_titre, True, BLANC)
        # Placement du titre au centre horizontal
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre

        # Position verticale de base
        y_position = hauteur_ecran // 7 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 5
        # Affichage du premier texte explicatif (description)
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 10, y_position, 15, largeur_ecran * 0.8, police_texte) + hauteur_ecran // 50
        y_position += 0 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 18 # Ajoute un espace en fonction de si on est en plein écran ou non
        # Affichage de la formule (en bleu pour la mettre en évidence)
        for ligne in texte_formule :
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position + 15, 15, largeur_ecran * 0.8, police_texte, BLEU, souligner=True if ligne == "La formule utilisée est :" else False) + hauteur_ecran // 50
        y_position += 0 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 18 # Ajoute un espace en fonction de si on est en plein écran ou non
        # Affichage d'un second bloc d'explications (utilisation, visualisation, etc.)
        for ligne in texte_visualisation:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position + 15, 15, largeur_ecran * 0.8, police_texte, souligner=True if ligne == "Visualisation :" else False) + hauteur_ecran // 50

        # Texte d'instruction invitant l'utilisateur à cliquer pour continuer
        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer.", True, ROUGE)
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))

        bouton_menu()  # Bouton de menu
        croix_fermer()  # Bouton de fermeture
        pygame.display.update()  # Mise à jour de l'affichage

        # Récupère l'action effectuée par l'utilisateur
        evenement_boutons, _ = gestionnaire_evenements()
        if evenement_boutons == "menu":  # S'il clique sur le bouton menu, on arrête
            return False
        if evenement_boutons == "clic":  # S'il clique n'importe où, on valide la poursuite
            ecran.fill(NOIR)
            return True

def monte_carlo_detaille(informations_affichees=True):
    """
    Version détaillée et interactive de la méthode de Monte-Carlo
    parametres:
        informations_affichees: Booléen qui permet de ne pas réafficher les infos si on retourne sur cette fonction ap^rès avoir été dans la version performante.
    retourne:
        Rien. Gère le calcul et l'affichage de la méthode Monte-Carlo (point par point).
    """
    if informations_affichees:  # Affiche l'information si on arrive pas de monte_carlo_performant
        if not information_monte_carlo(): # Affiche l'écran d'informations
            return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu

    ecran.fill(NOIR)  # Nettoie l'écran en noir
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Taille de l'écran

    nombre_tentatives = 0  # Compteur du nombre total de points générés
    nombre_points_dans_cercle = 0  # Compteur de points situés dans le cercle
    pi = 0  # initialisation de la variable qui contiendra la valeur de pi

    textinput = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)  # Zone de saisie pour "points par seconde"
    points_par_seconde = 20  # Valeur par défaut

    debut_ticks = pygame.time.get_ticks()  # Enregistre l'heure de départ
    dernier_temps = pygame.time.get_ticks()  # Temps de la dernière génération de point

    rayon = min(largeur_ecran, hauteur_ecran) // 3.8  # Détermine le rayon du cercle (inscrit dans l'écran)
    centre_x = largeur_ecran // 2  # Centre horizontal
    centre_y = hauteur_ecran - 50 - rayon  # Centre vertical, on laisse un espace en bas

    while True:  # Boucle principale
        rectangle_bouton = pygame.Rect(largeur_ecran // 2 - 175, hauteur_ecran // 4, 350, 50)  # Bouton pour passer au mode rapide

        # Récupère les interactions (boutons de l'interface, événements pygame)
        evenement_boutons, evenements = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Bouton menu => on retourne au menu
            return
        if evenement_boutons == 'info':  # Bouton informations => réaffiche la description
            if not information_monte_carlo():
                return # On retourne au menu si on clique sur le bouton menu dans la fonction d'informations

        for evenement in evenements:  # Parcourt chaque événement
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                # Vérifie si on a cliqué sur le bouton pour activer le mode rapide
                if rectangle_bouton.collidepoint(evenement.pos):
                    ecran.fill(NOIR) # Nettoie l'écran pour afficher monte_carlo_performant
                    monte_carlo_performant()  # Lance la version performante
                    return # Quitte la fonction actuelle pour ne pas qu'elle reste active
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN: # Si on presse Entrée
                if textinput.value.isdigit(): # si la valeur saisie est un nombre
                    points_par_seconde = min(500, int(textinput.value))  # on l'assigne; et limite à 500
                textinput.value = ""  # Réinitialise la zone de texte

        textinput.update(evenements)  # Met à jour la saisie
        if len(textinput.value) > 3:  # On limite la saisie à 3 caractères
            textinput.value = textinput.value[:3]

        temps_actuel = pygame.time.get_ticks()  # Récupère le temps actuel
        delta_temps = temps_actuel - dernier_temps  # Durée écoulée depuis la dernière tentative
        intervalle = 1000 / points_par_seconde  # Intervalle (en ms) entre deux points successifs

        if delta_temps >= intervalle:  # Si on est au-delà de l'intervalle, on génère un point
            x = random.uniform(-1, 1)  # Coordonnée aléatoire (axe x) dans [-1, 1]
            y = random.uniform(-1, 1)  # Coordonnée aléatoire (axe y) dans [-1, 1]

            x_affiche = int(centre_x + x * rayon)  # Convertit en coordonnées sur l'écran
            y_affiche = int(centre_y - y * rayon)  # idem (inversion pour l'axe vertical)

            if x**2 + y**2 <= 1:  # Vérifie si le point est dans le cercle
                couleur = VERT  # VERT si c'est dans le cercle
                nombre_points_dans_cercle += 1  # Incrémente le compteur de points dans le cercle
            else:
                couleur = ROUGE  # ROUGE si c'est en dehors

            pygame.draw.circle(ecran, couleur, (x_affiche, y_affiche), 1)  # Dessine les points
            nombre_tentatives += 1  # Incrémente le nombre total de lancés
            dernier_temps = temps_actuel  # Met à jour le dernier temps de génération

        if nombre_tentatives > 0:  # Calcule l'estimation de π
            pi = 4 * nombre_points_dans_cercle / nombre_tentatives

        # Dessine un rectangle noir pour effacer la zone d'information
        pygame.draw.rect(ecran, NOIR, (0, 0, largeur_ecran, hauteur_ecran // 4 + 50))
        pygame.draw.rect(ecran, BLANC, rectangle_bouton)  # Dessine le bouton 'mode rapide' en blanc

        police = pygame.font.Font(POLICE, hauteur_ecran // 25)  # Police pour l'affichage
        police_fixe = pygame.font.Font(POLICE, 30)  # Police un peu plus grande mais fixe pour le texte du bouton
        affichage_animation = police_fixe.render("Activer le mode rapide", True, NOIR)  # Texte du bouton

        affichage_pi = police.render(f"Estimation de Pi: {pi:.6f}", True, BLANC)  # on affiche 6 décimales
        affichage_tentatives = police.render(f"Tentatives: {nombre_tentatives}", True, BLANC)
        affichage_temps = police.render(f"Temps écoulé: {temps_ecoule(debut_ticks)}", True, BLANC)
        affichage_points_par_seconde = police.render(f"Points/s : {points_par_seconde}", True, BLANC)
        affichage_texte_entree = police.render("Entrer points par seconde :", True, BLANC)

        # Place les différents textes sur l'écran
        ecran.blit(affichage_pi, (20, hauteur_ecran // 50))
        ecran.blit(affichage_tentatives, (20, hauteur_ecran // 15))
        ecran.blit(affichage_temps, (20, hauteur_ecran // 9))
        ecran.blit(affichage_points_par_seconde, (20, hauteur_ecran // 6.5))
        ecran.blit(affichage_texte_entree, (20, hauteur_ecran // 5))
        ecran.blit(affichage_animation, (rectangle_bouton.x + rectangle_bouton.width // 2 - affichage_animation.get_width() // 2, rectangle_bouton.y + rectangle_bouton.height // 2 - affichage_animation.get_height() // 2))
        ecran.blit(textinput.surface, (20, hauteur_ecran // 4))

        # Dessine le contour du cercle (en blanc)
        pygame.draw.circle(ecran, BLANC, (centre_x, centre_y), rayon, 1)
        # Dessine le carré (en blanc) entourant le cercle
        carre_rect = (centre_x - rayon, centre_y - rayon, rayon * 2, rayon * 2)
        pygame.draw.rect(ecran, BLANC, carre_rect, 2)

        bouton_informations()  # Bouton d'information
        bouton_menu()  # Bouton de menu
        croix_fermer()  # Bouton de fermeture
        pygame.display.update()  # Rafraîchit l'affichage

def monte_carlo_performant():
    """
    Version optimisée de la méthode Monte-Carlo (Calcul de plusieurs points à la fois, et sans affichage graphique)
    parametres:
        Aucun
    retourne:
        Rien. Lance une version plus rapide du Monte-Carlo, sans affichage point par point.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Dimensions de la fenêtre
    police = pygame.font.Font(POLICE, hauteur_ecran // 25)  # Police d'écriture

    nombre_points = 100000  # Valeur par défaut
    dernier_nombre_points = nombre_points  # Variable pour savoir si le nombre de points a changé

    textinput = pygame_textinput.TextInputVisualizer(font_color=NOIR, cursor_color=NOIR)  # Saisie du nombre de points
    debut_ticks = pygame.time.get_ticks()  # Heure de départ

    nombre_tentatives = 0  # Total de points tirés
    nombre_points_dans_cercle = 0  # Nombre de points dans le cercle
    pi = 0  # Estimation de Pi

    while True:  # Boucle principale
        rectangle_bouton = pygame.Rect(largeur_ecran // 2 - 175, hauteur_ecran // 4, 350, 50)  # Bouton pour revenir à l'affichage

        affichage_texte_entree = police.render("Entrer nombre de points :", True, NOIR)  # Texte d'invite

        # Récupération des événements
        evenement_boutons, evenements = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Si clic menu
            return # Retour au menu
        if evenement_boutons == 'info':  # Si clic info, on réaffiche la description
            if not information_monte_carlo(): # Si on clique sur le bouton menu depuis l'écran d'informations
                return # Retour au menu

        for evenement in evenements:  # Parcours de tous les événements
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                # Vérifie si on a cliqué sur le bouton "Revenir à l'affichage"
                if rectangle_bouton.collidepoint(evenement.pos):
                    ecran.fill(NOIR) # Nettoie l'écran pour afficher la fonction monte_carlo_detaille
                    monte_carlo_detaille(False)  # Lance la version animée, mais sans remettre l'ecran d'informations
                    return # Quitte la fonction actuelle afin qu'elle ne reste pas active
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN: # Si on clique sur le bouton entrée
                if textinput.value.isdigit(): # Si c'est des nombres
                    nombre_points = min(5000000, int(textinput.value))  # Limite à 5 millions à la fois
                textinput.value = "" # Réinitialise la zone de saisie

        textinput.update(evenements)  # Met à jour la saisie
        if len(textinput.value) > 7:  # On limite la saisie à 7 caractères
            textinput.value = textinput.value[:7]

        # Si l'utilisateur a changé le nombre de points, on réinitialise
        if dernier_nombre_points != nombre_points:
            dernier_nombre_points = nombre_points
            nombre_tentatives = 0
            nombre_points_dans_cercle = 0
            pi = 0

        # Lance la génération de 'nombre_points' d'un coup
        for _ in range(nombre_points):
            x = random.uniform(-1, 1)  # Coordonnée aléatoire (axe x) dans [-1, 1]
            y = random.uniform(-1, 1)  # Coordonnée aléatoire (axe y) dans [-1, 1]

            if x**2 + y**2 <= 1:  # Vérifie si le point est dans le cercle
                nombre_points_dans_cercle += 1 # accrémente le nombre de points dans le cercle

        # Met à jour le compteur total et calcule la nouvelle approximation de π
        nombre_tentatives += nombre_points
        pi = 4 * (nombre_points_dans_cercle / nombre_tentatives)

        ecran.fill(BLANC)  # Fond blanc
        pygame.draw.rect(ecran, NOIR, rectangle_bouton)  # Dessine le bouton en noir
        police_fixe = pygame.font.Font(POLICE, 30)  # Police fixe pour le bouton
        # Prépare les textes à afficher
        affichage_pi = police.render(f"Estimation de Pi: {pi:.10f}", True, NOIR)
        affichage_tentatives = police.render(f"Tentatives: {nombre_tentatives}", True, NOIR)
        affichage_temps = police.render(f"Temps écoulé: {temps_ecoule(debut_ticks)}", True, NOIR)
        affichage_n_point = police.render(f"Points générés: {nombre_points}", True, NOIR)
        affichage_animation = police_fixe.render("Revenir à l'affichage", True, BLANC)

        # Placement des textes
        ecran.blit(affichage_pi, (20, hauteur_ecran // 50))
        ecran.blit(affichage_tentatives, (20, hauteur_ecran // 15))
        ecran.blit(affichage_temps, (20, hauteur_ecran // 9))
        ecran.blit(affichage_n_point, (20, hauteur_ecran // 6.5))
        ecran.blit(affichage_texte_entree, (20, hauteur_ecran // 5))
        # Place le texte sur le bouton
        ecran.blit(affichage_animation, (rectangle_bouton.x + rectangle_bouton.width // 2 - affichage_animation.get_width() // 2, rectangle_bouton.y + rectangle_bouton.height // 2 - affichage_animation.get_height() // 2))
        ecran.blit(textinput.surface, (20, hauteur_ecran // 4))

        bouton_informations()  # Bouton informations
        bouton_menu()  # Bouton menu
        croix_fermer()  # Bouton fermer
        pygame.display.update()  # Rafraîchit l'écran
