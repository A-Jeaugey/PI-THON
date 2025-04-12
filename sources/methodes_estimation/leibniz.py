#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # import de pygame pour l'affichage, événements etc.
import pygame_textinput  # Module pour créer et gérer des champs de saisie de texte dans Pygame.
from affichage import ecran, POLICE, BLANC, NOIR, ROUGE, GRIS, BLEU, bouton_menu, croix_fermer, bouton_informations, ecran_information # Composants d'affichage et couleurs.
from utils import temps_ecoule, gestionnaire_evenements, afficher_texte_dynamique, souligner_texte  # Fonctions utilitaires

def information_leibniz():
    """
    Affiche l'écran d'information sur la méthode de Leibniz.
    L'utilisateur peut cliquer pour commencer la simulation ou cliquer sur "menu" pour quitter.

    Paramètres: Aucun

    Retourne:
        bool: 
            - True si l'utilisateur clique pour lancer la démonstration,
            - False s'il clique sur le bouton menu.
    """
    # Récupère la largeur et la hauteur de la fenêtre pour adapter l'affichage.
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()

    # Création de polices pour le titre et le texte explicatif.
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 35)

    # Textes explicatifs
    texte_titre = "Méthode de Leibniz"
    texte_description = (
        "La série de Leibniz est une des plus simples méthodes pour estimer π, "
        "mais elle converge très lentement. Elle repose sur une somme alternée de termes qui tend vers π/4. "
        "Chaque terme ajoute ou enlève une fraction, permettant une "
        "approximation progressive de π. "
    )
    texte_formule = (
        "La formule est alors :",
        "π ≈ 4 * (1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ...)"
    )
    texte_visualisation = (
        "Visualisation :",
        "• L'axe vertical représente la valeur estimée de π.",
        "• Une ligne blanche marque la valeur réelle de π.",
        "• La courbe colorée montre comment l'estimation fluctue avec les itérations.",
        "• L'entrée utilisateur permet d'ajuster la vitesse d'affichage."
    )

    while True:
        ecran.fill(NOIR)  # On efface l'écran en le remplissant de noir.

        # Affichage du titre en haut de l'écran, centré horizontalement.
        titre_rendu = police_titre.render(texte_titre, True, BLANC)
        ecran.blit(titre_rendu, (largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40))
        souligner_texte(ecran, titre_rendu, largeur_ecran // 2 - titre_rendu.get_width() // 2, hauteur_ecran // 40) # Souligner le titre

        # Position de départ pour l'affichage dynamique du texte.
        y_position = hauteur_ecran // 6
        # Affiche le paragraphe décrivant la méthode de Leibniz.
        y_position += afficher_texte_dynamique(ecran, texte_description, largeur_ecran // 10, y_position, 15, largeur_ecran * 0.8, police_texte) + hauteur_ecran // 30
        y_position += 0  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 15 # Ajoute un espace en fonction de si on est en plein écran ou non
        # Affiche les deux lignes décrivant la formule, en BLEU.
        for ligne in texte_formule:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position, 15, largeur_ecran * 0.8, police_texte, BLEU, souligner=True if ligne == "La formule est alors :" else False) + hauteur_ecran // 50
        
        y_position += 0  if hauteur_ecran <= ecran_information.current_h * 0.9 else hauteur_ecran // 15 # Ajoute un espace en fonction de si on est en plein écran ou non
        # Affiche la partie "Visualisation" ligne par ligne.
        for ligne in texte_visualisation:
            y_position += afficher_texte_dynamique(ecran, ligne, largeur_ecran // 10, y_position + 40, 15, largeur_ecran * 0.8, police_texte, souligner=True if ligne == "Visualisation :" else False) + hauteur_ecran // 50

        # Invite l'utilisateur à cliquer pour lancer la démonstration.
        instruction_rendu = police_titre.render("Cliquez n'importe où pour commencer", True, ROUGE)
        ecran.blit(instruction_rendu, (largeur_ecran // 2 - instruction_rendu.get_width() // 2, hauteur_ecran * 0.92))

        # Dessine le bouton menu, la croix fermer, puis met à jour l'affichage.
        bouton_menu()
        croix_fermer()
        pygame.display.update()

        # Gestion des événements : on récupère les actions depuis la fonction gestionnaire_evenements.
        evenement_boutons, _ = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Si l'utilisateur clique sur le bouton menu
            return False # On retourne au menu
        if evenement_boutons == "clic":  # Si l'utilisateur clique dans la fenêtre
            return True # On passe à la méthode de calcul


def leibniz():
    """
    Affiche la démonstration de la méthode de Leibniz pour estimer π.
    L'utilisateur peut ajuster le nombre d'itérations par mise à jour en utilisant un champ de texte.

    Paramètres: Aucun

    Retourne:
        Rien. La fonction quitte lorsque l'utilisateur clique sur "menu" ou, en réaffichant l'information, renvoie False.
    """
    # On commence par l'écran d'information.
    if not information_leibniz():
        return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu

    # On récupère la taille de la fenêtre pour adapter les affichages.
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()
    # Coordonnées centrales (employées comme référence pour le tracé ou l'affichage).
    centre_x, centre_y = largeur_ecran // 2, hauteur_ecran // 2

    # Polices pour le titre et pour le texte plus petit.
    police_titre = pygame.font.Font(POLICE, largeur_ecran // 25)
    police_texte = pygame.font.Font(POLICE, largeur_ecran // 42)

    # On efface l'écran avant de commencer la simulation.
    ecran.fill(NOIR)
    
    pygame.display.update()  # Mise à jour de l'affichage

    # On mémorise l'instant de départ (ticks Pygame) pour mesurer le temps écoulé.
    debut_ticks = pygame.time.get_ticks()

    pi_estime = 0  # Valeur accumulée représentant la somme partielle (leibniz s'approche de pi/4)
    nombre_iterations = 0  # Nombre d'itérations déjà effectuées
    valeurs_pi = []  # On stocke ici les estimations successives de π pour tracer la courbe

    # Nombre d'itérations à effectuer à chaque update (paramétrable par l'utilisateur)
    iterations_par_update = 1

    # On utilise un champ texte pour que l'utilisateur puisse modifier 'iterations_par_update'
    textinput = pygame_textinput.TextInputVisualizer(font_color=BLANC, cursor_color=BLANC)

    while True:
        # Récupération des actions/événements
        evenement_boutons, evenements = gestionnaire_evenements()
        if evenement_boutons == "menu":  # Si clique sur le bouton menu
            return # On retourne au menu
        if evenement_boutons == "info":  # Si clique sur 'info', on réaffiche l'écran d'info Leibniz
            if not information_leibniz():
                return # Si on clique sur le bouton menu dans l'ecran d'infos, on revient au menu

        # On parcourt les événements renvoyés par Pygame
        for evenement in evenements:
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN: # Si l'utilisateur appuie sur la touche Entrée
                if textinput.value.isdigit(): # Et que l'entrée est un nombre
                    iterations_par_update = max(1, int(textinput.value))  # Au minimum 1
                textinput.value = ""  # On efface le champ après validation

        # Mise à jour du champ texte
        textinput.update(evenements)
        # On limite la longueur de l'input utilisateur
        if len(textinput.value) > 6:
            textinput.value = textinput.value[:6]

        # Calcul de la série de Leibniz sur 'iterations_par_update' itérations supplémentaires
        for i in range(nombre_iterations, nombre_iterations + iterations_par_update):
            # Leibniz : pi/4 = 1/1 - 1/3 + 1/5 - 1/7 + ...
            pi_estime += (-1)**i / (2 * i + 1)  
        # On conserve la valeur de 4 * pi_estime (car la série donne pi/4).
        valeurs_pi.append(4 * pi_estime)
        nombre_iterations += iterations_par_update  # On a avancé de iterations_par_update itérations

        # On efface l'écran avant de réafficher la nouvelle frame.
        ecran.fill(NOIR)

        # Dessine deux axes : horizontal en bas, vertical à gauche
        pygame.draw.line(ecran, GRIS, (50, hauteur_ecran - 50), (largeur_ecran - 50, hauteur_ecran - 50), 2)
        pygame.draw.line(ecran, GRIS, (50, 100), (50, hauteur_ecran - 50), 2)

        # On trace des marques horizontales et affiche les graduations (0,1,2,3,4,5,6...) sur l'axe vertical
        for i in range(7):
            valeur_reelle = i
            # On calcule la position Y de la marque : répartie entre 100 et hauteur_ecran-50
            y_position = int(hauteur_ecran - 50 - i * (hauteur_ecran - 150) / 6)

            # On convertit la valeur en string (affichée en format X.X)
            valeur_y = f"{valeur_reelle:.1f}"
            label = pygame.font.Font(POLICE, 25).render(valeur_y, True, BLANC)
            ecran.blit(label, (8, y_position - 10))  # Place le label légèrement à gauche
            pygame.draw.line(ecran, GRIS, (45, y_position), (55, y_position), 2)  # Petite graduation

        # On ajoute une petite graduation pour π, et on dessine une ligne horizontale où se situe π
        pi_label = pygame.font.Font(POLICE, 30).render("π", True, BLANC)
        # On place ce label à gauche.
        y_pi = int(centre_y - (3.14159265358979 - 3.14))
        ecran.blit(pi_label, (12, y_pi - 20))

        # Ligne de référence horizontale pour π (par exemple, pour y=(π-3.14)*facteur...)
        y_pi = int(centre_y - (3.14159265358979 - 3.14) * 100)
        pygame.draw.line(ecran, BLANC, (50, y_pi), (largeur_ecran - 50, y_pi), 2)

        # Tracé de la courbe de convergence. On parcourt les points successifs de 'valeurs_pi'.
        if len(valeurs_pi) > 1:
            for i in range(1, len(valeurs_pi)):
                # Coordonnée X du point précédent
                x1 = int(50 + (i - 1) * (largeur_ecran - 100) / len(valeurs_pi))
                # Coordonnée Y en fonction de la différence par rapport à 3.14
                y1 = int(centre_y - (valeurs_pi[i - 1] - 3.14) * 500)

                # Coordonnée X du point courant
                x2 = int(50 + i * (largeur_ecran - 100) / len(valeurs_pi))
                # Coordonnée Y du point courant
                y2 = int(centre_y - (valeurs_pi[i] - 3.14) * 500)

                # Couleur évoluant au fur et à mesure (de jaune à magenta). 
                couleur = (255,int(255 * (i / len(valeurs_pi))),int(255 * (1 - i / len(valeurs_pi))))
                pygame.draw.line(ecran, couleur, (x1, y1), (x2, y2), 3)

        largeur_caractere = police_texte.render("0", True, BLANC).get_width() # Donne la largeur d'un caractère pour bien centrer le texte

        # On crée et affiche du texte donnant le nombre d'itérations, la valeur de pi, et le temps écoulé.
        texte_iteration = police_texte.render(f"Étape {nombre_iterations}", True, BLANC)
        texte_pi = police_titre.render(f"Estimation de π : {4 * pi_estime:.15f}", True, BLANC)
        texte_temps = police_texte.render(f"Temps écoulé : {temps_ecoule(debut_ticks)}", True, BLANC)

        ecran.blit(texte_iteration, (largeur_ecran // 2 - texte_iteration.get_width() // 2, hauteur_ecran // 20))
        ecran.blit(texte_temps, ((largeur_ecran - texte_temps.get_width()) // 2, hauteur_ecran // 9))
        ecran.blit(texte_pi, (largeur_ecran // 2 - texte_temps.get_width() // 2 - 15 * largeur_caractere, hauteur_ecran // 6))

        # Indique à l'utilisateur le champ de saisie pour ajuster 'iterations_par_update'.
        texte_entree = police_texte.render("Entrer itérations par mise à jour :", True, BLANC)
        ecran.blit(texte_entree, ((largeur_ecran - texte_entree.get_width()) // 2, hauteur_ecran // 1.3))

        # Affiche le champ de texte (où l'utilisateur entre un nombre d'itérations).
        ecran.blit(textinput.surface, ((largeur_ecran - texte_entree.get_width()) // 2, hauteur_ecran // 1.2))

        # Affichage des boutons info, bouton menu, et croix fermer.
        bouton_informations()
        bouton_menu()
        croix_fermer()

        # Mise à jour de l'écran.
        pygame.display.update()

        # On insère un petit délai pour contrôler la vitesse d'animation.
        # Il diminue quand iterations_par_update augmente (pour ne pas aller trop vite).
        pygame.time.delay(int(max(30 / (iterations_par_update ** 0.5), 1)))
