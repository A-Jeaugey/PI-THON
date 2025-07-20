#Project: PI-THON
#Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Import pygame for display, events, etc.
import pygame_textinput  # Module to create and manage text input fields in Pygame.
from display import screen, FONT, WHITE, BLACK, RED, GRAY, BLUE, menu_button, close_cross, info_button, screen_info  # Display components and colors.
from utils import elapsed_time, event_handler, display_dynamic_text, underline_text  # Utility functions

def leibniz_information():
    """
    Displays the information screen about the Leibniz method.
    The user can click to start the simulation or click "menu" to exit.

    Parameters: None

    Returns:
        bool:
            - True if the user clicks to launch the demonstration,
            - False if they click the menu button.
    """
    # Get the window width and height to adapt the display.
    screen_width, screen_height = screen.get_width(), screen.get_height()

    # Create fonts for the title and explanatory text.
    title_font = pygame.font.Font(FONT, screen_height // 15)
    text_font = pygame.font.Font(FONT, screen_height // 35)

    # Explanatory texts
    title_text = "Leibniz Method"
    description_text = (
        "The Leibniz series is one of the simplest methods to estimate π, "
        "but it converges very slowly. It relies on an alternating sum of terms approaching π/4. "
        "Each term adds or subtracts a fraction, providing a "
        "progressive approximation of π."
    )
    formula_text = (
        "The formula is:",
        "π ≈ 4 * (1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ...)"
    )
    visualization_text = (
        "Visualization:",
        "• The vertical axis represents the estimated value of π.",
        "• A white line marks the real value of π.",
        "• The colored curve shows how the estimate fluctuates with iterations.",
        "• User input allows adjusting the display speed."
    )

    while True:
        screen.fill(BLACK)  # Clear the screen with black.

        # Display the title at the top, centered horizontally.
        title_rendered = title_font.render(title_text, True, WHITE)
        screen.blit(title_rendered, (screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40))
        underline_text(screen, title_rendered, screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40)  # Underline the title

        # Starting position for the dynamic text display.
        y_position = screen_height // 6
        # Display the paragraph describing the Leibniz method.
        y_position += display_dynamic_text(screen, description_text, screen_width // 10, y_position, 15, screen_width * 0.8, text_font) + screen_height // 30
        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 15  # Add space depending on fullscreen or not
        # Display the two formula lines in BLUE.
        for line in formula_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position, 15, screen_width * 0.8, text_font, BLUE, underline=True if line == "The formula is:" else False) + screen_height // 50

        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 15  # Add space depending on fullscreen or not
        # Display the "Visualization" section line by line.
        for line in visualization_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 40, 15, screen_width * 0.8, text_font, underline=True if line == "Visualization:" else False) + screen_height // 50

        # Prompt the user to click to start the demonstration.
        instruction_rendered = title_font.render("Click anywhere to start", True, RED)
        screen.blit(instruction_rendered, (screen_width // 2 - instruction_rendered.get_width() // 2, screen_height * 0.92))

        # Draw the menu button, close cross, then update the display.
        menu_button()
        close_cross()
        pygame.display.update()

        # Event handling: get actions from the event_handler function.
        button_event, _ = event_handler()
        if button_event == "menu":  # If the user clicks the menu button
            return False  # Return to the menu
        if button_event == "click":  # If the user clicks inside the window
            return True  # Proceed to the calculation method


def leibniz():
    """
    Displays the demonstration of the Leibniz method to estimate π.
    The user can adjust the number of iterations per update using a text field.

    Parameters: None

    Returns:
        Nothing. The function exits when the user clicks "menu" or, when re-displaying the info, returns False.
    """
    # Start with the information screen.
    if not leibniz_information():
        return  # If the menu button is clicked on the info screen, return to menu

    # Get the window size to adjust the displays.
    screen_width, screen_height = screen.get_width(), screen.get_height()
    # Center coordinates (used as reference for drawing or display).
    center_x, center_y = screen_width // 2, screen_height // 2

    # Fonts for the title and smaller text.
    font_title = pygame.font.Font(FONT, screen_width // 25)
    font_text = pygame.font.Font(FONT, screen_width // 42)

    # Clear the screen before starting the simulation.
    screen.fill(BLACK)
    
    pygame.display.update()  # Update the display

    # Record the start time (Pygame ticks) to measure elapsed time.
    start_ticks = pygame.time.get_ticks()

    pi_estimate = 0  # Accumulated value representing the partial sum (Leibniz approaches pi/4)
    iteration_count = 0  # Number of iterations already performed
    pi_values = []  # Stores successive estimates of π to plot the curve

    # Number of iterations to perform per update (user-configurable)
    iterations_per_update = 1

    # Use a text field so the user can modify 'iterations_per_update'
    text_input = pygame_textinput.TextInputVisualizer(font_color=WHITE, cursor_color=WHITE)

    while True:
        # Retrieve actions/events
        button_event, events = event_handler()
        if button_event == "menu":  # If menu button clicked
            return  # Return to menu
        if button_event == "info":  # If 'info' clicked, re-display the Leibniz info screen
            if not leibniz_information():
                return  # If menu button clicked on info screen, return to menu

        # Loop through Pygame events
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # If user presses Enter
                if text_input.value.isdigit():  # And input is a number
                    iterations_per_update = max(1, int(text_input.value))  # Minimum of 1
                text_input.value = ""  # Clear the field after validation

        # Update the text field
        text_input.update(events)
        # Limit the length of the user input
        if len(text_input.value) > 6:
            text_input.value = text_input.value[:6]

        # Compute the Leibniz series over 'iterations_per_update' additional iterations
        for i in range(iteration_count, iteration_count + iterations_per_update):
            # Leibniz: pi/4 = 1/1 - 1/3 + 1/5 - 1/7 + ...
            pi_estimate += (-1)**i / (2 * i + 1)
        # Keep the value of 4 * pi_estimate (since the series gives pi/4).
        pi_values.append(4 * pi_estimate)
        iteration_count += iterations_per_update  # Advanced by iterations_per_update iterations

        # Clear the screen before re-displaying the new frame.
        screen.fill(BLACK)

        # Draw two axes: horizontal at bottom, vertical on the left
        pygame.draw.line(screen, GRAY, (50, screen_height - 50), (screen_width - 50, screen_height - 50), 2)
        pygame.draw.line(screen, GRAY, (50, 100), (50, screen_height - 50), 2)

        # Draw horizontal ticks and display graduations (0,1,2,3,4,5,6...) on vertical axis
        for i in range(7):
            real_value = i
            # Calculate the Y position of the mark: spread between 100 and screen_height-50
            y_position = int(screen_height - 50 - i * (screen_height - 150) / 6)

            # Convert value to string (displayed as X.X)
            value_y = f"{real_value:.1f}"
            label = pygame.font.Font(FONT, 25).render(value_y, True, WHITE)
            screen.blit(label, (8, y_position - 10))  # Place label slightly to the left
            pygame.draw.line(screen, GRAY, (45, y_position), (55, y_position), 2)  # Small tick

        # Add a small tick for π and draw a horizontal line where π is
        pi_label = pygame.font.Font(FONT, 30).render("π", True, WHITE)
        # Place this label on the left.
        y_pi = int(center_y - (3.14159265358979 - 3.14))
        screen.blit(pi_label, (12, y_pi - 20))

        # Horizontal reference line for π (e.g., for y=(π-3.14)*factor...)
        y_pi = int(center_y - (3.14159265358979 - 3.14) * 100)
        pygame.draw.line(screen, WHITE, (50, y_pi), (screen_width - 50, y_pi), 2)

        # Draw the convergence curve. Loop through successive points in 'pi_values'.
        if len(pi_values) > 1:
            for i in range(1, len(pi_values)):
                # X coordinate of previous point
                x1 = int(50 + (i - 1) * (screen_width - 100) / len(pi_values))
                # Y coordinate based on difference relative to 3.14
                y1 = int(center_y - (pi_values[i - 1] - 3.14) * 500)

                # X coordinate of current point
                x2 = int(50 + i * (screen_width - 100) / len(pi_values))
                # Y coordinate of current point
                y2 = int(center_y - (pi_values[i] - 3.14) * 500)

                # Color evolving progressively (from yellow to magenta).
                color = (255, int(255 * (i / len(pi_values))), int(255 * (1 - i / len(pi_values))))
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), 3)

        char_width = font_text.render("0", True, WHITE).get_width()  # Gives character width to center text properly

        # Create and display text showing the number of iterations, pi value, and elapsed time.
        text_iteration = font_text.render(f"Step {iteration_count}", True, WHITE)
        text_pi = font_title.render(f"Estimation of π: {4 * pi_estimate:.15f}", True, WHITE)
        text_time = font_text.render(f"Elapsed time: {elapsed_time(start_ticks)}", True, WHITE)

        screen.blit(text_iteration, (screen_width // 2 - text_iteration.get_width() // 2, screen_height // 20))
        screen.blit(text_time, ((screen_width - text_time.get_width()) // 2, screen_height // 9))
        screen.blit(text_pi, (screen_width // 2 - text_time.get_width() // 2 - 15 * char_width, screen_height // 6))

        # Indicate to the user the input field to adjust 'iterations_per_update'.
        input_label = font_text.render("Enter iterations per update:", True, WHITE)
        screen.blit(input_label, ((screen_width - input_label.get_width()) // 2, screen_height // 1.3))

        # Display the text field (where the user enters a number of iterations).
        screen.blit(text_input.surface, ((screen_width - input_label.get_width()) // 2, screen_height // 1.2))

        # Display info button, menu button, and close cross.
        info_button()
        menu_button()
        close_cross()

        # Update the screen.
        pygame.display.update()

        # Insert a small delay to control animation speed.
        # It decreases when iterations_per_update increases (to avoid going too fast).
        pygame.time.delay(int(max(30 / (iterations_per_update ** 0.5), 1)))
