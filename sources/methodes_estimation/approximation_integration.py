#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import math  # Module math pour les fonctions mathématiques (sqrt, pi, etc.)
import pygame  # Bibliothèque Pygame pour la gestion de l'interface graphique et des événements
from affichage import ecran, BLANC, NOIR, ROUGE, BLEU, POLICE, bouton_menu, croix_fermer, bouton_informations, ecran_information  # Composants d'affichage et couleurs.
from utils import gestionnaire_evenements, afficher_texte_dynamique, souligner_texte # Fonctions utilitaires

def information_approximation_integration():
    """
    Affiche un écran d'informations sur la méthode d'approximation de π par intégration.
    L'utilisateur peut cliquer pour passer à l'étape suivante, ou cliquer sur le bouton "menu".

    Paramètres:
        Aucun
    
    Retourne:
        bool: 
            - True si l'utilisateur clique dans la fenêtre pour commencer la démonstration,
            - False s'il clique sur le bouton "menu".
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la largeur et la hauteur de la fenêtre
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police pour le titre, taille proportionnelle à la hauteur d'écran
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 30)  # Police pour le texte descriptif, un peu plus petite

    texte_titre = "Approximation par Intégration"  # Titre de la méthode

    # Texte décrivant le principe d'approximation de π par intégration (aire sous la demi-courbe d'un cercle)
    texte_description = (
        "L'approximation de π par intégration repose sur le calcul de l'aire sous la courbe "
        "d'un demi cercle en utilisant des rectangles. En augmentant le nombre de subdivisions, "
        "l'approximation devient plus précise."
    )

    # Informations sur la formule mathématique utilisée pour l'intégration
    texte_formule = (
        "La formule utilisée est basée sur la somme des aires des rectangles : ",
        "π ≈ 2 × Σ [sqrt(1 - x²) × dx], où dx est la largeur des subdivisions."
    )

    # Complément sur l'utilisation en enseignement et l'intérêt de cette méthode
    texte_utilisation = (
        "Cette méthode illustre la notion d'intégrale définie et est couramment utilisée "
        "pour enseigner les bases de l'analyse mathématique et des calculs numériques."
    )

    while True:  # Boucle d'affichage des informations
        ecran.fill(NOIR)  # Remplit l'écran en noir

        # Affichage du titre centré en haut de l'écran
        titre_rendu = police_titre.render(texte_titre, True, BLANC)  # Surface texte pour le titre
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))  # Placement centré horizontalement
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre

        # On affiche progressivement le texte explicatif
        y_position = hauteur_ecran // 5  # Point de départ vertical
        # Affiche le texte principal décrivant la méthode
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 10, y_position, 15, largeur_ecran * 0.8, police_texte) + hauteur_ecran // 50
        y_position += 0 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 13
        # Affiche chaque ligne de la formule en bleu
        for lignes in texte_formule:
            y_position += afficher_texte_dynamique(ecran, lignes, largeur_ecran // 10, y_position + 15, 15, largeur_ecran * 0.8, police_texte, BLEU, souligner=True if lignes == "La formule utilisée est basée sur la somme des aires des rectangles : " else False) + hauteur_ecran // 30

        y_position += hauteur_ecran // 50 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 13

        # Affiche la dernière partie d'explication (utilisation)
        y_position += afficher_texte_dynamique(ecran, texte_utilisation, largeur_ecran // 10, y_position + 15, 15, largeur_ecran * 0.8, police_texte)

        # Affiche un message encourageant l'utilisateur à cliquer pour commencer
        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer.", True, ROUGE)
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))

        # Dessine le bouton menu et la croix de fermeture, puis met à jour l'affichage
        bouton_menu()
        croix_fermer()
        pygame.display.update()

        # Gestion des événements via la fonction dédiée
        evenement_boutons, _ = gestionnaire_evenements()
        if evenement_boutons == "menu":
            return False  # L'utilisateur revient en arrière
        if evenement_boutons == "clic":
            return True  # L'utilisateur clique sur la fenêtre pour commencer

def approximation_integration():
    """
    Affiche la démonstration interactive pour approximer π par intégration (aire sous la courbe d'un demi-cercle).
    L'utilisateur peut régler le nombre de subdivisions pour améliorer la précision de l'intégration.
    
    Paramètres:
        Aucun
    
    Retourne:
        Rien. La fonction se termine lorsque l'utilisateur clique sur "menu" ou ferme la fenêtre.
    """
    # On commence par afficher l'écran d'information
    if not information_approximation_integration():
        return # Si on clique sur le bouton menu dans la fonction d'informations, retour au menu

    pygame.time.delay(200)  # Petite pause pour éviter un double-clic non intentionnel.

    # Récupération des dimensions de la fenêtre
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()

    # Définition des coordonnées du centre du demi-cercle et de son rayon (prend 1/3 de la dimension la plus petite)
    centre_x, centre_y = largeur_ecran // 2, hauteur_ecran // 1.4
    rayon_cercle = min(largeur_ecran, hauteur_ecran) // 3

    # Bornes et valeur initiale pour le nombre de subdivisions
    nombre_subdivisions_min = 1
    nombre_subdivisions_max = 450
    nombre_subdivisions = 1

    # Positions et dimensions de la barre de réglage (curseur)
    position_barre_x = 50
    position_barre_y = hauteur_ecran - 100
    largeur_barre = largeur_ecran - 100
    position_curseur_x = position_barre_x  # Position initiale du curseur

    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 22)  # Police

    while True: # Boucle principale
        ecran.fill(NOIR)  # Efface l'écran avec du noir.

        # On récupère l'action renvoyée par le gestionnaire d'événements.
        evenement_boutons, _ = gestionnaire_evenements()

        if evenement_boutons == "menu":  # Si l'utilisateur clique sur le bouton menu
            return  # On retourne au menu
        if evenement_boutons == "info":  # S'il clique sur le bouton "info"
            if not information_approximation_integration():  # Ré-affiche l'écran d'information
                return # Si on clique sur le bouton menu dans la fonction d'informations, retour au menu

        # Gestion du clic de souris maintenu pour déplacer le curseur de subdivisions.
        if pygame.mouse.get_pressed()[0]:  # Vérifie si le bouton gauche est enfoncé
            position_souris_x, _ = pygame.mouse.get_pos()  # On récupère juste la coordonnée X de la souris
            # On limite le curseur pour qu'il ne sorte pas de la barre
            if position_barre_x <= position_souris_x <= position_barre_x + largeur_barre:
                position_curseur_x = position_souris_x

        # Calcule la position relative du curseur entre 0 et 1
        position_relative = (position_curseur_x - position_barre_x) / largeur_barre

        # Selon la position, on fait évoluer nombre_subdivisions de manière mixte :
        # - la première moitié => de 1 à 50 en progression linéaire
        # - la deuxième => de 50 à 530 en progression accélérée (puissance 2.5).
        if position_relative <= 0.5:
            nombre_subdivisions = int(1 + (50 - 1) * (position_relative / 0.5))
        else:
            progression_acceleration = (position_relative - 0.5) / 0.5
            facteur_acceleration = 2.5
            nombre_subdivisions = int(50 + (nombre_subdivisions_max - 50) * (progression_acceleration ** facteur_acceleration))

        # On s'assure que le nombre de subdivisions ne dépasse pas les bornes.
        nombre_subdivisions = min(nombre_subdivisions_max, max(nombre_subdivisions_min, nombre_subdivisions))

        # Dessine l'arc d'un demi-cercle en haut (pour symboliser y = sqrt(1 - x^2))
        pygame.draw.arc(ecran, BLANC, (centre_x - rayon_cercle, centre_y - rayon_cercle, 2 * rayon_cercle, 2 * rayon_cercle), 
            0,  # Angle de départ (0 radians => sur l'axe X à droite)
            math.pi,  # Angle d'arrivée (π radians => sur l'axe X à gauche)
            2  # Épaisseur de 2 pixels pour l'arc
        )

        # Calcul numérique de l'intégrale via la somme des aires de rectangles.
        somme_aire = 0.0
        largeur_rectangle = 2 / nombre_subdivisions  # Si l'intervalle est [-1, 1], on a donc longueur de 2
        for i in range(nombre_subdivisions):
            # On prend ici le point du milieu de chaque subdivision.
            position_x = -1 + (i + 0.5) * largeur_rectangle  # X est dans l'intervalle [-1, 1]
            hauteur_rectangle = math.sqrt(1 - position_x**2)  # hauteur du demi-cercle
            # Conversion en coordonnées Pygame:
            position_rectangle_x = centre_x + int(position_x * rayon_cercle)
            position_rectangle_y = centre_y - int(hauteur_rectangle * rayon_cercle)
            largeur_affichage_rectangle = int(largeur_rectangle * rayon_cercle)
            hauteur_affichage_rectangle = int(hauteur_rectangle * rayon_cercle)
            # Couleur dégradée en fonction de la hauteur (simple effet visuel)
            couleur_rectangle = (255, int(255 * hauteur_rectangle), 0)
            
            # Dessine le rectangle de hauteur "hauteur_affichage_rectangle" à la position calculée
            pygame.draw.rect(ecran, couleur_rectangle, (position_rectangle_x - largeur_affichage_rectangle // 2, position_rectangle_y, largeur_affichage_rectangle, hauteur_affichage_rectangle))
            # On ajoute l'aire (hauteur_rectangle * largeur_rectangle) à la somme, correspondant à la surface sous la courbe
            somme_aire += hauteur_rectangle * largeur_rectangle

        # L'intégrale sur [-1,1] de sqrt(1 - x^2) représente un demi-cercle d'aire π/2.
        # Pour obtenir π, on multiplie par 2 la somme trouvée.
        estimation_pi = 2 * somme_aire

        # On affiche le texte d'information : l'estimation de pi, et le nombre de subdivisions.
        texte_estimation_pi = police_texte.render(f"Estimation de Pi: {estimation_pi:.6f}", True, BLANC)
        texte_nombre_subdivisions = police_texte.render(f"Subdivisions: {nombre_subdivisions}", True, BLANC)
        ecran.blit(texte_estimation_pi, (largeur_ecran // 2 - texte_estimation_pi.get_width() // 2, hauteur_ecran // 5))
        ecran.blit(texte_nombre_subdivisions, (largeur_ecran // 2 - texte_nombre_subdivisions.get_width() // 2, hauteur_ecran // 10))

        # Dessine la barre de réglage en gris et le curseur (cercle blanc).
        pygame.draw.rect(ecran, (150, 150, 150), (position_barre_x, position_barre_y, largeur_barre, 5))
        pygame.draw.circle(ecran, BLANC, (position_curseur_x, position_barre_y + 2), 10)

        # Affiche les boutons d'information, le bouton de retour au menu et la croix de fermeture.
        bouton_informations()
        bouton_menu()
        croix_fermer()

        # Met à jour la fenêtre Pygame avec tout ce qui a été dessiné.
        pygame.display.update()
