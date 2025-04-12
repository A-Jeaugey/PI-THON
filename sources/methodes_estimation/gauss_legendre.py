#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Importe la bibliothèque Pygame pour la fenêtre, l'affichage et les événements.
import pygame_textinput  # Permet d'avoir un champ de texte interactif dans Pygame.
import gmpy2  # Bibliothèque offrant une haute précision de calcul.
from gmpy2 import mpfr, sqrt  # mpfr pour la précision, sqrt pour la racine carrée.
from affichage import ecran, POLICE, BLANC, NOIR, GRIS, ROUGE, BLEU, bouton_menu, croix_fermer, bouton_informations, ecran_information  # Import de l'écran, d'une police, de couleurs et de fonctions d'affichage.
from utils import temps_ecoule, gestionnaire_evenements, verifier_estimation_pi, afficher_texte_dynamique, afficher_resultat, souligner_texte  # Fonctions utilitaires (temps, événements, vérification, etc.).

def temps_estime_gauss_legendre(nombre_decimales, format=True):
    """
    Estime le temps de calcul pour la méthode Gauss-Legendre (Brent-Salamin) via une formule empirique.
    
    Paramètres:
        nombre_decimales (int): Le nombre de décimales à calculer.
        format (bool): Si True, renvoie le résultat au format 'HH:MM:SS'. Sinon, renvoie un float (secondes).
    
    Retourne:
        str ou float: Une chaîne 'HH:MM:SS' ou un nombre de secondes (float), selon 'format'.
    """
    temps_estime_calcul = 1.00e-7 * nombre_decimales**1.184  # Relation empirique pour estimer le temps de calcul
    if format:  # Si on souhaite le format HH:MM:SS.
        heures, minutes, secondes = int(max(temps_estime_calcul, 0)//3600), int((max(temps_estime_calcul, 0)%3600)//60), int(max(temps_estime_calcul, 0)%60)
        return f"{heures:02}:{minutes:02}:{secondes:02}"  # Retourne la chaîne formatée.
    else:  # Sinon, on renvoie un float en secondes.
        return temps_estime_calcul

def information_gauss_legendre():
    """
    Affiche un écran d'informations sur la méthode Gauss-Legendre (Brent-Salamin).
    Attend un clic pour poursuivre, ou un clic sur "menu" pour annuler.
    
    Paramètres:
        Aucun.
    
    Retourne:
        bool:
        - True si l'utilisateur clique dans la fenêtre (commencer),
        - False s'il clique sur le bouton menu.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la taille de la fenêtre.
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police pour le titre.
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 42)  # Police pour le texte explicatif.
    texte_titre = "Gauss-Legendre / Brent-Salamin"  # Titre de la méthode.
    texte_description = (  # Explication sur la méthode.
        "La méthode de Gauss-Legendre, également appelée formule de Brent-Salamin, est un algorithme itératif permettant de calculer "
        "les décimales de π avec une grande précision. Développée à partir des travaux de Carl Friedrich Gauss et Adrien-Marie Legendre,  "
        "elle repose sur l'utilisation des moyennes arithmétique et géométrique pour raffiner progressivement la valeur de π."
        "Cette méthode est particulièrement utilisée pour les calculs nécessitant une très haute précision, notamment dans les records "
        "de décimales de π et les tests de performance des systèmes informatiques."
    )
    texte_formule = (  # Formules mathématiques de l'algorithme Gauss-Legendre.
        "Formules de l'algorithme Gauss-Legendre : ",
        "a_n+1 = (a_n + b_n) / 2 ",
        "b_n+1 = sqrt(a_n * b_n) ",
        "t_n+1 = t_n - p_n * (a_n - a_n+1)^2 ",
        "p_n+1 = 2 * p_n ",
        "π ≈ (a_n + b_n)^2 / (4 * t_n)"
    )
    while True:  # Boucle d'affichage jusqu'à un clic ou "menu".
        ecran.fill(NOIR)  # Efface l'écran en noir.
        titre_rendu = police_titre.render(texte_titre, True, BLANC)  # Surface texte pour le titre.
        ecran.blit(titre_rendu, (largeur_ecran//2 - titre_rendu.get_width() // 2, hauteur_ecran // 20))  # Place le titre en haut.
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 20) # Souligne le titre

        y_position = hauteur_ecran // 5  # Position de départ en hauteur pour le texte.

        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran//10, y_position, 15, largeur_ecran*0.8, police_texte)  # Affiche la description.
        y_position += hauteur_ecran // 50 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 10 # Ajoute un espace en fonction de si on est en plein écran ou non
        for ligne in texte_formule:  # On affiche chaque ligne de la formule (en revenant à la ligne).
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran//10, y_position+40, 15, largeur_ecran*0.8, police_texte, BLEU, souligner=True if ligne == "Formules de l'algorithme Gauss-Legendre : " else False) + 15

        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer", True, ROUGE)  # Texte invitant l'utilisateur à continuer
        ecran.blit(instruction_rendu, (largeur_ecran//2 - instruction_rendu.get_width()//2, hauteur_ecran*0.92))  # Place en bas.

        bouton_menu()  # Dessine le bouton menu.
        croix_fermer()  # Dessine la croix de fermeture.
        pygame.display.update()  # Met à jour l'affichage.
        
        evenement_boutons, _ = gestionnaire_evenements()  # Récupère les événements
        if evenement_boutons == "menu":  # Si on clique sur "menu".
            return False  # On retourne au menu
        if evenement_boutons == "clic":  # Si on clique dans la fenêtre.
            return True  # On passe à l'étape suivante.

def gauss_legendre():
    """
    Lance le calcul de π via la méthode Gauss-Legendre et affiche le résultat final.
    
    Paramètres:
        Aucun.
    
    Retourne:
        Rien. Quitte la fonction lorsque l'utilisateur revient de l'écran de résultats ou clique sur "menu".
    """
    if not information_gauss_legendre():  # Affiche l'écran d'info
        return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu
    
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Dimensions de la fenêtre.
    textinput = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)  # Champ de saisie.
    nombre_decimales = None  # Stockera le nombre de décimales saisies.
    nombre_decimales_actuelles = 0  # Mis à jour pour estimer le temps en direct.
    temps_estime_affiche = "Temps estimé : -"  # Texte d'affichage du temps estimé.
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police pour le titre.
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 25)  # Police pour le texte.

    while nombre_decimales is None:  # Boucle de saisie pour le nombre de décimales.
        ecran.fill(NOIR)  # Nettoie l'écran.
        titre = police_titre.render("Méthode de Gauss-Legendre", True, BLANC)  # Surface texte pour le titre.
        explication = police_texte.render("Entrez le nombre de décimales à calculer (300 millions max) :", True, BLANC)  # Texte explicatif.
        temps_affiche = police_texte.render(temps_estime_affiche, True, BLANC)  # Texte affichant le temps estimé.
        note = "Note : le temps de calcul réel peut possiblement varier en fonction de la puissance de votre machine." # Texte sur l'imprécision de l'estimation
        avertissement = "Le calcul ne sera pas vérifié car le fichier de référence contient 100 millions de décimales" # Avertissement sur la limite du fichier de référence

        ecran.blit(titre, (largeur_ecran//2 - titre.get_width()//2, hauteur_ecran//15))  # Place le titre.
        souligner_texte(ecran, titre, largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 15) 
        ecran.blit(explication, (largeur_ecran//2 - explication.get_width()//2, hauteur_ecran//3))  # Place le texte d'explication.
        ecran.blit(textinput.surface, (largeur_ecran//2 - textinput.surface.get_width()//2, hauteur_ecran//2))  # Place le champ de saisie.
        ecran.blit(temps_affiche, (largeur_ecran//2 - temps_affiche.get_width()//2, hauteur_ecran//2.5))  # Place le texte du temps estimé.
        afficher_texte_dynamique(ecran, note, 0, hauteur_ecran//1.7, 15, largeur_ecran*0.99, police_texte)  # Affiche la note.
        if nombre_decimales_actuelles > 100000000:  # Si plus de 100 millions de décimales.
            afficher_texte_dynamique(ecran, avertissement, 0, hauteur_ecran//1.3, 15, largeur_ecran*0.99, police_texte, ROUGE)  # Avertissement sur la limite du fichier de référence
        bouton_informations()  # Bouton "?"
        bouton_menu()  # Bouton menu
        croix_fermer()  # Bouton fermer
        pygame.display.update()  # Mise à jour de l'écran.
        evenement_boutons, evenements = gestionnaire_evenements()  # On récupère l'action (menu, info, etc.).
        if evenement_boutons == "menu":  # Si on clique sur "menu".
            return  # On retourne au menu
        if evenement_boutons == "info":  # Si on clique sur info.
            if not information_gauss_legendre():  # On réaffiche l'info si nécessaire.
                return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu
        textinput.update(evenements)  # Mise à jour du champ de saisie.
        if textinput.value.isdigit():  # Si la saisie est un entier.
            nombre_decimales_actuelles = int(textinput.value)  # Met à jour la variable.
            temps_estime_affiche = f"Temps estimé : {temps_estime_gauss_legendre(nombre_decimales_actuelles)} sec"  # Calcule le temps estimé.
        else:
            temps_estime_affiche = "Temps estimé : -"  # Sinon, pas d'estimation.

        for evenement in evenements:  # Parcourt les événements Pygame.
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:  # Si la touche Entrée cliquée
                if textinput.value.isdigit(): # Si la saisie est un entier
                    nombre_decimales = min(300000000, int(textinput.value)) # La saisie utilisateur est attribuée au nombre de décimales
                textinput.value = ""  # Vide le champ après validation.
        if len(textinput.value) > 9:  # Limite à 10 caractères pour éviter de gros inputs.
            textinput.value = textinput.value[:9]

    ecran.fill(NOIR)  # On vide l'écran pour le calcul.
    texte_calcul = police_texte.render("Calcul en cours...", True, BLANC)  # Message de calcul.
    ecran.blit(texte_calcul, (50, 200))  # Place ce message.
    # La note suivante est affichée dû au fait que lorsqu'on est en plein calcul, la page est considérée comme ne répondant pas si on clique dessus et ainsi causer un crash.
    texte_avertissement = pygame.font.Font(POLICE, hauteur_ecran // 34).render("Avertissement : Veuillez ne pas cliquer sur l'écran pendant un long calcul !", True, BLANC)
    ecran.blit(texte_avertissement, (largeur_ecran // 2 - texte_avertissement.get_width() // 2, hauteur_ecran // 1.05))
    progression = 0.0  # Pour la barre de progression.
    # Dimensions de la barre.
    largeur_barre = largeur_ecran // 2
    hauteur_barre = 30
    position_x_barre = (largeur_ecran - largeur_barre)//2
    position_y_barre = hauteur_ecran // 2
    largeur_remplie = int(largeur_barre * progression)
    # Affiche les éléments de la barre de progression
    pygame.draw.rect(ecran, NOIR, (position_x_barre - 10, position_y_barre - 10, largeur_barre + 20, hauteur_barre + 20)) 
    pygame.draw.rect(ecran, GRIS, (position_x_barre, position_y_barre, largeur_barre, hauteur_barre))
    pygame.draw.rect(ecran, (255, 255, 50), (position_x_barre, position_y_barre, largeur_remplie, hauteur_barre))

    texte_progression = police_texte.render(f"{int(progression * 100)}%", True, BLANC) # Texte pour le pourcentage
    ecran.blit(texte_progression, (largeur_ecran//2 - texte_progression.get_width()//2, position_y_barre - hauteur_ecran // 20))
    pygame.display.update()  # Mise à jour de l'écran.

    debut_ticks = pygame.time.get_ticks()  # On note le temps de départ.
    gmpy2.get_context().precision = min(int(nombre_decimales * 3.32193) + 50, 10**9) # Ajuste la précision en bits.

    # Variables Gauss-Legendre.
    a = mpfr(1)  # a_0 = 1
    b = mpfr(1) / sqrt(mpfr(2))  # b_0 = 1 / √2
    t = mpfr(1) / 4  # t_0 = 1/4
    p = mpfr(1)  # p_0 = 1

    for i in range(30):  # 30 itérations sont en général suffisantes pour une excellente précision.
        a_suivant = (a + b) / 2  # (a_n + b_n)/2
        b_suivant = sqrt(a * b)  # √(a_n b_n)
        t -= p * (a - a_suivant)**2  # t_n+1 = t_n - p_n (a_n - a_n+1)²
        p *= 2  # p_n+1 = 2 * p_n
        a, b = a_suivant, b_suivant  # Mise à jour des variables.
        progression = (i + 1) / 30  # Calcul du pourcentage d'avancement.
        largeur_remplie = int(largeur_barre * progression)
        ecran.fill(NOIR)
        pygame.draw.rect(ecran, GRIS, (position_x_barre, position_y_barre, largeur_barre, hauteur_barre)) # Pour la barre de progression
        pygame.draw.rect(ecran, (255, 255, 50), (position_x_barre, position_y_barre, largeur_remplie, hauteur_barre))
        texte_progression = police_texte.render(f"{int(progression*100)}%", True, BLANC) # Texte pour le pourcentage
        ecran.blit(texte_progression, (largeur_ecran//2 - texte_progression.get_width()//2, position_y_barre - hauteur_ecran // 20))
        texte_calcul = police_texte.render("Calcul en cours...", True, BLANC) # Réaffiche le message de calcul.
        ecran.blit(texte_avertissement, (largeur_ecran // 2 - texte_avertissement.get_width() // 2, hauteur_ecran // 1.05)) # Réaffiche l'avertissement
        ecran.blit(texte_calcul, (50, 200))

        pygame.display.update() # On met à jour l'affichage

    estimation_pi = (a + b)**2 / (4*t)  # Formule finale : π = (a_n + b_n)² / (4 t_n).

    temps_total = temps_ecoule(debut_ticks)  # Temps écoulé formaté.

    estimation_pi_str = str(estimation_pi)[:nombre_decimales + 2]  # Tronque la chaîne pour conserver la partie nécessaire.

    message_verification = verifier_estimation_pi(estimation_pi_str, nombre_decimales)  # Vérifie l'estimation de π.
    
    afficher_resultat(estimation_pi_str, temps_total, "Gauss-Legendre", message_verification, nombre_decimales, information_gauss_legendre)  # Affiche le résultat.
