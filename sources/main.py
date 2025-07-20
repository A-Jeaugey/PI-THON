# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"  # Hides the pygame support message

import pygame  # Importing pygame for the graphical interface
from display import main_menu  # Main menu function

# Imports of π estimation methods
from estimation_methods.monte_carlo import monte_carlo_detailed
from estimation_methods.machin_formula import machin
from estimation_methods.gauss_legendre import gauss_legendre
from estimation_methods.collisions import collisions
from estimation_methods.leibniz import leibniz
from estimation_methods.nilakantha import nilakantha
from estimation_methods.buffon import buffon
from estimation_methods.archimedes import archimedes
from estimation_methods.chudnovsky import chudnovsky
from estimation_methods.integration_approximation import approximation_integration
from estimation_methods.ramanujan import ramanujan
from estimation_methods.borwein import borwein
from estimation_methods.pendulum import pendulum

pygame.init()  # Initializing pygame

# Dictionary of estimation methods associated with their functions
methods = {
    "Monte Carlo": monte_carlo_detailed,
    "Machin": machin,
    "Gauss-Legendre": gauss_legendre,
    "Collisions": collisions,
    "Leibniz": leibniz,
    "Nilakantha": nilakantha,
    "Buffon": buffon,
    "Archimedes": archimedes,
    "Chudnovsky": chudnovsky,
    "Integration Approximation": approximation_integration,
    "Ramanujan": ramanujan,
    "Borwein": borwein,
    "Pendulum": pendulum
}

while True:  # Main program loop
    choice = main_menu()  # Displays the menu and gets the user’s choice
    if choice in methods:  # Checks if the choice is valid
        methods[choice]()  # Executes the chosen method
