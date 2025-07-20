# Project: PI-THON
# Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import os  # Module to interact with the operating system (paths, folders, etc.)
import pygame  # Library for managing display, events, and timing (Pygame).

from display import screen, FONT, WHITE, BLACK, GRAY, GREEN, RED, info_button, menu_button, close_cross  # Specific imports from display.py

PI_PATH = os.path.join("data", "pi_reference.txt")  # Path to the file containing the reference decimals of π
RESULTS_FOLDER_PATH = os.path.join("data", "pi_estimation_results")  # Folder to store estimation results

def elapsed_time(start_ticks, formatted=True):
    """
    Calculates the elapsed time since 'start_ticks' and returns it either as HH:MM:SS or in seconds.

    Parameters:
        start_ticks (int): Reference value in milliseconds (pygame.time.get_ticks()) at the start.
        formatted (bool): If True, returns a formatted string HH:MM:SS. Otherwise, a float representing time in seconds.

    Returns:
        str or float: The elapsed time as "HH:MM:SS" if formatted=True, or a float in seconds.
    """
    total_time = max(0, (pygame.time.get_ticks() - start_ticks) / 1000)  # Calculates elapsed time in seconds since start_ticks
    return f"{int(total_time // 3600):02}:{int((total_time % 3600) // 60):02}:{int(total_time % 60):02}" if formatted else total_time  # Returns as HH:MM:SS or float

def event_handler():
    """
    Handles events (keyboard, mouse, etc.) and returns an action code along with the list of events.
    This allows centralizing event handlers in functions to reduce code repetition.

    Parameters:
        None.

    Returns:
        tuple: (action, events) where 'action' can be:
            - "menu": if the menu button is clicked
            - "info": if the info button is clicked
            - "click": for a simple left click elsewhere
            - None if no special event
        and 'events' is the list from pygame.event.get().
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get window width and height
    events = pygame.event.get()  # List of events since last call
    for event in events:  # Loop through each event
        if event.type == pygame.QUIT:  # If user closes the window
            pygame.quit()  # Close Pygame
            exit()  # Exit the Python program
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # If left mouse click
            if pygame.Rect(screen_width - 50, 0, 50, 50).collidepoint(event.pos):  # Click on close cross
                pygame.quit()  # Close Pygame
                exit()  # Exit the program
            if pygame.Rect(screen_width - 130, 0, 50, 50).collidepoint(event.pos):  # Click on menu button
                return "menu", events  # Return "menu" + list of events
            if pygame.Rect(screen_width - 200, 10, 40, 40).collidepoint(event.pos):  # Click on info button at bottom right
                return "info", events  # Return "info" + list of events
            return "click", events  # Any other clicked zone => "click"
    return None, events  # No particular event => None

def check_pi_estimation(pi_estimate, num_decimals):
    """
    Checks the validity of a π estimation by comparing it to the reference decimals (in PI_PATH).

    Parameters:
        pi_estimate (str): String representing the estimated decimals (e.g., "3.14159265...").
        num_decimals (int): Number of decimals to verify.

    Returns:
        str: A message on the validity of the estimation (correct, or error at decimal n, etc.).
    """
    with open(PI_PATH, "r") as file:  # Open the reference file
        pi_reference = file.read().strip()  # Read all decimals and strip surrounding spaces
    
    if num_decimals > len(pi_reference) - 2:  # Check we don't exceed available decimals in the file
        return "The calculated decimals cannot be verified."
    
    pi_reference_slice = pi_reference[:num_decimals + 2]  # Includes "3." + num_decimals
    
    if pi_estimate == pi_reference_slice:  # Directly compare the strings
        return "The π estimation is correct!"
    else:
        for i in range(len(pi_estimate)):  # Loop through the estimated string
            if pi_estimate[i] != pi_reference_slice[i]:  # If difference between program estimate and reference file
                return f"Error in the estimation starting at decimal #{i - 1}"  # Indicate position of error
    return "Unknown error."  # Default message if no other condition matched

def display_dynamic_text(screen, text, x, y, line_spacing, max_width, font, color=(255, 255, 255), center_text=True, rect_height=None, underline=False):
    """
    Displays text automatically wrapped over multiple lines, with optional centering.

    Parameters:
        screen (pygame.Surface): The surface to draw on (here, the window).
        text (str): The text to display.
        x (int): Starting X coordinate.
        y (int): Starting Y coordinate.
        line_spacing (int): Vertical space between each line.
        max_width (int): Maximum allowed width before wrapping to the next line.
        font (pygame.font.Font): Font used to render the text.
        color (tuple): Text color in RGB (default: white).
        center_text (bool): If True, horizontally centers each line in the given area.
        rect_height (int or None): Height within which to vertically center the text (used only for sidebar rectangles).

    Returns:
        int: The total height occupied by the displayed text.
    """
    words = text.split(" ")  # Split the text into words
    lines = []  # List of finalized lines
    current_line = ""  # Accumulated words for the current line

    for word in words:  # Loop through each word
        test_line = current_line + " " + word if current_line else word  # Test if this word can be added to the line
        if font.size(test_line)[0] <= max_width:  # If the line width stays within the limit
            current_line = test_line  # Update current line
        else:
            lines.append(current_line)  # Otherwise, store the previous line
            current_line = word  # And start a new line
    
    lines.append(current_line)  # Add the last line left in memory

    total_text_height = len(lines) * (font.get_height() + line_spacing) - line_spacing  # Total height of the text block

    if rect_height:  # If vertical centering is requested within a sidebar rectangle
        y += (rect_height - total_text_height) // 2  # Adjust Y coordinate to center vertically

    index = 0  # Counter for the loop
    for line in lines:  # Draw each line
        rendered_text = font.render(line, True, color)  # Create the text surface
        if center_text:
            # Horizontally center
            text_position = rendered_text.get_rect(center=(x + max_width // 2, y + index * (font.get_height() + line_spacing)))
            if underline:
                underline_text(screen, rendered_text, text_position.x, text_position.y, offset=4, color=color)
        else:
            # Place the line at (x, y)
            text_position = (x, y + index * (font.get_height() + line_spacing))
            if underline:
                underline_text(screen, rendered_text, x, y + index * (font.get_height() + line_spacing), offset=4, color=color)
        screen.blit(rendered_text, text_position)  # Blit the text to the screen
        index += 1  # Increment index each iteration

    return total_text_height  # Return the total height of the text


def underline_text(screen, rendered_text, x, y, offset=4, color=WHITE):
    """
    Underlines text.

    Parameters:
        screen (pygame.Surface): The surface to draw on (here, the window).
        rendered_text (pygame.render): A rendered text surface.
        x (int): Starting X coordinate.
        y (int): Starting Y coordinate.
        offset (int): Distance between the text and the underline (default: 4).
        color (tuple): Text color in RGB (default: white).

    Returns:
        None. The function just draws a line under the text.
    """
    pygame.draw.line(screen, color, (x, y + rendered_text.get_height() + offset), (x + rendered_text.get_width(), y + rendered_text.get_height() + offset), 2)


def display_result(estimation_pi_str, total_time, method_title, pi_check, num_decimals, info_function=None):
    """
    Displays the final result of the π estimation, with the ability to navigate through the decimals (pages).

    Parameters:
        estimation_pi_str (str): String containing all estimated π decimals.
        total_time (str): Elapsed time (formatted).
        method_title (str): Name of the calculation method used.
        pi_check (str): Verification result (correct or error).
        num_decimals (int): Number of calculated decimals.
        info_function (callable or None): Optional function to display additional information, called on "info".

    Returns:
        None: The function loops until "menu" or "info" triggers a state change.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get the window size
    title_font = pygame.font.Font(FONT, screen_height // 15)  # Font for main title
    text_font = pygame.font.Font(FONT, screen_height // 25)  # Font for medium texts
    decimals_font = pygame.font.Font(FONT, screen_height // 28)  # Smaller font to display decimals
    fixed_font = pygame.font.Font(FONT, 35)  # "Fixed" font for buttons

    margin_space = screen_width // 40  # Margin on each side
    max_space = screen_width - margin_space * 2  # Available width for displaying decimals
    example_text = decimals_font.render("0", True, WHITE)  # Measure the width of a "0" (fixed-width font)
    char_width = example_text.get_width()  # Width of one character
    chars_per_line = max_space // char_width  # Number of characters displayable per line
    x_position = screen_width - margin_space - max_space + char_width // 2  # Starting X position for decimals
    top_space_used = screen_height // 4  # Space at the top (title, text)
    bottom_space_used = 80  # Space at the bottom (buttons)
    available_space = screen_height - top_space_used - bottom_space_used  # Vertical space for decimals
    line_height = example_text.get_height() + 5  # Height of one text line
    lines_per_page = available_space // line_height  # Number of text lines per page

    decimals_per_page = chars_per_line * lines_per_page  # Total characters displayed per page
    pi_pages = [estimation_pi_str[i:i + decimals_per_page] for i in range(0, len(estimation_pi_str), decimals_per_page)]  # Split string into pages

    current_page = 0  # Current page index

    prev_button = pygame.Rect(50, screen_height - 80, 200, 50)  # Rectangle for "Previous" button
    next_button = pygame.Rect(screen_width - 250, screen_height - 80, 200, 50)  # Rectangle for "Next" button
    save_button = pygame.Rect(screen_width * 0.8 - 10, screen_height // 20 + screen_height // 20 - 10, screen_height * 0.2, screen_height * 0.127)  # Rectangle for "Save"

    while True:  # Display and interaction loop
        button_event, events = event_handler()  # Get potential action and events
        if button_event == 'menu':  # If "menu" button is clicked
            return  # Exit the function, thus leaving this screen
        if button_event == "info":  # If "info" button is clicked
            if not info_function():  # Call info function, if False => exit
                return

        for event in events:  # Loop through each event
            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click
                if prev_button.collidepoint(event.pos) and current_page > 0 or event.button == 4 and current_page > 0:  # Click "previous" or scroll up
                    current_page -= 1  # Previous page
                if next_button.collidepoint(event.pos) and current_page < len(pi_pages) - 1 or event.button == 5 and current_page < len(pi_pages) - 1:  # Click "next" or scroll down
                    current_page += 1  # Next page
                if save_button.collidepoint(event.pos):  # Click "Save" button
                    save_result(method_title, estimation_pi_str, num_decimals, total_time, pi_check)  # Save result

        screen.fill(BLACK)  # Clear the screen with black

        title = title_font.render(method_title, True, WHITE)  # Text surface for title
        description = text_font.render(f"Calculation of Pi using {method_title}.", True, WHITE)  # Short description
        final_time = text_font.render(f"Actual calculation time: {total_time}", True, WHITE)  # Total time indication
        pi_check_text = text_font.render(pi_check, True, GREEN if pi_check == "The π estimation is correct!" else RED)  # Check message (green or red)

        screen.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 50))  # Center the title
        screen.blit(description, (screen_width // 2 - description.get_width() // 2, screen_height // 20 + screen_height // 20))  # Place description lower
        screen.blit(final_time, (screen_width // 2 - final_time.get_width() // 2, screen_height // 20 + screen_height // 20 * 2))  # Place final time
        screen.blit(pi_check_text, (screen_width // 2 - pi_check_text.get_width() // 2, screen_height // 20 + screen_height // 20 * 3))  # Place check message

        y_position = top_space_used  # Starting Y coordinate for decimals
        for i in range(0, len(pi_pages[current_page]), chars_per_line):
            # Split current page into lines
            pi_line = pi_pages[current_page][i:i + chars_per_line]
            rendered_text = decimals_font.render(pi_line, True, WHITE)  # Surface for decimal lines
            screen.blit(rendered_text, (x_position, y_position))  # Display the decimal line
            y_position += line_height  # Move down for next line

        pygame.draw.rect(screen, GRAY, prev_button)  # Draw gray "Previous" button rectangle
        pygame.draw.rect(screen, GRAY, next_button)  # Draw gray "Next" button rectangle
        pygame.draw.rect(screen, GRAY, save_button)  # Draw gray "Save" button rectangle

        prev_text = fixed_font.render("Previous", True, BLACK)  # Text surface "Previous"
        next_text = fixed_font.render("Next", True, BLACK)  # Text surface "Next"

        screen.blit(prev_text, (prev_button.x + 100 - prev_text.get_width() // 2, prev_button.y + 25 - prev_text.get_height() // 2))  # Center and display text in button
        screen.blit(next_text, (next_button.x + 100 - next_text.get_width() // 2, next_button.y + 25 - next_text.get_height() // 2))  # Center and display text in button
        display_dynamic_text(screen, "save to a .txt file", screen_width * 0.8, screen_height // 20 + screen_height // 20 + screen_height // 100, save_button.height // 17, screen_height * 0.2 - 20, pygame.font.Font(FONT, screen_height // 38), WHITE)  # Display "Save" button text

        page_info = f"Page {current_page + 1}/{len(pi_pages)}"  # Current page / total pages text
        page_text = text_font.render(page_info, True, WHITE)  # Text surface for pagination
        screen.blit(page_text, (screen_width // 2 - page_text.get_width() // 2, screen_height - 70))  # Centered at bottom

        info_button()  # Draw "?" info button
        menu_button()  # Draw menu button
        close_cross()  # Draw close cross
        pygame.display.update()  # Update display to show all elements


def save_result(method, estimation_pi_str, num_decimals, total_time, estimation_check):
    """
    Saves the π estimation into a .txt file, inside the folder defined by RESULTS_FOLDER_PATH.

    Parameters:
        method (str): Name of the calculation method.
        estimation_pi_str (str): String containing all estimated π decimals.
        num_decimals (int): Number of calculated decimals.
        total_time (str): Calculation time (formatted).
        estimation_check (str): Message indicating the validity of the estimation.

    Returns:
        None: Creates or overwrites a .txt file containing all calculation details.
    """
    if num_decimals >= 1000000000:
        num_decimals = f"{num_decimals // 1000000000} billion(s)"  # Converts to "billion(s)" notation
    elif num_decimals >= 1000000:
        num_decimals = f"{num_decimals // 1000000} million(s)"  # Converts to "million(s)" notation
    elif num_decimals > 1000:
        num_decimals = f"{num_decimals // 1000} thousand"  # Converts to "thousand" notation
    elif num_decimals == 1000:
        num_decimals = "thousand"  # Exact case of 1000
    else:
        num_decimals = str(num_decimals)  # Otherwise, keep as string

    if not os.path.exists(RESULTS_FOLDER_PATH):  # Check if folder exists
        os.makedirs(RESULTS_FOLDER_PATH)  # Create if necessary

    file_name = f"pi_{method.lower()}_{num_decimals}.txt"  # Build file name
    if " " in file_name:
        file_name = file_name.replace(" ", "_")  # Replace spaces with underscores

    file_path = os.path.join(RESULTS_FOLDER_PATH, file_name)  # Build final absolute path

    with open(file_path, "w", encoding="utf-8") as file:  # Open file in write mode (UTF-8)
        file.write(f"Method: {method}\n")  # Write method
        file.write(f"Number of decimals: {num_decimals}\n")  # Write number of decimals
        file.write(f"Calculation time: {total_time}\n")  # Write total time
        file.write(f"{estimation_check}\n")  # Write verification result
        file.write(f"π estimation: \n{estimation_pi_str}")  # Write string containing π estimation
