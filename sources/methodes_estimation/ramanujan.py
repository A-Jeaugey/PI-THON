#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Bibliothèque Pygame pour la gestion de la fenêtre, des événements et de l'affichage.
import pygame_textinput  # Permet de créer un champ de saisie de texte interactif dans Pygame.
import gmpy2  # Bibliothèque de calcul haute précision.
from gmpy2 import mpfr, sqrt  # Import spécifique pour la précision (mpfr), la racine carrée (sqrt) et la factorielle (fac).
from affichage import ecran, POLICE, BLANC, NOIR, GRIS, ROUGE, BLEU, bouton_menu, croix_fermer, bouton_informations, ecran_information  # Composants d'affichage et couleurs.
from utils import temps_ecoule, gestionnaire_evenements, verifier_estimation_pi, afficher_resultat, afficher_texte_dynamique, souligner_texte  # Fonctions utilitaires (temps, événements, vérification π, etc.)


def temps_estime_ramanujan(nombre_decimales, format=True):
    """
    Calcule une estimation empirique du temps de calcul pour la méthode de Ramanujan.
    
    Paramètres:
        nombre_decimales (int): Nombre de décimales à calculer.
        format (bool): Si True, on retourne une chaîne 'HH:MM:SS'. Sinon, un float en secondes.

    Retourne:
        str ou float: Le temps estimé au format HH:MM:SS (si format=True) 
                    ou directement en secondes (si format=False).
    """
    temps_estime_calcul = 3.01e-10 * nombre_decimales**2.253 # Relation empirique. Attention cela peut varier en fonction de la puissance de calcul réel de la machine.
    if format:  # Si on souhaite un format HH:MM:SS
        heures = int(max(temps_estime_calcul, 0) // 3600)  # Calcule le nombre d'heures entières.
        minutes = int((max(temps_estime_calcul, 0) % 3600) // 60)  # Calcule le nombre de minutes restantes.
        secondes = int(max(temps_estime_calcul, 0) % 60)  # Calcule le nombre de secondes restantes.
        return f"{heures:02}:{minutes:02}:{secondes:02}"  # Retourne une chaîne formatée.
    else:  # Sinon, on renvoie le nombre de secondes (float).
        return temps_estime_calcul


def information_ramanujan():
    """
    Affiche un écran d'information sur la formule de Ramanujan, 
    en boucle jusqu'au clic de l'utilisateur (ou "menu").

    Paramètres:
        Aucun.

    Retourne:
        bool:
        - True si l'utilisateur clique dans la fenêtre (pour continuer),
        - False s'il clique sur le bouton menu.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la taille de la fenêtre.
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police de grande taille pour le titre.
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 35)  # Police plus petite pour le texte explicatif.

    texte_titre = "Formule de Ramanujan"  # Titre principal.
    texte_description = (  # Paragraphe décrivant la méthode de Ramanujan.
        "La formule de Ramanujan est une méthode rapide pour calculer π. "
        "Découverte par le mathématicien indien Srinivasa Ramanujan en 1910, "
        "elle a inspiré des formules encore plus puissantes comme celle de Chudnovsky. "
        "Cette dernière a une convergence rapide (~8 décimales par itération), mais "
        "puisque la formule inclut des calculs lourds de factorielles et de puissances, "
        "elle n'est pas forcément la plus performante pour un petit nombre de décimales."
    )
    texte_formule = (  # La formule au sens strict (1/π = ...).
        "La formule de Ramanujan est :",
        "1/π ≈ (2√2 / 9801) * ∑ [ (4k)! (1103 + 26390k) ] / [ (k!)^4 396^(4k) ]"
    )

    while True:  # Boucle d'affichage, attend que l'utilisateur clique ou appuie sur "menu".
        ecran.fill(NOIR)  # Remplit l'écran de noir.
        titre_rendu = police_titre.render(texte_titre, True, BLANC)  # Crée une surface texte pour le titre.
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))  # Placement du titre, centré.
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre

        y_position = hauteur_ecran // 4.5  # Position de départ du texte.
        # Affiche la description principale en utilisant afficher_texte_dynamique.
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 10, y_position, 15, largeur_ecran * 0.8, police_texte)
        y_position += hauteur_ecran // 18  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 10 # Ajoute un espace en fonction de si on est en plein écran ou non
        # Affiche la formule Ramanujan (en BLEU)
        for ligne in texte_formule:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position + 50, 15, largeur_ecran * 0.8, police_texte, BLEU, souligner=True if ligne == "La formule de Ramanujan est :" else False) + 20

        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer", True, ROUGE)  # Invite en rouge
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))  # Centré en bas.

        bouton_menu()   # Dessine le bouton menu en haut à droite.
        croix_fermer()    # Dessine la croix de fermeture en haut à droite.
        pygame.display.update()  # Met à jour tout l'affichage.

        evenement_boutons, _ = gestionnaire_evenements()  # Récupère l'action de l'utilisateur.
        if evenement_boutons == "menu":  # S'il clique sur le bouton menu
            return False  # On retourne False => abandon.
        if evenement_boutons == "clic":    # S'il clique n'importe où
            return True   # On retourne True => continuer.


def ramanujan():
    """
    Calcule π via la formule de Ramanujan et affiche le résultat.
    L'utilisateur saisit le nombre de décimales voulu, on montre une barre de progression,
    puis on affiche l'estimation finale et une vérification.

    Paramètres:
        Aucun.

    Retourne:
        Rien (la fonction se termine après l'affichage du résultat).
    """
    if not information_ramanujan():  # On affiche l'écran d'info
        return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu

    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupération de la taille de la fenêtre.
    saisie_texte = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)  # Champ de saisie.
    nombre_decimales = None  # Contiendra la valeur saisie par l'utilisateur.
    nombre_decimales_actuelles = 0  # Pour le temps estimé, mis à jour à chaque frappe.
    temps_estime_affiche = "Temps estimé : -"  # Affiche par défaut un temps estimé non défini.

    # Polices pour le titre et le texte plus petit.
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 25)

    # Boucle de saisie pour obtenir le nombre de décimales désirées.
    while nombre_decimales is None:
        ecran.fill(NOIR)  # On efface l'écran en noir.

        # Création des surfaces texte pour le titre et les explications.
        titre = police_titre.render("Méthode de Ramanujan", True, BLANC)
        explication = police_texte.render("Entrez le nombre de décimales à calculer :", True, BLANC)
        temps_affiche = police_texte.render(temps_estime_affiche, True, BLANC)
        note = "Note : le temps de calcul réel peut possiblement varier en fonction de la puissance de votre machine."

        # Placement de ces textes à l'écran (titre, explication, champ de saisie, etc.)
        ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 20))
        souligner_texte(ecran, titre, largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 20) 
        ecran.blit(explication, (largeur_ecran // 2 - explication.get_width() // 2, hauteur_ecran // 3))
        ecran.blit(saisie_texte.surface, (largeur_ecran // 2 - saisie_texte.surface.get_width() // 2, hauteur_ecran // 2))
        ecran.blit(temps_affiche, (largeur_ecran // 2 - temps_affiche.get_width() // 2, hauteur_ecran // 2.5))
        afficher_texte_dynamique(ecran, note, 0, hauteur_ecran // 1.7, 15, largeur_ecran * 0.99, police_texte)

        bouton_informations()  # Bouton "?"
        bouton_menu()        # Bouton "menu"
        croix_fermer()         # Bouton "fermer"
        pygame.display.update()  # On met à jour l'affichage.

        # Gestion des événements.
        evenement_boutons, evenements = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur le bouton menu
            return # Retour au menu
        if evenement_boutons == "info":  # S'il clique sur le bouton info
            if not information_ramanujan():  # Réaffiche la page d'info si l'utilisateur le souhaite
                return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu

        saisie_texte.update(evenements) # Mise à jour du champ de saisie de texte.
        if len(saisie_texte.value) > 7:  # On limite la saisie à 7 caractères
            saisie_texte.value = saisie_texte.value[:7]

        # Si l'utilisateur a tapé seulement des chiffres, on met à jour l'estimation du temps.
        if saisie_texte.value.isdigit(): # Vérifie que c'est bien un nombre
            nombre_decimales_actuelles = int(saisie_texte.value) # La saisie utilisateur est enregistrée ici pour l'utiliser dans l'estimation de temps
            temps_estime_affiche = f"Temps estimé : {temps_estime_ramanujan(nombre_decimales_actuelles)} sec" # Prépare l'affichage du temps estimé
        else:
            temps_estime_affiche = "Temps estimé : -" # Si aucun nombre n'est entré, on laisse le texte par défaut.

        # On regarde si l'utilisateur valide avec la touche Entrée
        for evenement in evenements: # Parcours des événements
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN: # Touche entrée cliquée
                # Si la saisie est un nombre valide, on assigne nombre_decimales
                if saisie_texte.value.isdigit(): # Vérifie que c'est bien un nombre
                    nombre_decimales = int(saisie_texte.value) # On valide le nombre de décimales
                saisie_texte.value = ""  # On réinitialise la zone de saisie

    # Maintenant qu'on a le nombre de décimales, on lance le calcul.
    ecran.fill(NOIR)  # Efface l'écran
    texte_calcul = police_texte.render("Calcul en cours...", True, BLANC)  # Affiche un petit message
    ecran.blit(texte_calcul, (50, 200))  # Placement du texte à Gauche

    # On prépare une barre de progression
    progression = 0.0  # Pourcentage progressif
    largeur_barre = largeur_ecran // 2  # Largeur de la barre
    hauteur_barre = 30                 # Hauteur de la barre
    position_x_barre = (largeur_ecran - largeur_barre) // 2  # Centrée en X
    position_y_barre = hauteur_ecran // 2  # Placée au milieu en Y
    largeur_remplie = int(largeur_barre * progression)  # Nombre de pixels remplis (initialement 0)

    pygame.draw.rect(ecran, NOIR, (position_x_barre - 10, position_y_barre - 10, largeur_barre + 20, hauteur_barre + 20))  # Contour noir
    pygame.draw.rect(ecran, GRIS, (position_x_barre, position_y_barre, largeur_barre, hauteur_barre))  # Barre en GRIS
    pygame.draw.rect(ecran, (255, 255, 50), (position_x_barre, position_y_barre, largeur_remplie, hauteur_barre))  # Barre de remplissage en jaune
    texte_progression = police_texte.render(f"{int(progression * 100)}%", True, BLANC)  # Affiche "0%"
    ecran.blit(texte_progression, (largeur_ecran // 2 - texte_progression.get_width() // 2, position_y_barre - hauteur_ecran // 20))  # Position de pourcentage
    bouton_menu()  # On redessine le bouton menu
    croix_fermer()   # On redessine la croix
    pygame.display.update()  # On met à jour l'écran.

    debut_temps = pygame.time.get_ticks()  # On note l'heure de début de calcul
    gmpy2.get_context().precision = int(nombre_decimales * 3.32193) + 50  # Ajuste la précision en bits

    somme_ramanujan = mpfr(0)  # Somme accumulée de la série
    # On approxime le nombre d'itérations (chaque itération apporte ~8 décimales, on ajoute 100 pour être safe)
    nombre_iterations = max(3, (nombre_decimales // 7))

    # On boucle sur chaque itération pour calculer le terme de la série
    for index in range(nombre_iterations):
        # Terme : ((4k)! (1103 + 26390k)) / ((k!)^4 396^(4k))
        terme_ramanujan = (gmpy2.fac(4 * index) * (1103 + 26390 * index)) / ((gmpy2.fac(index) ** 4)* (mpfr(396) ** (4 * index))) # Utilisation de gmpy2 pour la rapidité
        somme_ramanujan += terme_ramanujan  # On ajoute le terme à la somme.

        progression = (index + 1) / nombre_iterations  # Calcul du pourcentage (entre 0 et 1)
        largeur_remplie = int(largeur_barre * progression)  # Largeur remplie proportionnelle

        pygame.draw.rect(ecran, NOIR, (largeur_ecran // 2 - texte_progression.get_width() // 2 - 20, position_y_barre - 75, texte_progression.get_width() + 40, texte_progression.get_height() + 40)) # Mets à jour l'affichage au niveau du pourcentage
        
        pygame.draw.rect(ecran, GRIS, (position_x_barre, position_y_barre, largeur_barre, hauteur_barre))  # Barre grise
        pygame.draw.rect(ecran, (255, 255, 50), (position_x_barre, position_y_barre, largeur_remplie, hauteur_barre))  # Remplissage
        texte_progression = police_texte.render(f"{int(progression * 100)}%", True, BLANC) # Texte du pourcentage
        ecran.blit(texte_progression, (largeur_ecran // 2 - texte_progression.get_width() // 2, position_y_barre - hauteur_ecran // 20))

        # On n'actualise l'écran que toutes les 50 itérations, pour éviter un trop grand ralentissement
        if index % 100 == 0 or index == nombre_iterations - 1:
            pygame.display.update()

        # On vérifie si l'utilisateur a cliqué sur "menu" pendant le calcul
        for evenement in gestionnaire_evenements():
            if evenement == "menu":
                return None  # Si c'est le cas, on abandonne le calcul

    # Formule finale : facteur = (2√2 / 9801), pi = 1 / (facteur * somme)
    facteur_ramanujan = (2 * sqrt(mpfr(2))) / 9801
    pi_estime = 1 / (facteur_ramanujan * somme_ramanujan)

    temps_total = temps_ecoule(debut_temps)  # Mesure du temps total écoulé
    estimation_pi_str = str(pi_estime)[:nombre_decimales + 2]  # Tronque la chaîne au bon nombre de décimales

    # Vérifie l'estimation par rapport au fichier de référence
    message_verification = verifier_estimation_pi(estimation_pi_str, nombre_decimales)

    # Affiche le résultat final (pages de décimales, etc.)
    afficher_resultat(estimation_pi_str, temps_total, "Ramanujan", message_verification, nombre_decimales, information_ramanujan)