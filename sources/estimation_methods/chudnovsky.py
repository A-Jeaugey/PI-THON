#Project: PI-THON
#Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Import of the pygame library (graphical interface)
import pygame_textinput  # Allows text input under pygame
import gmpy2  # Allows arbitrary precision management and advanced operations
from gmpy2 import mpfr  # mpfr to handle high-precision floats
from display import screen, FONT, WHITE, BLACK, GRAY, RED, BLUE, menu_button, close_cross, info_button, screen_info  # Display objects/constants
from utils import elapsed_time, event_handler, check_pi_estimation, display_dynamic_text, display_result, underline_text  # Utility functions

def chudnovsky_estimated_time(decimal_count, format=True):
    """
    Function to estimate the computation time of Chudnovsky
    parameters:
        decimal_count: Number of decimals to calculate for pi.
        format: Boolean indicating whether to return an HH:MM:SS string (True) or a raw number in seconds (False).
    returns:
        A string or float representing the estimated computation time.
    """
    estimated_calc_time = 6.51e-11 * decimal_count**2.26  # Empirical evaluation of time in seconds
    if format:  # If we want to format time as HH:MM:SS
        hours = int(max(estimated_calc_time, 0) // 3600)  # Calculate whole hours
        minutes = int((max(estimated_calc_time, 0) % 3600) // 60)  # Calculate remaining whole minutes
        seconds = int(max(estimated_calc_time, 0) % 60)  # Calculate remaining whole seconds
        return f"{hours:02}:{minutes:02}:{seconds:02}"  # Return the formatted string
    else:
        return estimated_calc_time  # Return the raw numeric value in seconds

def chudnovsky_information():
    """
    Manages the display of information about the Chudnovsky method
    parameters:
        None
    returns:
        True if the user clicks to continue, False if they click the menu button.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get current window size
    title_font = pygame.font.Font(FONT, screen_height // 15)  # Font for the title
    text_font = pygame.font.Font(FONT, screen_height // 33)  # Font for the body text

    title_text = "Chudnovsky Method"  # Title
    # General description of the method
    description_text = (
        "The Chudnovsky formula, developed in 1987 by David and Gregory Chudnovsky, "
        "is an improved variant of Ramanujan's formulas for calculating π. "
        "It relies on an extremely fast mathematical series and adds "
        "14 new decimals with each iteration. "
        "This method is mainly used for π decimal records "
        "and high-precision calculations. Its time complexity is O(n (log n)³), "
        "which makes it very efficient for large numbers with optimizations "
        "like the fast Fourier transform (FFT)."
    )
    # Mathematical formula illustrating the method
    formula_text = (
        "The Chudnovsky formula is given by:",
        "1/π ≈ 12 * ∑ [(-1)^k (6k)! (13591409 + 545140134k)] / [(3k)! (k!)^3 (640320)^(3k + 3/2)]"
    )

    while True:  # Display loop
        screen.fill(BLACK)  # Fill the screen black
        title_rendered = title_font.render(title_text, True, WHITE)  # Prepare the title
        screen.blit(title_rendered, (screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40))  # Center the title
        underline_text(screen, title_rendered, screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40)  # Underline the title

        y_position = screen_height // 5  # Starting position for text
        # Display description with automatic line breaks
        y_position += display_dynamic_text(screen, description_text, screen_width // 10, y_position, 15, screen_width * 0.8, text_font)

        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 10  # Add space depending on fullscreen or not

        # Display each formula line, in blue, with extra margins
        for line in formula_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 50, 15, screen_width * 0.8, text_font, BLUE, underline=True if line == "The Chudnovsky formula is given by:" else False) + screen_height // 30

        instruction_rendered = title_font.render("Click anywhere to start", True, RED)  # Message to start
        # Place this message at the bottom of the screen
        screen.blit(instruction_rendered, (screen_width // 2 - instruction_rendered.get_width() // 2, screen_height * 0.92))

        menu_button()  # Menu button
        close_cross()  # Close button
        pygame.display.update()  # Refresh the display

        button_event, _ = event_handler()  # Get user actions
        if button_event == "menu":  # If the user clicks the menu button
            return False  # Exit returning False
        if button_event == "click":  # If click anywhere in the window
            return True  # Exit returning True (continue)


def chudnovsky():
    """
    Starts the π calculation procedure using the Chudnovsky method
    parameters:
        None
    returns:
        Nothing. Manages display, pi calculation, and final result display.
    """
    if not chudnovsky_information():  # Display info screen; if menu clicked, stop
        return  # If menu button clicked in info screen, return to menu

    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window dimensions
    text_input = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)  # Input box for decimal count
    decimal_count = None  # Variable to store desired decimal count
    current_decimal_count = 0  # Variable for current input
    displayed_estimated_time = "Estimated time: -"  # Default estimated time message

    title_font = pygame.font.Font(FONT, screen_height // 15)  # Font for title
    text_font = pygame.font.Font(FONT, screen_height // 25)  # Font for standard text

    while decimal_count is None:  # While no valid integer entered
        screen.fill(BLACK)  # Clear screen with black background

        # Prepare the various texts
        title = title_font.render("Chudnovsky Method", True, WHITE)
        explanation = text_font.render("Enter the number of decimals to calculate:", True, WHITE)
        time_display = text_font.render(displayed_estimated_time, True, WHITE)
        note = "Note: actual calculation time may vary depending on your machine's power for this method"

        # Position these texts on screen
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 20))
        underline_text(screen, title, screen_width // 2 - title.get_width() // 2, screen_height // 20)
        screen.blit(explanation, (screen_width // 2 - explanation.get_width() // 2, screen_height // 3))
        screen.blit(text_input.surface, (screen_width // 2 - text_input.surface.get_width() // 2, screen_height // 2))
        screen.blit(time_display, (screen_width // 2 - time_display.get_width() // 2, screen_height // 2.5))
        display_dynamic_text(screen, note, 0, screen_height // 1.7, 15, screen_width * 0.99, text_font)

        menu_button()  # Menu button
        close_cross()  # Close button
        info_button()  # Info button
        pygame.display.update()  # Update screen to show all

        button_event, events = event_handler()  # Analyze events
        if button_event == "menu":  # If menu button clicked
            return  # Return to menu
        if button_event == "info":  # If info button clicked
            if not chudnovsky_information():  # Open Chudnovsky info window
                return  # If menu button clicked in info screen, return to menu

        text_input.update(events)  # Update input with current events
        if len(text_input.value) > 7:  # Limit to 7 characters to avoid excessive calculations
            text_input.value = text_input.value[:7]  # Truncate if overflow

        # If the input is an integer
        if text_input.value.isdigit():  # Check if it's a number
            current_decimal_count = int(text_input.value)  # Store user input for time estimate
            displayed_estimated_time = f"Estimated time: {chudnovsky_estimated_time(current_decimal_count)} sec"  # Prepare time display
        else:
            displayed_estimated_time = "Estimated time: -"  # If no number entered, keep default text

        for event in events:  # Loop through events
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Detect Enter key press
                if text_input.value.isdigit():  # Check if it's a number
                    decimal_count = int(text_input.value)  # Validate decimal count
                text_input.value = ""  # Reset input box

    screen.fill(BLACK)  # Clear screen
    calculating_text = text_font.render("Calculating...", True, WHITE)  # Message indicating calculation
    screen.blit(calculating_text, (50, 200))  # Place message
    warning_text = pygame.font.Font(FONT, screen_height // 34).render("Warning: Do not click the screen during long calculations!", True, WHITE)
    screen.blit(warning_text, (screen_width // 2 - warning_text.get_width() // 2, screen_height // 1.05))
    progress = 0.0  # Initial progress at 0%

    # Progress bar parameters
    bar_width = screen_width // 2
    bar_height = 30
    bar_x = (screen_width - bar_width) // 2
    bar_y = screen_height // 2
    filled_width = int(bar_width * progress)

    # Draw progress bar
    pygame.draw.rect(screen, BLACK, (bar_x - 10, bar_y - 10, bar_width + 20, bar_height + 20))
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (255, 255, 50), (bar_x, bar_y, filled_width, bar_height))
    progress_text = text_font.render(f"{int(progress * 100)}%", True, WHITE)  # Display percentage
    screen.blit(progress_text, (screen_width // 2 - progress_text.get_width() // 2, bar_y - screen_height // 20))
    close_cross()  # Show close cross
    menu_button()  # Show menu button
    pygame.display.update()  # Update display

    start_time = pygame.time.get_ticks()  # Note start time
    gmpy2.get_context().precision = int(decimal_count * 3.32193) + 50  # Set gmpy2 precision

    chudnovsky_factor = 12 / (mpfr(640320) ** mpfr(1.5))  # Constant factor 12 / (640320^(3/2))
    chudnovsky_sum = mpfr(0)  # Cumulative sum
    iteration_count = max(6, (decimal_count + 13) // 14)  # Estimate iterations (~14 decimals per iteration)
    numerator_factor = mpfr(1)  # Cumulative numerator factor
    denominator_factor = mpfr(1)  # Cumulative denominator factor

    # Main calculation loop
    for index in range(iteration_count):
        if index > 0:  # From second loop, update multiplicative factors
            numerator_factor *= (6 * index - 5) * (2 * index - 1) * (6 * index - 1)
            denominator_factor *= (index ** 3) * (640320 ** 3 // 24)

        chudnovsky_term = (mpfr((-1) ** index) * numerator_factor * (13591409 + 545140134 * index)) / denominator_factor
        chudnovsky_sum += chudnovsky_term  # Add term to sum

        progress = (index + 1) / iteration_count  # Calculate progress percentage
        filled_width = int(bar_width * progress)  # Update filled part
        pygame.draw.rect(screen, BLACK, (screen_width // 2 - progress_text.get_width() // 2 - 20, bar_y - 75, progress_text.get_width() + 40, progress_text.get_height() + 40))
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))  # Gray bar
        pygame.draw.rect(screen, (255, 255, 50), (bar_x, bar_y, filled_width, bar_height))  # Yellow bar
        progress_text = text_font.render(f"{int(progress * 100)}%", True, WHITE)  # Percentage display
        screen.blit(progress_text, (screen_width // 2 - progress_text.get_width() // 2, bar_y - screen_height // 20))

        button_event, _ = event_handler()  # Check if user wants to return
        if button_event == "menu":  # If menu button clicked
            return  # Return to menu
        if index % 100 == 0 or index == iteration_count - 1:
            pygame.display.update()  # Refresh every 100 iterations or at end to save performance

    pi_estimate = 1 / (chudnovsky_factor * chudnovsky_sum)  # Final 1 / (factor * sum) equals π

    total_time = elapsed_time(start_time)  # Calculate total time
    pi_estimate_str = str(pi_estimate)[:decimal_count + 2]  # Truncate string to desired decimals (+2 = "3.")
    verification_message = check_pi_estimation(pi_estimate_str, decimal_count)  # Compare with reference

    display_result(pi_estimate_str, total_time, "Chudnovsky", verification_message, decimal_count, chudnovsky_information)
