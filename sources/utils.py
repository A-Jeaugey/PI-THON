#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import os  # Module pour interagir avec le système d'exploitation (chemins, dossiers, etc.)
import pygame  # Bibliothèque pour la gestion de l'affichage, des événements et du temps (Pygame).

from affichage import ecran, POLICE, BLANC, NOIR, GRIS, VERT, ROUGE, bouton_informations, bouton_menu, croix_fermer  # Imports spécifiques depuis affichage.py

CHEMIN_PI = os.path.join("data", "pi_reference.txt")  # Emplacement du fichier contenant les décimales de référence de π
CHEMIN_DOSSIER_RESULTATS = os.path.join("data", "resultats_estimations_pi")  # Dossier où stocker les résultats d'estimation

def temps_ecoule(debut_ticks, format=True):
    """
    Calcule le temps écoulé depuis 'debut_ticks' et le renvoie au choix sous format HH:MM:SS ou en secondes.
    
    Paramètres:
        debut_ticks (int): La valeur de référence en millisecondes (pygame.time.get_ticks()) au début.
        format (bool): Si True, retourne une chaîne formatée HH:MM:SS. Sinon, un float représentant le temps en secondes.
    
    Retourne:
        str ou float: Le temps écoulé soit en format "HH:MM:SS" si format=True, soit un float en secondes.
    """
    temps_total = max(0, (pygame.time.get_ticks() - debut_ticks) / 1000)  # Calcule le temps écoulé en secondes depuis debut_ticks
    return f"{int(temps_total // 3600):02}:{int((temps_total % 3600) // 60):02}:{int(temps_total % 60):02}" if format else temps_total  # Retourne en HH:MM:SS ou en float

def gestionnaire_evenements():
    """
    Gère les événements (clavier, souris, etc.) et renvoie un code d'action ainsi que la liste des événements.
    Cela permet une centralisation des gestionnaires d'événements des fonctions afin de réduire le code.
    
    Paramètres:
        Aucun.
    
    Retourne:
        tuple: (action, evenements) où 'action' peut être:
            - "menu": si on clique sur le bouton menu
            - "info": si on clique sur le bouton informations
            - "clic": pour un clic gauche simple ailleurs
            - None si aucun événement spécial
        et 'evenements' est la liste pygame.event.get().
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la largeur et la hauteur de la fenêtre
    evenements = pygame.event.get()  # Liste des événements depuis le dernier appel
    for evenement in evenements:  # On parcourt chaque événement
        if evenement.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
            pygame.quit()  # Ferme Pygame
            exit()  # Quitte le programme Python
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:  # Si clic gauche de la souris
            if pygame.Rect(largeur_ecran - 50, 0, 50, 50).collidepoint(evenement.pos):  # Clique sur la croix de fermeture
                pygame.quit()  # Ferme Pygame
                exit()  # Quitte le programme
            if pygame.Rect(largeur_ecran - 130, 0, 50, 50).collidepoint(evenement.pos):  # Clique sur le bouton menu
                return "menu", evenements  # Renvoie "menu" + la liste d'événements
            if pygame.Rect(largeur_ecran - 200, 10, 40, 40).collidepoint(evenement.pos):  # Clique sur le bouton "info" en bas à droite
                return "info", evenements  # Renvoie "info" + la liste d'événements
            return "clic", evenements  # Toute autre zone cliquée => "clic"
    return None, evenements  # Aucun événement particulier => None

def verifier_estimation_pi(pi_estime, nombre_decimales):
    """
    Vérifie la validité d'une estimation de π en la comparant aux décimales de référence (dans CHEMIN_PI).

    Paramètres:
        pi_estime (str): Chaîne représentant les décimales estimées (ex: "3.14159265...").
        nombre_decimales (int): Nombre de décimales qu'on souhaite vérifier.

    Retourne:
        str: Un message sur la validité de l'estimation (correcte, ou erreur à telle décimale, etc.).
    """
    with open(CHEMIN_PI, "r") as fichier:  # Ouvre le fichier de référence
        pi_reference = fichier.read().strip()  # Lit toutes les décimales et enlève les espaces autour
    
    if nombre_decimales > len(pi_reference) - 2:  # Vérifie qu'on ne dépasse pas le stock de décimales du fichier
        return "Les décimales calculées ne peuvent pas être vérifiées."
    
    pi_reference_slice = pi_reference[:nombre_decimales + 2]  # Inclut "3." + nombre_decimales
    
    if pi_estime == pi_reference_slice:  # Compare directement la chaîne
        return "L'estimation de π est correcte !"
    else:
        for i in range(len(pi_estime)):  # Parcourt la chaîne estimée
            if pi_estime[i] != pi_reference_slice[i]:  # Si différence entre l'estimation du programme et le fichier de référence
                return f"Erreur dans l'estimation à partir de la décimale n°{i - 1}"  # Indique la position de l'erreur
    return "Erreur inconnue."  # Si jamais on ne rentre pas dans le if, message par défaut

def afficher_texte_dynamique(ecran, texte, x, y, espacement_ligne, largeur_max, police, couleur=(255, 255, 255), texte_centre=True, hauteur_rectangle=None, souligner=False):
    """
    Affiche un texte en le découpant automatiquement sur plusieurs lignes, avec option de centrage.
    
    Paramètres:
        ecran (pygame.Surface): La surface où dessiner (ici la fenêtre).
        texte (str): Le texte à afficher.
        x (int): Coordonnée X de départ.
        y (int): Coordonnée Y de départ.
        espacement_ligne (int): Espace vertical entre chaque ligne.
        largeur_max (int): Largeur max autorisée pour le texte avant de faire un saut à la ligne.
        police (pygame.font.Font): Police utilisée pour dessiner le texte.
        couleur (tuple): Couleur du texte en RGB (défaut: blanc).
        texte_centre (bool): Si True, centre horizontalement chaque ligne dans la zone donnée.
        hauteur_rectangle (int ou None): Hauteur dans laquelle centrer verticalement le texte. (utilisé uniquement pour les rectangles de la barre latérale).
    
    Retourne:
        int: La hauteur totale occupée par le texte affiché.
    """
    mots = texte.split(" ")  # Sépare le texte en mots
    lignes = []  # Liste des lignes finalisées
    ligne_actuelle = ""  # Accumulation de mots pour la ligne courante

    for mot in mots:  # On parcourt chaque mot
        test_ligne = ligne_actuelle + " " + mot if ligne_actuelle else mot  # On teste si ce mot peut s'ajouter à la ligne
        if police.size(test_ligne)[0] <= largeur_max:  # Si la largeur du texte reste dans la limite
            ligne_actuelle = test_ligne  # On met à jour la ligne courante
        else:
            lignes.append(ligne_actuelle)  # Sinon, on stocke la ligne précédente
            ligne_actuelle = mot  # Et on démarre une nouvelle ligne
    
    lignes.append(ligne_actuelle)  # On ajoute la dernière ligne restant en mémoire

    hauteur_texte_total = len(lignes) * (police.get_height() + espacement_ligne) - espacement_ligne  # Hauteur totale du bloc de texte

    if hauteur_rectangle:  # Si on souhaite un centrage vertical dans un rectangle de la barre latérale
        y += (hauteur_rectangle - hauteur_texte_total) // 2  # Ajuste la coordonnée Y pour centrer verticalement

    index = 0  # Compteur pour la boucle
    for ligne in lignes:  # On dessine chaque ligne
        texte_rendu = police.render(ligne, True, couleur)  # Création de la surface texte
        if texte_centre:
            # On centre horizontalement
            position_texte = texte_rendu.get_rect(center=(x + largeur_max // 2, y + index * (police.get_height() + espacement_ligne)))
            if souligner : 
                souligner_texte(ecran, texte_rendu, position_texte.x, position_texte.y, eloignement=4, couleur=couleur)
        else:
            # On place la ligne en (x, y)
            position_texte = (x, y + index * (police.get_height() + espacement_ligne))
            if souligner : 
                souligner_texte(ecran, texte_rendu, x, + index * (police.get_height() + espacement_ligne), eloignement=4, couleur=couleur)
        ecran.blit(texte_rendu, position_texte)  # Blit du texte sur l'écran
        index += 1 # On accrémente l'index à chaque itérations.

    return hauteur_texte_total  # On retourne la hauteur totale du texte

def souligner_texte(ecran, texte_rendu, x, y, eloignement=4, couleur=BLANC):
    """
    Souligne du texte
    
    Paramètres:
        ecran : (pygame.Surface): La surface où dessiner (ici la fenêtre).
        texte_rendu (pygame.render): Un texte rendu
        x (int): Coordonnée X de départ.
        y (int): Coordonnée Y de départ.
        eloignement (int) = Eloignement entre le texte et le soulignement (défaut: 4)
        couleur (tuple) = Couleur du texte en RGB (défaut: blanc).
    
    Retourne:
        Rien. La fonction affiche juste une barre en dessous du texte.
    """
    pygame.draw.line(ecran, couleur, (x, y + texte_rendu.get_height() + eloignement), (x + texte_rendu.get_width(), y + texte_rendu.get_height() + eloignement), 2)


def afficher_resultat(estimation_pi_str, temps_total, titre_methode, verification_pi, nombre_decimales, fonction_information=None):
    """
    Affiche le résultat final de l'estimation de π, avec possibilité de naviguer dans les décimales (pages).
    
    Paramètres:
        estimation_pi_str (str): Chaîne contenant toutes les décimales estimées de π.
        temps_total (str): Temps écoulé (formaté).
        titre_methode (str): Nom de la méthode de calcul utilisée.
        verification_pi (str): Résultat de la vérification (correct ou erreur).
        nombre_decimales (int): Nombre de décimales calculées.
        fonction_information (callable ou None): Fonction éventuelle pour afficher des informations supplémentaires, appelée sur "info".
    
    Retourne:
        None: La fonction boucle jusqu'au "menu" ou "info" qui déclenchent un changement d'état.
    """
    largeur_ecran, hauteur_ecran = ecran.get_width(), ecran.get_height()  # Récupère la taille de la fenêtre
    police_titre = pygame.font.Font(POLICE, hauteur_ecran // 15)  # Police pour le titre principal
    police_texte = pygame.font.Font(POLICE, hauteur_ecran // 25)  # Police pour les textes moyens
    police_decimales = pygame.font.Font(POLICE, hauteur_ecran // 28)  # Police plus petite pour afficher les décimales
    police_fixe = pygame.font.Font(POLICE, 35)  # Police "fixe" pour les boutons

    espace_marges = largeur_ecran // 40  # Marge de chaque côté
    espace_max = largeur_ecran - espace_marges * 2  # Largeur dispo pour l'affichage des décimales
    exemple_texte = police_decimales.render("0", True, BLANC)  # On mesure la largeur d'un "0" pour avoir la largeur de n'importe quel chiffre (la police est fixée)
    caractere_largeur = exemple_texte.get_width()  # Largeur d'un caractère
    caracteres_par_ligne = espace_max // caractere_largeur  # Nombre de caractères affichables par ligne
    position_x = largeur_ecran - espace_marges - espace_max + caractere_largeur // 2  # Position X de départ pour les décimales
    espace_haut_occupe = hauteur_ecran // 4  # Espace en haut (titre, texte)
    espace_bas_occupe = 80  # Espace en bas (boutons)
    espace_disponible = hauteur_ecran - espace_haut_occupe - espace_bas_occupe  # Espace vertical pour les décimales
    ligne_hauteur = exemple_texte.get_height() + 5  # Hauteur d'une ligne de texte
    lignes_par_page = espace_disponible // ligne_hauteur  # Nombre de lignes de texte par page

    decimales_par_page = caracteres_par_ligne * lignes_par_page  # Nombre total de caractères affichés par page
    pages_pi = [estimation_pi_str[i:i + decimales_par_page] for i in range(0, len(estimation_pi_str), decimales_par_page)]  # Découpe la chaîne en pages

    page_actuelle = 0  # Index de la page courante

    bouton_precedent = pygame.Rect(50, hauteur_ecran - 80, 200, 50)  # Rectangle du bouton "Précédent"
    bouton_suivant = pygame.Rect(largeur_ecran - 250, hauteur_ecran - 80, 200, 50)  # Rectangle du bouton "Suivant"
    bouton_enregistrer = pygame.Rect(largeur_ecran * 0.8 - 10, hauteur_ecran // 20 + hauteur_ecran // 20 - 10, hauteur_ecran * 0.2, hauteur_ecran * 0.127)  # Rectangle pour "Enregistrer"

    while True:  # Boucle d'affichage et d'interaction
        evenement_boutons, evenements = gestionnaire_evenements()  # On récupère l'action éventuelle et les événements
        if evenement_boutons == 'menu':  # Si on clique sur le bouton "menu"
            return  # On sort de la fonction, donc on quitte cet écran
        if evenement_boutons == "info":  # Si on clique sur le bouton "info"
            if not fonction_information():  # Appelle la fonction d'info, si False => on quitte
                return

        for evenement in evenements:  # Parcourt chaque événement
            if evenement.type == pygame.MOUSEBUTTONDOWN:  # Clic souris
                if bouton_precedent.collidepoint(evenement.pos) and page_actuelle > 0 or evenement.button == 4 and page_actuelle > 0: # si on clique sur le bouton "precedent" ou on scroll vers le haut 
                    page_actuelle -= 1  # Page précédente
                if bouton_suivant.collidepoint(evenement.pos) and page_actuelle < len(pages_pi) - 1 or evenement.button == 5 and page_actuelle < len(pages_pi) - 1: # si on clique sur le bouton "suivant" ou on scroll vers le bas
                    page_actuelle += 1  # Page suivante
                if bouton_enregistrer.collidepoint(evenement.pos): # Si on clique sur le bouton "Enregistrer"
                    enregistrer_resultat(titre_methode, estimation_pi_str, nombre_decimales, temps_total, verification_pi)  # Enregistre le résultat

        ecran.fill(NOIR)  # Nettoie l'écran avec la couleur noire

        titre = police_titre.render(titre_methode, True, BLANC)  # Surface texte pour le titre
        explication = police_texte.render(f"Calcul de Pi via {titre_methode}.", True, BLANC)  # Court descriptif
        temps_final = police_texte.render(f"Temps de calcul réel : {temps_total}", True, BLANC)  # Indication du temps total
        texte_verification_pi = police_texte.render(verification_pi, True, VERT if verification_pi == "L'estimation de π est correcte !" else ROUGE)  # Message de vérification (vert ou rouge)

        ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, hauteur_ecran // 50))  # Centre le titre
        ecran.blit(explication, (largeur_ecran // 2 - explication.get_width() // 2, hauteur_ecran // 20 + hauteur_ecran // 20))  # Place l'explication plus bas
        ecran.blit(temps_final, (largeur_ecran // 2 - temps_final.get_width() // 2, hauteur_ecran // 20 + hauteur_ecran // 20 * 2))  # Place le temps final
        ecran.blit(texte_verification_pi, (largeur_ecran // 2 - texte_verification_pi.get_width() // 2, hauteur_ecran // 20 + hauteur_ecran // 20 * 3))  # Place le message de vérification

        position_y = espace_haut_occupe  # Coordonnée Y de départ pour les décimales
        for i in range(0, len(pages_pi[page_actuelle]), caracteres_par_ligne):
            # Découpe la page courante en lignes
            ligne_pi = pages_pi[page_actuelle][i:i + caracteres_par_ligne]
            texte_rendu = police_decimales.render(ligne_pi, True, BLANC) # Surface pour les lignes de décimales
            ecran.blit(texte_rendu, (position_x, position_y))  # Affiche la ligne de décimales
            position_y += ligne_hauteur  # On descend pour la ligne suivante

        pygame.draw.rect(ecran, GRIS, bouton_precedent)  # Dessine le rectangle gris du bouton "Précédent"
        pygame.draw.rect(ecran, GRIS, bouton_suivant)  # Dessine le rectangle gris du bouton "Suivant"
        pygame.draw.rect(ecran, GRIS, bouton_enregistrer)  # Dessine le rectangle gris du bouton "Enregistrer"

        texte_precedent = police_fixe.render("Précédent", True, NOIR)  # Surface texte "Précédent"
        texte_suivant = police_fixe.render("Suivant", True, NOIR)  # Surface texte "Suivant"

        ecran.blit(texte_precedent, (bouton_precedent.x + 100 - texte_precedent.get_width() // 2, bouton_precedent.y + 25 - texte_precedent.get_height() // 2))  # Centre le texte dans le bouton et l'affiche
        ecran.blit(texte_suivant, (bouton_suivant.x + 100 - texte_suivant.get_width() // 2, bouton_suivant.y + 25 - texte_suivant.get_height() // 2))  # Centre le texte dans le bouton et l'affiche
        afficher_texte_dynamique(ecran, "enregistrer dans un fichier .txt", largeur_ecran * 0.8, hauteur_ecran // 20 + hauteur_ecran // 20 + hauteur_ecran // 100, bouton_enregistrer.height // 17, hauteur_ecran * 0.2 - 20, pygame.font.Font(POLICE, hauteur_ecran // 38), BLANC)  # Affiche le texte du bouton "Enregistrer"

        page_info = f"Page {page_actuelle + 1}/{len(pages_pi)}"  # Texte indiquant la page courante / pages totales
        texte_page = police_texte.render(page_info, True, BLANC)  # Surface texte pour la pagination
        ecran.blit(texte_page, (largeur_ecran // 2 - texte_page.get_width() // 2, hauteur_ecran - 70))  # Centré en bas

        bouton_informations()  # Dessine le bouton "?" d'informations
        bouton_menu()  # Dessine le bouton menu
        croix_fermer()  # Dessine la croix de fermeture
        pygame.display.update()  # Met à jour l'affichage pour prendre en compte tous les éléments

def enregistrer_resultat(methode, estimation_pi_str, nombre_decimales, temps_total, verification_estimation):
    """
    Enregistre l'estimation de π dans un fichier .txt, dans le dossier défini par CHEMIN_DOSSIER_RESULTATS.
    
    Paramètres:
        methode (str): Nom de la méthode de calcul.
        estimation_pi_str (str): Chaîne contenant toutes les décimales de l'estimation de π.
        nombre_decimales (int): Nombre de décimales calculées.
        temps_total (str): Temps de calcul (formaté).
        verification_estimation (str): Message indiquant la validité de l'estimation.
    
    Retourne:
        None: Crée ou écrase un fichier .txt contenant tous les détails du calcul.
    """
    if nombre_decimales >= 1000000000:
        nombre_decimales = f"{nombre_decimales // 1000000000} milliard(s)"  # Convertit en notation "milliard(s)"
    elif nombre_decimales >= 1000000:
        nombre_decimales = f"{nombre_decimales // 1000000} million(s)"  # Convertit en notation "million(s)"
    elif nombre_decimales > 1000:
        nombre_decimales = f"{nombre_decimales // 1000} mille"  # Convertit en notation "mille"
    elif nombre_decimales == 1000:
        nombre_decimales = "mille"  # Cas exact de 1000
    else:
        nombre_decimales = str(nombre_decimales)  # Sinon, on reste sur une simple conversion en str
    
    if not os.path.exists(CHEMIN_DOSSIER_RESULTATS):  # Vérifie l'existence du dossier
        os.makedirs(CHEMIN_DOSSIER_RESULTATS)  # Le crée si nécessaire

    nom_fichier = f"pi_{methode.lower()}_{nombre_decimales}.txt"  # Construit le nom du fichier
    if " " in nom_fichier:
        nom_fichier = nom_fichier.replace(" ", "_")  # Remplace les espaces par des underscores

    chemin_fichier = os.path.join(CHEMIN_DOSSIER_RESULTATS, nom_fichier)  # Construit le chemin absolu final

    with open(chemin_fichier, "w", encoding="utf-8") as fichier:  # Ouvre le fichier en écriture (UTF-8)
        fichier.write(f"Méthode de {methode}\n")  # Ecrit la méthode
        fichier.write(f"Nombre de décimales : {nombre_decimales}\n")  # Ecrit le nombre de décimales
        fichier.write(f"Temps de calcul : {temps_total}\n")  # Ecrit le temps total
        fichier.write(f"{verification_estimation}\n")  # Ecrit le résultat de la vérification
        fichier.write(f"Estimation de π : \n{estimation_pi_str}")  # Ecrit la chaîne contenant l'estimation de π
