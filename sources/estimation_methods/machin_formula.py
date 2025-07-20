# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Import pygame library for window management, events, and display.
import pygame_textinput  # Allows creation of interactive text input fields.
import gmpy2  # Library for high-precision calculations.
from gmpy2 import mpfr, atan  # Specific import of useful types and functions (mpfr for precision, atan for Machin formula).
from display import screen, font, FONT, WHITE, BLACK, RED, BLUE, menu_button, close_cross, info_button, screen_info  # Display components and colors.
from utils import elapsed_time, event_handler, check_pi_estimation, display_result, display_dynamic_text, underline_text  # Utilities for time, events, pi checking, etc.

def estimated_machin_time(decimal_count):
    """
    Computes an empirical estimate of the time needed for the Machin method.
    
    Parameters:
        decimal_count (int): The number of decimals to calculate.
    
    Returns:
        str: A string in HH:MM:SS format representing the estimated calculation time.
    
    Notes:
        - The relation used is strictly empirical 
        and may vary depending on the machine or context.
    """
    estimated_calc_time = 6.46e-8 * decimal_count**1.31  # Estimate time based on the number of decimals
    hours, minutes, seconds = int(max(estimated_calc_time, 0) // 3600), int((max(estimated_calc_time, 0) % 3600) // 60), int(max(estimated_calc_time, 0) % 60)  # Convert to hours, minutes, seconds
    return f"{hours:02}:{minutes:02}:{seconds:02}"  # Return formatted string HH:MM:SS

def machin_information():
    """
    Displays an information screen about the Machin method, 
    waiting for the user to click to continue or click "menu".
    
    Parameters:
        None
    
    Returns:
        bool:
        - True if the user clicks in the window (proceeds),
        - False if they click the menu button.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window size
    font_title = pygame.font.Font(FONT, screen_height // 15)  # Large font for title
    font_text = pygame.font.Font(FONT, screen_height // 32)  # Medium font for text

    title_text = "Machin Method"  # Title displayed at the top of the screen

    # Text describing the Machin method (history, principle, use)
    description_text = (
        "The Machin formula is an efficient method to calculate π, "
        "discovered by John Machin in 1706. It relies on the arctangent "
        "identity and allows precise calculation in few iterations. "
        "Historically, it was used to compute 100 decimals of π "
        "at a time when calculations were fully manual! "
        "Today, it remains useful to understand the properties of convergent series "
        "and to test numerical algorithms."
    )

    # Mathematical formula of Machin
    formula_text = (
        "The Machin formula is: ",
        "π ≈ 16 * arctan(1/5) - 4 * arctan(1/239)"
    )

    while True:  # Display loop for Machin introduction
        screen.fill(BLACK)  # Fill screen with black

        # Display the title in white, centered horizontally
        title_render = font_title.render(title_text, True, WHITE)  # Text surface for title
        screen.blit(title_render, (screen_width // 2 - title_render.get_width() // 2, screen_height // 40))  # Place title
        underline_text(screen, title_render, screen_width // 2 - title_render.get_width() // 2, screen_height // 40)  # Underline title

        y_position = screen_height // 5  # Vertical start point for explanatory text
        # Display the paragraph describing Machin's history and principle
        y_position += display_dynamic_text(screen, description_text, screen_width // 10, y_position, 15, screen_width * 0.8, font_text)
        y_position += screen_height // 25 if screen_height <= screen_info.current_h * 0.9 else screen_height // 10  # Add space depending on fullscreen or not
        # Display the two lines describing the formula, in blue
        for line in formula_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 50, 15, screen_width * 0.8, font_text, BLUE, underline=True if line == "The Machin formula is: " else False) + screen_height // 50

        # Prompt user to click to continue
        instruction_render = font_title.render("Click anywhere to start", True, RED)  # Text surface
        screen.blit(instruction_render, (screen_width // 2 - instruction_render.get_width() // 2, screen_height * 0.92))  # Position at bottom

        menu_button()  # Display "menu" button at top right
        close_cross()  # Display cross to close window
        pygame.display.update()  # Update complete display

        # Get button actions and event list
        button_event, _ = event_handler()
        if button_event == "menu":  # If user clicks "menu"
            return False  # Return to menu
        if button_event == "click":  # If user clicks in the window
            return True  # Start the method


def machin():
    """
    Starts the calculation of π using the Machin method.
    
    The user inputs the desired number of decimals. The program then performs 
    a high-precision calculation using gmpy2, displays the result, 
    and checks the validity of the estimation (correct number of decimals).
    
    Parameters:
        None
    
    Returns:
        Nothing (when the user exits the results screen, it returns to the previous menu).
    """
    if not machin_information():  # First display the intro
        return  # Return to menu if clicked in the info function

    # Text input field to get the number of decimals
    text_input = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)
    decimal_count = None  # Initialize variable (None until user validates)
    estimated_time_display = "Estimated time: -"  # Text showing estimated time, updated progressively

    # Get window dimensions
    screen_width, screen_height = screen.get_width(), screen.get_height()

    # Fonts for title and text
    font_title = pygame.font.Font(FONT, screen_height // 15)
    font_text = pygame.font.Font(FONT, screen_height // 25)

    # Loop to ask user for the number of decimals
    while decimal_count is None:
        screen.fill(BLACK)  # Clear screen in black

        title = font_title.render("Machin Method", True, WHITE)  # Text "Machin Method"
        explanation = font_text.render("Enter the number of decimals to calculate:", True, WHITE)  # Explanation text
        time_display = font_text.render(estimated_time_display, True, WHITE)  # Estimated time text (updated if typing a number)
        note = "Note: actual computation time may slightly vary depending on your machine's power."  # Small note

        # Place elements on screen
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 20))
        underline_text(screen, title, screen_width // 2 - title.get_width() // 2, screen_height // 20)
        screen.blit(explanation, (screen_width // 2 - explanation.get_width() // 2, screen_height // 3))
        screen.blit(text_input.surface, (screen_width // 2 - text_input.surface.get_width() // 2, screen_height // 2))
        screen.blit(time_display, (screen_width // 2 - time_display.get_width() // 2, screen_height // 2.5))
        display_dynamic_text(screen, note, 0, screen_height // 1.7, 15, screen_width * 0.99, font_text)

        info_button()  # "info" button
        menu_button()  # "menu" button
        close_cross()  # "close" button
        pygame.display.update()  # Update window

        # Get action and event list
        button_event, events = event_handler()
        if button_event == "menu":  # If user clicks "menu"
            return  # Return to menu
        if button_event == "info":  # If clicks "info", re-display intro
            if not machin_information():
                return  # Return to menu if clicked in info function

        # Update text input based on events
        text_input.update(events)
        if len(text_input.value) > 8:
            text_input.value = text_input.value[:8]  # Limit to avoid overly long inputs

        # If input is a number, compute estimated time
        if text_input.value.isdigit():
            current_decimal_count = int(text_input.value)  # User input used here to display real-time time estimation
            estimated_time_display = f"Estimated time: {estimated_machin_time(current_decimal_count)} sec"  # Update estimated time text in real-time
        else:
            estimated_time_display = "Estimated time: -"  # Default text if nothing entered

        # If user validates with Enter
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # If value is an integer
                if text_input.value.isdigit():
                    decimal_count = int(text_input.value)  # User input becomes decimal count
                text_input.value = ""  # Clear text field after validation

    # Once decimal count is entered, start calculation
    screen.fill(BLACK)
    calculating_text = font.render("Calculating...", True, WHITE)
    screen.blit(calculating_text, (50, screen_height // 2.3))  # Visually indicate calculation start
    display_dynamic_text(screen, "Warning: Please do not click on the screen during calculation!", 50, screen_height // 2, 15, screen_width * 0.92, font_text, WHITE, False)
    pygame.display.update()  # Update display

    # Note start time
    start_ticks = pygame.time.get_ticks()

    # Set precision for gmpy2:
    # We take ~ log2(10) ~ 3.32193 bits per decimal, plus a margin
    gmpy2.get_context().precision = int(decimal_count * 3.32193) + 50

    # First compute arctan(1/5) and arctan(1/239)
    arctan_1_5 = atan(mpfr('1') / 5)
    arctan_1_239 = atan(mpfr('1') / 239)

    # Then the formula: pi = 4*(4*arctan(1/5) - arctan(1/239))
    pi_estimation = 4 * (4 * arctan_1_5 - arctan_1_239)

    # Total elapsed time
    total_time = elapsed_time(start_ticks)

    # Convert to string, keeping "decimal_count + 2" (for "3.")
    pi_estimation_str = str(pi_estimation)[:decimal_count + 2]

    # Check estimation accuracy by comparing to reference file
    verification_message = check_pi_estimation(pi_estimation_str, decimal_count)

    # Display final result (pages, text, verification, etc.)
    display_result(pi_estimation_str, total_time, "Machin", verification_message, decimal_count, machin_information)
