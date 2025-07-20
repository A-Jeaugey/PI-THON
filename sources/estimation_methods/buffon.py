# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Importing pygame for display and event management
import random  # Importing random to generate random numbers
import math  # Importing math for mathematical functions (cosine, sine, etc.)
import time  # Importing time to measure time
import pygame_textinput  # Importing pygame_textinput to handle text input in pygame
from display import screen, FONT, WHITE, BLACK, RED, GRAY, BLUE, menu_button, close_cross, info_button, screen_info  # Importing display objects and constants
from utils import event_handler, display_dynamic_text, underline_text  # Importing utility functions to handle events and display text

def buffon_info():
    """
    Displays information about Buffon's experiment.

    Parameters:
        None

    Returns:
        True if the user clicks anywhere to start,
        False if the user clicks the menu button.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get screen width and height
    title_font = pygame.font.Font(FONT, screen_height // 15)  # Font for the title
    text_font = pygame.font.Font(FONT, screen_height // 33)  # Font for the explanatory text

    # Title text for the information screen
    title_text = "Buffon's Needle Experiment"

    # Description text of the experiment
    description_text = (
        "Buffon's experiment is a probabilistic method to estimate π by throwing needles "
        "onto a floor with parallel lines. The ratio between the needles crossing a line and "
        "the total number of needles gives an approximation of π."
    )

    # Text containing the formula used in the experiment
    formula_text = (
        "The formula used is:",
        "π ≈ (2 × needle length × total number of needles) / (number of needles crossing a line × line spacing)."
    )

    # Text describing the simulation visualization
    visualization_text = (
        "Visualization:",
        "• In this simulation, needles are continuously thrown onto the screen.",
        "• Needles crossing a line are shown in red, while those that don't remain gray.",
        "• User input allows changing the experiment speed."
    )

    while True:
        screen.fill(BLACK)  # Fill the screen with black

        # Display the title
        title_rendered = title_font.render(title_text, True, WHITE)  # Render the title in white
        screen.blit(title_rendered, (screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40))  # Center the title
        underline_text(screen, title_rendered, screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40)  # Underline the title

        # Display the descriptions
        y_position = screen_height // 6 if screen_height <= screen_info.current_h * 0.9 else screen_height // 5
        # Display the description text
        y_position += display_dynamic_text(screen, description_text, screen_width // 15, y_position, 15, screen_width * 0.85, text_font) + screen_height // 50
        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 30  # Add space depending on fullscreen or not
        # For each formula line, display it in blue
        for line in formula_text:
            y_position += display_dynamic_text(screen, line, screen_width // 15, y_position + 15, 15, screen_width * 0.85, text_font, BLUE, underline=True if line == "The formula used is:" else False) + screen_height // 50
        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 30  # Add space depending on fullscreen or not
        # Display the visualization text
        for line in visualization_text:
            y_position += display_dynamic_text(screen, line, screen_width // 15, y_position + 15, 15, screen_width * 0.85, text_font, underline=True if line == "Visualization:" else False) + screen_height // 50

        # Prepare and display the instruction to start
        instruction_rendered = title_font.render("Click anywhere to start.", True, RED)
        screen.blit(instruction_rendered, (screen_width // 2 - instruction_rendered.get_width() // 2, screen_height * 0.92))

        menu_button()  # Display the menu button
        close_cross()  # Display the close cross
        pygame.display.update()  # Update the display

        # Handle user events
        button_event, _ = event_handler()
        if button_event == "menu":  # If the user clicks the menu button
            return False  # Return to menu
        if button_event == "click":  # If the user clicks anywhere
            return True  # Return True to continue

def buffon():
    """
    Runs Buffon's needle experiment simulation.

    Parameters:
        None

    Returns:
        Nothing. The function runs in a loop until the user exits.
    """
    if not buffon_info():  # Displays the information screen and checks if the user goes back to the menu
        return  # Return to menu
    # Get the display window dimensions
    screen_width, screen_height = screen.get_width(), screen.get_height()
    screen.fill(WHITE)  # Fill the screen with white at the start of the simulation
    font = pygame.font.Font(FONT, screen_height // 25)  # Initialize the font for statistics display

    needle_count = 0  # Total number of needles thrown
    needles_crossing = 0  # Number of needles crossing a line
    needle_length = 50  # Length of a needle
    line_spacing = 50   # Spacing between lines
    needles = []  # List to store each needle's information

    needle_lifetime = 3  # Lifetime of a needle in seconds
    fade_duration = 1  # Time during which the needle fades (decreases opacity)

    needles_per_second = 20  # Initial speed: needles generated per second
    last_time = time.perf_counter()  # Record current time for generation timing

    text_input = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)  # Input box to change speed

    needle_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)  # Create a transparent surface to draw the needles

    while True:
        screen.fill(WHITE)  # Fill the screen with white on each iteration

        # Draw the horizontal grid lines
        for y_line in range(0, screen_height, line_spacing):
            pygame.draw.line(screen, BLACK, (0, y_line), (screen_width, y_line), 2)

        # Get user events
        button_event, events = event_handler()
        if button_event == "menu":  # If the user clicks the menu button
            return  # Return to menu
        if button_event == 'info':  # If the user clicks the info button
            if not buffon_info():  # Show the info screen again
                return  # Return to menu if they click menu button from info function
        for event in events:
            # If the Enter key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if text_input.value.isdigit():  # If it's numbers
                    needles_per_second = max(1, int(text_input.value))  # Update speed (minimum 1)
                text_input.value = ""  # Reset input box

        text_input.update(events)  # Update input with recent events
        if len(text_input.value) > 5:  # Limit input to 5 characters
            text_input.value = text_input.value[:5]

        current_time = time.perf_counter()  # Get the current time with a precise time function
        interval = 1 / max(1, needles_per_second)  # Calculate the interval between throws

        new_needles = []  # List to store needles generated this iteration

        # Generate needles while enough time has passed for a new throw
        while current_time - last_time >= interval:
            last_time += interval  # Update last throw time

            # Generate random center coordinates for the needle in the display area
            x_center = random.uniform(needle_length / 2, screen_width - needle_length / 2)
            y_center = random.uniform(needle_length / 2, screen_height - needle_length / 2)
            angle = random.uniform(0, math.pi)  # Generate random angle between 0 and π

            # Calculate the two endpoints of the needle
            x1 = x_center - (needle_length / 2) * math.cos(angle)
            y1 = y_center - (needle_length / 2) * math.sin(angle)
            x2 = x_center + (needle_length / 2) * math.cos(angle)
            y2 = y_center + (needle_length / 2) * math.sin(angle)

            # Check if the needle crosses a line by comparing vertical positions
            crosses_line = int(y1 // line_spacing) != int(y2 // line_spacing)
            color = RED if crosses_line else GRAY  # Choose red if crossing, else gray
            # Add the generated needle with its properties to the list of new needles
            new_needles.append({'p1': (x1, y1), 'p2': (x2, y2), 'color': color, 'time': time.perf_counter(), 'opacity': 255})

            if crosses_line:  # If the needle crosses a line
                needles_crossing += 1  # Increment crossing needle counter
            needle_count += 1  # Increment total needle counter

        # Remove needles that exceeded their lifetime
        needles = [needle for needle in needles if time.perf_counter() - needle['time'] < needle_lifetime]

        needles.extend(new_needles)  # Add new needles to the global list

        # Reset the needle surface with full transparency to redraw
        needle_surface.fill((0, 0, 0, 0))

        for needle in needles:
            # Calculate time elapsed since needle creation
            elapsed_time = time.perf_counter() - needle['time']

            # If the needle is not yet in fade phase, opacity stays at 255
            if elapsed_time < (needle_lifetime - fade_duration):
                opacity = 255
            else:
                # Calculate time spent in fade phase and adjust opacity accordingly
                fade_time = elapsed_time - (needle_lifetime - fade_duration)
                opacity = max(0, int(255 * (1 - fade_time / fade_duration)))
            needle['opacity'] = opacity  # Update needle's opacity in its dictionary
            needle_color = (*needle['color'], opacity)  # Combine base color with opacity to get RGBA color
            pygame.draw.line(needle_surface, needle_color, needle['p1'], needle['p2'], 2)  # Draw the needle on the surface

        screen.blit(needle_surface, (0, 0))  # Blit the needle surface onto the main screen

        # Calculate the π estimation according to Buffon's formula, if at least one needle crosses a line
        pi_estimate = (2 * needle_length * needle_count) / (needles_crossing * line_spacing) if needles_crossing > 0 else 0

        # Create a transparent surface to display text information
        text_surface = pygame.Surface((screen.get_width(), 300), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 100))  # Fill the surface with semi-transparent black

        # Prepare the statistic display texts
        text_pi = font.render(f"Estimation of π: {pi_estimate:.6f}", True, WHITE)
        text_needle_count = font.render(f"Needles thrown: {needle_count}", True, WHITE)
        text_crossings = font.render(f"Needles crossing a line: {needles_crossing}", True, WHITE)
        text_speed = font.render(f"Needles/sec: {needles_per_second}", True, WHITE)
        text_input_label = font.render("Change speed:", True, WHITE)

        # Display the text surface and stats on the screen
        screen.blit(text_surface, (0, 0))
        screen.blit(text_pi, (20, 50 - 25 - text_pi.get_height() // 2))
        screen.blit(text_needle_count, (20, 100 - 25 - text_needle_count.get_height() // 2))
        screen.blit(text_crossings, (20, 150 - 25 - text_crossings.get_height() // 2))
        screen.blit(text_speed, (20, 200 - 25 - text_speed.get_height() // 2))
        screen.blit(text_input_label, (20, 250 - 25 - text_input_label.get_height() // 2))
        screen.blit(text_input.surface, (20, 300 - 25 - 25 // 2))

        info_button()  # Display the information button
        menu_button()  # Display the menu button
        close_cross()  # Display the close cross
        pygame.display.update()  # Update the display
