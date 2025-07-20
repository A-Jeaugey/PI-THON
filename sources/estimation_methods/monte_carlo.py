# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import random  # Allows generating random numbers
import pygame  # Library for managing the graphical window and events
import pygame_textinput  # Enables text input in pygame
from display import screen, FONT, WHITE, BLACK, BLUE, RED, GREEN, close_cross, menu_button, info_button, screen_info  # Display objects/constants
from utils import elapsed_time, event_handler, display_dynamic_text, underline_text  # Utility functions (event handling, time, etc.)

def monte_carlo_information():
    """
    Function that manages the display of information about Monte Carlo.
    Parameters:
        None
    Returns:
        True if the user clicks in the window to continue, False if they click the menu button.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window size
    font_title = pygame.font.Font(FONT, screen_height // 15)  # Font adapted for title
    font_text = pygame.font.Font(FONT, screen_height // 39)  # Font adapted for regular text

    # Titles and explanatory texts
    title_text = "Monte Carlo Method"
    description_text = (
        "The Monte Carlo method estimates π by randomly generating points inside a square "
        "containing an inscribed circle. The ratio between points inside the circle and the total "
        "number of points gives an approximation of π."
    )
    formula_text = (
        "The formula used is:",
        "π ≈ 4 × (number of points in the circle) / (total number of points)."
    )
    visualization_text = (
        "Visualization:",
        "• In this implementation, points are colored green if they are inside the circle, and red otherwise.",
        "• The 'points per second' input allows controlling the generation speed.",
        "• The 'Enable fast mode' button switches to a more performant version without display.",
        "• The fast version can generate a large number of points at once, but it also shows that this method "
        "is not really efficient even with a high number of iterations in the experiment."
    )

    while True:  # Display loop
        screen.fill(BLACK)  # Fill screen with black
        # Prepare the title
        title_render = font_title.render(title_text, True, WHITE)
        # Center the title horizontally
        screen.blit(title_render, (screen_width // 2 - title_render.get_width() // 2, screen_height // 40))
        underline_text(screen, title_render, screen_width // 2 - title_render.get_width() // 2, screen_height // 40)  # Underline title

        # Base vertical position
        y_position = screen_height // 7 if screen_height <= screen_info.current_h * 0.9 else screen_height // 5
        # Display first explanatory text (description)
        y_position += display_dynamic_text(screen, description_text, screen_width // 10, y_position, 15, screen_width * 0.8, font_text) + screen_height // 50
        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 18  # Add space depending on fullscreen or not
        # Display formula (in blue to highlight)
        for line in formula_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 15, 15, screen_width * 0.8, font_text, BLUE, underline=True if line == "The formula used is:" else False) + screen_height // 50
        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 18  # Add space depending on fullscreen or not
        # Display second block of explanations (usage, visualization, etc.)
        for line in visualization_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 15, 15, screen_width * 0.8, font_text, underline=True if line == "Visualization:" else False) + screen_height // 50

        # Instruction text inviting user to click to continue
        instruction_render = font_title.render("Click anywhere to start.", True, RED)
        screen.blit(instruction_render, (screen_width // 2 - instruction_render.get_width() // 2, screen_height * 0.92))

        menu_button()  # Menu button
        close_cross()  # Close button
        pygame.display.update()  # Update display

        # Get the user's action
        button_event, _ = event_handler()
        if button_event == "menu":  # If menu button clicked, stop
            return False
        if button_event == "click":  # If clicked anywhere, validate continuation
            screen.fill(BLACK)
            return True


def monte_carlo_detailed(display_info=True):
    """
    Detailed and interactive version of the Monte Carlo method.
    Parameters:
        display_info: Boolean to skip re-displaying info if returning here after fast mode.
    Returns:
        Nothing. Manages calculation and display of Monte Carlo (point by point).
    """
    if display_info:  # Show information if coming not from monte_carlo_fast
        if not monte_carlo_information():  # Show info screen
            return  # Return to menu if clicked on menu button in info screen

    screen.fill(BLACK)  # Clear the screen in black
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Screen size

    total_attempts = 0  # Counter for total points generated
    points_in_circle = 0  # Counter for points inside the circle
    pi = 0  # Initialize variable to hold pi value

    text_input = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)  # Input field for "points per second"
    points_per_second = 20  # Default value

    start_ticks = pygame.time.get_ticks()  # Record start time
    last_time = pygame.time.get_ticks()  # Time of last point generation

    radius = min(screen_width, screen_height) // 3.8  # Determine circle radius (inscribed in screen)
    center_x = screen_width // 2  # Horizontal center
    center_y = screen_height - 50 - radius  # Vertical center, leave space at bottom

    while True:  # Main loop
        button_rect = pygame.Rect(screen_width // 2 - 175, screen_height // 4, 350, 50)  # Button for fast mode

        # Get interactions (UI buttons, pygame events)
        button_event, events = event_handler()
        if button_event == "menu":  # Menu button => return to menu
            return
        if button_event == 'info':  # Info button => re-display description
            if not monte_carlo_information():
                return  # Return to menu if clicked on menu button in info function

        for event in events:  # Go through each event
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if clicked on button to enable fast mode
                if button_rect.collidepoint(event.pos):
                    screen.fill(BLACK)  # Clear screen to display monte_carlo_fast
                    monte_carlo_fast()  # Launch fast version
                    return  # Exit current function to avoid overlap
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # If Enter key pressed
                if text_input.value.isdigit():  # If input is a number
                    points_per_second = min(500, int(text_input.value))  # Assign; limit to 500
                text_input.value = ""  # Reset text input

        text_input.update(events)  # Update input
        if len(text_input.value) > 3:  # Limit input to 3 characters
            text_input.value = text_input.value[:3]

        current_time = pygame.time.get_ticks()  # Get current time
        delta_time = current_time - last_time  # Time since last point
        interval = 1000 / points_per_second  # Interval (ms) between points

        if delta_time >= interval:  # If beyond interval, generate a point
            x = random.uniform(-1, 1)  # Random x coordinate in [-1, 1]
            y = random.uniform(-1, 1)  # Random y coordinate in [-1, 1]

            x_display = int(center_x + x * radius)  # Convert to screen coordinates
            y_display = int(center_y - y * radius)  # Same (invert y-axis)

            if x**2 + y**2 <= 1:  # Check if point is inside circle
                color = GREEN  # GREEN if inside circle
                points_in_circle += 1  # Increment circle point counter
            else:
                color = RED  # RED if outside

            pygame.draw.circle(screen, color, (x_display, y_display), 1)  # Draw point
            total_attempts += 1  # Increment total attempts
            last_time = current_time  # Update last time

        if total_attempts > 0:  # Calculate pi estimate
            pi = 4 * points_in_circle / total_attempts

        # Draw black rectangle to clear info area
        pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height // 4 + 50))
        pygame.draw.rect(screen, WHITE, button_rect)  # Draw 'fast mode' button in white

        font_main = pygame.font.Font(FONT, screen_height // 25)  # Font for display
        font_fixed = pygame.font.Font(FONT, 30)  # Slightly larger font for button text
        animation_display = font_fixed.render("Enable fast mode", True, BLACK)  # Button text

        pi_display = font_main.render(f"Pi estimate: {pi:.6f}", True, WHITE)  # Show 6 decimals
        attempts_display = font_main.render(f"Attempts: {total_attempts}", True, WHITE)
        time_display = font_main.render(f"Elapsed time: {elapsed_time(start_ticks)}", True, WHITE)
        points_per_sec_display = font_main.render(f"Points/s: {points_per_second}", True, WHITE)
        input_text_display = font_main.render("Enter points per second:", True, WHITE)

        # Place texts on screen
        screen.blit(pi_display, (20, screen_height // 50))
        screen.blit(attempts_display, (20, screen_height // 15))
        screen.blit(time_display, (20, screen_height // 9))
        screen.blit(points_per_sec_display, (20, screen_height // 6.5))
        screen.blit(input_text_display, (20, screen_height // 5))
        screen.blit(animation_display, (button_rect.x + button_rect.width // 2 - animation_display.get_width() // 2, button_rect.y + button_rect.height // 2 - animation_display.get_height() // 2))
        screen.blit(text_input.surface, (20, screen_height // 4))

        # Draw circle outline (white)
        pygame.draw.circle(screen, WHITE, (center_x, center_y), radius, 1)
        # Draw surrounding square (white)
        square_rect = (center_x - radius, center_y - radius, radius * 2, radius * 2)
        pygame.draw.rect(screen, WHITE, square_rect, 2)

        info_button()  # Info button
        menu_button()  # Menu button
        close_cross()  # Close button
        pygame.display.update()  # Refresh display


def monte_carlo_fast():
    """
    Optimized version of the Monte Carlo method (calculates multiple points at once, without graphical display).
    Parameters:
        None
    Returns:
        Nothing. Launches a faster Monte Carlo version, without point-by-point display.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Window dimensions
    font_main = pygame.font.Font(FONT, screen_height // 25)  # Font

    point_count = 100000  # Default value
    last_point_count = point_count  # Track if point count changed

    text_input = pygame_textinput.TextInputVisualizer(font_color=BLACK, cursor_color=BLACK)  # Input for point count
    start_ticks = pygame.time.get_ticks()  # Start time

    total_attempts = 0  # Total points drawn
    points_in_circle = 0  # Points inside circle
    pi = 0  # Pi estimate

    while True:  # Main loop
        button_rect = pygame.Rect(screen_width // 2 - 175, screen_height // 4, 350, 50)  # Button to return to display mode

        input_text_display = font_main.render("Enter number of points:", True, BLACK)  # Prompt text

        # Get events
        button_event, events = event_handler()
        if button_event == "menu":  # If menu click
            return  # Return to menu
        if button_event == 'info':  # If info click, re-display description
            if not monte_carlo_information():  # If clicked menu from info screen
                return  # Return to menu

        for event in events:  # Loop through events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if clicked "Return to display" button
                if button_rect.collidepoint(event.pos):
                    screen.fill(BLACK)  # Clear screen to show monte_carlo_detailed
                    monte_carlo_detailed(False)  # Launch animated version without re-displaying info
                    return  # Exit current function to avoid overlap
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # If Enter key
                if text_input.value.isdigit():  # If input is a number
                    point_count = min(5000000, int(text_input.value))  # Limit to 5 million
                text_input.value = ""  # Reset input field

        text_input.update(events)  # Update input
        if len(text_input.value) > 7:  # Limit input to 7 characters
            text_input.value = text_input.value[:7]

        # If user changed point count, reset counters
        if last_point_count != point_count:
            last_point_count = point_count
            total_attempts = 0
            points_in_circle = 0
            pi = 0

        # Generate 'point_count' at once
        for _ in range(point_count):
            x = random.uniform(-1, 1)  # Random x in [-1, 1]
            y = random.uniform(-1, 1)  # Random y in [-1, 1]

            if x**2 + y**2 <= 1:  # Check if inside circle
                points_in_circle += 1  # Increment in-circle count

        # Update total count and compute new π estimate
        total_attempts += point_count
        pi = 4 * (points_in_circle / total_attempts)

        screen.fill(WHITE)  # White background
        pygame.draw.rect(screen, BLACK, button_rect)  # Draw button in black
        font_fixed = pygame.font.Font(FONT, 30)  # Fixed font for button

        # Prepare texts to display
        pi_display = font_main.render(f"Pi estimate: {pi:.10f}", True, BLACK)
        attempts_display = font_main.render(f"Attempts: {total_attempts}", True, BLACK)
        time_display = font_main.render(f"Elapsed time: {elapsed_time(start_ticks)}", True, BLACK)
        n_point_display = font_main.render(f"Points generated: {point_count}", True, BLACK)
        button_text_display = font_fixed.render("Return to display", True, WHITE)

        # Place texts
        screen.blit(pi_display, (20, screen_height // 50))
        screen.blit(attempts_display, (20, screen_height // 15))
        screen.blit(time_display, (20, screen_height // 9))
        screen.blit(n_point_display, (20, screen_height // 6.5))
        screen.blit(input_text_display, (20, screen_height // 5))
        # Place text on button
        screen.blit(button_text_display, (button_rect.x + button_rect.width // 2 - button_text_display.get_width() // 2, button_rect.y + button_rect.height // 2 - button_text_display.get_height() // 2))
        screen.blit(text_input.surface, (20, screen_height // 4))

        info_button()  # Info button
        menu_button()  # Menu button
        close_cross()  # Close button
        pygame.display.update()  # Refresh screen
