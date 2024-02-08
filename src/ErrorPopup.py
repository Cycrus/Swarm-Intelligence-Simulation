#!/usr/bin/env python3
#
# An error popup which appears if the user starts the simulation scene with
# a faulty configuration.
#
#############################################################################

import pygame
import sys
import typing

class ErrorPopup:
  def __init__(self, title: str, message: str):
    """
    Constructor. Sets up the popup to just be rendered later on.
    :param title: The title of the popup.
    :param message: The message shown on the popup. Not formatted, so this must
                    be done in the string.
    """
    pygame.init()
    self.width = 800
    self.height = 400
    self.title = title
    self.message = message
    self.font = pygame.font.Font(None, 36)
    self.title_font = pygame.font.Font(None, 52)
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("Scene Error Popup")
    self.bg_color = (170, 170, 170)
    self.button_color = (255, 255, 255)
    self.black = (0, 0, 0)

  def _drawText(self, text: str, font: "pygame.Font", x: int = None, y: int = None):
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
      text_surface = font.render(line, True, (0, 0, 0))
      text_width, text_height = text_surface.get_size()
      if center_text:
        x = (self.width - text_width) // 2

      self.screen.blit(text_surface, (x, y + y_offset))
      y_offset += font.get_linesize()

  def show(self):
    """
    Invokes the popup to render on the screen.
    """
    self.screen.fill(self.bg_color)

    ok_button = pygame.draw.rect(self.screen, self.button_color, ((self.width - 100) // 2, self.height - 80, 100, 40))
    ok_text = self.font.render("OK", True, self.black)
    ok_text_rect = ok_text.get_rect(center=ok_button.center)

    self._drawText(self.title, self.title_font, None, 50)
    self._drawText(self.message, self.font, None, 130)

    self.screen.blit(ok_text, ok_text_rect)
    pygame.display.update()

    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if ok_button.collidepoint(event.pos):
            pygame.quit()
            return