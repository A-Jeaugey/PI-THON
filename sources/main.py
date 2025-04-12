#Projet : PI-THON
#Auteurs : Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1" # Masque le message de soutien pygame

import pygame  # Importation de pygame pour l'interface graphique
from affichage import menu_principal  # Fonction du menu principal

# Importations des méthodes d'estimation de π
from methodes_estimation.monte_carlo import monte_carlo_detaille
from methodes_estimation.formule_de_machin import machin
from methodes_estimation.gauss_legendre import gauss_legendre
from methodes_estimation.collisions import collisions
from methodes_estimation.leibniz import leibniz
from methodes_estimation.nilakantha import nilakantha
from methodes_estimation.buffon import buffon
from methodes_estimation.archimede import archimede
from methodes_estimation.chudnovsky import chudnovsky
from methodes_estimation.approximation_integration import approximation_integration
from methodes_estimation.ramanujan import ramanujan
from methodes_estimation.borwein import borwein
from methodes_estimation.pendule import pendule

pygame.init()  # Initialisation de pygame

# Dictionnaire des méthodes d'estimation associées à leurs fonctions
methodes = {
    "Monte Carlo": monte_carlo_detaille,
    "Machin": machin,
    "Gauss-Legendre": gauss_legendre,
    "Collisions": collisions,
    "Leibniz": leibniz,
    "Nilakantha": nilakantha,
    "Buffon": buffon,
    "Archimède": archimede,
    "Chudnovsky": chudnovsky,
    "Approximation par intégration": approximation_integration,
    "Ramanujan": ramanujan,
    "Borwein": borwein,
    "Pendule": pendule
}

while True:  # Boucle principale du programme
    choix = menu_principal()  # Affiche le menu et récupère le choix utilisateur
    if choix in methodes:  # Vérifie la validité du choix
        methodes[choix]()  # Exécute la méthode choisie
