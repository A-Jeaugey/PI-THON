#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Importation de pygame pour la gestion de l'affichage et des événements
import pygame_textinput  # Importation de pygame_textinput pour gérer la saisie de texte dans pygame
import math  # Importation de math pour les fonctions mathématiques (sin, cos, etc.)
from affichage import ecran, POLICE, BLANC, NOIR, ROUGE, BLEU, GRIS, bouton_menu, croix_fermer, bouton_informations, ecran_information  # Importation des objets, polices et icônes d'affichage
from utils import gestionnaire_evenements, afficher_texte_dynamique, temps_ecoule, souligner_texte  # Importation des fonctions utilitaires pour gérer les événements, afficher du texte et mesurer le temps

def information_pendule():
    """
    Affiche un écran d'information pour la méthode du pendule simple.
    
    Paramètres :
        Aucun
        
    Retourne :
        True si l'utilisateur clique pour commencer, False s'il clique sur menu.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère les dimensions de la fenêtre
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Initialise la police pour le titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 40)  # Initialise la police pour le texte explicatif

    texte_titre = "Méthode du Pendule Simple"  # Définit le titre de l'écran d'information

    texte_description = (  # Texte décrivant la méthode du pendule simple
        "La méthode du pendule simple est une approche physique classique "
        "pour estimer la valeur de π, basée sur la mesure expérimentale de la période "
        "d'un pendule oscillant avec une faible amplitude. "
    )

    texte_formule = (  # Texte contenant la formule du pendule simple
        "La période d'un pendule simple est donnée par :",
        "T ≈ 2π × √(L / g)",
        "• T est la période du pendule (temps d'un aller-retour complet).",
        "• L est la longueur du pendule (en mètres).",
        "• g ≈ 9.81 m/s² est l'accélération de la pesanteur terrestre."
    )

    texte_calcul_pi = (  # Texte expliquant comment isoler π à partir de la période mesurée
        "En mesurant la période T expérimentalement, on peut isoler π :",
        "π = T / (2 × √(L / g))"
    )

    texte_visualisation = (  # Texte décrivant la visualisation de la simulation du pendule
        "Visualisation :",
        "• Le pendule est simulé graphiquement à l'écran en temps réel.",
        "• La période est mesurée automatiquement en détectant les passages par la position d'équilibre.",
        "• Vous pouvez choisir la longueur du pendule au début de la simulation."
    )

    while True:
        ecran.fill(NOIR)  # Remplit l'écran de noir pour le fond

        rendu_titre = police_titre.render(texte_titre, True, BLANC)  # Rend le titre en blanc
        ecran.blit(rendu_titre, (largeur_ecran // 2 - rendu_titre.get_width() // 2, hauteur_ecran // 40))  # Affiche le titre centré en haut
        souligner_texte(ecran, rendu_titre, largeur_ecran // 2 - rendu_titre.get_width() // 2, hauteur_ecran // 40) # Souligne le titre

        y_position = hauteur_ecran // 7  # Définit la position verticale de départ pour le texte
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 15, y_position, 15, largeur_ecran * 0.85, police_texte) + 20  
        # Affiche le texte de description
        y_position += -10  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 50 # Ajoute un espace en fonction de si on est en plein écran ou non
        for ligne in texte_formule:  # Pour chaque ligne de la formule
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 15, y_position + 5, 15, largeur_ecran * 0.85, police_texte, BLEU, souligner=True if ligne == "La période d'un pendule simple est donnée par :" else False) + hauteur_ecran // 50
            # Affiche la ligne de formule en bleu

        y_position += - 10  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 50 # Ajoute un espace en fonction de si on est en plein écran ou non

        for ligne in texte_calcul_pi:  # Pour chaque ligne du texte de calcul de π
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 15, y_position + 5, 15, largeur_ecran * 0.85, police_texte, BLEU, souligner=True if ligne == "En mesurant la période T expérimentalement, on peut isoler π :" else False) + hauteur_ecran // 50
            # Affiche la ligne en bleu
        y_position += 0  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 50 # Ajoute un espace en fonction de si on est en plein écran ou non
        for ligne in texte_visualisation:  # Pour chaque ligne du texte de visualisation
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 15, y_position + 5, 15, largeur_ecran * 0.85, police_texte, souligner=True if ligne == "Visualisation :" else False) + hauteur_ecran // 50
            # Affiche la ligne en blanc

        rendu_instruction = police_titre.render("Cliquez n'importe où pour commencer", True, ROUGE)  # Rend l'instruction en rouge
        ecran.blit(rendu_instruction, (largeur_ecran // 2 - rendu_instruction.get_width() // 2, hauteur_ecran * 0.92))  
        # Affiche l'instruction centrée en bas

        bouton_menu()  # Affiche l'icône de le bouton menu
        croix_fermer()  # Affiche l'icône de la croix de fermeture
        pygame.display.update()  # Actualise l'affichage

        evenement_boutons, _ = gestionnaire_evenements()  # Récupère les événements utilisateur
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur menu
            return False  # Retourne au menu
        if evenement_boutons == "clic":  # Si l'utilisateur clique sur l'écran
            return True  # Retourne True pour continuer

def pendule():
    """
    Fonction principale de la simulation du pendule simple pour estimer π.
    
    Paramètres :
        Aucun
        
    Retourne :
        Rien. La fonction gère le paramétrage, l'animation et l'affichage de la simulation.
    """
    if not information_pendule():  # Affiche l'écran d'information et retourne au menu si il clique sur le bouton menu
        return
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère les dimensions de la fenêtre
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Initialise la police pour le titre du paramétrage
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 30)  # Initialise la police pour le texte explicatif

    zone_saisie = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)  # Crée une zone de saisie pour entrer la longueur du pendule
    longueur_pendule = None  # Variable pour stocker la longueur du pendule (L) saisie par l'utilisateur
    gravite = 9.81  # Définition de l'accélération de la pesanteur terrestre

    while longueur_pendule is None:
        ecran.fill(NOIR)  # Remplit l'écran de noir pour le paramétrage

        rendu_titre = police_titre.render("Pendule simple - Paramétrage", True, BLANC)  # Rend le titre du paramétrage
        rendu_explication = police_texte.render("Entrez la longueur L du pendule (en mètres) : (min 0.2, max 5)", True, BLANC)  
        # Rend le texte explicatif indiquant la plage autorisée pour L

        ecran.blit(rendu_titre, (largeur_ecran // 2 - rendu_titre.get_width() // 2, hauteur_ecran // 10))  # Affiche le titre centré
        ecran.blit(rendu_explication, (largeur_ecran // 2 - rendu_explication.get_width() // 2, hauteur_ecran // 5))  # Affiche l'explication centrée
        ecran.blit(zone_saisie.surface, (largeur_ecran // 2 - zone_saisie.surface.get_width() // 2, hauteur_ecran // 3.8))  
        # Affiche la zone de saisie centrée

        bouton_informations()  # Affiche le bouton d'information
        bouton_menu()  # Affiche le bouton menu
        croix_fermer()  # Affiche la croix de fermeture
        pygame.display.update()  # Actualise l'affichage

        evenement_boutons, evenements = gestionnaire_evenements()  # Récupère les événements utilisateur
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur menu
            return # Retourne au menu
        if evenement_boutons == "info":  # Si l'utilisateur clique sur le bouton d'information
            if not information_pendule():  # Réaffiche l'écran d'information
                return # Si il clique sur le bouton menu dans la fonction d'informations, retour au menu

        zone_saisie.update(evenements)  # Met à jour la zone de saisie avec les événements
        for evenement in evenements:
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:  # Si l'utilisateur appuie sur Entrée
                if zone_saisie.value.replace('.', '', 1).isdigit():  # Vérifie que la valeur saisie est un nombre (avec possibilité de point décimal)
                    longueur_pendule = min(5, max(0.2, float(zone_saisie.value)))  # Contrainte : L doit être entre 0.2 et 5
                zone_saisie.value = ""  # Réinitialise la zone de saisie

    # Initialisation des variables du pendule
    theta = 0.07  # Angle initial (en radians)
    omega = 0.0  # Vitesse angulaire initiale
    abscisse_pivot = largeur_ecran // 2  # Position x du pivot du pendule (centré horizontalement)
    ordonnee_pivot = hauteur_ecran // 4  # Position y du pivot du pendule
    rayon_boule = 15  # Rayon de la boule du pendule
    ancien_signe_theta = 1 if theta >= 0 else -1  # Détection du passage par zéro
    dernier_temps_croisement = None  # Temps du dernier passage par zéro
    periodes_mesurees = []  # Liste des périodes mesurées

    # Temps initial
    temps_precedent = pygame.time.get_ticks()
    debut_ticks = temps_precedent

    # Boucle d'animation
    while True:
        ecran.fill(NOIR)  # Efface l'écran

        # Calcul du delta-temps réel
        temps_actuel = pygame.time.get_ticks()
        dt_reel = (temps_actuel - temps_precedent) / 1000.0  # Convertir en secondes
        temps_precedent = temps_actuel  # Mise à jour du temps de référence

        # Gestion des événements
        evenement_boutons, evenements = gestionnaire_evenements()
        if evenement_boutons == "menu":
            return  # Retour au menu
        if evenement_boutons == "info":
            if not information_pendule():
                return  # Retour au menu si l'utilisateur quitte l'info

        # Dessiner boutons, croix, et bouton d'informations
        croix_fermer()
        bouton_menu()
        bouton_informations()

        # Simulation physique du pendule
        acceleration_angulaire = - (gravite / longueur_pendule) * math.sin(theta)
        omega += acceleration_angulaire * dt_reel  # Mettre à jour la vitesse angulaire
        theta += omega * dt_reel  # Mettre à jour l'angle

        # Détection des passages par zéro
        nouveau_signe_theta = 1 if theta >= 0 else -1
        if nouveau_signe_theta != ancien_signe_theta:
            if ancien_signe_theta < 0 and nouveau_signe_theta > 0:
                if dernier_temps_croisement is not None:
                    periode_ms = temps_actuel - dernier_temps_croisement
                    periode_s = periode_ms / 1000.0  # Convertir en secondes
                    periodes_mesurees.append(periode_s)
                dernier_temps_croisement = temps_actuel  # Mettre à jour le dernier passage
        ancien_signe_theta = nouveau_signe_theta  # Mettre à jour l'ancien signe

        # Calcul de π
        periode_estimee = sum(periodes_mesurees) / len(periodes_mesurees) if periodes_mesurees else 0
        pi_estime = periode_estimee / (2 * math.sqrt(longueur_pendule / gravite)) if periode_estimee > 0 else 0

        # Calcul de la position de la boule
        position_x_boule = abscisse_pivot + int(longueur_pendule * 100.0 * math.sin(theta))
        position_y_boule = ordonnee_pivot + int(longueur_pendule * 100.0 * math.cos(theta))

        # Dessiner le pendule
        pygame.draw.line(ecran, GRIS, (abscisse_pivot, ordonnee_pivot), (position_x_boule, position_y_boule), 3)
        pygame.draw.circle(ecran, ROUGE, (position_x_boule, position_y_boule), rayon_boule)

        # Affichage du texte
        texte_longueur = police_texte.render(f"L = {longueur_pendule:.2f} m", True, BLANC)
        texte_nombre_periodes = police_texte.render(f"Nombre périodes mesurées : {len(periodes_mesurees)}", True, BLANC)
        texte_periode = police_texte.render(f"Temps moyen = {periode_estimee:.2f} s", True, BLANC)
        texte_pi = police_texte.render(f"Pi estimé = {pi_estime:.6f}", True, BLANC)
        texte_temps = police_texte.render(f"Temps réel : {temps_ecoule(debut_ticks)}", True, BLANC)
        #Positionnement du texte
        ecran.blit(texte_longueur, (50, hauteur_ecran // 40))
        ecran.blit(texte_nombre_periodes, (50, hauteur_ecran // 15))
        ecran.blit(texte_periode, (50, hauteur_ecran // 9))
        ecran.blit(texte_pi, (50, hauteur_ecran // 6.5))
        ecran.blit(texte_temps, (50, hauteur_ecran // 5.1))

        pygame.display.update()  # Actualiser l'affichage
