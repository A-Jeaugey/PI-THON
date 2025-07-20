#Project: PI-THON
#Authors: Arthur Jeaugey, Samuel Mopty, Paul Chevasson

import pygame  # Import pygame for graphics and event handling
import pygame_textinput  # Import pygame_textinput to handle pygame text input
from display import screen, FONT, WHITE, BLACK, RED, GRAY, BLUE, close_cross, menu_button, info_button, screen_info  # Import display objects and constants
from utils import event_handler, display_dynamic_text, underline_text  # Import utility functions

def collisions_information():
    """
    Displays an information screen for the elastic collisions method
    
    Parameters:
        None
        
    Returns:
        True if the user clicks to start, False if they choose to go back.
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()  # Get screen width and height
    title_font = pygame.font.Font(FONT, screen_height // 15)  # Initialize font for title
    text_font = pygame.font.Font(FONT, screen_height // 50 if screen_height <= screen_info.current_h * 0.9 else screen_height // 40)  # Initialize font for description

    title_text = "Elastic Collisions Method"  # Title text

    description_text = (  # Description explaining the elastic collisions method
        "The elastic collisions method is an experimental approach to estimate π. "
        "It is based on the physics of elastic collisions between two blocks, where one is "
        "much more massive than the other. If the mass of the second block is 100^n times larger than "
        "the first, by counting the total number of collisions, one can get n decimal places of π. "
        "This concept was introduced by Gregory Galperin and Leonid A. Bunimovich in the 1990s."
    )

    formula_text = (  # Text containing the physics formula as a list of strings
        "The collisions follow two fundamental physics laws:",
        "1) Conservation of energy:",
        "1/2 * m1 * v1^2 + 1/2 * m2 * v2^2 = constant",
        "2) Conservation of momentum:",
        "m1 * v1 + m2 * v2 = constant"
    )

    visualization_text = (  # Text describing the visualization in the simulation
        "Visualization:",
        "• In the simulation, two blocks (one black and one red) collide and bounce.",
        "• The collision counter increases with each contact.",
        "• The total number of collisions directly provides an estimate of π.",
        "• A progress bar shows the percentage of collisions relative to the final estimate.",
        "• The user input allows changing the mass exponent of the red block. (0 to 6 to avoid overload)"
    )

    while True:
        screen.fill(BLACK)  # Fill screen with black

        # Display title
        title_rendered = title_font.render(title_text, True, WHITE)  # Render title text in white
        screen.blit(title_rendered, (screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40))  # Center title horizontally
        underline_text(screen, title_rendered, screen_width // 2 - title_rendered.get_width() // 2, screen_height // 40)  # Underline title

        # Display descriptions
        y_position = screen_height // 6  # Starting position for text
        y_position += display_dynamic_text(screen, description_text, screen_width // 20, y_position, 15, screen_width * 0.9, text_font) + 10  # Display description
        y_position += 10 if screen_height <= screen_info.current_h * 0.9 else screen_height // 50  # Add space depending on fullscreen
        for i, line in enumerate(formula_text):  # For each line of the formula
            y_position += display_dynamic_text(screen, line, screen_width // 20, y_position, 15, screen_width * 0.9, text_font, BLUE, underline=True if i == 0 or i == 1 or i == 3 else False) + screen_height // 50  # Display line in blue
        y_position += 0 if screen_height <= screen_info.current_h * 0.9 else screen_height // 50  # Add space depending on fullscreen
        for line in visualization_text:
            y_position += display_dynamic_text(screen, line, screen_width // 20, y_position, 15, screen_width * 0.9, text_font, underline=True if line == "Visualization:" else False) + screen_height // 50  # Display visualization text

        # Instruction to start
        instruction_rendered = title_font.render("Click anywhere to start.", True, RED)  # Render instruction in red
        screen.blit(instruction_rendered, (screen_width // 2 - instruction_rendered.get_width() // 2, screen_height * 0.92))  # Display instruction centered at bottom

        menu_button()  # Display menu button
        close_cross()  # Display close cross
        pygame.display.update()  # Update display

        # Event handling
        button_event, _ = event_handler()  # Get events
        if button_event == "menu":  # If user clicks menu
            return False  # Return to menu
        if button_event == "click":  # If user clicks screen
            return True  # Return True to continue


def collisions():
    """
    Main function to simulate elastic collisions between two blocks to estimate π.
    
    Parameters:
        None
        
    Returns:
        Nothing. The function manages the simulation display and updates the counters and π estimation.
    """
    if not collisions_information():  # Displays the info screen and returns to the menu if the user clicks the menu button in collisions_information
        return

    # Get display window dimensions
    screen_width, screen_height = screen.get_width(), screen.get_height()
    # Initialize font for on-screen information text
    text_font = pygame.font.Font(FONT, screen_height // 20)

    counter = 0  # Total collision counter
    x1, x2 = 200, 400  # Initial positions of the two blocks
    speed_1 = 0  # Initial speed of block 1
    speed_2 = -1  # Initial speed of block 2
    mass_power = 1  # Initial mass exponent
    last_mass_input = mass_power  # Stores the last entered mass exponent value
    mass_1, mass_2 = 1, 100 ** mass_power  # Masses of the two blocks, the second being much more massive
    cube_size = (mass_power * 700) ** 0.65 + 50  # Calculate block size based on mass exponent
    text_input = pygame_textinput.TextInputVisualizer(font_color=BLACK, cursor_color=BLACK)  # Initialize input box to change mass exponent
    current_explosion = 0  # Control variable for explosion animation during a collision
    explosion_position = (0, 0)  # Explosion position
    fast_collisions = 0  # Counter for fast collisions (for animation)

    # Dictionary associating mass exponent to an estimated number of collisions (for progress bar only)
    COLLISIONS_ESTIMATE = {
        0: 3,
        1: 31,
        2: 314,
        3: 3141,
        4: 31415,
        5: 314159,
        6: 3141592
    }

    if mass_power in COLLISIONS_ESTIMATE:
        collision_estimate = COLLISIONS_ESTIMATE[mass_power]  # Use the corresponding estimate
    else:
        collision_estimate = COLLISIONS_ESTIMATE[6]  # Default to value for 6

    while True:  # Main loop
        button_event, events = event_handler()  # Get user events
        if button_event == "menu":  # If user clicks menu
            return  # Return to menu
        if button_event == "info":  # If user clicks the info button
            if not collisions_information():  # Redisplay the info screen
                return  # Return to menu if they click the menu button in the info function
        for event in events:
            # If the Enter key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if text_input.value.isdigit():  # If input is numbers only
                    mass_power = min(6, int(text_input.value))  # Update mass exponent, max 6
                    collision_estimate = COLLISIONS_ESTIMATE[mass_power]  # Update the corresponding estimate
                text_input.value = ""  # Reset input box

        text_input.update(events)  # Update input box with events
        if len(text_input.value) > 1:  # Limit input to 1 character
            text_input.value = text_input.value[:1]

        x1 += speed_1  # Update block 1 position based on speed
        x2 += speed_2  # Update block 2 position based on speed

        if x1 < 20:  # If block 1 hits the left edge of the screen
            speed_1 *= -1  # Reverse block 1 speed
            counter += 1  # Increment collision counter

        # If blocks are close enough or crossed each other
        if (x1 - x2) ** 2 <= 50 ** 2 or x2 < x1:
            # Calculate new speeds after collision using conservation of energy and momentum
            speed_1, speed_2 = ((mass_1 - mass_2) * speed_1 + 2 * mass_2 * speed_2) / (mass_1 + mass_2), ((mass_2 - mass_1) * speed_2 + 2 * mass_1 * speed_1) / (mass_1 + mass_2)
            counter += 1  # Increment collision counter
            
            fast_collisions += 1  # Increment fast collision counter

            if current_explosion == 0:  # If no explosion is ongoing
                explosion_position = ((x1 + x2) // 2, 620)  # Set explosion position between blocks

            current_explosion = 10  # Start explosion animation
            if fast_collisions > 5:
                fast_collisions = 5  # Limit fast collision counter

        progress = (counter / collision_estimate) * 100  # Calculate progress percentage

        screen.fill(WHITE)  # Fill screen white to refresh display
        counter_text = text_font.render(f"Collisions: {counter}", True, BLACK)  # Prepare collision counter text
        mass_display = text_font.render(f"Mass exponent: {mass_power}", True, BLACK)  # Prepare mass exponent text
        pi_display = text_font.render(f"π estimate: {str(counter)[0]}.{str(counter)[1:]}", True, BLACK)  # Display π estimate based on counter
        progress_text = text_font.render(f"Progress: {progress:.2f}%", True, RED)  # Prepare progress percentage text

        bar_width = screen_width // 4  # Set progress bar width
        bar_height = 20  # Set progress bar height
        progress_bar = pygame.Rect(screen_width // 2 - bar_width // 2, screen_height // 3, bar_width, bar_height)  # Progress bar position and size
        filled_bar = pygame.Rect(screen_width // 2 - bar_width // 2, screen_height // 3, int((progress / 100) * bar_width), bar_height)  # Filled part based on progress

        pygame.draw.rect(screen, GRAY, progress_bar)  # Draw empty gray progress bar
        pygame.draw.rect(screen, RED, filled_bar)  # Draw filled red part

        # Display texts centered horizontally
        screen.blit(counter_text, (screen_width // 2 - counter_text.get_width() // 2, screen_height // 10))
        screen.blit(mass_display, (screen_width // 2 - mass_display.get_width() // 2, screen_height // 6.5))
        screen.blit(pi_display, (screen_width // 2 - pi_display.get_width() // 2, screen_height // 4.8))
        screen.blit(progress_text, (screen_width // 2 - progress_text.get_width() // 2, screen_height // 3.8))
        screen.blit(text_input.surface, (screen_width // 2 - text_input.surface.get_width() // 2, screen_height // 2.6))
        
        # Draw red block (with minimal position adjustment to avoid going off screen due to a bug)
        if x2 > 70:
            pygame.draw.rect(screen, (255, 0, 0), (x2, 600 - cube_size + 50, cube_size, cube_size))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (70, 600 - cube_size + 50, cube_size, cube_size))
        
        # Draw black block (with minimal position adjustment to avoid going off screen due to a bug)
        if x1 <= 20:
            pygame.draw.rect(screen, BLACK, (20, 600, 50, 50))
        else:
            pygame.draw.rect(screen, BLACK, (x1, 600, 50, 50))

        # Reset simulation if mass exponent has changed
        if last_mass_input != mass_power:
            last_mass_input = mass_power
            screen.fill(WHITE)  # Clear screen
            counter = 0
            x1, x2 = 200, 400
            speed_1 = 0
            speed_2 = -1
            mass_1, mass_2 = 1, 100 ** mass_power
            cube_size = (mass_power * 700) ** 0.65 + 50
            collision_estimate = COLLISIONS_ESTIMATE[mass_power]

        # Delay depending on mass exponent to adjust simulation speed (for user experience)
        if mass_power == 0 or mass_power == 1:
            pygame.time.delay(4)
        elif mass_power == 2 or mass_power == 3:
            pygame.time.delay(2)
        else:
            pygame.time.delay(0)
    
        # Explosion animation during collision
        if current_explosion > 0:  # Check if an explosion is ongoing (animation state control)
            base_size = (10 - current_explosion) * 5  # Calculate base size of explosion (gets bigger as current_explosion decreases)
            explosion_radius = base_size + fast_collisions * 3  # Determine final explosion radius with fast collision factor
            explosion_color = (255, 100, 0, current_explosion * 25)  # Define explosion color (orange) with opacity depending on current_explosion

            explosion_surface = pygame.Surface((explosion_radius * 2, explosion_radius * 2), pygame.SRCALPHA)  # Create transparent surface large enough for explosion
            pygame.draw.circle(explosion_surface, explosion_color, (explosion_radius, explosion_radius), explosion_radius)  # Draw explosion circle

            screen.blit(explosion_surface, (explosion_position[0] - explosion_radius, explosion_position[1] - explosion_radius))  # Display explosion centered on position

            current_explosion -= 1  # Decrease current_explosion to gradually animate disappearance

        info_button()  # Display info button
        menu_button()  # Display menu button
        close_cross()  # Display close cross
        pygame.display.update()  # Refresh display
