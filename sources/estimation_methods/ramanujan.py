# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Pygame library for window, event, and display management.
import pygame_textinput  # Allows creating interactive text input fields in Pygame.
import gmpy2  # High-precision calculation library.
from gmpy2 import mpfr, sqrt  # Specific import for precision (mpfr) and square root (sqrt).
from display import screen, FONT, WHITE, BLACK, GRAY, RED, BLUE, menu_button, close_cross, info_button, screen_info  # Display components and colors.
from utils import elapsed_time, event_handler, check_pi_estimation, display_result, display_dynamic_text, underline_text  # Utility functions (time, events, pi check, etc.)

def estimated_time_ramanujan(decimal_count, formatted=True):
    """
    Calculates an empirical estimate of computation time for Ramanujan's method.

    Parameters:
        decimal_count (int): Number of decimals to compute.
        formatted (bool): If True, returns 'HH:MM:SS' string; if False, returns float in seconds.

    Returns:
        str or float: Estimated time as 'HH:MM:SS' if formatted=True, or as float seconds otherwise.
    """
    estimated_calc_time = 3.01e-10 * decimal_count**2.253  # Empirical relation; may vary depending on actual machine power.
    if formatted:
        hours = int(max(estimated_calc_time, 0) // 3600)  # Calculate full hours.
        minutes = int((max(estimated_calc_time, 0) % 3600) // 60)  # Calculate remaining minutes.
        seconds = int(max(estimated_calc_time, 0) % 60)  # Calculate remaining seconds.
        return f"{hours:02}:{minutes:02}:{seconds:02}"  # Return as formatted string.
    else:
        return estimated_calc_time  # Return as float seconds.

def ramanujan_information():
    """
    Displays an information screen about Ramanujan's formula,
    looping until user clicks (or presses 'menu').

    Parameters:
        None.

    Returns:
        bool:
        - True if the user clicks anywhere (to continue),
        - False if they click the menu button.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window size.
    font_title = pygame.font.Font(FONT, screen_height // 15)  # Large font for title.
    font_text = pygame.font.Font(FONT, screen_height // 35)  # Smaller font for description.

    title_text = "Ramanujan Formula"  # Title text.
    description_text = (  # Paragraph describing the method.
        "Ramanujan's formula is a fast method to calculate π. "
        "Discovered by Indian mathematician Srinivasa Ramanujan in 1910, "
        "it inspired even more powerful formulas like Chudnovsky's. "
        "It converges quickly (~8 decimals per iteration), but since the formula "
        "includes heavy factorial and power calculations, it's not necessarily "
        "the fastest for small decimal counts."
    )
    formula_text = (  # The actual formula.
        "Ramanujan's formula is:",
        "1/π ≈ (2√2 / 9801) * ∑ [ (4k)! (1103 + 26390k) ] / [ (k!)^4 396^(4k) ]"
    )

    while True:  # Display loop; waits for user click or menu.
        screen.fill(BLACK)  # Fill background black.
        title_render = font_title.render(title_text, True, WHITE)  # Render title text.
        screen.blit(title_render, (screen_width // 2 - title_render.get_width() // 2, screen_height // 40))  # Centered.
        underline_text(screen, title_render, screen_width // 2 - title_render.get_width() // 2, screen_height // 40)  # Underline title.

        y_position = screen_height // 4.5  # Starting y-position.
        y_position += display_dynamic_text(screen, description_text, screen_width // 10, y_position, 15, screen_width * 0.8, font_text)
        y_position += screen_height // 18 if screen_height <= screen_info.current_h * 0.9 else screen_height // 10  # Adjust vertical space depending on fullscreen.

        # Display the formula (in blue).
        for line in formula_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 50, 15, screen_width * 0.8, font_text, BLUE, underline=True if line == "Ramanujan's formula is:" else False) + 20

        instruction_render = font_title.render("Click anywhere to start", True, RED)  # Render red instruction text.
        screen.blit(instruction_render, (screen_width // 2 - instruction_render.get_width() // 2, screen_height * 0.92))  # Centered at bottom.

        menu_button()  # Draw menu button.
        close_cross()  # Draw close cross.
        pygame.display.update()  # Update entire screen.

        button_event, _ = event_handler()  # Get user events.
        if button_event == "menu":
            return False  # Return False if menu clicked.
        if button_event == "click":
            return True  # Return True if anywhere else clicked.


def ramanujan():
    """
    Calculates π using Ramanujan's formula and displays the result.
    The user enters the desired number of decimals, we show a progress bar,
    then display the final estimate and a verification.

    Parameters:
        None.

    Returns:
        Nothing (the function ends after displaying the result).
    """
    if not ramanujan_information():  # Show info screen
        return  # If user clicks menu button in info screen, go back to menu

    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window size.
    text_input = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)  # Input field.
    decimal_count = None  # Will hold the user's entered value.
    current_decimal_count = 0  # For estimated time, updated on each keystroke.
    estimated_time_display = "Estimated time: -"  # Default display with undefined time.

    # Fonts for title and smaller text.
    font_title = pygame.font.Font(FONT, screen_height // 15)
    font_text = pygame.font.Font(FONT, screen_height // 25)

    # Input loop to get the desired number of decimals.
    while decimal_count is None:
        screen.fill(BLACK)  # Clear screen black.

        # Create text surfaces for title and explanations.
        title = font_title.render("Ramanujan Method", True, WHITE)
        explanation = font_text.render("Enter the number of decimals to calculate:", True, WHITE)
        time_display = font_text.render(estimated_time_display, True, WHITE)
        note = "Note: Actual computation time may vary depending on your machine's power."

        # Place these texts on screen (title, explanation, input field, etc.)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 20))
        underline_text(screen, title, screen_width // 2 - title.get_width() // 2, screen_height // 20)
        screen.blit(explanation, (screen_width // 2 - explanation.get_width() // 2, screen_height // 3))
        screen.blit(text_input.surface, (screen_width // 2 - text_input.surface.get_width() // 2, screen_height // 2))
        screen.blit(time_display, (screen_width // 2 - time_display.get_width() // 2, screen_height // 2.5))
        display_dynamic_text(screen, note, 0, screen_height // 1.7, 15, screen_width * 0.99, font_text)

        info_button()  # "?" button
        menu_button()  # "menu" button
        close_cross()  # "close" button
        pygame.display.update()  # Update display.

        # Event handling.
        button_event, events = event_handler()
        if button_event == "menu":  # If user clicks menu button
            return  # Go back to menu
        if button_event == "info":  # If user clicks info button
            if not ramanujan_information():  # Show info page again if desired
                return  # If menu clicked in info screen, go back to menu

        text_input.update(events)  # Update text input field.
        if len(text_input.value) > 7:  # Limit input length to 7 characters
            text_input.value = text_input.value[:7]

        # If user typed only numbers, update time estimate.
        if text_input.value.isdigit():
            current_decimal_count = int(text_input.value)  # Store user input for time estimate
            estimated_time_display = f"Estimated time: {estimated_time_ramanujan(current_decimal_count)} sec"  # Prepare time display
        else:
            estimated_time_display = "Estimated time: -"  # Default text if no number entered.

        # Check if user validates with Enter key
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if text_input.value.isdigit():  # Check if valid number
                    decimal_count = int(text_input.value)  # Confirm decimal count
                text_input.value = ""  # Reset input field

    # Now that we have decimal count, start computation.
    screen.fill(BLACK)  # Clear screen
    calc_text = font_text.render("Calculating...", True, WHITE)  # Small message
    screen.blit(calc_text, (50, 200))  # Position left

    # Prepare progress bar
    progress = 0.0  # Progress percentage
    bar_width = screen_width // 2  # Bar width
    bar_height = 30  # Bar height
    bar_x = (screen_width - bar_width) // 2  # Centered X
    bar_y = screen_height // 2  # Centered Y
    filled_width = int(bar_width * progress)  # Filled pixels (initially 0)

    pygame.draw.rect(screen, BLACK, (bar_x - 10, bar_y - 10, bar_width + 20, bar_height + 20))  # Black border
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))  # Gray bar
    pygame.draw.rect(screen, (255, 255, 50), (bar_x, bar_y, filled_width, bar_height))  # Yellow fill
    progress_text = font_text.render(f"{int(progress * 100)}%", True, WHITE)  # Show "0%"
    screen.blit(progress_text, (screen_width // 2 - progress_text.get_width() // 2, bar_y - screen_height // 20))  # Percentage position
    menu_button()  # Redraw menu button
    close_cross()  # Redraw cross
    pygame.display.update()  # Update screen.

    start_time = pygame.time.get_ticks()  # Note start time
    gmpy2.get_context().precision = int(decimal_count * 3.32193) + 50  # Adjust precision in bits

    ramanujan_sum = mpfr(0)  # Accumulated series sum
    iteration_count = max(3, (decimal_count // 7))  # Approximate number of iterations (~8 decimals per iteration)

    # Loop over each iteration to compute series term
    for index in range(iteration_count):
        term = (gmpy2.fac(4 * index) * (1103 + 26390 * index)) / ((gmpy2.fac(index) ** 4) * (mpfr(396) ** (4 * index)))  # Fast gmpy2 computation
        ramanujan_sum += term  # Add term to sum

        progress = (index + 1) / iteration_count  # Calculate progress percentage
        filled_width = int(bar_width * progress)  # Filled width proportional

        pygame.draw.rect(screen, BLACK, (screen_width // 2 - progress_text.get_width() // 2 - 20, bar_y - 75, progress_text.get_width() + 40, progress_text.get_height() + 40))  # Update percentage area

        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))  # Gray bar
        pygame.draw.rect(screen, (255, 255, 50), (bar_x, bar_y, filled_width, bar_height))  # Fill
        progress_text = font_text.render(f"{int(progress * 100)}%", True, WHITE)  # Percentage text
        screen.blit(progress_text, (screen_width // 2 - progress_text.get_width() // 2, bar_y - screen_height // 20))

        if index % 100 == 0 or index == iteration_count - 1:
            pygame.display.update()  # Refresh screen every 100 iterations to avoid slowdown

        # Check if user clicked "menu" during calculation
        for event in event_handler():
            if event == "menu":
                return None  # If so, abort computation

    # Final formula: factor = (2√2 / 9801), pi = 1 / (factor * sum)
    ramanujan_factor = (2 * sqrt(mpfr(2))) / 9801
    pi_estimate = 1 / (ramanujan_factor * ramanujan_sum)

    total_time = elapsed_time(start_time)  # Total elapsed time
    pi_estimate_str = str(pi_estimate)[:decimal_count + 2]  # Truncate string to desired decimals

    # Check estimate against reference file
    verification_message = check_pi_estimation(pi_estimate_str, decimal_count)

    # Display final result (decimal pages, etc.)
    display_result(pi_estimate_str, total_time, "Ramanujan", verification_message, decimal_count, ramanujan_information)
