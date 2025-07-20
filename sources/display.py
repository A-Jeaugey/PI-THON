# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import os  # Module to interact with the operating system (file paths, etc.)
import pygame  # Pygame library for managing the window, display, and events

pygame.init()  # Initializes Pygame's internal modules
pygame.display.set_caption("- THON")  # Sets the window title
pygame.display.set_icon(pygame.image.load("data/logo.png"))  # Sets the icon, which is just the pi symbol, but combined with the title forms the project name
FONT = os.path.join("data", "Iosevka_fixed.ttf")  # Path to the custom font
screen_info = pygame.display.Info()  # Object containing screen information (resolution, etc.)
screen_width, screen_height = 1000, 800  # Default window dimensions in windowed mode
fullscreen_state = True  # Boolean indicating whether we are in fullscreen mode (True) or not (False)

WHITE = (255, 255, 255)  # Definition of the white color in RGB
BLACK = (0, 0, 0)  # Black color
RED = (255, 0, 0)  # Red color
GREEN = (0, 255, 0)  # Green color
BLUE = (119, 181, 254)  # Light blue color
GRAY = (100, 100, 100)  # Medium gray color
LIGHT_GRAY = (150, 150, 150)  # Light gray color
DARK_GRAY = (56, 56, 56)  # Dark gray color
BLACK_MENU = (50, 48, 48)

screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)  # Creates the Pygame window with the specified dimensions
font = pygame.font.Font(FONT, 45)  # Loads the font, size 45

close_cross_rect = pygame.Rect(screen.get_width() - 50, 0, 50, 50)  # Rectangle to place the close cross at the top right
menu_button_rect = pygame.Rect(screen.get_width() - 132, 8, 50, 50)  # Rectangle for the return-to-menu button
fullscreen_button_rect = pygame.Rect(screen.get_width() - 100, 10, 35, 35)  # Rectangle for the "F" (fullscreen) button

sidebar_rectangles = []  # List of clickable rectangles in the sidebar
selected_group = None  # Holds the selected group (or None if none)


def main_menu():
    """
    Manages the display and logic of the main menu (welcome screen).
    Parameters: None
    Returns: The name of a method (str) if the user selects one, else None if the window is closed.
    """
    from utils import display_dynamic_text  # Local import of a function that handles dynamic text display. Local import avoids circular import
    global selected_group  # Indicates that we modify these global variables inside the function
    title_font = pygame.font.SysFont(FONT, screen_width // 5, italic=True)  # Font for the title, size depending on screen width
    text_font = pygame.font.Font(FONT, screen_width // 38)  # Font for regular text, size depending on screen width

    scrollable_rects = {
        "intro": pygame.Rect(screen_width * 0.04, screen.get_height() // 4 if fullscreen_state else screen.get_height() // 3.5,  screen.get_width() // 1.42 if fullscreen_state else screen.get_width() // 1.55, screen.get_width() // 6 if fullscreen_state else screen.get_width() // 4),
        "groups": pygame.Rect(screen_width * 0.04, screen.get_height() // 1.6,  screen.get_width() // 1.42 if fullscreen_state else screen.get_width() // 1.55, screen.get_width() // 6 if fullscreen_state else screen.get_width() // 4),
    }

    intro_text = (
            "π is a mathematical constant representing the ratio between a circle's "
            "circumference and its diameter. It is irrational and appears in many "
            "branches of mathematics and science. The first approximations of π "
            "go back to Antiquity with Archimedes, but today, we have many "
            "methods to calculate it with extreme precision."
        )
    
    group_texts = (
        "We have classified the pi estimation methods into different groups: ",
        "- Geometric methods: ",
        "Approaches based on polygons and integration.",
        "- Series and mathematical sequences: ",
        "Using infinite series to approximate π.",
        "- Algorithms and high precision: ",
        "Algorithms optimized for a large number of decimals.",
        "- Stochastic methods: ",
        "Probabilistic simulations to estimate π.",
        "- Physical and dynamic: ",
        "Approaches based on real physical phenomena.",
        " "
    )

    scroll_positions = {"intro": 0, "groups": 0}

    while True:  # Main execution loop of the menu
        screen.fill(DARK_GRAY)  # Clears the screen by filling it with dark gray

        scrollable_rects = {
        "intro": pygame.Rect(screen_width * 0.04, screen.get_height() // 4 if fullscreen_state else screen.get_height() // 3.5,  screen.get_width() // 1.42 if fullscreen_state else screen.get_width() // 1.55, screen.get_width() // 6 if fullscreen_state else screen.get_width() // 4),
        "groups": pygame.Rect(screen_width * 0.04, screen.get_height() // 1.6,  screen.get_width() // 1.42 if fullscreen_state else screen.get_width() // 1.55, screen.get_width() // 6 if fullscreen_state else screen.get_width() // 4),
        }

        title = title_font.render("π - thon", True, WHITE)  # Creates a text surface (title) "PI-THON"
        title_rect = pygame.Rect(screen.get_width() // 4 - 20 if fullscreen_state else screen.get_width() // 10 - 20, 40, title.get_width() + 30, title.get_height() + 15)  # Creates a rectangle to place the title
        pygame.draw.rect(screen, GRAY, title_rect, border_radius=40)  # Displays this rectangle
        screen.blit(title, (screen.get_width() // 4 if fullscreen_state else screen.get_width() // 10, 50))  # Displays the title centered horizontally

        rectangles = sidebar(selected_group)  # Draws the sidebar and gets its clickable zones

        pygame.draw.rect(screen, RED, fullscreen_button_rect, 7)  # Draws a red rectangle around the fullscreen button
        f_letter_font = pygame.font.Font(FONT, 25)  # Font for the letter "F"
        f_letter_surface = f_letter_font.render("F", True, RED)  # Text surface "F" in red
        screen.blit(f_letter_surface, (fullscreen_button_rect[0] + 11, fullscreen_button_rect[1] + 2))  # Positions the "F" inside the fullscreen button rectangle
        
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Gets mouse coordinates
        active_rect = None  # Variable indicating the active rectangle

        for key, rect in scrollable_rects.items():
            if rect.collidepoint(mouse_x, mouse_y):
                active_rect = key  # If the mouse hovers over a rectangle, it becomes the active rectangle

        for key, rect in scrollable_rects.items():
            pygame.draw.rect(screen, LIGHT_GRAY, rect, border_radius=20)  # Draws the rectangles

            # Apply clipping to prevent text from overflowing the rectangle
            screen.set_clip(rect)

            # Display text
            if key == "groups":  # Display with scroll for groups
                y_pos = rect.y + 10 - scroll_positions[key]  # Vertical position
                total_groups_height = 0  # To calculate the total height of the text

                for i in range(0, len(group_texts), 2):  # Displays text line by line, alternating red
                    title_height = display_dynamic_text(screen, group_texts[i], rect.x + 10, y_pos, 15, rect.width - 40, text_font, WHITE, False)
                    y_pos += title_height + 20  # Adds space
                    desc_height = display_dynamic_text(screen, group_texts[i + 1], rect.x + 10, y_pos, 15, rect.width - 40, text_font, RED, False)
                    y_pos += desc_height + 5  # Adds spacing between groups
                    total_groups_height += title_height + desc_height + 25

                text_height = total_groups_height  # We use this height for scrolling

            elif key == "intro":  # Display of intro with scroll
                text_height = display_dynamic_text(screen, intro_text, rect.x + 10, rect.y + 10 - scroll_positions[key], 15, rect.width - 40, text_font, WHITE, False)

            # Add the scrollbar
            max_scroll_height = max(0, text_height + 50 - rect.height)

            if max_scroll_height > 0:  # Show the scrollbar only if text overflows
                bar_height = max(20, (rect.height - 40) * rect.height // text_height)  # Reduction factor (-40 to avoid rounded corners)
                bar_pos = rect.y + 20 + (rect.height - 40 - bar_height) * (scroll_positions[key] / max_scroll_height)  # Offset to avoid corners
                
                # Draw the scrollbar slightly inward
                pygame.draw.rect(screen, GRAY, (rect.right - 15, bar_pos, 5, bar_height), border_radius=2)
            
            screen.set_clip(None)  # Remove clipping after display

        close_cross()  # Draws the close cross at the top right
        pygame.display.update()  # Updates the display

        for event in pygame.event.get():  # Loops through the list of Pygame events
            if event.type == pygame.QUIT:  # Checks if the user closes the window
                pygame.quit()  # Closes Pygame modules
                exit()  # Fully exits the Python program
            if event.type == pygame.MOUSEBUTTONDOWN and fullscreen_button_rect.collidepoint(event.pos) and event.button == 1 or event.type == pygame.KEYDOWN and event.key in (pygame.K_f, pygame.K_F11):  # Checks click on fullscreen button OR F/F11 key
                toggle_fullscreen()  # Switches display to fullscreen or windowed mode
            
            if event.type == pygame.MOUSEBUTTONDOWN:  # Handling mouse events (scroll and clicks)
                if active_rect:
                    # Recalculate height for each scroll
                    if active_rect == "groups":
                        text_height = total_groups_height
                    else:
                        text_height = display_dynamic_text(screen, intro_text, 0, 0, 15, scrollable_rects[active_rect].width - 20, text_font, WHITE, False)
                    
                    # Recalculate max height
                    max_scroll_height = max(0, (text_height + text_font.get_height() + 25) - scrollable_rects[active_rect].height)

                    # Disable scroll if all text is visible
                    if text_height + text_font.get_height() + 5 <= scrollable_rects[active_rect].height:
                        max_scroll_height = 0
                        scroll_positions[active_rect] = 0

                    if event.button == 4:  # Scroll up
                        scroll_positions[active_rect] = max(0, scroll_positions[active_rect] - 20)
                    elif event.button == 5:  # Scroll down
                        scroll_positions[active_rect] = min(max_scroll_height, scroll_positions[active_rect] + 20)

                if event.button == 1:  # Left mouse click
                    if close_cross_rect.collidepoint(event.pos):  # Checks if the close cross was clicked
                        pygame.quit()  # Closes Pygame
                        exit()  # Exits Python
                    for rect, action in rectangles:  # Loops through the list of sidebar buttons/rectangles
                        if rect.collidepoint(event.pos):  # Checks if a rectangle was clicked
                            if action == "menu":  # "menu" button
                                selected_group = None  # Go back to general group list
                            elif action in [1, 2, 3, 4, 5, 6]:  # Selecting a group by number
                                selected_group = action
                            else:  # If action is a string corresponding to a method
                                selected_group = None
                                return action  # Return the chosen method's name and exit main_menu



def sidebar(selected_group=None):
    """
    Displays the sidebar (list of groups or methods) and returns the clickable zones.
    Parameters: selected_group (int or None)
    Returns: A list of tuples (rectangle, action) representing each button.
    """
    from utils import display_dynamic_text  # Function for dynamic text display; local import avoids circular import
    sidebar_width = screen.get_width() // 4  # Calculates the sidebar width based on the current window size
    screen_height = screen.get_height()  # Window height
    left_x_position = screen.get_width() - sidebar_width - 20  # Horizontal start point of the sidebar (right side)

    top_bottom_margin = screen_height // 15  # Top and bottom margins of the sidebar
    total_sidebar_height = screen_height - 2 * top_bottom_margin  # Total vertical space available for the sidebar
    first_last_rect_space = total_sidebar_height // 20  # Space reserved above the first and below the last rectangle

    spacing_factor = 1.1  # Factor to space the rectangles vertically in the sidebar

    pygame.draw.rect(screen, BLACK_MENU, (left_x_position, top_bottom_margin, sidebar_width + 20, total_sidebar_height), border_top_left_radius=30, border_bottom_left_radius=30)  # Draws a large rounded gray rectangle representing the sidebar

    groups = {  # Dictionary linking a group number to a tuple (name, [list of methods])
        1: ("Geometric methods", ["Archimedes", "Integration Approximation"]),
        2: ("Series and mathematical sequences", ["Leibniz", "Nilakantha", "Machin", "Ramanujan"]),
        3: ("Algorithms and high precision", ["Gauss-Legendre", "Borwein", "Chudnovsky"]),
        4: ("Stochastic methods", ["Monte Carlo", "Buffon"]),
        5: ("Physical and dynamic", ["Collisions", "Pendulum"]),
    }

    sidebar_rectangles = []  # List to store each (rectangle, action)

    if selected_group is None:  # If no group is selected, display the list of all groups
        counter = 0  # Used to calculate vertical offset
        for group_number in groups:  # Loop through each group
            num_sections = len(groups)  # Total number of groups
            rect_height = (total_sidebar_height - 2 * first_last_rect_space) / (spacing_factor * num_sections)  # Calculate the height of each rectangle
            font_size = max(20, int(rect_height // 4))  # Font size, with a minimum of 20
            rect_font = pygame.font.Font(FONT, int(font_size))  # Font to display the group name

            group_name = groups[group_number][0]  # Get the group name
            y_position = top_bottom_margin + first_last_rect_space + counter * spacing_factor * rect_height  # Calculate vertical position
            rect = pygame.Rect(left_x_position + 11, y_position, sidebar_width, rect_height)  # Create the rectangle associated with this group

            pygame.draw.rect(screen, LIGHT_GRAY if counter % 2 == 0 else DARK_GRAY, rect, border_radius=20)  # Draw rectangle with alternating color
            display_dynamic_text(screen, group_name, left_x_position + 20, y_position + 10, 5, sidebar_width - 20, rect_font, WHITE, True, rect_height)  # Display the group name

            sidebar_rectangles.append((rect, group_number))  # Store the pair (rectangle, action) = group number
            counter += 1  # Increment to move to the next group
    else:  # If a group is selected, display the methods linked to that group
        counter = 0
        for method in groups[selected_group][1]:  # Loop through the methods of the selected group
            num_sections = len(groups[selected_group][1])  # Number of methods in this group
            rect_height = min((2.8 * first_last_rect_space), (total_sidebar_height - 2 * first_last_rect_space) / (spacing_factor * num_sections))  # Height constrained not to exceed
            font_size = max(20, int(rect_height // 4))  # Font size to display the method
            rect_font = pygame.font.Font(FONT, int(font_size))  # Font specific for method display

            y_position = top_bottom_margin + first_last_rect_space + counter * spacing_factor * rect_height  # Calculate vertical position of the rectangle
            rect = pygame.Rect(left_x_position + 11, y_position, sidebar_width, rect_height)  # Create the rectangle for this method

            pygame.draw.rect(screen, LIGHT_GRAY if counter % 2 == 0 else DARK_GRAY, rect, border_radius=20)  # Draw rectangle with alternating color
            display_dynamic_text(screen, method, left_x_position + 20, y_position + 10, 5, sidebar_width - 20, rect_font, WHITE, True, rect_height)  # Display the method name

            sidebar_rectangles.append((rect, method))  # Store the tuple (rectangle, method name)
            counter += 1  # Increment to move to the next method

        bottom_last_rect = y_position + rect_height  # Calculate the position of the bottom of the last drawn rectangle
        remaining_space = (top_bottom_margin + total_sidebar_height) - bottom_last_rect  # Empty space left in the sidebar
        return_y_position = bottom_last_rect + remaining_space // 2 - 17  # Vertical position of the "Back" button
        back_rect = pygame.Rect(left_x_position - 50 + sidebar_width // 2, return_y_position, 100, 35)  # Rectangle for the "Back" button

        pygame.draw.rect(screen, RED, back_rect, border_radius=50)  # Draw a red rectangle for the "Back" button
        back_font = pygame.font.Font(FONT, 28)  # Font for the "Back" button text
        back_text = back_font.render("Back", True, WHITE)  # Text surface "Back" in white
        back_text_rect = back_text.get_rect(center=(left_x_position + sidebar_width // 2, return_y_position + 17))  # Center the "Back" text
        screen.blit(back_text, back_text_rect)  # Draw the text on the screen
        sidebar_rectangles.append((back_rect, "back"))  # Store (back_rect, "back") for the event handler

    return sidebar_rectangles  # Return the final list of clickable rectangles and their associated action



def close_cross():
    """
    Displays an "X" at the designated position to close the window.
    Parameters: None
    Returns: Nothing
    """
    cross = font.render("X", True, RED)  # Creates the text surface "X" in red
    screen.blit(cross, close_cross_rect)  # Positions ("blits") the "X" into the close_cross_rect


def menu_button():
    """
    Displays "menu" in red.
    Parameters: None
    Returns: Nothing
    """
    menu_text = pygame.font.Font(FONT, 30).render("menu", True, RED)  # Text surface "<" in red
    screen.blit(menu_text, menu_button_rect)  # Positions the text


def toggle_fullscreen():
    """
    Switches between fullscreen mode and windowed mode, and updates button positions.
    Parameters: None
    Returns: Nothing
    """
    global close_cross_rect, menu_button_rect, fullscreen_button_rect
    global screen, fullscreen_state, screen_width, screen_height
    if fullscreen_state:  # If the app is already in fullscreen
        screen = pygame.display.set_mode((screen_width, screen_height))  # Switch back to windowed mode with initial dimensions
        fullscreen_state = False  # Set the fullscreen boolean to False
    else:  # If not in fullscreen, switch to it
        screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)  # Adapt window to current resolution
        fullscreen_state = True  # Set the boolean to True
    close_cross_rect = pygame.Rect(screen.get_width() - 50, 0, 50, 50)  # Update close cross area based on new size
    menu_button_rect = pygame.Rect(screen.get_width() - 132, 8, 50, 50)  # Update menu button area
    fullscreen_button_rect = pygame.Rect(screen.get_width() - 100, 10, 35, 35)  # Update fullscreen "F" button area


def info_button():
    """
    Displays a red circle with a white "?" in the bottom right corner.
    Parameters: None
    Returns: Nothing
    """
    pygame.draw.circle(screen, RED, (screen.get_width() - 180, 28), 20)  # Draws a red circle
    info = pygame.font.Font(FONT, 30).render("?", True, WHITE)  # Text surface "?" in white
    # Calculates the position to center the "?" in the circle and display it
    screen.blit(info, (screen.get_width() - 180 - info.get_width() // 2, 28 - info.get_height() // 2))
