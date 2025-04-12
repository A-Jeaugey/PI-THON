#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Importation de pygame pour la gestion des graphismes et des événements
import pygame_textinput  # Importation de pygame_textinput pour gérer la saisie de texte pygame
from affichage import ecran, POLICE, BLANC, NOIR, ROUGE, GRIS, BLEU, croix_fermer, bouton_menu, bouton_informations, ecran_information  # Importation des objets et constantes d'affichage
from utils import gestionnaire_evenements, afficher_texte_dynamique, souligner_texte  # Importation des fonctions utilitaires

def information_collisions():
    """
    Affiche un écran d'information pour la méthode des collisions élastiques
    
    Paramètres :
        Aucun
        
    Retourne :
        True si l'utilisateur clique pour commencer, False s'il choisit de revenir en arrière.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la largeur et la hauteur de l'écran
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Initialise la police pour le titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 50 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 40)  # Initialise la police pour le texte descriptif

    texte_titre = "Méthode des collisions élastiques"  # Texte du titre

    texte_description = (  # Texte descriptif expliquant la méthode des collisions élastiques
        "La méthode des collisions élastiques est une approche expérimentale pour estimer π. "
        "Elle repose sur la physique des collisions élastiques entre deux blocs, où l’un est "
        "beaucoup plus massif que l’autre. Si la masse du second bloc est 100^n fois plus grande que "
        "le premier, en comptant le nombre total de collisions, on peut obtenir n décimales de π. "
        "Ce concept a été introduit par Gregory Galperin et Leonid A. Bunimovich dans les années 1990. "
    )

    texte_formule = (  # Texte contenant la formule physique sous forme de liste de chaînes
        "Les collisions suivent deux lois fondamentales de la physique :",
        "1) Conservation de l’énergie :",
        "1/2 * m1 * v1^2 + 1/2 * m2 * v2^2 = constante",
        "2) Conservation de la quantité de mouvement :",
        "m1 * v1 + m2 * v2 = constante"
    )

    texte_visualisation = (  # Texte décrivant la visualisation dans la simulation
        "Visualisation :",
        "• Dans la simulation, deux blocs (un noir et un rouge) entrent en collision et rebondissent.",
        "• Le compteur de collisions augmente à chaque contact.",
        "• Le nombre total de collisions fournit une estimation directe de π.",
        "• Une barre de progression indique le pourcentage de collisions par rapport à l’estimation finale.",
        "• L'entrée utilisateur permet de modifier la puissance de la masse du bloc rouge. (0 à 6 pour éviter la surcharge)"
    )

    while True:
        ecran.fill(NOIR)  # Remplit l'écran de noir

        # Affichage du titre
        titre_rendu = police_titre.render(texte_titre, True, BLANC)  # Rend le texte du titre en blanc
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))  # Affiche le titre centré horizontalement
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre

        # Affichage des descriptions
        y_position = hauteur_ecran // 6  # Position de départ pour le texte
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 20, y_position, 15, largeur_ecran * 0.9, police_texte) + 10  # Affiche la description
        y_position += 10 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 50 # Ajoute un espace en fonction de si on est en plein écran ou non
        for i, ligne in enumerate(texte_formule):  # Pour chaque ligne de la formule
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 20, y_position, 15, largeur_ecran * 0.9, police_texte, BLEU, souligner=True if i == 0 or i == 1 or i == 3 else False) + hauteur_ecran // 50  # Affiche la ligne en bleu
        y_position += 0  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 50 # Ajoute un espace en fonction de si on est en plein écran ou non
        for ligne in texte_visualisation:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 20, y_position, 15, largeur_ecran * 0.9, police_texte, souligner=True if ligne == "Visualisation :" else False)  + hauteur_ecran // 50 # Affiche le texte de visualisation

        # Instruction pour commencer
        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer.", True, ROUGE)  # Rend l'instruction en rouge
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))  # Affiche l'instruction centrée en bas

        bouton_menu()  # Affiche le bouton menu
        croix_fermer()  # Affiche la croix de fermeture
        pygame.display.update()  # Met à jour l'affichage

        # Gestion des événements
        evenement_boutons, _ = gestionnaire_evenements()  # Récupère les événements
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur menu
            return False  # Retourne au menu
        if evenement_boutons == "clic":  # Si l'utilisateur clique sur l'écran
            return True  # Retourne True pour continuer

def collisions():
    """
    Fonction principale pour simuler les collisions élastiques entre deux blocs afin d'estimer π.
    
    Paramètres :
        Aucun
        
    Retourne :
        Rien. La fonction gère l'affichage de la simulation et met à jour les compteurs et l'estimation de π.
    """
    if not information_collisions():  # Affiche l'écran d'information et retourne au menu si il clique sur le bouton menu dans information_collisions
        return
    
    # Récupère les dimensions de la fenêtre d'affichage
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()
    # Initialise la police pour le texte des informations affichées pendant la simulation
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 20)
    
    compteur = 0  # Compteur du nombre total de collisions
    x1, x2 = 200, 400  # Positions initiales des deux blocs
    vitesse_1 = 0  # Vitesse initiale du bloc 1
    vitesse_2 = -1  # Vitesse initiale du bloc 2
    puissance_masse = 1  # Puissance de masse initiale
    derniere_entree_masse = puissance_masse  # Stocke la dernière valeur entrée de puissance de masse
    masse_1, masse_2 = 1, 100**puissance_masse  # Masse des deux blocs, le second étant beaucoup plus massif
    taille_cube = (puissance_masse * 700) ** 0.65 + 50  # Calcul de la taille du bloc en fonction de la puissance de masse
    textinput = pygame_textinput.TextInputVisualizer(font_color=NOIR, cursor_color=NOIR)  # Initialise la zone de saisie pour modifier la puissance de masse
    explosion_actuelle = 0  # Variable de contrôle pour l'animation d'explosion lors d'une collision
    position_explosion = (0, 0)  # Position de l'explosion
    collisions_rapides = 0  # Compteur pour les collisions rapides (pour l'animation)

    # Dictionnaire associant la puissance de masse à une estimation du nombre de collisions pour la barre de progression uniquement
    COLLISIONS_ESTIMATION = {
        0: 3,
        1: 31,
        2: 314,
        3: 3141,
        4: 31415,
        5: 314159,
        6: 3141592
    }

    if puissance_masse in COLLISIONS_ESTIMATION:
        nombre_collisions_estimation = COLLISIONS_ESTIMATION[puissance_masse]  # Utilise l'estimation correspondante
    else:
        nombre_collisions_estimation = COLLISIONS_ESTIMATION[6]  # Par défaut, utilise la valeur pour 6

    while True: # Boucle principale
        evenement_boutons, evenements = gestionnaire_evenements()  # Récupère les événements utilisateur
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur menu
            return # Retour au menu
        if evenement_boutons == "info":  # Si l'utilisateur clique sur le bouton d'information
            if not information_collisions():  # Réaffiche l'écran d'information
                return # Retourne au menu si il clique sur le bouton menu dans la fonction d'information
        for evenement in evenements:
            # Si la touche Entrée est pressée
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:
                if textinput.value.isdigit(): # Si l'entrée est un nombre uniquement
                    puissance_masse = min(6, int(textinput.value))  # Met à jour la puissance de masse, maximum 6
                    nombre_collisions_estimation = COLLISIONS_ESTIMATION[puissance_masse]  # Met à jour l'estimation correspondante
                textinput.value = ""  # Réinitialise la zone de saisie

        textinput.update(evenements)  # Met à jour la zone de saisie avec les événements
        if len(textinput.value) > 1:  # Limite la saisie à 1 caractère
            textinput.value = textinput.value[:1]

        x1 += vitesse_1  # Met à jour la position du bloc 1 selon sa vitesse
        x2 += vitesse_2  # Met à jour la position du bloc 2 selon sa vitesse

        if x1 < 20:  # Si le bloc 1 atteint la limite gauche de l'écran
            vitesse_1 *= -1  # Inverse la vitesse du bloc 1
            compteur += 1  # Incrémente le compteur de collisions

        # Si les blocs sont suffisamment proches ou se sont croisés
        if (x1 - x2) ** 2 <= 50 ** 2 or x2 < x1:
            # Calcul des nouvelles vitesses après collision selon la conservation de l'énergie et de la quantité de mouvement
            vitesse_1, vitesse_2 = ((masse_1 - masse_2) * vitesse_1 + 2 * masse_2 * vitesse_2) / (masse_1 + masse_2), ((masse_2 - masse_1) * vitesse_2 + 2 * masse_1 * vitesse_1) / (masse_1 + masse_2)
            compteur += 1  # Incrémente le compteur de collisions
            
            collisions_rapides += 1  # Incrémente le compteur de collisions rapides

            if explosion_actuelle == 0:  # Si aucune explosion n'est en cours
                position_explosion = ((x1 + x2) // 2, 620)  # Détermine la position de l'explosion entre les deux blocs

            explosion_actuelle = 10  # Initialise l'animation d'explosion
            if collisions_rapides > 5:
                collisions_rapides = 5   # Limite le nombre de collisions rapides

        progression = (compteur / nombre_collisions_estimation) * 100  # Calcule le pourcentage de progression

        ecran.fill(BLANC)  # Remplit l'écran de blanc pour actualiser l'affichage
        compteur_texte = police_texte.render(f"Collisions : {compteur}", True, NOIR)  # Prépare le texte du compteur de collisions
        affichage_puissance = police_texte.render(f"Puissance masse : {puissance_masse}", True, NOIR)  # Prépare le texte affichant la puissance de masse
        affichage_pi = police_texte.render(f"Estimation de π : {str(compteur)[0]}.{str(compteur)[1:]}", True, NOIR)  # Affiche l'estimation de π basée sur le compteur de collisions
        progression_texte = police_texte.render(f"Progression : {progression:.2f}%", True, ROUGE)  # Prépare le texte indiquant la progression en pourcentage

        largeur_barre = largeur_ecran // 4  # Définit la largeur de la barre de progression
        hauteur_barre = 20  # Définit la hauteur de la barre de progression
        # Définit la position et la taille de la barre de progression
        barre_progression = pygame.Rect(largeur_ecran // 2 - largeur_barre // 2, hauteur_ecran // 3, largeur_barre, hauteur_barre)
        # Définit la partie remplie de la barre en fonction de la progression
        barre_avancement = pygame.Rect(largeur_ecran // 2 - largeur_barre // 2, hauteur_ecran // 3, int((progression / 100) * largeur_barre), hauteur_barre)

        pygame.draw.rect(ecran, GRIS, barre_progression)  # Dessine la barre de progression vide en gris
        pygame.draw.rect(ecran, ROUGE, barre_avancement)  # Dessine la partie remplie de la barre en rouge

        # Affiche les textes centrés horizontalement
        ecran.blit(compteur_texte, (largeur_ecran // 2 - compteur_texte.get_width() // 2, hauteur_ecran // 10))
        ecran.blit(affichage_puissance, (largeur_ecran // 2 - affichage_puissance.get_width() // 2, hauteur_ecran // 6.5))
        ecran.blit(affichage_pi, (largeur_ecran // 2 - affichage_pi.get_width() // 2, hauteur_ecran // 4.8))
        ecran.blit(progression_texte, (largeur_ecran // 2 - progression_texte.get_width() // 2, hauteur_ecran // 3.8))
        ecran.blit(textinput.surface, (largeur_ecran // 2 - textinput.surface.get_width() // 2, hauteur_ecran // 2.6))
        
        # Dessine le bloc rouge (avec ajustement de la position minimale pour ne pas qu'il parte hors de l'écran dû à un bug)
        if x2 > 70:
            pygame.draw.rect(ecran, (255, 0, 0), (x2, 600 - taille_cube + 50, taille_cube, taille_cube))
        else:
            pygame.draw.rect(ecran, (255, 0, 0), (70, 600 - taille_cube + 50, taille_cube, taille_cube))
        
        # Dessine le bloc noir (avec ajustement de la position minimale  pour ne pas qu'il parte hors de l'écran dû à un bug)
        if x1 <= 20:
            pygame.draw.rect(ecran, NOIR, (20, 600, 50, 50))
        else:
            pygame.draw.rect(ecran, NOIR, (x1, 600, 50, 50))

        # Réinitialise la simulation si la puissance de masse a changé
        if derniere_entree_masse != puissance_masse:
            derniere_entree_masse = puissance_masse
            ecran.fill(BLANC) # Nettoie l'écran
            compteur = 0
            x1, x2 = 200, 400
            vitesse_1 = 0
            vitesse_2 = -1
            masse_1, masse_2 = 1, 100 ** puissance_masse
            taille_cube = (puissance_masse * 700) ** 0.65 + 50
            nombre_collisions_estimation = COLLISIONS_ESTIMATION[puissance_masse]

        # Délai en fonction de la puissance de masse pour ajuster la simulation (pour l'expérience utilisateur)
        if puissance_masse == 0 or puissance_masse == 1:
            pygame.time.delay(4)
        elif puissance_masse == 2 or puissance_masse == 3:
            pygame.time.delay(2)
        else:
            pygame.time.delay(0)
    
        # Gestion de l'animation d'explosion lors d'une collision
        if explosion_actuelle > 0:  # Vérifie si une explosion est en cours (contrôle d'état de l'animation)
            taille_base = (10 - explosion_actuelle) * 5  # Calcule la taille de base de l'explosion en diminuant progressivement (plus explosion_actuelle diminue, plus la taille augmente)
            rayon_explosion = taille_base + collisions_rapides * 3  # Détermine le rayon final de l'explosion en ajoutant un facteur lié aux collisions rapides
            couleur_explosion = (255, 100, 0, explosion_actuelle * 25)  # Définit la couleur de l'explosion (orange) avec une opacité dépendant de explosion_actuelle

            surface_explosion = pygame.Surface((rayon_explosion * 2, rayon_explosion * 2), pygame.SRCALPHA)  # Crée une surface transparente de taille suffisante pour contenir l'explosion
            pygame.draw.circle(surface_explosion, couleur_explosion, (rayon_explosion, rayon_explosion), rayon_explosion)  # Dessine un cercle sur la surface pour représenter l'explosion

            ecran.blit(surface_explosion, (position_explosion[0] - rayon_explosion, position_explosion[1] - rayon_explosion))  # Affiche l'explosion sur l'écran en centrant la surface sur la position d'explosion

            explosion_actuelle -= 1  # Décrémente explosion_actuelle pour animer progressivement la disparition de l'explosion


        bouton_informations()  # Affiche le bouton d'information
        bouton_menu()  # Affiche le bouton menu
        croix_fermer()  # Affiche la croix de fermeture
        pygame.display.update()  # Actualise l'affichage
