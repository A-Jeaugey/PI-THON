#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Importation de pygame pour la gestion de l'affichage et des événements
import random  # Importation de random pour générer des nombres aléatoires
import math  # Importation de math pour les fonctions mathématiques (cosinus, sinus, etc.)
import time  # Importation de time pour mesurer le temps
import pygame_textinput  # Importation de pygame_textinput pour gérer la saisie de texte dans pygame
from affichage import ecran, POLICE, BLANC, NOIR, ROUGE, GRIS, BLEU, bouton_menu, croix_fermer, bouton_informations, ecran_information  # Importation d'objets et constantes d'affichage
from utils import gestionnaire_evenements, afficher_texte_dynamique, souligner_texte  # Importation des fonctions utilitaires pour gérer les événements et afficher du texte

def information_buffon():
    """
    Affiche les informations concernant l'expérience de Buffon.

    Paramètres :
        Aucun

    Retourne :
        True si l'utilisateur clique n'importe où pour commencer,
        False si l'utilisateur clique sur le bouton menu.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height() # Récupère la largeur et la hauteur de la fenêtre d'affichage
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15) # Police pour le titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 33) # Police pour le texte explicatif

    # Texte du titre de l'écran d'information
    texte_titre = "L'expérience de Buffon"

    # Texte descriptif de l'expérience
    texte_description = (
        "L'expérience de Buffon est une méthode probabiliste qui permet d'estimer π en lançant des aiguilles "
        "sur un sol quadrillé de lignes parallèles. Le rapport entre les aiguilles qui croisent une ligne et "
        "le nombre total d'aiguilles donne une approximation de π."
    )

    # Texte contenant la formule utilisée dans l'expérience
    texte_formule = (
        "La formule utilisée est :",
        "π ≈ (2 × longueur de l’aiguille × nombre total d’aiguilles) / (nombre d’aiguilles coupant une ligne × espacement entre les lignes)."
    )

    # Texte décrivant la visualisation dans la simulation
    texte_visualisation = (
        "Visualisation :",
        "• Dans cette simulation, des aiguilles sont projetées en continu sur l'écran.",
        "• Les aiguilles qui coupent une ligne sont affichées en rouge, tandis que celles qui ne la croisent pas restent grises",
        "• L'entrée utilisateur permet de changer la vitesse de l'expérience."
    )

    while True:
        ecran.fill(NOIR)  # Remplit l'écran de noir

        # Affichage du titre
        titre_rendu = police_titre.render(texte_titre, True, BLANC)  # Rend le titre en blanc
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))  # Affiche le titre centré
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre

        # Affichage des descriptions
        y_position = hauteur_ecran // 6 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 5
        # Affiche le texte descriptif
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 15, y_position, 15, largeur_ecran * 0.85, police_texte) + hauteur_ecran // 50
        y_position += 0  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 30 # Ajoute un espace en fonction de si on est en plein écran ou non
        # Pour chaque ligne de la formule, affiche la ligne en bleu
        for ligne in texte_formule:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 15, y_position + 15, 15, largeur_ecran * 0.85, police_texte, BLEU, souligner=True if ligne == "La formule utilisée est :" else False) + hauteur_ecran // 50
        y_position += 0  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 30 # Ajoute un espace en fonction de si on est en plein écran ou non
        # Affiche le texte de visualisation
        for ligne in texte_visualisation :
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 15, y_position + 15, 15, largeur_ecran * 0.85, police_texte, souligner=True if ligne == "Visualisation :" else False) + hauteur_ecran // 50

        # Prépare et affiche l'instruction pour commencer
        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer.", True, ROUGE)
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))

        bouton_menu()  # Affiche le bouton menu
        croix_fermer()  # Affiche la croix de fermeture
        pygame.display.update()  # Met à jour l'affichage

        # Gestion des événements utilisateur
        evenement_boutons, _ = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur le bouton menu
            return False  # Retourne au menu
        if evenement_boutons == "clic":  # Si l'utilisateur clique n'importe où
            return True  # Retourne True pour continuer

def buffon():
    """
    Exécute la simulation de l'expérience de Buffon.

    Paramètres :
        Aucun

    Retourne :
        Rien. La fonction s'exécute en boucle jusqu'à ce que l'utilisateur quitte.
    """
    if not information_buffon():  # Affiche les informations et vérifie si l'utilisateur ne retourne pas au menu
        return  # Retourne au menu
    # Récupère les dimensions de la fenêtre d'affichage
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()
    ecran.fill(BLANC)  # Remplit l'écran de blanc pour le début de la simulation
    police = pygame.font.Font(POLICE, hauteur_ecran // 25)  # Initialise la police pour l'affichage des statistiques

    nombre_aiguilles = 0  # Compteur du nombre total d'aiguilles lancées
    aiguilles_coupent = 0  # Compteur des aiguilles qui coupent une ligne
    longueur_aiguille = 50  # Longueur d'une aiguille
    espacement_lignes = 50   # Espacement entre les lignes
    aiguilles = []  # Liste pour stocker les informations sur chaque aiguille lancée

    duree_vie_aiguille = 3  # Durée de vie d'une aiguille en secondes
    duree_fondu = 1  # Durée pendant laquelle l'aiguille se fond (diminue son opacité)

    aiguilles_par_seconde = 20  # Vitesse initiale : nombre d'aiguilles générées par seconde
    dernier_temps = time.perf_counter()  # Enregistre le temps actuel pour le timing de génération

    textinput = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)  # Zone de saisie pour changer la vitesse

    surface_aiguilles = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)  # Crée une surface transparente pour dessiner les aiguilles

    while True:
        ecran.fill(BLANC)  # Remplit l'écran de blanc à chaque itération

        # Dessine les lignes horizontales du quadrillage
        for y_lignes in range(0, hauteur_ecran, espacement_lignes):
            pygame.draw.line(ecran, NOIR, (0, y_lignes), (largeur_ecran, y_lignes), 2)

        # Récupère les événements utilisateur
        evenement_boutons, evenements = gestionnaire_evenements()            
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur le bouton menu
                return  # retourne au menu
        if evenement_boutons == 'info':  # Si l'utilisateur clique sur le bouton d'information
            if not information_buffon():  # Affiche à nouveau l'écran d'information
                return  # retourne au menu si il clique sur le bouton menu depuis la fonction d'infos
        for evenement in evenements:
            # Si la touche Entrée est pressée
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:
                if textinput.value.isdigit(): # Si c'est des nombres
                    aiguilles_par_seconde = max(1, int(textinput.value))  # Met à jour la vitesse (minimum 1)
                textinput.value = ""  # Réinitialise la zone de saisie

        textinput.update(evenements)  # Met à jour la saisie avec les événements récents
        if len(textinput.value) > 5:  # Limite la saisie à 5 caractères
            textinput.value = textinput.value[:5]

        temps_actuel = time.perf_counter()  # Récupère le temps actuel avec une fonction de time plus performante
        intervalle = 1 / max(1, aiguilles_par_seconde)  # Calcule l'intervalle entre deux lancements

        nouvelles_aiguilles = []  # Liste pour stocker les aiguilles générées dans cette itération

        # Génère des aiguilles tant que le temps écoulé est suffisant pour un nouveau lancement
        while temps_actuel - dernier_temps >= intervalle:
            dernier_temps += intervalle  # Met à jour le temps du dernier lancement

            # Génère des coordonnées centrales aléatoires pour l'aiguille dans la zone d'affichage
            x_centre = random.uniform(longueur_aiguille / 2, largeur_ecran - longueur_aiguille / 2)
            y_centre = random.uniform(longueur_aiguille / 2, hauteur_ecran - longueur_aiguille / 2)
            angle = random.uniform(0, math.pi)  # Génère un angle aléatoire entre 0 et π

            # Calcule les coordonnées des deux extrémités de l'aiguille
            x1 = x_centre - (longueur_aiguille / 2) * math.cos(angle)
            y1 = y_centre - (longueur_aiguille / 2) * math.sin(angle)
            x2 = x_centre + (longueur_aiguille / 2) * math.cos(angle)
            y2 = y_centre + (longueur_aiguille / 2) * math.sin(angle)

            # Vérifie si l'aiguille coupe une ligne en comparant les positions verticales
            coupe_ligne = int(y1 // espacement_lignes) != int(y2 // espacement_lignes)
            couleur = ROUGE if coupe_ligne else GRIS  # Choisit la couleur rouge si coupe, sinon gris
            # Ajoute l'aiguille générée avec ses propriétés à la liste des nouvelles aiguilles
            nouvelles_aiguilles.append({'p1': (x1, y1), 'p2': (x2, y2), 'couleur': couleur, 'temps': time.perf_counter(), 'opacite': 255})

            if coupe_ligne:  # Si l'aiguille coupe une ligne
                aiguilles_coupent += 1  # Incrémente le compteur des aiguilles coupant une ligne
            nombre_aiguilles += 1  # Incrémente le compteur total d'aiguilles lancées

        # Supprime les aiguilles qui ont dépassé leur durée de vie
        aiguilles = [aiguille for aiguille in aiguilles if time.perf_counter() - aiguille['temps'] < duree_vie_aiguille]

        aiguilles.extend(nouvelles_aiguilles)  # Ajoute les nouvelles aiguilles à la liste globale

        # Réinitialise la surface tampon des aiguilles avec une transparence totale pour redessiner
        surface_aiguilles.fill((0, 0, 0, 0))

        for aiguille in aiguilles:
            # Calcule le temps écoulé depuis la création de l'aiguille
            temps_ecoule = time.perf_counter() - aiguille['temps']

            # Si l'aiguille n'est pas encore en phase de fondu, son opacité reste à 255
            if temps_ecoule < (duree_vie_aiguille - duree_fondu):
                opacite = 255
            else:
                # Calcule le temps passé dans la phase de fondu et ajuste l'opacité en conséquence
                temps_fondu = temps_ecoule - (duree_vie_aiguille - duree_fondu)
                opacite = max(0, int(255 * (1 - temps_fondu / duree_fondu)))
            aiguille['opacite'] = opacite  # Met à jour l'opacité de l'aiguille dans son dictionnaire
            couleur_aiguille = (*aiguille['couleur'], opacite)  # Combine la couleur de base avec l'opacité pour obtenir une couleur RGBA
            pygame.draw.line(surface_aiguilles, couleur_aiguille, aiguille['p1'], aiguille['p2'], 2)  # Dessine l'aiguille sur la surface tampon

        ecran.blit(surface_aiguilles, (0, 0))  # Colle la surface tampon sur l'écran principal

        # Calcule l'estimation de π selon la formule de Buffon, si au moins une aiguille coupe une ligne
        pi_estime = (2 * longueur_aiguille * nombre_aiguilles) / (aiguilles_coupent * espacement_lignes) if aiguilles_coupent > 0 else 0

        # Crée une surface transparente pour afficher les textes d'information
        surface_textes = pygame.Surface((ecran.get_width(), 300), pygame.SRCALPHA)
        surface_textes.fill((0, 0, 0, 100))  # Remplit la surface avec du noir semi-transparent

        # Prépare les textes d'affichage des statistiques
        texte_pi = police.render(f"Estimation de π: {pi_estime:.6f}", True, BLANC)
        texte_aiguilles = police.render(f"Aiguilles lancées: {nombre_aiguilles}", True, BLANC)
        texte_coupes = police.render(f"Aiguilles coupant une ligne: {aiguilles_coupent}", True, BLANC)
        texte_vitesse = police.render(f"Aiguilles/sec: {aiguilles_par_seconde}", True, BLANC)
        texte_input = police.render("Changer la vitesse:", True, BLANC)

        # Affiche la surface de texte et les textes statistiques sur l'écran
        ecran.blit(surface_textes, (0, 0))
        ecran.blit(texte_pi, (20,  50 - 25 - texte_pi.get_height() // 2))
        ecran.blit(texte_aiguilles, (20, 100 - 25 - texte_aiguilles.get_height() // 2))
        ecran.blit(texte_coupes, (20,  150 - 25 - texte_coupes.get_height() // 2))
        ecran.blit(texte_vitesse, (20,  200 - 25 - texte_vitesse.get_height() // 2))
        ecran.blit(texte_input, (20, 250 - 25 - texte_input.get_height() // 2))
        ecran.blit(textinput.surface, (20,  300 - 25 - 25 // 2))

        bouton_informations()  # Affiche le bouton d'information
        bouton_menu()  # Affiche le bouton menu
        croix_fermer()  # Affiche la croix de fermeture
        pygame.display.update()  # Met à jour l'affichage

