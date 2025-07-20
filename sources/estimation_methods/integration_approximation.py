# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import math  # Math module for mathematical functions (sqrt, pi, etc.)
import pygame  # Pygame library for GUI management and events
from display import screen, WHITE, BLACK, RED, BLUE, FONT, menu_button, close_cross, info_button, screen_info  # Display components and colors
from utils import event_handler, display_dynamic_text, underline_text  # Utility functions

def integration_approximation_information():
    """
    Displays an information screen about the π approximation by integration method.
    The user can click to proceed to the next step or click the "menu" button.

    Parameters:
        None

    Returns:
        bool:
            - True if the user clicks in the window to start the demonstration,
            - False if they click the "menu" button.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Gets the width and height of the window
    title_font = pygame.font.Font(FONT, screen_height // 15)  # Font for the title, proportional size to screen height
    text_font = pygame.font.Font(FONT, screen_height // 30)  # Font for the descriptive text, slightly smaller

    title_text = "Approximation by Integration"  # Method title

    # Text describing the principle of approximating π by integration (area under half a circle curve)
    description_text = (
        "The approximation of π by integration is based on calculating the area under the "
        "curve of a semicircle using rectangles. By increasing the number of subdivisions, "
        "the approximation becomes more precise."
    )

    # Information on the mathematical formula used for integration
    formula_text = (
        "The formula used is based on the sum of the areas of the rectangles:",
        "π ≈ 2 × Σ [sqrt(1 - x²) × dx], where dx is the width of the subdivisions."
    )

    # Additional info on educational use and the interest of this method
    usage_text = (
        "This method illustrates the concept of definite integrals and is commonly used "
        "to teach the basics of mathematical analysis and numerical calculations."
    )

    while True:  # Information display loop
        screen.fill(BLACK)  # Fills the screen with black

        # Display the title centered at the top of the screen
        title_rendered = title_font.render(title_text, True, WHITE)  # Text surface for the title
        screen.blit(title_rendered, (screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40))  # Centered horizontally
        underline_text(screen, title_rendered, screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40)  # Underline the title

        # Gradually display the explanatory text
        y_position = screen_height // 5  # Vertical starting point
        # Display the main text describing the method
        y_position += display_dynamic_text(screen, description_text, screen_width // 10, y_position, 15, screen_width * 0.8, text_font) + screen_height // 50
        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 13
        # Display each formula line in blue
        for line in formula_text:
            y_position += display_dynamic_text(screen, line, screen_width // 10, y_position + 15, 15, screen_width * 0.8, text_font, BLUE, underline=True if line == "The formula used is based on the sum of the areas of the rectangles:" else False) + screen_height // 30

        y_position += screen_height // 50 if screen_height <= screen_info.current_h * 0.9 else screen_height // 13

        # Display the final part of the explanation (usage)
        y_position += display_dynamic_text(screen, usage_text, screen_width // 10, y_position + 15, 15, screen_width * 0.8, text_font)

        # Display a message encouraging the user to click to start
        instruction_rendered = title_font.render("Click anywhere to start.", True, RED)
        screen.blit(instruction_rendered, (screen_width // 2 - instruction_rendered.get_width() // 2, screen_height * 0.92))

        # Draw the menu button and close cross, then update the display
        menu_button()
        close_cross()
        pygame.display.update()

        # Event handling via the dedicated function
        button_event, _ = event_handler()
        if button_event == "menu":
            return False  # User goes back
        if button_event == "click":
            return True  # User clicks the window to start



def approximation_integration():
    """
    Displays the interactive demonstration to approximate π by integration (area under the semicircle curve).
    The user can adjust the number of subdivisions to improve the integration precision.
    
    Parameters:
        None
    
    Returns:
        Nothing. The function ends when the user clicks "menu" or closes the window.
    """
    # Start by displaying the information screen
    if not integration_approximation_information():
        return  # If "menu" button is clicked in the info function, return to menu

    pygame.time.delay(200)  # Small pause to avoid accidental double-click.

    # Get window dimensions
    screen_width, screen_height = screen.get_width(), screen.get_height()

    # Define center coordinates of the semicircle and its radius (takes 1/3 of the smaller dimension)
    center_x, center_y = screen_width // 2, screen_height // 1.4
    circle_radius = min(screen_width, screen_height) // 3

    # Bounds and initial value for the number of subdivisions
    min_subdivisions = 1
    max_subdivisions = 450
    subdivisions = 1

    # Positions and dimensions of the adjustment bar (slider)
    bar_x = 50
    bar_y = screen_height - 100
    bar_width = screen_width - 100
    cursor_x = bar_x  # Initial cursor position

    text_font = pygame.font.Font(FONT, screen_height // 22)  # Font

    while True:  # Main loop
        screen.fill(BLACK)  # Clear screen with black

        # Get the action returned by the event handler
        button_event, _ = event_handler()

        if button_event == "menu":  # If the user clicks the menu button
            return  # Return to menu
        if button_event == "info":  # If they click the "info" button
            if not integration_approximation_information():  # Re-display the info screen
                return  # If "menu" button is clicked in the info function, return to menu

        # Handle held mouse click to move the subdivisions slider
        if pygame.mouse.get_pressed()[0]:  # Check if left button is pressed
            mouse_x, _ = pygame.mouse.get_pos()  # Get only the X coordinate of the mouse
            # Limit the cursor so it doesn't go outside the bar
            if bar_x <= mouse_x <= bar_x + bar_width:
                cursor_x = mouse_x

        # Calculate the relative cursor position between 0 and 1
        relative_position = (cursor_x - bar_x) / bar_width

        # Based on position, evolve subdivisions in mixed mode:
        # - first half => from 1 to 50 linearly
        # - second half => from 50 to 530 in accelerated progression (power 2.5)
        if relative_position <= 0.5:
            subdivisions = int(1 + (50 - 1) * (relative_position / 0.5))
        else:
            acceleration_progress = (relative_position - 0.5) / 0.5
            acceleration_factor = 2.5
            subdivisions = int(50 + (max_subdivisions - 50) * (acceleration_progress ** acceleration_factor))

        # Ensure subdivisions stay within bounds
        subdivisions = min(max_subdivisions, max(min_subdivisions, subdivisions))

        # Draw the semicircle arc at the top (to symbolize y = sqrt(1 - x^2))
        pygame.draw.arc(screen, WHITE, (center_x - circle_radius, center_y - circle_radius, 2 * circle_radius, 2 * circle_radius),
            0,  # Start angle (0 radians => on X axis to the right)
            math.pi,  # End angle (π radians => on X axis to the left)
            2  # Arc thickness of 2 pixels
        )

        # Numerical integration via sum of rectangle areas
        area_sum = 0.0
        rectangle_width = 2 / subdivisions  # If interval is [-1, 1], length is 2
        for i in range(subdivisions):
            # Take midpoint of each subdivision
            x_position = -1 + (i + 0.5) * rectangle_width  # X in [-1, 1]
            rectangle_height = math.sqrt(1 - x_position**2)  # semicircle height
            # Convert to Pygame coordinates:
            screen_x = center_x + int(x_position * circle_radius)
            screen_y = center_y - int(rectangle_height * circle_radius)
            display_width = int(rectangle_width * circle_radius)
            display_height = int(rectangle_height * circle_radius)
            # Gradient color based on height (simple visual effect)
            rectangle_color = (255, int(255 * rectangle_height), 0)
            
            # Draw rectangle of height "display_height" at calculated position
            pygame.draw.rect(screen, rectangle_color, (screen_x - display_width // 2, screen_y, display_width, display_height))
            # Add area (height * width) to sum, corresponding to area under the curve
            area_sum += rectangle_height * rectangle_width

        # Integral over [-1,1] of sqrt(1 - x^2) represents half-circle area π/2
        # To get π, multiply sum by 2
        pi_estimate = 2 * area_sum

        # Display information text: pi estimate and number of subdivisions
        pi_text = text_font.render(f"Pi Estimate: {pi_estimate:.6f}", True, WHITE)
        subdivisions_text = text_font.render(f"Subdivisions: {subdivisions}", True, WHITE)
        screen.blit(pi_text, (screen_width // 2 - pi_text.get_width() // 2, screen_height // 5))
        screen.blit(subdivisions_text, (screen_width // 2 - subdivisions_text.get_width() // 2, screen_height // 10))

        # Draw adjustment bar in gray and cursor (white circle)
        pygame.draw.rect(screen, (150, 150, 150), (bar_x, bar_y, bar_width, 5))
        pygame.draw.circle(screen, WHITE, (cursor_x, bar_y + 2), 10)

        # Display info button, menu button, and close cross
        info_button()
        menu_button()
        close_cross()

        # Update Pygame window with everything drawn
        pygame.display.update()
