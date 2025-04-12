#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Bibliothèque Pygame pour la gestion des surfaces, événements, affichage, etc.
import pygame_textinput  # Module pour gérer un champ de texte éditable dans Pygame.
from affichage import ecran, POLICE, BLANC, NOIR, ROUGE, BLEU, bouton_menu, croix_fermer, bouton_informations, ecran_information # Composants d'affichage et couleurs.
from utils import temps_ecoule, gestionnaire_evenements, afficher_texte_dynamique, souligner_texte  # Fonctions utilitaires


def information_nilakantha():
    """
    Affiche une introduction à la méthode de Nilakantha, sous forme de texte explicatif.
    L'utilisateur peut cliquer sur l'écran pour lancer le calcul interactif, ou cliquer sur "menu".

    Paramètres:
        Aucun

    Retourne:
        bool: True si l'utilisateur clique pour commencer, False s'il clique sur "menu".
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Dimensions de la fenêtre
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)         # Police pour le gros titre
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 39)         # Police plus petite pour le texte

    texte_titre = "Méthode de Nilakantha"  # Intitulé principal
    # Description générale de la méthode
    texte_description = (
        "La méthode de Nilakantha est une série infinie qui améliore la série de Leibniz "
        "en accélérant la convergence vers π. Développée au 15e siècle par le mathématicien indien "
        "Nilakantha Somayaji, elle ajoute et soustrait des fractions de la forme 4/(n·(n+1)·(n+2)). "
        "Chaque itération affine la valeur de π, offrant une approximation plus rapide que la série de Leibniz."
    )
    # Formule mathématique illustrant la série
    texte_formule = (
        "La formule est alors :",
        "π ≈ 3 + 4/(2·3·4) - 4/(4·5·6) + 4/(6·7·8) - 4/(8·9·10) + ..."
    )
    # Informations sur la visualisation dans le programme
    texte_visualisation = (
        "Visualisation :",
        "• Les fractions ajoutées ou soustraites sont affichées en temps réel.",
        "• la dernière fraction ajoutée est marquée en rouge.",
        "• L'entrée utilisateur permet d'ajuster le nombre de fractions calculées par seconde."
    )

    while True:  # Boucle d'affichage du texte informatif
        ecran.fill(NOIR)  # Efface l'écran en le remplissant de noir

        # Crée et affiche le titre, centré horizontalement
        titre_rendu = police_titre.render(texte_titre, True, BLANC)
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligne le titre
        # Position de départ pour l'affichage dynamique du texte
        y_position = hauteur_ecran // 6
        
        # Affiche le paragraphe principal décrivant la méthode
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 10, y_position, 15, largeur_ecran * 0.8, police_texte)
        y_position += 0 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 10

        # Affiche les lignes de la formule
        for ligne in texte_formule:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position + 50, 15, largeur_ecran * 0.8, police_texte, BLEU, souligner=True if ligne == "La formule est alors :" else False) + hauteur_ecran // 50

        y_position += hauteur_ecran // 18 if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 10 # Ajoute un espace en fonction de si on est en plein écran ou non

        # Affiche le bloc expliquant la visualisation
        for ligne in texte_visualisation:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position + 40, 15, largeur_ecran * 0.8, police_texte, souligner=True if ligne == "Visualisation :" else False) + hauteur_ecran // 50

        # Invite l'utilisateur à cliquer pour commencer
        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer", True, ROUGE)
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))

        # Dessine le bouton menu, la croix de fermeture, et met à jour l'affichage
        bouton_menu()
        croix_fermer()
        pygame.display.update()

        # Gère les événements
        evenement_boutons, _ = gestionnaire_evenements()
        if evenement_boutons == "menu": # Si clique sur le bouton menu
            return False # Retour au menu
        if evenement_boutons == "clic": # Si clique n'importe où sur l'écran
            return True # On passe à la méthode


def nilakantha():
    """
    Lance la démonstration de la méthode de Nilakantha pour calculer π,
    avec un affichage temps réel des fractions ajoutées ou soustraites.
    L'utilisateur peut également régler le nombre de fractions calculées par seconde.

    Paramètres: Aucun
    Retourne: Rien (on quitte si "menu" ou après réaffichage éventuel de l'information).
    """
    # D'abord, on affiche l'introduction
    if not information_nilakantha():
        return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu

    # On récupère les dimensions de la fenêtre pour calibrer l'affichage.
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()

    # Polices pour le titre, le texte général, et l'affichage des fractions.
    police_titre = pygame.font.Font(POLICE, largeur_ecran // 25)
    police_texte = pygame.font.Font(POLICE, largeur_ecran // 35)
    police_fraction = pygame.font.Font(POLICE, largeur_ecran // 30)

    # On efface l'écran et on affiche le titre principal
    ecran.fill(NOIR)

    # Initialisation de la somme : Nilakantha commence à 3, puis ajoute / soustrait 4 / (n(n+1)(n+2))
    pi_estime = 3
    denominateur = 2  # C'est n dans la formule, on part de 2 (pour 4/(2*3*4))
    ajout = True      # Booléen indiquant si on ajoute ou si on soustrait le terme
    etapes = 0        # Nombre total d'étapes calculées
    historique_fractions = []  # Liste pour stocker les fractions récentes et les afficher

    # Champ de saisie pour modifier le nombre d'itérations (fractions) calculées par seconde
    saisie_texte = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)
    iterations_par_seconde = 100  # Valeur par défaut

    # On mémorise l'instant de départ pour mesurer le temps écoulé, 
    # et l'instant de la dernière mise à jour pour gérer l'intervalle de calcul
    debut_temps = pygame.time.get_ticks()
    dernier_temps = pygame.time.get_ticks()

    while True:
        # Récupère l'action (boutons) et les événements
        evenement_boutons, evenements = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur le bouton menu
            return # Retour au menu
        if evenement_boutons == "info":   # S'il clique sur le bouton info, on réaffiche la page d'introduction
            if not information_nilakantha():
                return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu

        # On parcourt les événements Pygame pour gérer le champ de texte
        for evenement in evenements:
            # Si l'utilisateur appuie sur 'Entrée'
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:
                # Si la valeur saisie est un entier
                if saisie_texte.value.isdigit():
                    # On borne la valeur entre 1 et 1000 pour éviter des excès
                    iterations_par_seconde = min(1000, max(1, int(saisie_texte.value)))
                # On efface le champ une fois la valeur récupérée
                saisie_texte.value = ""

        # On met à jour le champ de texte
        saisie_texte.update(evenements)
        # On limite la longueur de la saisie (4 caractères max)
        if len(saisie_texte.value) > 4:
            saisie_texte.value = saisie_texte.value[:4]

        # Gestion de l'intervalle de temps entre deux mises à jour de la série
        temps_actuel = pygame.time.get_ticks()
        delta_temps = temps_actuel - dernier_temps
        intervalle_temps = 1000 / iterations_par_seconde  # Durée en ms entre deux calculs

        # Si suffisamment de temps s'est écoulé depuis la dernière mise à jour
        if delta_temps >= intervalle_temps:
            # On calcule le terme 4 / (n(n+1)(n+2))
            terme = 4 / (denominateur * (denominateur + 1) * (denominateur + 2))
            # On prépare une chaîne représentant la fraction (pour affichage)
            fraction = f" 4 / ({denominateur} × {denominateur + 1} × {denominateur + 2})"

            # On ajoute ou soustrait ce terme à pi_estime, selon la logique alternée
            if ajout:
                pi_estime += terme
                fraction = "+ " + fraction
            else:
                pi_estime -= terme
                fraction = "- " + fraction

            # On alterne l'état d'ajout
            ajout = not ajout
            # On avance de 2 dans la formule : (2 -> 4 -> 6 -> 8, etc.)
            denominateur += 2

            # On enregistre cette fraction dans l'historique
            historique_fractions.append(fraction)
            # On conserve seulement les 8 fractions les plus récentes pour l'affichage
            if len(historique_fractions) > 8:
                historique_fractions = historique_fractions[-8:]

            # On a fait une étape de plus
            etapes += 1
            # On met à jour dernier_temps
            dernier_temps = temps_actuel

        # On efface l'écran
        ecran.fill(NOIR)

        # On va afficher les fractions de l'historique en partant de la plus récente
        position_y = hauteur_ecran // 1.46
        index_fractions = 0
        for fraction in reversed(historique_fractions):
            couleur = ROUGE if index_fractions == 0 else BLANC # La fraction la plus récente (index 0) s'affiche en rouge, les autres en blanc
            texte_fraction = police_fraction.render(fraction, True, couleur) # Rendu des fractions
            ecran.blit(texte_fraction, (largeur_ecran // 2 - texte_fraction.get_width() // 2, position_y)) # Placement des fractions
            position_y -= hauteur_ecran // 20 # On les fait défiler
            index_fractions += 1

        # Texte affichant le nombre d'étapes, la valeur de pi, le temps écoulé, et les itérations par seconde
        texte_iteration = police_texte.render(f"Étape : {etapes}", True, BLANC)
        texte_pi = police_titre.render(f"Estimation de π : {pi_estime:.15f}", True, BLANC)
        texte_temps = police_texte.render(f"Temps écoulé : {temps_ecoule(debut_temps)}", True, BLANC)
        texte_iterations_par_seconde = police_texte.render(f"Iterations par seconde : {iterations_par_seconde}", True, BLANC)

        # On place ces textes à l'écran
        ecran.blit(texte_iteration, ((largeur_ecran - texte_iteration.get_width()) // 2, hauteur_ecran // 8))
        ecran.blit(texte_pi, (largeur_ecran // 2 - texte_pi.get_width() // 2, hauteur_ecran // 5))
        ecran.blit(texte_temps, ((largeur_ecran - texte_temps.get_width()) // 2, hauteur_ecran // 20))
        ecran.blit(texte_iterations_par_seconde, ((largeur_ecran - texte_iterations_par_seconde.get_width()) // 2, hauteur_ecran * 0.9))

        # Partie champ de saisie pour modifier 'iterations_par_seconde'
        texte_entree = police_texte.render("Entrer itérations par seconde :", True, BLANC)
        ecran.blit(texte_entree, ((largeur_ecran - texte_entree.get_width()) // 2, hauteur_ecran * 0.8))
        ecran.blit(saisie_texte.surface, ((largeur_ecran - saisie_texte.surface.get_width()) // 2, hauteur_ecran * 0.865))

        # Boutons d'information, de menu et de fermeture
        bouton_informations()
        bouton_menu()
        croix_fermer()

        # Mise à jour de l'affichage final
        pygame.display.update()
