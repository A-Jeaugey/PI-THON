#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Import de la bibliothèque pygame (interface graphique)
import pygame_textinput  # Permet la saisie de texte sous pygame
import gmpy2  # Permet la gestion de la précision arbitraire et des opérations avancées
from gmpy2 import mpfr  # mpfr pour manipuler des flottants en haute précision
from affichage import ecran, POLICE, BLANC, NOIR, GRIS, ROUGE, BLEU, bouton_menu, croix_fermer, bouton_informations, ecran_information  # Objets/constantes pour l'affichage
from utils import temps_ecoule, gestionnaire_evenements, verifier_estimation_pi, afficher_texte_dynamique, afficher_resultat, souligner_texte  # Fonctions utilitaires

def temps_estime_chudnovsky(nombre_decimales, format=True):
    """
    Fonction pour estimer la durée de calcul de Chudnovsky
    parametres:
        nombre_decimales: Nombre de décimales à calculer pour pi.
        format: Booléen qui indique si on retourne une chaîne HH:MM:SS (True) ou un nombre brut en secondes (False).
    retourne:
        Une chaîne de caractères ou un float représentant le temps estimé de calcul.
    """
    temps_estime_calcul = 6.51e-11 * nombre_decimales**2.26  # Évaluation empirique du temps en secondes
    if format:  # Si on souhaite formater le temps en HH:MM:SS
        heures = int(max(temps_estime_calcul, 0) // 3600)  # Calcule le nombre d'heures entières
        minutes = int((max(temps_estime_calcul, 0) % 3600) // 60)  # Calcule les minutes entières restantes
        secondes = int(max(temps_estime_calcul, 0) % 60)  # Calcule le reste en secondes entières
        return f"{heures:02}:{minutes:02}:{secondes:02}"  # Retourne la chaîne de caractères formatée
    else:
        return temps_estime_calcul  # Retourne la valeur numérique brute en secondes

def information_chudnovsky():
    """
    Gère l'affichage des informations sur la méthode de Chudnovsky
    parametres:
        Aucun
    retourne:
        True si l'utilisateur clique pour continuer, False s'il clique sur le bouton menu.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la taille actuelle de la fenêtre
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police pour le titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 33)  # Police pour le texte courant

    texte_titre = "Méthode de Chudnovsky"  # Titre
    # Description générale de la méthode
    texte_description = (
        "La formule de Chudnovsky, développée en 1987 par David et Gregory Chudnovsky, "
        "est une variante améliorée des formules de Ramanujan pour le calcul de π. "
        "Elle repose sur une série mathématique extrêmement rapide et permet d'ajouter "
        "14 nouvelles décimales à chaque itération. "
        "Cette méthode est principalement utilisée pour les records de décimales de π "
        "et les calculs haute précision. Sa complexité temporelle est de O(n (log n)³), "
        "ce qui la rend très efficace sur les grands nombres avec des optimisations "
        "comme la transformée de Fourier rapide (FFT)."
    )
    # Formule mathématique illustrant la méthode
    texte_formule = (
        "La formule de Chudnovsky est donnée par :",
        "1/π ≈ 12 * ∑ [(-1)^k (6k)! (13591409 + 545140134k)] / [(3k)! (k!)^3 (640320)^(3k + 3/2)]"
    )

    while True:  # Boucle d'affichage
        ecran.fill(NOIR)  # Remplit l'écran en noir
        titre_rendu = police_titre.render(texte_titre, True, BLANC)  # Prépare le titre
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))  # Centre le titre
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre

        y_position = hauteur_ecran // 5  # Position de départ pour le texte
        # Affiche la description avec retours à la ligne automatiques
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 10, y_position, 15, largeur_ecran * 0.8, police_texte)

        y_position += 0  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 10 # Ajoute un espace en fonction de si on est en plein écran ou non

        # Affiche chaque ligne de la formule, en bleu, avec des marges supplémentaires
        for ligne in texte_formule:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position + 50, 15, largeur_ecran * 0.8, police_texte, BLEU, souligner=True if ligne == "La formule de Chudnovsky est donnée par :" else False) + hauteur_ecran // 30

        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer", True, ROUGE)  # Message pour commencer
        # Place ce message au bas de l'écran
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))

        bouton_menu()  # Bouton menu
        croix_fermer()  # Bouton de fermeture
        pygame.display.update()  # Actualise l'affichage

        evenement_boutons, _ = gestionnaire_evenements()  # Récupère les actions de l'utilisateur
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur le bouton menu
            return False  # On sort en retournant False
        if evenement_boutons == "clic":  # Si clic n'importe où dans la fenêtre
            return True  # On sort en retournant True (poursuite)

def chudnovsky():
    """
    Lance la procédure de calcul de π via la méthode de Chudnovsky
    parametres:
        Aucun
    retourne:
        Rien. Gère l'affichage, le calcul de pi et l'affichage du résultat final.
    """
    if not information_chudnovsky():  # Affiche l'écran d'information, si on clique sur menu, on arrête
        return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu

    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Mesure les dimensions de la fenêtre
    saisie_texte = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)  # Zone de saisie pour le nombre de décimales
    nombre_decimales = None  # Variable qui stockera le nombre de décimales voulu
    nombre_decimales_actuelles = 0  # Variable pour la saisie en cours
    temps_estime_affiche = "Temps estimé : -"  # Message par défaut pour le temps estimé

    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police pour le titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 25)  # Police pour le texte standard

    while nombre_decimales is None:  # Tant qu'on n'a pas entré un entier valide
        ecran.fill(NOIR)  # Nettoie l'écran avec un fond noir

        # Prépare les différents textes
        titre = police_titre.render("Méthode de Chudnovsky", True, BLANC)
        explication = police_texte.render("Entrez le nombre de décimales à calculer :", True, BLANC)
        temps_affiche = police_texte.render(temps_estime_affiche, True, BLANC)
        note = "Note : le temps de calcul réel peut varier en fonction de la puissance de votre machine sur cette méthode"

        # Positionne ces textes sur l'écran
        ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 20))
        souligner_texte(ecran, titre, largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 20) 
        ecran.blit(explication, (largeur_ecran // 2 - explication.get_width() // 2, hauteur_ecran // 3))
        ecran.blit(saisie_texte.surface, (largeur_ecran // 2 - saisie_texte.surface.get_width() // 2, hauteur_ecran // 2))
        ecran.blit(temps_affiche, (largeur_ecran // 2 - temps_affiche.get_width() // 2, hauteur_ecran // 2.5))
        afficher_texte_dynamique(ecran, note, 0, hauteur_ecran // 1.7, 15, largeur_ecran * 0.99, police_texte)

        bouton_menu()  # Bouton menu
        croix_fermer()  # Bouton pour fermer
        bouton_informations()  # Bouton d'informations
        pygame.display.update()  # Met à jour l'écran pour afficher tout ça

        evenement_boutons, evenements = gestionnaire_evenements()  # Analyse les événements
        if evenement_boutons == "menu":  # Si clic sur le bouton menu
            return # on retourne au menu
        if evenement_boutons == "info":  # Si clic sur le bouton d'information
            if not information_chudnovsky():  # Ouvre la fenêtre d'info Chudnovsky
                return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu

        saisie_texte.update(evenements)  # Met à jour la saisie avec les événements actuels
        if len(saisie_texte.value) > 7:  # On limite à 7 caractères pour éviter les calculs excessifs
            saisie_texte.value = saisie_texte.value[:7]  # Tronque si dépassement

        # Si la saisie est un nombre entier
        if saisie_texte.value.isdigit(): # Vérifie que c'est bien un nombre
            nombre_decimales_actuelles = int(saisie_texte.value) # La saisie utilisateur est enregistrée ici pour l'utiliser dans l'estimation de temps
            temps_estime_affiche = f"Temps estimé : {temps_estime_chudnovsky(nombre_decimales_actuelles)} sec" # Prépare l'affichage du temps estimé
        else:
            temps_estime_affiche = "Temps estimé : -" # Si aucun nombre n'est entré, on laisse le texte par défaut.

        for evenement in evenements: # parcours les événements
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN: # Détecte si on a appuyé sur la touche Entrée
                if saisie_texte.value.isdigit():  # Vérifie que c'est bien un nombre
                    nombre_decimales = int(saisie_texte.value)  # On valide le nombre de décimales
                saisie_texte.value = ""  # Réinitialise la zone de saisie

    ecran.fill(NOIR)  # Nettoie l'écran
    texte_calcul = police_texte.render("Calcul en cours...", True, BLANC)  # Message pour indiquer que ça calcule
    ecran.blit(texte_calcul, (50, 200))  # Place ce message
    # La note suivante est affichée dû au fait que lorsqu'on est en plein calcul, la page est considérée comme ne répondant pas si on clique dessus et ainsi causer un crash.
    texte_avertissement = pygame.font.Font(POLICE, hauteur_ecran // 34).render("Avertissement : Veuillez ne pas cliquer sur l'écran pendant un long calcul !", True, BLANC)
    ecran.blit(texte_avertissement, (largeur_ecran // 2 - texte_avertissement.get_width() // 2, hauteur_ecran // 1.05))
    progression = 0.0  # La progression initiale est de 0%

    # Paramètres de la barre de progression
    largeur_barre = largeur_ecran // 2
    hauteur_barre = 30
    position_x_barre = (largeur_ecran - largeur_barre) // 2
    position_y_barre = hauteur_ecran // 2
    largeur_remplie = int(largeur_barre * progression)

    # Dessin de la barre de progression
    pygame.draw.rect(ecran, NOIR, (position_x_barre - 10, position_y_barre - 10, largeur_barre + 20, hauteur_barre + 20))
    pygame.draw.rect(ecran, GRIS, (position_x_barre, position_y_barre, largeur_barre, hauteur_barre))
    pygame.draw.rect(ecran, (255, 255, 50), (position_x_barre, position_y_barre, largeur_remplie, hauteur_barre))
    texte_progression = police_texte.render(f"{int(progression * 100)}%", True, BLANC) # Affichage du pourcentage
    ecran.blit(texte_progression, (largeur_ecran // 2 - texte_progression.get_width() // 2, position_y_barre - hauteur_ecran // 20))
    croix_fermer()  # Affiche la croix de fermeture
    bouton_menu()  # Affiche le bouton menu
    pygame.display.update() # Mets à jour l'affichage

    debut_temps = pygame.time.get_ticks()  # Note l'heure de départ
    # Règle la précision nécessaire dans gmpy2
    gmpy2.get_context().precision = int(nombre_decimales * 3.32193) + 50

    facteur_chudnovsky = 12 / (mpfr(640320) ** mpfr(1.5))  # Facteur constant 12 / (640320^(3/2))
    somme_chudnovsky = mpfr(0)  # Somme accumulative
    # On estime le nombre d'itérations en tenant compte du fait qu'une itération ajoute ~14 décimales
    nombre_iterations = max(6, (nombre_decimales + 13) // 14)
    facteur_numerateur = mpfr(1)  # Facteur cumulatif au numérateur
    facteur_denominateur = mpfr(1)  # Facteur cumulatif au dénominateur

    # Boucle de calcul principale
    for index in range(nombre_iterations):
        if index > 0:  # À partir du second tour, on met à jour les facteurs multiplicatifs
            # Met à jour le facteur_numerateur selon la progression du terme (6k)! etc.
            facteur_numerateur *= (6 * index - 5) * (2 * index - 1) * (6 * index - 1)
            # Met à jour facteur_denominateur avec des puissances de 640320 et index^3
            facteur_denominateur *= (index**3) * (640320**3 // 24)

        # Calcule le terme de la série (-1)^k * (6k)! * (13591409+545140134k) / ...
        terme_chudnovsky = (mpfr((-1) ** index) * facteur_numerateur * (13591409 + 545140134 * index)) / facteur_denominateur
        
        somme_chudnovsky += terme_chudnovsky  # Ajoute le terme dans la somme

        progression = (index + 1) / nombre_iterations  # Calcule la progression en pourcentage
        largeur_remplie = int(largeur_barre * progression)  # Met à jour la partie remplie
        pygame.draw.rect(ecran, NOIR, (largeur_ecran // 2 - texte_progression.get_width() // 2 - 20, position_y_barre - 75, texte_progression.get_width() + 40, texte_progression.get_height() + 40)) # Mets à jour l'affichage au niveau du pourcentage
        
        pygame.draw.rect(ecran, GRIS, (position_x_barre, position_y_barre, largeur_barre, hauteur_barre)) # Affiche la barre grise
        pygame.draw.rect(ecran, (255, 255, 50), (position_x_barre, position_y_barre, largeur_remplie, hauteur_barre))  # Barre jaune
        texte_progression = police_texte.render(f"{int(progression * 100)}%", True, BLANC) # Affichage du pourcentage
        ecran.blit(texte_progression, (largeur_ecran // 2 - texte_progression.get_width() // 2, position_y_barre - hauteur_ecran // 20))

        evenement_boutons, _ = gestionnaire_evenements()  # Vérifie si l'utilisateur demande à revenir
        if evenement_boutons == "menu":  # Si clic sur le bouton menu
            return  # On retourne au menu
        # On rafraîchit l'affichage toutes les 100 itérations ou bien à la fin du calcul pour économiser des performances
        if index % 100 == 0 or index == nombre_iterations - 1:
            pygame.display.update()

    pi_estime = 1 / (facteur_chudnovsky * somme_chudnovsky)  # Au final, 1 / (facteur * somme) correspond à π

    temps_total = temps_ecoule(debut_temps)  # Calcule la durée totale du calcul
    estimation_pi_str = str(pi_estime)[:nombre_decimales + 2]  # Tronque la chaîne pour n'afficher que le nombre de décimales voulues (+2 = "3.")
    message_verification = verifier_estimation_pi(estimation_pi_str, nombre_decimales)  # Compare avec la référence

    # Affiche le résultat final sur l'écran
    afficher_resultat(estimation_pi_str, temps_total, "Chudnovsky", message_verification, nombre_decimales, information_chudnovsky)
