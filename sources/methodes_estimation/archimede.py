#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import math  # Module math pour les fonctions mathématiques (sin, cos, etc.)
import pygame  # Module Pygame pour gérer l'affichage, les événements, etc.
from affichage import ecran, POLICE, BLANC, NOIR, ROUGE, BLEU, bouton_menu, croix_fermer, bouton_informations, ecran_information # Composants d'affichage et couleurs.
from utils import gestionnaire_evenements, afficher_texte_dynamique, souligner_texte # Fonctions utilitaires


def information_archimede():
    """
    Affiche un écran d'information sur la méthode d'Archimède et attend un clic pour passer à l'étape suivante.
    
    Paramètres: Aucun
    Retourne: 
        - True si l'utilisateur clique dans la fenêtre pour commencer,
        - False si l'utilisateur clique sur le bouton menu.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la largeur et la hauteur de la fenêtre
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police pour le grand titre, dont la taille dépend de la hauteur de l'écran
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 42)  # Police plus petite pour le corps du texte
    texte_titre = "Méthode d'Archimède"  # Titre de la page

    # Texte principal décrivant l'historique et le principe de la méthode d'Archimède
    texte_description = (
        "Développée par Archimède vers 250 av. J.-C., cette méthode est l'une des premières tentatives "
        "pour estimer π avec précision. elle consiste à encadrer un cercle à l'aide d'un polygone régulier "
        "inscrit, qui sous-estime la circonférence du cercle et d'un polygone circonscrit qui la surestime "
        "La moyenne des deux fournit une approximation de π. Plus le nombre de côtés du polygone est grand, plus cette approximation est précise. "
    )

    # Formule mathématique utilisée par Archimède : polygone inscrit / polygone circonscrit
    texte_formule = (
        "La formule est alors :",
        "π ≈ ( P_inscrit + P_circonscrit ) / 2, où : ",
        "P_inscrit = n × sin(π/n) et P_circonscrit = n × tan(π/n), ",
        "avec n le nombre de côtés du polygone utilisé."
    )

    # Explications sur la partie interactive (visualisation, couleurs, etc.)
    texte_utilisation = (
        "Visualisation :",
        "• le cercle est tracé en blanc, le polygone inscrit en rouge et le polygone circonscrit en vert. ",
        "• Le nombre de côtés du polygone peut être ajusté à l'aide de la barre en bas de l'écran. "
    )

    while True:  # Boucle d'affichage de l'écran d'information
        ecran.fill(NOIR)  # Remplit l'écran de noir

        # Affichage du titre, centré horizontalement, placé en haut
        titre_rendu = police_titre.render(texte_titre, True, BLANC)  # Surface de texte pour le titre
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))  # Placement centré
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre
        # Calcul d'une position Y de départ pour afficher le texte explicatif
        y_position = hauteur_ecran // 7
        # Affiche la description principale, en utilisant la fonction afficher_texte_dynamique
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran * 0.05, y_position, 15, largeur_ecran * 0.9, police_texte) + hauteur_ecran // 50
        y_position += hauteur_ecran // 18  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 10 # Ajoute un espace en fonction de si on est en plein écran ou non

        # Affiche les lignes de la formule, chacune colorée en bleu
        for ligne in texte_formule:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran * 0.05, y_position, 15, largeur_ecran * 0.9, police_texte, BLEU, souligner=True if ligne == "La formule est alors :" else False) + hauteur_ecran // 50
        y_position += hauteur_ecran // 18  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 10 # Ajoute un espace en fonction de si on est en plein écran ou non

        for ligne in texte_utilisation :
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran * 0.05, y_position + 15, 15, largeur_ecran * 0.9, police_texte, souligner=True if ligne == "Visualisation :" else False) + hauteur_ecran // 50
    
        # Indique à l'utilisateur qu'il peut cliquer pour commencer
        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer.", True, ROUGE)
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))

        # Dessine le bouton menu, la croix de fermeture, et met à jour l'affichage
        bouton_menu()
        croix_fermer()
        pygame.display.update()

        # Gestion des événements via notre fonction gestionnaire_evenements
        evenement_boutons, _ = gestionnaire_evenements()
        if evenement_boutons == "menu":  # L'utilisateur clique sur le bouton menu
            return False  # On retourne au menu
        if evenement_boutons == "clic":  # L'utilisateur clique dans la fenêtre
            return True  # On sort en renvoyant True (prêt à lancer la partie interactive)


def archimede():
    """
    Affiche la démonstration interactive de la méthode d'Archimède pour estimer π,
    en traçant un cercle, puis un polygone inscrit et un polygone circonscrit dont le nombre de côtés est ajustable.
    
    Paramètres: Aucun
    Retourne: Rien (on quitte la fonction si l'utilisateur clique sur 'menu').
    """
    if not information_archimede():  # On commence par afficher l'écran d'information
        return # Si on clique sur le bouton menu dans la fonction d'informations, retour au menu
    
    pygame.time.delay(200)  # Petite pause pour éviter que le clic ne déclenche immédiatement autre chose

    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # On récupère la taille de la fenêtre
    centre_cercle = (largeur_ecran // 2, hauteur_ecran // 1.85)  # Coordonnées du centre du cercle
    rayon = hauteur_ecran // 4  # Rayon du cercle

    nombre_cotes_min = 3  # Nombre minimal de côtés (un triangle)
    nombre_cotes_max = 50000  # Nombre maximal de côtés (un pentakismyriagone). (^-^)
    nombre_cotes = 3  # Valeur initiale du nombre de côtés

    position_x_barre = 50  # Position X pour la barre de réglage (curseur)
    position_y_barre = hauteur_ecran - 100  # Position Y pour la barre de réglage
    largeur_barre = largeur_ecran - 100  # Largeur de cette barre
    position_curseur = position_x_barre  # Position initiale du curseur sur la barre

    police_titre = pygame.font.Font(POLICE, largeur_ecran // 20)  # Police pour le titre en haut
    police_texte = pygame.font.Font(POLICE, largeur_ecran // 40)  # Police pour le texte d'information

    while True:  # Boucle principale de la démonstration
        ecran.fill(NOIR)  # Efface l'écran avec du noir

        # Récupère l'action renvoyée par gestionnaire_evenements
        evenement_boutons, _ = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur le bouton menu
            return  # On retourne au menu
        if evenement_boutons == "info":  # Si l'utilisateur clique sur le bouton d'information
            if not information_archimede():  # On ré-affiche la page d'info et on vérifie le retour au menu
                return

        # Gestion du clic gauche prolongé pour déplacer le curseur le long de la barre
        if pygame.mouse.get_pressed()[0]:  # Vérifie si le bouton gauche de la souris est enfoncé
            position_souris_x, _ = pygame.mouse.get_pos()  # Récupère uniquement la coordonnée X de la souris
            if position_x_barre <= position_souris_x <= position_x_barre + largeur_barre + 5:
                # On limite la position du curseur pour qu'il ne sorte pas de la barre
                position_curseur = position_souris_x

        # On calcule la proportion de déplacement sur la barre (entre 0 et 1)
        position_relative = (position_curseur - position_x_barre) / largeur_barre

        # Pour la première moitié de la barre, on fait varier nombre_cotes de 3 à 30, de façon linéaire.
        # Pour la seconde moitié, on passe à une échelle beaucoup plus rapide (exposant 2.5) pour atteindre 50 000.

        if position_relative <= 0.5:
            nombre_cotes = int(3 + (30 - 3) * (position_relative / 0.5))
        else:
            progression_acceleration = (position_relative - 0.5) / 0.5
            facteur_acceleration = 2.5
            nombre_cotes = int(30 + (nombre_cotes_max - 30) * (progression_acceleration ** facteur_acceleration))

        # On s'assure que le nombre de subdivisions ne dépasse pas les bornes.
        nombre_cotes = min(nombre_cotes_max, max(nombre_cotes_min, nombre_cotes))

        # Calcul des périmètres inscrit et circonscrit (formules Archimède)
        perimetre_inscrit = nombre_cotes * math.sin(math.pi / nombre_cotes)  # n × sin(π/n)
        perimetre_circonscrit = nombre_cotes * math.tan(math.pi / nombre_cotes)  # n × tan(π/n)
        pi_estime = (perimetre_inscrit + perimetre_circonscrit) / 2  # Moyenne des deux périmètres => approximation de π

        # Dessine le cercle en blanc
        pygame.draw.circle(ecran, BLANC, centre_cercle, rayon, 2)

        points_inscrits = []  # Liste des sommets du polygone inscrit
        points_circonscrits = []  # Liste des sommets du polygone circonscrit

        # On calcule pour chaque côté la position (x, y) des sommets, en fonction de l'angle
        for i in range(nombre_cotes):
            angle = (2 * math.pi * i) / nombre_cotes  # Angle pour le sommet i
            # Polygone inscrit (rayon constant)
            position_x_inscrit = int(centre_cercle[0] + rayon * math.sin(angle))
            position_y_inscrit = int(centre_cercle[1] - rayon * math.cos(angle))
            points_inscrits.append((position_x_inscrit, position_y_inscrit)) # On ajoute ces positions à la liste correspondante

            # Polygone circonscrit (rayon divisé par cos(π/n))
            position_x_circonscrit = int(centre_cercle[0] + (rayon / math.cos(math.pi / nombre_cotes)) * math.sin(angle))
            position_y_circonscrit = int(centre_cercle[1] - (rayon / math.cos(math.pi / nombre_cotes)) * math.cos(angle))
            points_circonscrits.append((position_x_circonscrit, position_y_circonscrit)) # On ajoute ces positions à la liste correspondante

        # Dessine le polygone inscrit en rouge (épaisseur 2) et circonscrit en vert (épaisseur 2)
        pygame.draw.polygon(ecran, (255, 0, 0), points_inscrits, 2)
        pygame.draw.polygon(ecran, (0, 255, 0), points_circonscrits, 2)

        # Création et affichage des surfaces de texte
        texte_nombre_cotes = police_texte.render(f"Nombres de côtés: {nombre_cotes}", True, BLANC)
        texte_pi = police_texte.render(f"Estimation de π: {pi_estime:.8f}", True, BLANC)

        # Placement des informations (nombre de côtés, estimation de pi)
        ecran.blit(texte_nombre_cotes, (50, hauteur_ecran // 10))
        ecran.blit(texte_pi, (50, hauteur_ecran // 6))

        # Dessine la barre grise de réglage et le curseur (petit cercle blanc)
        pygame.draw.rect(ecran, (150, 150, 150), (position_x_barre, position_y_barre, largeur_barre, 5))
        pygame.draw.circle(ecran, BLANC, (position_curseur, position_y_barre + 2), 10)

        # Bouton info, bouton menu, croix de fermeture
        bouton_informations()
        bouton_menu()
        croix_fermer()

        # Met à jour l'affichage
        pygame.display.update()
