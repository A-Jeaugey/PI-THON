# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Importing pygame for display and event management
import pygame_textinput  # Importing pygame_textinput to handle text input in pygame
import math  # Importing math for mathematical functions (sin, cos, etc.)
from display import screen, FONT, WHITE, BLACK, RED, BLUE, GRAY, menu_button, close_cross, info_button, screen_info  # Importing display objects, fonts, and icons
from utils import event_handler, display_dynamic_text, elapsed_time, underline_text  # Importing utility functions for event handling, text display, and time measurement

def pendulum_information():
    """
    Displays an information screen for the simple pendulum method.
    
    Parameters:
        None
        
    Returns:
        True if the user clicks to start, False if they click menu.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window dimensions
    font_title = pygame.font.Font(FONT, screen_height // 15)  # Initialize font for the title
    font_text = pygame.font.Font(FONT, screen_height // 40)  # Initialize font for explanatory text

    title_text = "Simple Pendulum Method"  # Set the title text

    description_text = (  # Description of the simple pendulum method
        "The simple pendulum method is a classic physical approach "
        "to estimate the value of π, based on the experimental measurement of the period "
        "of a pendulum swinging with a small amplitude."
    )

    formula_text = (  # Text containing the simple pendulum formula
        "The period of a simple pendulum is given by:",
        "T ≈ 2π × √(L / g)",
        "• T is the pendulum period (time for a full back-and-forth).",
        "• L is the pendulum length (in meters).",
        "• g ≈ 9.81 m/s² is the Earth's gravitational acceleration."
    )

    pi_calculation_text = (  # Text explaining how to isolate π from the measured period
        "By experimentally measuring the period T, we can isolate π:",
        "π = T / (2 × √(L / g))"
    )

    visualization_text = (  # Text describing the simulation visualization
        "Visualization:",
        "• The pendulum is graphically simulated on screen in real time.",
        "• The period is measured automatically by detecting equilibrium crossings.",
        "• You can choose the pendulum length at the start of the simulation."
    )

    while True:
        screen.fill(BLACK)  # Fill screen with black background

        title_render = font_title.render(title_text, True, WHITE)  # Render title in white
        screen.blit(title_render, (screen_width // 2 - title_render.get_width() // 2, screen_height // 40))  # Display title centered at top
        underline_text(screen, title_render, screen_width // 2 - title_render.get_width() // 2, screen_height // 40)  # Underline the title

        y_position = screen_height // 7  # Set vertical start position for text
        y_position += display_dynamic_text(screen, description_text, screen_width // 15, y_position, 15, screen_width * 0.85, font_text) + 20  
        # Display the description text

        y_position += -10 if screen_height <= screen_info.current_h * 0.9 else screen_height // 50  # Add space depending on fullscreen

        for line in formula_text:  # For each line in the formula text
            y_position += display_dynamic_text(screen, line, screen_width // 15, y_position + 5, 15, screen_width * 0.85, font_text, BLUE, underline=True if line == "The period of a simple pendulum is given by:" else False) + screen_height // 50
            # Display the line in blue

        y_position += -10 if screen_height <= screen_info.current_h * 0.9 else screen_height // 50  # Add space depending on fullscreen

        for line in pi_calculation_text:  # For each line in the π calculation text
            y_position += display_dynamic_text(screen, line, screen_width // 15, y_position + 5, 15, screen_width * 0.85, font_text, BLUE, underline=True if line == "By experimentally measuring the period T, we can isolate π:" else False) + screen_height // 50
            # Display the line in blue

        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 50  # Add space depending on fullscreen

        for line in visualization_text:  # For each line in the visualization text
            y_position += display_dynamic_text(screen, line, screen_width // 15, y_position + 5, 15, screen_width * 0.85, font_text, underline=True if line == "Visualization:" else False) + screen_height // 50
            # Display the line in white

        instruction_render = font_title.render("Click anywhere to start", True, RED)  # Render instruction in red
        screen.blit(instruction_render, (screen_width // 2 - instruction_render.get_width() // 2, screen_height * 0.92))  
        # Display instruction centered at the bottom

        menu_button()  # Display menu icon
        close_cross()  # Display close icon
        pygame.display.update()  # Update display

        button_event, _ = event_handler()  # Get user events
        if button_event == "menu":  # If user clicks menu
            return False  # Return to menu
        if button_event == "click":  # If user clicks on screen
            return True  # Return True to continue


def pendulum():
    """
    Main function of the simple pendulum simulation to estimate π.

    Parameters:
        None

    Returns:
        Nothing. The function manages setup, animation, and display of the simulation.
    """
    if not pendulum_information():  # Show info screen; return to menu if menu button clicked
        return
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window dimensions
    font_title = pygame.font.Font(FONT, screen_height // 15)  # Font for setup title
    font_text = pygame.font.Font(FONT, screen_height // 30)  # Font for explanatory text

    input_box = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)  # Input box for pendulum length
    pendulum_length = None  # Variable to store the user-entered pendulum length (L)
    gravity = 9.81  # Gravitational acceleration

    while pendulum_length is None:
        screen.fill(BLACK)  # Clear screen for setup

        title_render = font_title.render("Simple Pendulum - Setup", True, WHITE)  # Render setup title
        explanation_render = font_text.render("Enter pendulum length L (meters): (min 0.2, max 5)", True, WHITE)
        # Render explanatory text indicating allowed L range

        screen.blit(title_render, (screen_width // 2 - title_render.get_width() // 2, screen_height // 10))  # Center title
        screen.blit(explanation_render, (screen_width // 2 - explanation_render.get_width() // 2, screen_height // 5))  # Center explanation
        screen.blit(input_box.surface, (screen_width // 2 - input_box.surface.get_width() // 2, screen_height // 3.8))
        # Center input box

        info_button()  # Show info button
        menu_button()  # Show menu button
        close_cross()  # Show close button
        pygame.display.update()  # Update display

        button_event, events = event_handler()  # Get user events
        if button_event == "menu":
            return  # Return to menu
        if button_event == "info":
            if not pendulum_information():  # Re-display info screen
                return  # Return to menu if menu clicked in info

        input_box.update(events)  # Update input box with events
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # If Enter is pressed
                if input_box.value.replace('.', '', 1).isdigit():  # Check if value is a number (allow decimal point)
                    pendulum_length = min(5, max(0.2, float(input_box.value)))  # Constrain L between 0.2 and 5
                input_box.value = ""  # Reset input box

    # Initialize pendulum variables
    theta = 0.07  # Initial angle (radians)
    omega = 0.0  # Initial angular velocity
    pivot_x = screen_width // 2  # Pivot x-position (centered)
    pivot_y = screen_height // 4  # Pivot y-position
    ball_radius = 15  # Ball radius
    prev_theta_sign = 1 if theta >= 0 else -1  # Detect zero crossings
    last_cross_time = None  # Last zero crossing time
    measured_periods = []  # List of measured periods

    # Initial time
    prev_time = pygame.time.get_ticks()
    start_ticks = prev_time

    # Animation loop
    while True:
        screen.fill(BLACK)  # Clear screen

        # Calculate real delta time
        current_time = pygame.time.get_ticks()
        dt_real = (current_time - prev_time) / 1000.0  # Convert to seconds
        prev_time = current_time  # Update reference time

        # Handle events
        button_event, events = event_handler()
        if button_event == "menu":
            return  # Return to menu
        if button_event == "info":
            if not pendulum_information():
                return  # Return to menu if leaving info

        # Draw buttons, close cross, and info button
        close_cross()
        menu_button()
        info_button()

        # Physics simulation
        angular_acceleration = - (gravity / pendulum_length) * math.sin(theta)
        omega += angular_acceleration * dt_real  # Update angular velocity
        theta += omega * dt_real  # Update angle

        # Zero crossing detection
        new_theta_sign = 1 if theta >= 0 else -1
        if new_theta_sign != prev_theta_sign:
            if prev_theta_sign < 0 and new_theta_sign > 0:
                if last_cross_time is not None:
                    period_ms = current_time - last_cross_time
                    period_s = period_ms / 1000.0  # Convert to seconds
                    measured_periods.append(period_s)
                last_cross_time = current_time  # Update last crossing time
        prev_theta_sign = new_theta_sign  # Update previous sign

        # Calculate π
        avg_period = sum(measured_periods) / len(measured_periods) if measured_periods else 0
        pi_estimate = avg_period / (2 * math.sqrt(pendulum_length / gravity)) if avg_period > 0 else 0

        # Calculate ball position
        ball_x = pivot_x + int(pendulum_length * 100.0 * math.sin(theta))
        ball_y = pivot_y + int(pendulum_length * 100.0 * math.cos(theta))

        # Draw pendulum
        pygame.draw.line(screen, GRAY, (pivot_x, pivot_y), (ball_x, ball_y), 3)
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        # Display text
        text_length = font_text.render(f"L = {pendulum_length:.2f} m", True, WHITE)
        text_num_periods = font_text.render(f"Measured periods: {len(measured_periods)}", True, WHITE)
        text_period = font_text.render(f"Average time = {avg_period:.2f} s", True, WHITE)
        text_pi = font_text.render(f"Estimated Pi = {pi_estimate:.6f}", True, WHITE)
        text_time = font_text.render(f"Elapsed time: {elapsed_time(start_ticks)}", True, WHITE)
        # Positioning text
        screen.blit(text_length, (50, screen_height // 40))
        screen.blit(text_num_periods, (50, screen_height // 15))
        screen.blit(text_period, (50, screen_height // 9))
        screen.blit(text_pi, (50, screen_height // 6.5))
        screen.blit(text_time, (50, screen_height // 5.1))

        pygame.display.update()  # Update display
