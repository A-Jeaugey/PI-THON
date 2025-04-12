import pygame  # Import principal de la bibliothèque pygame
import pygame_textinput  # Permet la saisie de texte dans pygame
import gmpy2  # Gère la haute précision arithmétique
from gmpy2 import mpfr, sqrt  # mpfr et sqrt pour des floats à précision arbitraire
from affichage import ecran, POLICE, BLANC, NOIR, GRIS, ROUGE, BLEU, bouton_menu, croix_fermer, bouton_informations, ecran_information  # Objets/constantes d'affichage
from utils import temps_ecoule, gestionnaire_evenements, verifier_estimation_pi, afficher_texte_dynamique, afficher_resultat, souligner_texte  # Fonctions utilitaires

def temps_estime_borwein(nombre_decimales, format=True):
    """
    Fonction qui donne une estimation de temps de calcul pour un nombre de décimales donné avec la méthode de Borwein.
    parametres:
        nombre_decimales: Nombre de décimales à calculer pour π
        format: Booléen ; True pour un format HH:MM:SS, False pour un float
    retourne:
        Une chaîne (si format=True) ou un float (si format=False) correspondant au temps estimé.
    """
    temps_estime_calcul = 6.67e-8 * nombre_decimales**1.23  # Calcule une estimation empirique du temps (en s)
    if format:  # Vérifie si on doit formater le résultat
        heures = int(max(temps_estime_calcul, 0) // 3600)  # Convertit le temps en heures entières
        minutes = int((max(temps_estime_calcul, 0) % 3600) // 60)  # Convertit le reste en minutes
        secondes = int(max(temps_estime_calcul, 0) % 60)  # Le reste en secondes
        return f"{heures:02}:{minutes:02}:{secondes:02}"  # Retourne au format HH:MM:SS
    else:
        return temps_estime_calcul  # Retourne la valeur brute en secondes

def information_borwein():
    """
    Fonction qui gère l'affichage d'information sur la méthode Borwein
    parametres:
        Aucun
    retourne:
        True si clic pour continuer, False si l'utilisateur clique sur le bouton menu.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la taille de l'écran
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police pour le titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 33)  # Police pour le texte normal

    texte_titre = "Méthode de Borwein"  # Titre à afficher
    texte_description = (  # Description de la méthode
        "La méthode de Borwein, développée par Jonathan et Peter Borwein en 1984, "
        "est un algorithme itératif rapide pour l'estimation de π. Il repose sur "
        "une convergence quartique, ce qui signifie que le nombre de décimales double "
        "à chaque itération. Cette méthode est particulièrement utile pour les calculs de π "
        "nécessitant une haute précision, notamment dans les tests de supercalculateurs et les records de décimales de π. "
    )
    texte_formule = (  # Formules mathématiques employées
        "Formules de la méthode de Borwein :",
        "y_(n+1) = (1 - (1 - y_n^4)^(1/4)) / (1 + (1 - y_n^4)^(1/4))",
        "a_(n+1) = a_n * (1 + y_(n+1))^4 - 2^(2n+3) * y_(n+1) * (1 + y_(n+1) + y_(n+1)^2)",
        " π ≈ 1 / a_n"
    )

    while True:  # Boucle principale d'affichage
        ecran.fill(NOIR)  # Fond noir
        titre_rendu = police_titre.render(texte_titre, True, BLANC)  # Rend le titre
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))  # Centre le titre
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre

        y_position = hauteur_ecran // 5  # Position verticale de départ pour le texte
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 10, y_position, 15, largeur_ecran * 0.8, police_texte)  # Affiche la description
        
        y_position += 0  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 10 # Ajoute un espace en fonction de si on est en plein écran ou non

        for ligne in texte_formule:  # Parcourt chaque ligne des formules
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position + 50, 15, largeur_ecran * 0.8, police_texte, BLEU, souligner=True if ligne == "Formules de la méthode de Borwein :" else False) + hauteur_ecran // 50

        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer", True, ROUGE)  # Invite à cliquer
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))  # Place en bas de l'écran

        bouton_menu()  # Dessine le bouton menu
        croix_fermer()  # Dessine la croix de fermeture
        pygame.display.update()  # Rafraîchit l'écran

        evenement_boutons, _ = gestionnaire_evenements()  # Récupère les actions de l'utilisateur
        if evenement_boutons == "menu":  # Si clic sur le bouton menu
            return False  # On retourne au menu
        if evenement_boutons == "clic":  # Si clic n'importe où
            return True  # On lance la suite

def borwein():
    """
    Fonction principale du calcul de π par la méthode de Borwein
    parametres:
        Aucun
    retourne:
        Rien. Gère l'affichage et la logique de calcul, puis affiche les résultats.
    """
    if not information_borwein():  # Affiche l'écran d'info
        return  # Retour au menu si clique en étant dans la fonction d'informations

    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la taille de l'écran
    saisie_texte = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)  # Saisie de texte
    nombre_decimales = None  # Nombre de décimales pas encore défini
    nombre_decimales_actuelles = 0  # Compteur pour gestion d'avertissement et d'estimation de temps
    temps_estime_affiche = "Temps estimé : -"  # Message d'estimation par défaut

    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police pour titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 25)  # Police pour texte standard

    while nombre_decimales is None:  # On attend une saisie correcte
        ecran.fill(NOIR)  # Fond noir
        titre = police_titre.render("Méthode de Borwein", True, BLANC)  # Rend le titre
        explication = police_texte.render("Entrez le nombre de décimales à calculer (300 millions max) :", True, BLANC)  # Texte explicatif
        temps_affiche = police_texte.render(temps_estime_affiche, True, BLANC)  # Affiche l'estimation du temps
        note = "Note : le temps de calcul réel peut possiblement varier en fonction de la puissance de votre machine."  # Note informative
        avertissement = "Le calcul ne sera pas vérifié car le fichier de référence contient 100 millions de décimales"  # Message si trop de décimales par rapport au fichier référence

        ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 20))  # Place le titre
        souligner_texte(ecran, titre, largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 20) 
        ecran.blit(explication, (largeur_ecran // 2 - explication.get_width() // 2, hauteur_ecran // 3))  # Place le texte
        ecran.blit(saisie_texte.surface, (largeur_ecran // 2 - saisie_texte.surface.get_width() // 2, hauteur_ecran // 2))  # Zone de saisie
        ecran.blit(temps_affiche, (largeur_ecran // 2 - temps_affiche.get_width() // 2, hauteur_ecran // 2.5))  # Temps estimé

        afficher_texte_dynamique(ecran, note, 0, hauteur_ecran // 1.7, 15, largeur_ecran * 0.99, police_texte)  # Affiche la note

        if nombre_decimales_actuelles > 100000000:  # Si plus de 100 millions
            afficher_texte_dynamique(ecran, avertissement, 0, hauteur_ecran // 1.3, 15, largeur_ecran * 0.99, police_texte, ROUGE)  # Message en rouge car trop de décimales par rapport au fichier référence

        bouton_informations()  # Bouton 'info'
        bouton_menu()  # Bouton menu
        croix_fermer()  # Croix fermer
        pygame.display.update()  # Mise à jour de l'écran

        evenement_boutons, evenements = gestionnaire_evenements()  # Récupère les événements
        if evenement_boutons == "menu":  # Si clic sur le bouton menu
            return  # On retourne au menu
        if evenement_boutons == "info":  # Si clic sur le bouton d'information
            if not information_borwein():  # Réaffiche la page d'information
                return  # Retourne au menu si clic sur le bouton menu dans l'écran d'informations

        saisie_texte.update(evenements)  # Actualise la saisie
        if len(saisie_texte.value) > 9:  # On limite la saisie à 10 chiffres
            saisie_texte.value = saisie_texte.value[:9]  # On tronque

        if saisie_texte.value.isdigit():  # Vérifie si c'est un nombre
            nombre_decimales_actuelles = int(saisie_texte.value)  # Convertit
            temps_estime_affiche = f"Temps estimé : {temps_estime_borwein(nombre_decimales_actuelles)} sec"  # Met à jour l'estimation
        else:
            temps_estime_affiche = "Temps estimé : -"  # Sinon, indéfini

        for evenement in evenements:  # Parcourt la liste des événements
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:  # Si on appuie sur Entrée
                if saisie_texte.value.isdigit():  # Et que la saisie est un nombre
                    nombre_decimales = min(300000000, int(saisie_texte.value))  # On valide
                saisie_texte.value = ""  # On réinitialise la zone de texte

    ecran.fill(NOIR)  # Nettoie l'écran
    texte_calcul = police_texte.render("Calcul en cours...", True, BLANC)  # Texte "Calcul en cours"
    ecran.blit(texte_calcul, (50, 200))  # Placement
    progression = 0.0  # Progression initiale

    largeur_barre = largeur_ecran // 2  # Largeur de la barre de progression
    hauteur_barre = 30  # Hauteur de la barre
    position_x_barre = (largeur_ecran - largeur_barre) // 2  # Position horizontale (centrée)
    position_y_barre = hauteur_ecran // 2  # Position verticale (moitié)
    largeur_remplie = int(largeur_barre * progression)  # À 0% au départ

    pygame.draw.rect(ecran, GRIS, (position_x_barre, position_y_barre, largeur_barre, hauteur_barre))  # Dessine la barre vide
    pygame.draw.rect(ecran, (255, 255, 50), (position_x_barre, position_y_barre, largeur_remplie, hauteur_barre))  # Remplit en jaune
    texte_avertissement = pygame.font.Font(POLICE, hauteur_ecran // 34).render("Avertissement : Veuillez ne pas cliquer sur l'écran pendant un long calcul !", True, BLANC)
    ecran.blit(texte_avertissement, (largeur_ecran // 2 - texte_avertissement.get_width() // 2, hauteur_ecran // 1.05))
    texte_progression = police_texte.render(f"{int(progression * 100)}%", True, BLANC)  # Affiche 0%
    ecran.blit(texte_progression, (largeur_ecran // 2 - texte_progression.get_width() // 2, position_y_barre - hauteur_ecran // 20))  # Position du %
    pygame.display.update()  # Rafraîchit

    debut_temps = pygame.time.get_ticks()  # Note le temps de début
    gmpy2.get_context().precision = int(nombre_decimales * 3.32193) + 50  # Règle la précision gmpy2 avec une marge supplémentaire

    y = sqrt(mpfr(2)) - 1  # Initialisation du paramètre y
    a = mpfr(6) - mpfr(4) * sqrt(mpfr(2))  # Initialisation du paramètre a

    nombre_iterations = max(1, (nombre_decimales.bit_length() // 2 + 1))  # Nombre d'itérations estimé

    for i in range(nombre_iterations):  # Boucle de calcul
        y_racine_quatrieme = gmpy2.root(1 - y**4, 4)  # Extrait la racine 4e de (1 - y^4)
        y_suivant = (1 - y_racine_quatrieme) / (1 + y_racine_quatrieme)  # Met à jour y
        a = a * (1 + y_suivant)**4 - 2**(2 * i + 3) * y_suivant * (1 + y_suivant + y_suivant**2)  # Met à jour a
        y = y_suivant  # Nouveau y

        progression = (i + 1) / nombre_iterations  # Pourcentage d'avancement
        largeur_remplie = int(largeur_barre * progression)  # Largeur de barre à remplir
        ecran.fill(NOIR)  # Nettoie l'écran
        pygame.draw.rect(ecran, GRIS, (position_x_barre, position_y_barre, largeur_barre, hauteur_barre))  # Barre grise
        pygame.draw.rect(ecran, (255, 255, 50), (position_x_barre, position_y_barre, largeur_remplie, hauteur_barre))  # Jaune pour la progression
        texte_progression = police_texte.render(f"{int(progression * 100)}%", True, BLANC)  # Texte %
        ecran.blit(texte_progression, (largeur_ecran // 2 - texte_progression.get_width() // 2, position_y_barre - hauteur_ecran // 20))  # Placement
        texte_calcul = police_texte.render("Calcul en cours...", True, BLANC)  # Réaffiche "Calcul en cours"
        ecran.blit(texte_calcul, (50, 200))  # Placement
        ecran.blit(texte_avertissement, (largeur_ecran // 2 - texte_avertissement.get_width() // 2, hauteur_ecran // 1.05))
        
        pygame.display.update() # On met à jour l'affichage

    pi_estime = mpfr(1) / mpfr(a)  # 1 / a = π approximé
    temps_total = temps_ecoule(debut_temps)  # Durée totale
    str_pi_estime = str(pi_estime)[:nombre_decimales + 2]  # Tronque la chaîne (3. + décimales)
    message_verification = verifier_estimation_pi(str_pi_estime, nombre_decimales)  # Vérifie avec référence

    afficher_resultat(str_pi_estime, temps_total, "Borwein", message_verification, nombre_decimales, information_borwein)  # Affiche le résultat
