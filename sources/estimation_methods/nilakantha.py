# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Pygame library for managing surfaces, events, display, etc.
import pygame_textinput  # Module to manage editable text input fields in Pygame.
from display import screen, FONT, WHITE, BLACK, RED, BLUE, menu_button, close_cross, info_button, screen_info  # Display components and colors.
from utils import elapsed_time, event_handler, display_dynamic_text, underline_text  # Utility functions


def nilakantha_information():
    """
    Displays an introduction to the Nilakantha method as an explanatory text.
    The user can click the screen to start the interactive calculation or click "menu".

    Parameters:
        None

    Returns:
        bool: True if the user clicks to start, False if they click "menu".
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Window dimensions
    font_title = pygame.font.Font(FONT, screen_height // 15)               # Font for the main title
    font_text = pygame.font.Font(FONT, screen_height // 39)               # Smaller font for the text

    title_text = "Nilakantha Method"  # Main heading
    # General description of the method
    description_text = (
        "The Nilakantha method is an infinite series that improves upon the Leibniz series "
        "by accelerating convergence towards π. Developed in the 15th century by Indian mathematician "
        "Nilakantha Somayaji, it adds and subtracts fractions of the form 4/(n·(n+1)·(n+2)). "
        "Each iteration refines the value of π, offering a faster approximation than the Leibniz series."
    )
    # Mathematical formula illustrating the series
    formula_text = (
        "The formula is:",
        "π ≈ 3 + 4/(2·3·4) - 4/(4·5·6) + 4/(6·7·8) - 4/(8·9·10) + ..."
    )
    # Information on the visualization in the program
    visualization_text = (
        "Visualization:",
        "• The added or subtracted fractions are displayed in real time.",
        "• The last added fraction is marked in red.",
        "• The user input allows adjusting the number of fractions calculated per second."
    )

    while True:  # Display loop for the informative text
        screen.fill(BLACK)  # Clear the screen by filling it black

        # Create and display the title, centered horizontally
        title_render = font_title.render(title_text, True, WHITE)
        screen.blit(title_render, (screen_width // 2 - title_render.get_width() // 2, screen_height // 40))
        underline_text(screen, title_render, screen_width // 2 - title_render.get_width() // 2, screen_height // 40)  # Underline title
        # Starting position for dynamic text display
        y_position = screen_height // 6
        
        # Display the main paragraph describing the method
        y_position += display_dynamic_text(screen, description_text, screen_width // 10, y_position, 15, screen_width * 0.8, font_text)
        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 10

        # Display the formula lines
        for line in formula_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 50, 15, screen_width * 0.8, font_text, BLUE, underline=True if line == "The formula is:" else False) + screen_height // 50

        y_position += screen_height // 18 if screen_height <= screen_info.current_h * 0.9 else screen_height // 10  # Add space depending on fullscreen or not

        # Display the block explaining the visualization
        for line in visualization_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 40, 15, screen_width * 0.8, font_text, underline=True if line == "Visualization:" else False) + screen_height // 50

        # Invite the user to click to start
        instruction_render = font_title.render("Click anywhere to start", True, RED)
        screen.blit(instruction_render, (screen_width // 2 - instruction_render.get_width() // 2, screen_height * 0.92))

        # Draw menu button, close cross, and update display
        menu_button()
        close_cross()
        pygame.display.update()

        # Handle events
        button_event, _ = event_handler()
        if button_event == "menu":  # If menu button clicked
            return False  # Return to menu
        if button_event == "click":  # If clicked anywhere on screen
            return True  # Proceed to the method


def nilakantha():
    """
    Launches the Nilakantha method demonstration to calculate π,
    with real-time display of added or subtracted fractions.
    The user can also adjust the number of fractions calculated per second.

    Parameters: None
    Returns: Nothing (exits if "menu" or after re-displaying the info).
    """
    # First, display the introduction
    if not nilakantha_information():
        return  # Return to menu if clicked menu in info screen

    # Get window dimensions for display calibration
    screen_width, screen_height = screen.get_width(), screen.get_height()

    # Fonts for title, general text, and fraction display
    font_title = pygame.font.Font(FONT, screen_width // 25)
    font_text = pygame.font.Font(FONT, screen_width // 35)
    font_fraction = pygame.font.Font(FONT, screen_width // 30)

    # Clear the screen and show main title
    screen.fill(BLACK)

    # Initialize sum: Nilakantha starts at 3, then adds/subtracts 4 / (n(n+1)(n+2))
    pi_estimate = 3
    denominator = 2  # This is n in the formula, starts at 2 (for 4/(2*3*4))
    add = True       # Boolean indicating if we add or subtract the term
    steps = 0        # Total number of calculated steps
    fraction_history = []  # List to store recent fractions for display

    # Input field to modify number of iterations (fractions) calculated per second
    text_input = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)
    iterations_per_second = 100  # Default value

    # Record start time to measure elapsed time and last update time to manage calculation interval
    start_time = pygame.time.get_ticks()
    last_time = pygame.time.get_ticks()

    while True:
        # Get actions (buttons) and events
        button_event, events = event_handler()
        if button_event == "menu":  # If user clicks the menu button
            return  # Return to menu
        if button_event == "info":  # If user clicks the info button, re-display intro
            if not nilakantha_information():
                return  # Return to menu if clicked menu in info screen

        # Go through Pygame events to manage text input
        for event in events:
            # If user presses 'Enter'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # If input value is an integer
                if text_input.value.isdigit():
                    # Limit the value between 1 and 1000 to avoid excess
                    iterations_per_second = min(1000, max(1, int(text_input.value)))
                # Clear the input field once value is retrieved
                text_input.value = ""

        # Update the input field
        text_input.update(events)
        # Limit input length (max 4 characters)
        if len(text_input.value) > 4:
            text_input.value = text_input.value[:4]

        # Manage time interval between two series updates
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        time_interval = 1000 / iterations_per_second  # Duration in ms between two calculations

        # If enough time has passed since last update
        if delta_time >= time_interval:
            # Calculate the term 4 / (n(n+1)(n+2))
            term = 4 / (denominator * (denominator + 1) * (denominator + 2))
            # Prepare a string representing the fraction (for display)
            fraction = f" 4 / ({denominator} × {denominator + 1} × {denominator + 2})"

            # Add or subtract this term to/from pi_estimate, alternating logic
            if add:
                pi_estimate += term
                fraction = "+ " + fraction
            else:
                pi_estimate -= term
                fraction = "- " + fraction

            # Alternate the add/subtract state
            add = not add
            # Advance by 2 in the formula: (2 -> 4 -> 6 -> 8, etc.)
            denominator += 2

            # Store this fraction in the history
            fraction_history.append(fraction)
            # Keep only the 8 most recent fractions for display
            if len(fraction_history) > 8:
                fraction_history = fraction_history[-8:]

            # One more step done
            steps += 1
            # Update last_time
            last_time = current_time

        # Clear the screen
        screen.fill(BLACK)

        # Display the history of fractions, starting from the most recent
        y_position = screen_height // 1.46
        index_fractions = 0
        for fraction in reversed(fraction_history):
            color = RED if index_fractions == 0 else WHITE  # Most recent fraction (index 0) is red, others white
            fraction_text = font_fraction.render(fraction, True, color)  # Render the fractions
            screen.blit(fraction_text, (screen_width // 2 - fraction_text.get_width() // 2, y_position))  # Place fractions
            y_position -= screen_height // 20  # Stack them vertically
            index_fractions += 1

        # Text showing number of steps, pi value, elapsed time, and iterations per second
        step_text = font_text.render(f"Step: {steps}", True, WHITE)
        pi_text = font_title.render(f"π estimate: {pi_estimate:.15f}", True, WHITE)
        time_text = font_text.render(f"Elapsed time: {elapsed_time(start_time)}", True, WHITE)
        iter_per_sec_text = font_text.render(f"Iterations per second: {iterations_per_second}", True, WHITE)

        # Place these texts on screen
        screen.blit(step_text, ((screen_width - step_text.get_width()) // 2, screen_height // 8))
        screen.blit(pi_text, (screen_width // 2 - pi_text.get_width() // 2, screen_height // 5))
        screen.blit(time_text, ((screen_width - time_text.get_width()) // 2, screen_height // 20))
        screen.blit(iter_per_sec_text, ((screen_width - iter_per_sec_text.get_width()) // 2, screen_height * 0.9))

        # Input section to modify 'iterations_per_second'
        input_label = font_text.render("Enter iterations per second:", True, WHITE)
        screen.blit(input_label, ((screen_width - input_label.get_width()) // 2, screen_height * 0.8))
        screen.blit(text_input.surface, ((screen_width - text_input.surface.get_width()) // 2, screen_height * 0.865))

        # Info, menu, and close buttons
        info_button()
        menu_button()
        close_cross()

        # Final screen update
        pygame.display.update()
