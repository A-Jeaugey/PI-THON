#Project: PI-THON
#Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Imports the Pygame library for window, display, and events.
import pygame_textinput  # Provides an interactive text field in Pygame.
import gmpy2  # Library offering high-precision calculations.
from gmpy2 import mpfr, sqrt  # mpfr for precision, sqrt for square root.
from display import screen, FONT, WHITE, BLACK, GRAY, RED, BLUE, menu_button, close_cross, info_button, screen_info  # Import of screen, font, colors, and display functions.
from utils import elapsed_time, event_handler, check_pi_estimation, display_dynamic_text, display_result, underline_text  # Utility functions (time, events, verification, etc.).

def gauss_legendre_estimated_time(decimal_count, format=True):
    """
    Estimates the computation time for the Gauss-Legendre (Brent-Salamin) method using an empirical formula.
    
    Parameters:
        decimal_count (int): Number of decimals to compute.
        format (bool): If True, returns result in 'HH:MM:SS' format. Otherwise, returns float (seconds).
    
    Returns:
        str or float: A 'HH:MM:SS' string or a float in seconds, depending on 'format'.
    """
    estimated_time = 1.00e-7 * decimal_count**1.184  # Empirical relation to estimate computation time
    if format:  # If we want HH:MM:SS format.
        hours, minutes, seconds = int(max(estimated_time, 0)//3600), int((max(estimated_time, 0)%3600)//60), int(max(estimated_time, 0)%60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"  # Return formatted string.
    else:  # Otherwise, return float in seconds.
        return estimated_time

def gauss_legendre_information():
    """
    Displays an information screen about the Gauss-Legendre (Brent-Salamin) method.
    Waits for a click to continue, or a click on 'menu' to cancel.
    
    Parameters:
        None.
    
    Returns:
        bool:
        - True if user clicks inside the window (continue),
        - False if user clicks on the menu button.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window size.
    title_font = pygame.font.Font(FONT, screen_height // 15)  # Font for title.
    text_font = pygame.font.Font(FONT, screen_height // 42)  # Font for explanatory text.
    title_text = "Gauss-Legendre / Brent-Salamin"  # Method title.
    description_text = (  # Explanation about the method.
        "The Gauss-Legendre method, also known as the Brent-Salamin formula, is an iterative algorithm that calculates "
        "π decimals with high precision. Developed from the work of Carl Friedrich Gauss and Adrien-Marie Legendre, "
        "it relies on the use of arithmetic and geometric means to progressively refine the value of π. "
        "This method is particularly used for calculations requiring very high precision, especially in π decimal records "
        "and performance testing of computer systems."
    )
    formula_text = (  # Mathematical formulas of the Gauss-Legendre algorithm.
        "Formulas of the Gauss-Legendre algorithm:",
        "a_n+1 = (a_n + b_n) / 2",
        "b_n+1 = sqrt(a_n * b_n)",
        "t_n+1 = t_n - p_n * (a_n - a_n+1)^2",
        "p_n+1 = 2 * p_n",
        "π ≈ (a_n + b_n)^2 / (4 * t_n)"
    )
    while True:  # Display loop until click or 'menu'.
        screen.fill(BLACK)  # Clear screen in black.
        title_rendered = title_font.render(title_text, True, WHITE)  # Text surface for title.
        screen.blit(title_rendered, (screen_width//2 - title_rendered.get_width() // 2, screen_height // 20))  # Place title at top.
        underline_text(screen, title_rendered, screen_width // 2 - title_rendered.get_width() // 2, screen_height // 20)  # Underline title

        y_position = screen_height // 5  # Starting height position for text.

        y_position += display_dynamic_text(screen, description_text, screen_width//10, y_position, 15, screen_width*0.8, text_font)  # Display description.
        y_position += screen_height // 50 if screen_height <= screen_info.current_h * 0.9 else screen_height // 10  # Add space depending on fullscreen
        for line in formula_text:  # Display each formula line.
            y_position += display_dynamic_text(screen, line, screen_width//10, y_position+40, 15, screen_width*0.8, text_font, BLUE, underline=True if line == "Formulas of the Gauss-Legendre algorithm:" else False) + 15

        instruction_rendered = title_font.render("Click anywhere to start", True, RED)  # Text inviting user to continue
        screen.blit(instruction_rendered, (screen_width//2 - instruction_rendered.get_width()//2, screen_height*0.92))  # Place at bottom.

        menu_button()  # Draw menu button.
        close_cross()  # Draw close cross.
        pygame.display.update()  # Update display.
        
        button_event, _ = event_handler()  # Get events
        if button_event == "menu":  # If 'menu' clicked.
            return False  # Return to menu
        if button_event == "click":  # If window clicked.
            return True  # Continue


def gauss_legendre():
    """
    Launches the π calculation using the Gauss-Legendre method and displays the final result.
    
    Parameters:
        None.
    
    Returns:
        Nothing. Exits the function when the user returns from the result screen or clicks "menu".
    """
    if not gauss_legendre_information():  # Displays the info screen
        return  # If the menu button is clicked in the info screen, return to menu

    screen_width, screen_height = screen.get_width(), screen.get_height()  # Window dimensions.
    textinput = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)  # Input field.
    decimal_count = None  # Will store the entered decimal count.
    current_decimal_count = 0  # Updated to estimate time live.
    displayed_estimated_time = "Estimated time: -"  # Estimated time display text.
    title_font = pygame.font.Font(FONT, screen_height // 15)  # Title font.
    text_font = pygame.font.Font(FONT, screen_height // 25)  # Text font.

    while decimal_count is None:  # Input loop for decimal count.
        screen.fill(BLACK)  # Clear screen.
        title = title_font.render("Gauss-Legendre Method", True, WHITE)  # Title text surface.
        explanation = text_font.render("Enter the number of decimals to compute (max 300 million):", True, WHITE)  # Explanation text.
        time_display = text_font.render(displayed_estimated_time, True, WHITE)  # Estimated time text.
        note = "Note: actual calculation time may vary depending on your machine's power."  # Note about estimation inaccuracy
        warning = "Calculation won't be verified because the reference file contains only 100 million decimals."  # Warning about reference limit

        screen.blit(title, (screen_width//2 - title.get_width()//2, screen_height//15))  # Place title.
        underline_text(screen, title, screen_width // 2 - title.get_width() // 2, screen_height // 15)
        screen.blit(explanation, (screen_width//2 - explanation.get_width()//2, screen_height//3))  # Place explanation.
        screen.blit(textinput.surface, (screen_width//2 - textinput.surface.get_width()//2, screen_height//2))  # Place input field.
        screen.blit(time_display, (screen_width//2 - time_display.get_width()//2, screen_height//2.5))  # Place estimated time text.
        display_dynamic_text(screen, note, 0, screen_height//1.7, 15, screen_width*0.99, text_font)  # Display note.
        if current_decimal_count > 100000000:  # If over 100 million decimals.
            display_dynamic_text(screen, warning, 0, screen_height//1.3, 15, screen_width*0.99, text_font, RED)  # Show reference limit warning
        info_button()  # "?" button
        menu_button()  # Menu button
        close_cross()  # Close button
        pygame.display.update()  # Update screen.

        button_event, events = event_handler()  # Get action (menu, info, etc.).
        if button_event == "menu":  # If "menu" clicked.
            return  # Return to menu
        if button_event == "info":  # If info clicked.
            if not gauss_legendre_information():  # Redisplay info if needed.
                return  # Return to menu if menu clicked in info screen
        textinput.update(events)  # Update input field.
        if textinput.value.isdigit():  # If input is an integer.
            current_decimal_count = int(textinput.value)  # Update variable.
            displayed_estimated_time = f"Estimated time: {gauss_legendre_estimated_time(current_decimal_count)} sec"  # Calculate estimated time.
        else:
            displayed_estimated_time = "Estimated time: -"  # Else, no estimate.

        for event in events:  # Loop through Pygame events.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # If Enter pressed
                if textinput.value.isdigit():  # If input is an integer
                    decimal_count = min(300000000, int(textinput.value))  # Assign input to decimal count
                textinput.value = ""  # Clear field after validation.
        if len(textinput.value) > 9:  # Limit to 10 characters to avoid huge inputs.
            textinput.value = textinput.value[:9]

    screen.fill(BLACK)  # Clear screen for calculation.
    calc_text = text_font.render("Calculating...", True, WHITE)  # Calculation message.
    screen.blit(calc_text, (50, 200))  # Place message.
    warning_text = pygame.font.Font(FONT, screen_height // 34).render("Warning: Do not click the screen during a long calculation!", True, WHITE)
    screen.blit(warning_text, (screen_width // 2 - warning_text.get_width() // 2, screen_height // 1.05))
    progress = 0.0  # For progress bar.
    bar_width = screen_width // 2  # Bar dimensions.
    bar_height = 30
    bar_x = (screen_width - bar_width)//2
    bar_y = screen_height // 2
    filled_width = int(bar_width * progress)
    # Draw progress bar elements
    pygame.draw.rect(screen, BLACK, (bar_x - 10, bar_y - 10, bar_width + 20, bar_height + 20))
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (255, 255, 50), (bar_x, bar_y, filled_width, bar_height))

    progress_text = text_font.render(f"{int(progress * 100)}%", True, WHITE)  # Percentage text
    screen.blit(progress_text, (screen_width//2 - progress_text.get_width()//2, bar_y - screen_height // 20))
    pygame.display.update()  # Update screen.

    start_ticks = pygame.time.get_ticks()  # Record start time.
    gmpy2.get_context().precision = min(int(decimal_count * 3.32193) + 50, 10**9)  # Adjust precision in bits.

    # Gauss-Legendre variables.
    a = mpfr(1)  # a_0 = 1
    b = mpfr(1) / sqrt(mpfr(2))  # b_0 = 1 / √2
    t = mpfr(1) / 4  # t_0 = 1/4
    p = mpfr(1)  # p_0 = 1

    for i in range(30):  # 30 iterations are usually enough for excellent precision.
        a_next = (a + b) / 2  # (a_n + b_n)/2
        b_next = sqrt(a * b)  # √(a_n b_n)
        t -= p * (a - a_next)**2  # t_n+1 = t_n - p_n (a_n - a_n+1)²
        p *= 2  # p_n+1 = 2 * p_n
        a, b = a_next, b_next  # Update variables.
        progress = (i + 1) / 30  # Compute progress percentage.
        filled_width = int(bar_width * progress)
        screen.fill(BLACK)
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))  # For progress bar
        pygame.draw.rect(screen, (255, 255, 50), (bar_x, bar_y, filled_width, bar_height))
        progress_text = text_font.render(f"{int(progress*100)}%", True, WHITE)  # Percentage text
        screen.blit(progress_text, (screen_width//2 - progress_text.get_width()//2, bar_y - screen_height // 20))
        calc_text = text_font.render("Calculating...", True, WHITE)  # Re-display calc message.
        screen.blit(warning_text, (screen_width // 2 - warning_text.get_width() // 2, screen_height // 1.05))  # Re-display warning
        screen.blit(calc_text, (50, 200))

        pygame.display.update()  # Refresh display

    pi_estimate = (a + b)**2 / (4*t)  # Final formula: π = (a_n + b_n)² / (4 t_n).

    total_time = elapsed_time(start_ticks)  # Formatted elapsed time.

    pi_estimate_str = str(pi_estimate)[:decimal_count + 2]  # Truncate string to keep needed part.

    verification_message = check_pi_estimation(pi_estimate_str, decimal_count)  # Check π estimate.
    
    display_result(pi_estimate_str, total_time, "Gauss-Legendre", verification_message, decimal_count, gauss_legendre_information)  # Show result.
