# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Main import of the pygame library
import pygame_textinput  # Allows text input in pygame
import gmpy2  # Handles high-precision arithmetic
from gmpy2 import mpfr, sqrt  # mpfr and sqrt for arbitrary precision floats
from display import screen, FONT, WHITE, BLACK, GRAY, RED, BLUE, menu_button, close_cross, info_button, screen_info  # Display objects/constants
from utils import elapsed_time, event_handler, check_pi_estimation, display_dynamic_text, display_result, underline_text  # Utility functions

def estimated_borwein_time(decimal_count, format=True):
    """
    Function that gives an estimated calculation time for a given number of decimals using Borwein's method.
    Parameters:
        decimal_count: Number of π decimals to compute
        format: Boolean; True for HH:MM:SS format, False for float
    Returns:
        A string (if format=True) or a float (if format=False) corresponding to the estimated time.
    """
    estimated_calc_time = 6.67e-8 * decimal_count**1.23  # Empirical time estimate (in s)
    if format:
        hours = int(max(estimated_calc_time, 0) // 3600)  # Convert time to full hours
        minutes = int((max(estimated_calc_time, 0) % 3600) // 60)  # Remaining minutes
        seconds = int(max(estimated_calc_time, 0) % 60)  # Remaining seconds
        return f"{hours:02}:{minutes:02}:{seconds:02}"  # Return as HH:MM:SS
    else:
        return estimated_calc_time  # Return raw value in seconds

def borwein_info():
    """
    Function that manages the display of information about the Borwein method.
    Parameters:
        None
    Returns:
        True if click to continue, False if user clicks the menu button.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get screen size
    title_font = pygame.font.Font(FONT, screen_height // 15)  # Font for the title
    text_font = pygame.font.Font(FONT, screen_height // 33)  # Font for normal text

    title_text = "Borwein Method"  # Title to display
    description_text = (
        "The Borwein method, developed by Jonathan and Peter Borwein in 1984, "
        "is a fast iterative algorithm for estimating π. It relies on "
        "quartic convergence, meaning the number of correct decimals doubles "
        "with each iteration. This method is particularly useful for high-precision π calculations, "
        "notably in supercomputer benchmarks and π decimal records."
    )
    formula_text = (
        "Borwein method formulas:",
        "y_(n+1) = (1 - (1 - y_n^4)^(1/4)) / (1 + (1 - y_n^4)^(1/4))",
        "a_(n+1) = a_n * (1 + y_(n+1))^4 - 2^(2n+3) * y_(n+1) * (1 + y_(n+1) + y_(n+1)^2)",
        "π ≈ 1 / a_n"
    )

    while True:  # Main display loop
        screen.fill(BLACK)  # Black background
        title_render = title_font.render(title_text, True, WHITE)  # Render the title
        screen.blit(title_render, (screen_width // 2 - title_render.get_width() // 2, screen_height // 40))  # Center the title
        underline_text(screen, title_render, screen_width // 2 - title_render.get_width() // 2, screen_height // 40)  # Underline the title

        y_position = screen_height // 5  # Starting vertical position for text
        y_position += display_dynamic_text(screen, description_text, screen_width // 10, y_position, 15, screen_width * 0.8, text_font)  # Display description
        
        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 10  # Add space depending on fullscreen or not

        for line in formula_text:  # Loop through each formula line
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 50, 15, screen_width * 0.8, text_font, BLUE, underline=True if line == "Borwein method formulas:" else False) + screen_height // 50

        instruction_render = title_font.render("Click anywhere to start", True, RED)  # Prompt to click
        screen.blit(instruction_render, (screen_width // 2 - instruction_render.get_width() // 2, screen_height * 0.92))  # Place at bottom

        menu_button()  # Draw menu button
        close_cross()  # Draw close cross
        pygame.display.update()  # Refresh screen

        button_event, _ = event_handler()  # Get user actions
        if button_event == "menu":  # If menu button clicked
            return False  # Return to menu
        if button_event == "click":  # If click anywhere
            return True  # Proceed to next step


def borwein():
    """
    Main function for π calculation using the Borwein method.
    Parameters:
        None
    Returns:
        Nothing. Manages display and calculation logic, then shows results.
    """
    if not borwein_info():  # Show info screen
        return  # Return to menu if clicking inside the info function

    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get screen size
    text_input = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)  # Text input
    decimal_count = None  # Number of decimals not yet defined
    current_decimal_count = 0  # Counter for warnings and time estimates
    estimated_time_display = "Estimated time: -"  # Default estimate message

    title_font = pygame.font.Font(FONT, screen_height // 15)  # Title font
    text_font = pygame.font.Font(FONT, screen_height // 25)  # Standard text font

    while decimal_count is None:  # Wait for valid input
        screen.fill(BLACK)  # Black background
        title = title_font.render("Borwein Method", True, WHITE)  # Render title
        explanation = text_font.render("Enter the number of decimals to calculate (max 300 million):", True, WHITE)  # Explanation text
        time_display = text_font.render(estimated_time_display, True, WHITE)  # Show time estimate
        note = "Note: Actual computation time may vary depending on your machine’s performance."  # Informative note
        warning = "Calculation will not be verified as the reference file contains 100 million decimals."  # Warning if too many decimals

        screen.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 20))  # Place title
        underline_text(screen, title, screen_width // 2 - title.get_width() // 2, screen_height // 20)
        screen.blit(explanation, (screen_width // 2 - explanation.get_width() // 2, screen_height // 3))  # Place explanation
        screen.blit(text_input.surface, (screen_width // 2 - text_input.surface.get_width() // 2, screen_height // 2))  # Input box
        screen.blit(time_display, (screen_width // 2 - time_display.get_width() // 2, screen_height // 2.5))  # Time estimate

        display_dynamic_text(screen, note, 0, screen_height // 1.7, 15, screen_width * 0.99, text_font)  # Display note

        if current_decimal_count > 100000000:  # If over 100 million
            display_dynamic_text(screen, warning, 0, screen_height // 1.3, 15, screen_width * 0.99, text_font, RED)  # Warning in red

        info_button()  # Info button
        menu_button()  # Menu button
        close_cross()  # Close cross
        pygame.display.update()  # Refresh screen

        button_event, events = event_handler()  # Get events
        if button_event == "menu":  # If menu button clicked
            return  # Return to menu
        if button_event == "info":  # If info button clicked
            if not borwein_info():  # Show info page again
                return  # Return to menu if clicking menu inside info screen

        text_input.update(events)  # Update input
        if len(text_input.value) > 9:  # Limit input to 10 digits
            text_input.value = text_input.value[:9]  # Truncate

        if text_input.value.isdigit():  # Check if input is number
            current_decimal_count = int(text_input.value)  # Convert
            estimated_time_display = f"Estimated time: {estimated_borwein_time(current_decimal_count)} sec"  # Update estimate
        else:
            estimated_time_display = "Estimated time: -"  # Undefined otherwise

        for event in events:  # Loop through events
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # If Enter key pressed
                if text_input.value.isdigit():  # And input is a number
                    decimal_count = min(300000000, int(text_input.value))  # Validate
                text_input.value = ""  # Reset input box

    screen.fill(BLACK)  # Clear screen
    calc_text = text_font.render("Calculation in progress...", True, WHITE)  # "Calculation in progress" text
    screen.blit(calc_text, (50, 200))  # Placement
    progress = 0.0  # Initial progress

    bar_width = screen_width // 2  # Progress bar width
    bar_height = 30  # Bar height
    bar_x = (screen_width - bar_width) // 2  # Horizontal position (centered)
    bar_y = screen_height // 2  # Vertical position (middle)
    filled_width = int(bar_width * progress)  # Start at 0%

    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))  # Draw empty bar
    pygame.draw.rect(screen, (255, 255, 50), (bar_x, bar_y, filled_width, bar_height))  # Fill yellow
    warning_text = pygame.font.Font(FONT, screen_height // 34).render("Warning: Please do not click the screen during a long computation!", True, WHITE)
    screen.blit(warning_text, (screen_width // 2 - warning_text.get_width() // 2, screen_height // 1.05))
    progress_text = text_font.render(f"{int(progress * 100)}%", True, WHITE)  # Show 0%
    screen.blit(progress_text, (screen_width // 2 - progress_text.get_width() // 2, bar_y - screen_height // 20))  # % position
    pygame.display.update()  # Refresh

    start_time = pygame.time.get_ticks()  # Note start time
    gmpy2.get_context().precision = int(decimal_count * 3.32193) + 50  # Set gmpy2 precision with extra margin

    y = sqrt(mpfr(2)) - 1  # Initialize y
    a = mpfr(6) - mpfr(4) * sqrt(mpfr(2))  # Initialize a

    iteration_count = max(1, (decimal_count.bit_length() // 2 + 1))  # Estimated iteration count

    for i in range(iteration_count):  # Calculation loop
        y_quarter_root = gmpy2.root(1 - y**4, 4)  # 4th root of (1 - y^4)
        y_next = (1 - y_quarter_root) / (1 + y_quarter_root)  # Update y
        a = a * (1 + y_next)**4 - 2**(2 * i + 3) * y_next * (1 + y_next + y_next**2)  # Update a
        y = y_next  # New y

        progress = (i + 1) / iteration_count  # Progress percentage
        filled_width = int(bar_width * progress)  # Bar fill width
        screen.fill(BLACK)  # Clear screen
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))  # Gray bar
        pygame.draw.rect(screen, (255, 255, 50), (bar_x, bar_y, filled_width, bar_height))  # Yellow fill
        progress_text = text_font.render(f"{int(progress * 100)}%", True, WHITE)  # % text
        screen.blit(progress_text, (screen_width // 2 - progress_text.get_width() // 2, bar_y - screen_height // 20))  # Placement
        calc_text = text_font.render("Calculation in progress...", True, WHITE)  # Re-display "in progress"
        screen.blit(calc_text, (50, 200))  # Placement
        screen.blit(warning_text, (screen_width // 2 - warning_text.get_width() // 2, screen_height // 1.05))
        
        pygame.display.update()  # Refresh display

    pi_estimate = mpfr(1) / mpfr(a)  # 1 / a = π estimate
    total_time = elapsed_time(start_time)  # Total duration
    str_pi_estimate = str(pi_estimate)[:decimal_count + 2]  # Truncate string (3. + decimals)
    verification_message = check_pi_estimation(str_pi_estimate, decimal_count)  # Verify with reference

    display_result(str_pi_estimate, total_time, "Borwein", verification_message, decimal_count, borwein_info)  # Show result
