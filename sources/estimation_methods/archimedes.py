# Project: PI-THON 
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import math  # Math module for mathematical functions (sin, cos, etc.)
import pygame  # Pygame module to manage display, events, etc.
from display import screen, FONT, WHITE, BLACK, RED, BLUE, menu_button, close_cross, info_button, screen_info  # Display components and colors.
from utils import event_handler, display_dynamic_text, underline_text  # Utility functions


def information_archimedes():
    """
    Displays an information screen about Archimedes' method and waits for a click to proceed to the next step.
    
    Parameters: None
    Returns: 
        - True if the user clicks in the window to start,
        - False if the user clicks the menu button.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Gets the width and height of the window
    title_font = pygame.font.Font(FONT, screen_height // 15)  # Font for the main title, size depends on screen height
    text_font = pygame.font.Font(FONT, screen_height // 42)  # Smaller font for body text
    title_text = "Archimedes' Method"  # Page title

    # Main text describing the history and principle of Archimedes' method
    description_text = (
        "Developed by Archimedes around 250 B.C., this method is one of the first attempts "
        "to estimate π accurately. It consists of surrounding a circle with a regular inscribed polygon, "
        "which underestimates the circumference of the circle, and a circumscribed polygon which overestimates it. "
        "The average of the two gives an approximation of π. The more sides the polygon has, the more precise the approximation."
    )

    # Mathematical formula used by Archimedes: inscribed polygon / circumscribed polygon
    formula_text = (
        "The formula is:",
        "π ≈ ( P_inscribed + P_circumscribed ) / 2, where:",
        "P_inscribed = n × sin(π/n) and P_circumscribed = n × tan(π/n),",
        "with n being the number of sides of the polygon used."
    )

    # Explanations on the interactive part (visualization, colors, etc.)
    usage_text = (
        "Visualization:",
        "• The circle is drawn in white, the inscribed polygon in red, and the circumscribed polygon in green.",
        "• The number of polygon sides can be adjusted using the slider at the bottom of the screen."
    )

    while True:  # Loop to display the information screen
        screen.fill(BLACK)  # Fill the screen with black

        # Display the title, centered horizontally, placed at the top
        title_rendered = title_font.render(title_text, True, WHITE)  # Text surface for the title
        screen.blit(title_rendered, (screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40))  # Centered placement
        underline_text(screen, title_rendered, screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40)  # Underline the title

        # Calculate a starting Y position to display the explanatory text
        y_position = screen_height // 7

        # Display the main description using the display_dynamic_text function
        y_position += display_dynamic_text(screen, description_text, screen_width * 0.05, y_position, 15, screen_width * 0.9, text_font) + screen_height // 50
        y_position += screen_height // 18 if screen_height <= screen_info.current_h * 0.9 else screen_height // 10  # Add space depending on fullscreen or not

        # Display the formula lines, each colored in blue
        for line in formula_text:
            y_position += display_dynamic_text(screen, line, screen_width * 0.05, y_position, 15, screen_width * 0.9, text_font, BLUE, underline=True if line == "The formula is:" else False) + screen_height // 50
        y_position += screen_height // 18 if screen_height <= screen_info.current_h * 0.9 else screen_height // 10  # Add space depending on fullscreen or not

        for line in usage_text:
            y_position += display_dynamic_text(screen, line, screen_width * 0.05, y_position + 15, 15, screen_width * 0.9, text_font, underline=True if line == "Visualization:" else False) + screen_height // 50

        # Prompt the user to click to start
        instruction_rendered = title_font.render("Click anywhere to start.", True, RED)
        screen.blit(instruction_rendered, (screen_width // 2 - instruction_rendered.get_width() // 2, screen_height * 0.92))

        # Draw the menu button, close cross, and update the display
        menu_button()
        close_cross()
        pygame.display.update()

        # Event handling via our event_handler function
        button_event, _ = event_handler()
        if button_event == "menu":  # The user clicks the menu button
            return False  # Go back to menu
        if button_event == "click":  # The user clicks in the window
            return True  # Proceed (ready to launch the interactive part)




def archimedes():
    """
    Displays the interactive demonstration of Archimedes' method to estimate π,
    by drawing a circle, then an inscribed polygon and a circumscribed polygon with adjustable number of sides.

    Parameters: None
    Returns: None (exits the function if the user clicks 'menu').
    """
    if not information_archimedes():  # Start by displaying the information screen
        return  # If the user clicks the menu button in the info function, return to menu

    pygame.time.delay(200)  # Small pause to avoid the click immediately triggering something else

    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window size
    circle_center = (screen_width // 2, screen_height // 1.85)  # Center coordinates of the circle
    radius = screen_height // 4  # Radius of the circle

    min_sides = 3  # Minimum number of sides (a triangle)
    max_sides = 50000  # Maximum number of sides (a pentakismyriagon). (^-^)
    num_sides = 3  # Initial number of sides

    slider_x = 50  # X position for the adjustment bar (slider)
    slider_y = screen_height - 100  # Y position for the adjustment bar
    slider_width = screen_width - 100  # Width of the slider
    cursor_pos = slider_x  # Initial cursor position on the slider

    font_title = pygame.font.Font(FONT, screen_width // 20)  # Font for the top title
    font_text = pygame.font.Font(FONT, screen_width // 40)  # Font for info text

    while True:  # Main demonstration loop
        screen.fill(BLACK)  # Clear the screen with black

        # Get the action returned by event_handler
        button_event, _ = event_handler()
        if button_event == "menu":  # If the user clicks the menu button
            return  # Go back to the menu
        if button_event == "info":  # If the user clicks the info button
            if not information_archimedes():  # Re-display the info page and check return to menu
                return

        # Handle held left click to move the cursor along the slider
        if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
            mouse_x, _ = pygame.mouse.get_pos()  # Get only the X coordinate of the mouse
            if slider_x <= mouse_x <= slider_x + slider_width + 5:
                # Limit cursor position to stay within the slider
                cursor_pos = mouse_x

        # Calculate the movement proportion on the slider (between 0 and 1)
        relative_pos = (cursor_pos - slider_x) / slider_width

        # For the first half of the slider, vary num_sides from 3 to 30 linearly.
        # For the second half, switch to a much faster scale (exponent 2.5) to reach 50,000.
        if relative_pos <= 0.5:
            num_sides = int(3 + (30 - 3) * (relative_pos / 0.5))
        else:
            accelerated_progress = (relative_pos - 0.5) / 0.5
            acceleration_factor = 2.5
            num_sides = int(30 + (max_sides - 30) * (accelerated_progress ** acceleration_factor))

        # Ensure num_sides stays within bounds
        num_sides = min(max_sides, max(min_sides, num_sides))

        # Calculate inscribed and circumscribed perimeters (Archimedes formulas)
        perimeter_in = num_sides * math.sin(math.pi / num_sides)  # n × sin(π/n)
        perimeter_out = num_sides * math.tan(math.pi / num_sides)  # n × tan(π/n)
        pi_estimate = (perimeter_in + perimeter_out) / 2  # Average of both perimeters => π approximation

        # Draw the circle in white
        pygame.draw.circle(screen, WHITE, circle_center, radius, 2)

        points_in = []  # List of vertices of the inscribed polygon
        points_out = []  # List of vertices of the circumscribed polygon

        # Calculate (x, y) positions of vertices for each side, based on angle
        for i in range(num_sides):
            angle = (2 * math.pi * i) / num_sides  # Angle for vertex i
            # Inscribed polygon (constant radius)
            x_in = int(circle_center[0] + radius * math.sin(angle))
            y_in = int(circle_center[1] - radius * math.cos(angle))
            points_in.append((x_in, y_in))  # Add to the corresponding list

            # Circumscribed polygon (radius divided by cos(π/n))
            x_out = int(circle_center[0] + (radius / math.cos(math.pi / num_sides)) * math.sin(angle))
            y_out = int(circle_center[1] - (radius / math.cos(math.pi / num_sides)) * math.cos(angle))
            points_out.append((x_out, y_out))  # Add to the corresponding list

        # Draw the inscribed polygon in red (thickness 2) and the circumscribed polygon in green (thickness 2)
        pygame.draw.polygon(screen, (255, 0, 0), points_in, 2)
        pygame.draw.polygon(screen, (0, 255, 0), points_out, 2)

        # Create and display text surfaces
        text_sides = font_text.render(f"Number of sides: {num_sides}", True, WHITE)
        text_pi = font_text.render(f"π estimate: {pi_estimate:.8f}", True, WHITE)

        # Place info texts (number of sides, π estimate)
        screen.blit(text_sides, (50, screen_height // 10))
        screen.blit(text_pi, (50, screen_height // 6))

        # Draw the gray slider and the cursor (small white circle)
        pygame.draw.rect(screen, (150, 150, 150), (slider_x, slider_y, slider_width, 5))
        pygame.draw.circle(screen, WHITE, (cursor_pos, slider_y + 2), 10)

        # Info button, menu button, close cross
        info_button()
        menu_button()
        close_cross()

        # Update the display
        pygame.display.update()
