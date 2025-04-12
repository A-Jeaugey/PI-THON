#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Import de la bibliothèque Pygame pour la gestion de la fenêtre, des événements et de l'affichage.
import pygame_textinput  # Permet de créer un champ de saisie de texte interactif.
import gmpy2  # Bibliothèque pour effectuer des calculs avec haute précision.
from gmpy2 import mpfr, atan  # Import spécifique de types et fonctions utiles (mpfr pour la précision, atan pour la formule Machin).
from affichage import ecran, police, POLICE, BLANC, NOIR, ROUGE, BLEU, bouton_menu, croix_fermer, bouton_informations, ecran_information   # Composants d'affichage et couleurs.
from utils import temps_ecoule, gestionnaire_evenements, verifier_estimation_pi, afficher_resultat, afficher_texte_dynamique, souligner_texte  # Utilitaires pour le temps, les événements, la vérification de pi, etc.

def temps_estime_machin(nombre_decimales):
    """
    Calcule une estimation empirique du temps nécessaire pour la méthode de Machin.
    
    Paramètres:
        nombre_decimales (int): Le nombre de décimales à calculer.
    
    Retourne:
        str: Une chaîne de caractères au format HH:MM:SS représentant le temps estimé pour le calcul.
    
    Notes:
        - La relation utilisée est strictement empirique 
        et peut varier en fonction de la machine ou du contexte.
    """
    temps_estime_calcul = 6.46e-8 * nombre_decimales**1.31  # Calcule un temps estimé basé sur le nombre de décimales
    heures, minutes, secondes = int(max(temps_estime_calcul, 0) // 3600), int((max(temps_estime_calcul, 0) % 3600) // 60), int(max(temps_estime_calcul, 0) % 60)  # Convertit en heures, minutes, secondes
    return f"{heures:02}:{minutes:02}:{secondes:02}"  # Retourne une chaîne formatée HH:MM:SS

def information_machin():
    """
    Affiche un écran d'information sur la méthode de Machin, 
    attendant que l'utilisateur clique pour continuer ou clique sur "menu".
    
    Paramètres:
        Aucun
    
    Retourne:
        bool:
        - True si l'utilisateur clique dans la fenêtre (passe à la suite),
        - False s'il clique sur le bouton menu.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la taille de la fenêtre
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police de grande taille pour le titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 32)  # Police de taille intermédiaire pour le texte

    texte_titre = "Méthode de Machin"  # Titre affiché en haut de l'écran

    # Texte détaillant la méthode Machin (histoire, principe, utilité)
    texte_description = (
        "La formule de Machin est une méthode efficace pour calculer π, "
        "découverte par John Machin en 1706. Elle repose sur l'identité "
        "de l'arctangente et permet un calcul précis en peu d'itérations. "
        "Historiquement, elle a été utilisée pour calculer 100 décimales de π "
        "à une époque où les calculs étaient entièrement manuels ! "
        "Aujourd’hui, elle reste utile pour comprendre les propriétés des séries "
        "convergentes et tester des algorithmes numériques."
    )

    # Formule mathématique de Machin
    texte_formule = (
        "La formule de Machin est : ",
        "π ≈ 16 * arctan(1/5) - 4 * arctan(1/239)"
    )

    while True:  # Boucle d'affichage de l'introduction Machin
        ecran.fill(NOIR)  # Remplissage de l'écran en noir

        # Affiche le titre en blanc, centré horizontalement
        titre_rendu = police_titre.render(texte_titre, True, BLANC)  # Surface de texte pour le titre
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))  # Placement du titre
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre

        y_position = hauteur_ecran // 5  # Point de départ vertical pour le texte explicatif
        # Affiche le paragraphe décrivant l'historique et le principe de Machin
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 10, y_position, 15, largeur_ecran * 0.8, police_texte)
        y_position += hauteur_ecran // 25  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 10 # Ajoute un espace en fonction de si on est en plein écran ou non
        # Affiche les deux lignes décrivant la formule, en bleu
        for ligne in texte_formule:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position + 50, 15, largeur_ecran * 0.8, police_texte, BLEU, souligner=True if ligne == "La formule de Machin est : " else False) + hauteur_ecran // 50

        # Invite l'utilisateur à cliquer pour continuer
        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer", True, ROUGE)  # Surface de texte
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))  # Position en bas de l'écran

        bouton_menu()  # Affiche le bouton "menu" en haut à droite
        croix_fermer()   # Affiche la croix pour fermer la fenêtre
        pygame.display.update()  # Mise à jour de l'affichage complet

        # Récupère l'action sur les boutons et la liste d'événements
        evenement_boutons, _ = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur "menu"
            return False  # On retourne au menu
        if evenement_boutons == "clic":    # Si l'utilisateur clique dans la fenêtre
            return True   # On lance la méthode

def machin():
    """
    Lance le calcul de π via la méthode de Machin.
    
    L'utilisateur saisit le nombre de décimales souhaité. Le programme effectue alors 
    un calcul haute précision à l'aide de gmpy2, puis affiche le résultat 
    et vérifie la validité de l'estimation (nombre de décimales correct).
    
    Paramètres:
        Aucun
    
    Retourne:
        Rien (lorsque l'utilisateur sort de l'écran de résultats, on revient au menu précédent).
    """
    if not information_machin():  # On affiche d'abord l'intro
        return # Retour au menu si clique en étant dans la fonction d'informations

    # Champ de texte pour récupérer le nombre de décimales
    textinput = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)
    nombre_decimales = None  # On initialise la variable (None tant que l'utilisateur n'a pas validé)
    temps_estime_affiche = "Temps estimé : -"  # Texte affichant le temps estimé, mis à jour au fur et à mesure

    # On récupère les dimensions de la fenêtre
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()

    # Polices pour le titre, et pour le texte
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 25)

    # Boucle pour demander le nombre de décimales à l'utilisateur
    while nombre_decimales is None:
        ecran.fill(NOIR)  # Efface l'écran en noir

        titre = police_titre.render("Méthode de Machin", True, BLANC) # Texte "Méthode de Machin"
        explication = police_texte.render("Entrez le nombre de décimales à calculer :", True, BLANC) # Texte d'explication
        temps_affiche = police_texte.render(temps_estime_affiche, True, BLANC)  # Texte affichant le temps estimé (mis à jour si on tape un chiffre)
        note = "Note : le temps de calcul réel peut légèrement varier en fonction de la puissance de votre machine." # Petite note

        # On place ces éléments à l'écran
        ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 20))
        souligner_texte(ecran, titre, largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 20)
        ecran.blit(explication, (largeur_ecran // 2 - explication.get_width() // 2, hauteur_ecran // 3))
        ecran.blit(textinput.surface, (largeur_ecran // 2 - textinput.surface.get_width() // 2, hauteur_ecran // 2))
        ecran.blit(temps_affiche, (largeur_ecran // 2 - temps_affiche.get_width() // 2, hauteur_ecran // 2.5))
        afficher_texte_dynamique(ecran, note, 0, hauteur_ecran // 1.7, 15, largeur_ecran * 0.99, police_texte)

        bouton_informations()  # Bouton "info"
        bouton_menu()        # Bouton "menu"
        croix_fermer()         # Bouton "fermer"
        pygame.display.update() # Mise à jour de la fenêtre

        # Récupère l'action et la liste d'événements
        evenement_boutons, evenements = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur "menu"
            return # Retour au menu
        if evenement_boutons == "info":  # S'il clique sur "info", on réaffiche l'intro
            if not information_machin():
                return # Retour au menu si clique en étant dans la fonction d'informations

        # On met à jour le champ de texte en fonction des événements
        textinput.update(evenements)
        if len(textinput.value) > 8:
            textinput.value = textinput.value[:8]  # Limite pour éviter des inputs trop longs

        # Si la saisie est un nombre, on calcule un temps estimé
        if textinput.value.isdigit():
            nombre_decimales_actuelles = int(textinput.value) # La saisie utilisateur est ici utilisée pour afficher en temps réel l'estimation de temps
            temps_estime_affiche = f"Temps estimé : {temps_estime_machin(nombre_decimales_actuelles)} sec" # On modifie le texte du temps estimé en temps réel
        else:
            temps_estime_affiche = "Temps estimé : -" # Si rien n'est entré, texte de base

        # Si l'utilisateur valide avec Entrée
        for evenement in evenements:
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:
                # Si la valeur est bien un entier
                if textinput.value.isdigit():
                    nombre_decimales = int(textinput.value) # La saisie utilisateur devient le nombre de décimales
                textinput.value = ""  # On efface la zone de texte après validation

    # Une fois le nombre de décimales saisi, on lance le calcul
    ecran.fill(NOIR)
    texte_calcul = police.render("Calcul en cours...", True, BLANC)
    ecran.blit(texte_calcul, (50, hauteur_ecran // 2.3))  # Indique visuellement que le calcul a commencé
    # La note suivante est affichée dû au fait que lorsqu'on est en plein calcul, la page est considérée comme ne répondant pas si on clique dessus et ainsi causer un crash.
    afficher_texte_dynamique(ecran, "Avertissement : Veuillez ne pas cliquer sur l'écran pendant le calcul !", 50, hauteur_ecran // 2, 15, largeur_ecran * 0.92, police_texte, BLANC, False)
    pygame.display.update() # On met à jour l'affichage

    # On note le temps de début
    debut_ticks = pygame.time.get_ticks()

    # Configuration de la précision pour gmpy2 : 
    # On prend ~ log2(10) ~ 3.32193 bits par décimale, plus une marge
    gmpy2.get_context().precision = int(nombre_decimales * 3.32193) + 50

    # On calcule d'abord arctan(1/5) et arctan(1/239)
    arctan_1_5 = atan(mpfr('1') / 5)
    arctan_1_239 = atan(mpfr('1') / 239)

    # Puis la formule : pi = 4*(4*arctan(1/5) - arctan(1/239))
    estimation_pi = 4 * (4 * arctan_1_5 - arctan_1_239)

    # Temps total écoulé
    temps_total = temps_ecoule(debut_ticks)

    # On convertit en chaîne de caractères, en gardant "nombre_decimales + 2" (pour "3.") 
    estimation_pi_str = str(estimation_pi)[:nombre_decimales + 2]

    # Vérifie l'exactitude de l'estimation en la comparant à un fichier de référence
    message_verification = verifier_estimation_pi(estimation_pi_str, nombre_decimales)

    # Affiche le résultat final (pages, texte, vérification, etc.)
    afficher_resultat(estimation_pi_str, temps_total, "Machin", message_verification, nombre_decimales, information_machin)
