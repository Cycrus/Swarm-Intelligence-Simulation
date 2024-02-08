#!/usr/bin/env python3
#
# The main menu of the program. Utilizes a state machine type to display different
# menu states.
#
#############################################################################

import pygame
import sys
import typing

from src.ConfigManager import ConfigManager


class MenuState:
  def __init__(self, name: str, menu_method: callable):
    """
    Constructor. Creates a new state for the menu.
    :param name: The name of the state.
    :param menu_method: The rendering method of the menu state.
    """
    self.name = name
    self.menu_method = menu_method
  
  def display(self):
    """
    Displays the menu state.
    """
    self.menu_method()

  def getName(self):
    """
    Returns the name of the state.
    :return: The name of the state.
    """
    return self.name


class Menu:
  def __init__(self):
    """
    Constructor. Initializes all aspect of the menu. Does not yet start pygame engine.
    """
    self.width = 1600
    self.height = 1000
    self.white = (255, 255, 255)
    self.button_color = (100, 100, 100)
    self.selected_button_color = (150, 150, 150)
    self.plain_text_color = (0, 0, 0)

    self.button_width = 600
    self.button_height = 130
    self.button_x = self.width / 2 - self.button_width / 2

    self.side_button_width = 350
    self.side_button_height = 90
    self.side_button_x = self.width - self.side_button_width - 20

    self.screen = None
    self.background_image = None
    self.button_font = None
    self.plain_text_font = None
    self.title_font = None
    self.small_font = None
    self.running = True
    self.continue_to_scene = True

    self.main_state = MenuState("Main Menu", self.displayMainMenu)
    self.help_state = MenuState("Help Text", self.displayHelp)
    self.curr_state = self.main_state

    self.mouse_clicked = False
    self.can_click_mouse = True

  def drawButton(self, text: str, button_rect: "pygame.Rect", font: "pygame.Font"):
    """
    Renders a button cursor sensitive onto the screen.
    :param text: The text on the button.
    :param button_rect: The rectangle defining the button outline.
    :param font: The font the text is rendered onto the button.
    """
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
      pygame.draw.rect(self.screen, self.selected_button_color, button_rect)
    else:
      pygame.draw.rect(self.screen, self.button_color, button_rect)

    text_surface = font.render(text, True, self.white)
    text_rect = text_surface.get_rect()
    text_rect.center = (button_rect.x + button_rect.width / 2,
                        button_rect.y + button_rect.height / 2)
    self.screen.blit(text_surface, text_rect)

  def drawText(self, text: str, font: "pygame.Font", x: int = None, y: int = None):
    """
    Draws the text on the popup.
    :param text: The text to render.
    :param font: The font to render the text with.
    :param x: The x position of the text center. If set to None, it is placed in the center of the x axis.
    :param y: The y position of the text center.
    """
    lines = text.split('\n')
    y_offset = 0

    center_text = False
    if x is None:
      center_text = True

    for line in lines:
      text_surface = font.render(line, True, self.plain_text_color)
      text_width, text_height = text_surface.get_size()
      if center_text:
        x = (self.width - text_width) // 2

      self.screen.blit(text_surface, (x, y + y_offset))
      y_offset += font.get_linesize()

  def startScene(self):
    """
    Leaves the menu loop and propagates the starting signal to the scene.
    """
    self.running = False
    self.continue_to_scene = True
    print("[INFO] Starting scene.")

  def exit(self):
    """
    Leaves the menu without propagating the starting signal to the scene.
    """
    self.running = False
    self.continue_to_scene = False
    print("[INFO] Exiting program.")

  def setDefaultSceneConfig(self):
    """
    Overwrites the default scene config file.
    """
    config_manager = ConfigManager()
    config_manager.setDefaultSceneConfig()

  def setDefaultQueensConfig(self):
    """
    Overwrites the default queens config file.
    """
    config_manager = ConfigManager()
    config_manager.setDefaultQueensConfig()

  def setState(self, state: "MenuState"):
    """
    Sets the new state of the menu to render.
    :param state: The new state to set the menu to.
    """
    self.curr_state = state
    print(f"[INFO] Showing {state.getName()}.")

  def setHelpState(self):
    """
    Sets the menu state to show the help dialog.
    """
    self.setState(self.help_state)

  def setMainState(self):
    """
    Sets the menu state to the main menu.
    """
    self.setState(self.main_state)

  def checkButtonMethod(self, button: "pygame.Rect", method: callable):
    """
    Checks if a button has been pressed and performs its method if yes.
    :param button: The button rectangle representing the outline of the button.
    :param method: The method to call when the button has been pressed.
    """
    mouse_pos = pygame.mouse.get_pos()
    if button.collidepoint(mouse_pos):
      if self.mouse_clicked:
        method()

  def checkEvents(self):
    """
    Checks for all keyboard and closing events fo pygame and performs
    according methods.
    """
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.exit()

  def displayMainMenu(self):
    """
    Displays all elements for the main menu.
    """
    start_button = pygame.Rect(self.button_x, 400, self.button_width, self.button_height)
    help_button = pygame.Rect(self.button_x, 600, self.button_width, self.button_height)
    exit_button = pygame.Rect(self.button_x, 800, self.button_width, self.button_height)

    default_scene_config_button = pygame.Rect(self.side_button_x, 720, self.side_button_width, self.side_button_height)
    default_queen_config_button = pygame.Rect(self.side_button_x, 840, self.side_button_width, self.side_button_height)

    self.checkButtonMethod(start_button, self.startScene)
    self.checkButtonMethod(help_button, self.setHelpState)
    self.checkButtonMethod(exit_button, self.exit)

    self.checkButtonMethod(default_scene_config_button, self.setDefaultSceneConfig)
    self.checkButtonMethod(default_queen_config_button, self.setDefaultQueensConfig)

    self.drawButton("Start", start_button, self.button_font)
    self.drawButton("Help", help_button, self.button_font)
    self.drawButton("Exit", exit_button, self.button_font)

    self.drawText("Set Default Configs", self.plain_text_font, self.side_button_x + 30, 670)
    self.drawButton("Default Scene Config", default_scene_config_button, self.small_font)
    self.drawButton("Default Queens Config", default_queen_config_button, self.small_font)

  def displayHelp(self):
    """
    Displays all elements for the help dialog.
    """
    back_button = pygame.Rect(self.button_x, 800, self.button_width, self.button_height)

    help_text = "Overview:\n" +\
                "This program is supposed to showcase a simple version of swarm behavior.\n" +\
                "There are queens with workers and food floating around. The small workers\n" +\
                "bring their dedicated queen food to survive. She can then produce new workers.\n\n" +\
                "Controls:\n" +\
                "Space - Pause/Resume simulation\n" +\
                "Escape - Exit to menu\n" +\
                "Left Click - Spawn new food source\n" +\
                "Right Click - Spawn/Remove obstacle\n" +\
                "Drag queen or food with mouse - Drag the element over the screen\n\n" +\
                "Configuration:\n" +\
                "You can configure the simulation with the files in the 'config' directory.\n" +\
                "In 'queen_config.json' you can add queens and configure their properties.\n" +\
                "In 'scene_config.json' You can configure global parameters of the simulation.\n"

    width = 1300
    height = 570
    x_pos = (self.width - width) //2 
    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    transparent_surface.set_alpha(128)

    pygame.draw.rect(transparent_surface, self.white, (0, 0, width, height))
    self.screen.blit(transparent_surface, (x_pos, 210))
    self.drawText(help_text, self.plain_text_font, None, 230)

    self.checkButtonMethod(back_button, self.setMainState)
    self.drawButton("Go Back", back_button, self.button_font)

  def registerMouseClick(self):
    """
    Registers if the left mouse button has been pressed and stores this info.
    Used for clicking buttons.
    """
    if pygame.mouse.get_pressed()[0]:
      if self.can_click_mouse:
        self.mouse_clicked = True
        self.can_click_mouse = False
      else:
        self.mouse_clicked = False

    else:
      self.mouse_clicked = False
      self.can_click_mouse = True

  def start(self) -> bool:
    """
    Launches the main menu. Initializes pygame engine.
    :return: The signal propagated to the scene if it should start or not.
    """
    pygame.init()
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("Main Menu")
    self.button_font = pygame.font.Font(None, 70)
    self.plain_text_font = pygame.font.Font(None, 45)
    self.title_font = pygame.font.Font(None, 130)
    self.small_font = pygame.font.Font(None, 40)
    self.continue_to_scene = True
    self.background_image = pygame.image.load("resources/ant_background.png")

    while self.running:
      self.registerMouseClick()
      self.screen.blit(self.background_image, (0, 0))
      self.drawText("Swarm Behavior Simulator", self.title_font, None, 80)
      self.drawText("2023 by Cyril Marx", self.small_font, 10, self.height - 40)
      self.drawText("Background generated with pruned-emaonly 1.5", self.small_font, 945, self.height - 40)
      self.curr_state.display()
      self.checkEvents()
      pygame.display.update()

    pygame.quit()

    return self.continue_to_scene


if __name__ == "__main__":
  menu = Menu()
  menu.start()