#!/usr/bin/env python3
#
# The class representing a food source workers can take bites from to give to
# their queens.
#
#############################################################################

import pygame
import random
import typing
from .Entity import Entity

class Food(Entity):
  def __init__(self, x: int, y: int, energy: float, speed: int, type: int):
    """
    Constructor. Sets up the food.
    :param x: Initial x position of food.
    :param y: Initial y position of food.
    :param speed: Movement (floating) speed.
    :param type: Food type. Currently only acts as color scheme.
    """
    super().__init__(x, y)
    self.setRandomDirection()
    self.setRandomSpeed(speed / 2, speed * 2)

    self.setRandomEnergy(energy / 2, energy * 2)

    self._type = type

    if self._type == 0:
      self._color = (0, 150, 0)
    elif self._type == 1:
      self._color = (150, 0, 0)
    elif self._type == 2:
      self._color = (0, 0, 150)
    else:
      self._color = (150, 150, 150)

    self._sec_color = (self._color[0] / 2,
                       self._color[1] / 2,
                       self._color[2] / 2)

  def renderShadow(self, screen: "pygame.Screen"):
    """
    Renders the shadow of the food onto screen.
    :param screen: The screen to render the shadow on.
    """
    size = self._energy / 10
    if size <= 1:
      size = 1
    pygame.draw.circle(screen, self._shadow_color, (self._x + self._shadow_distance, self._y + self._shadow_distance), size)

  def render(self, screen: "pygame.Screen"):
    """
    Renders the food onto screen.
    :param screen: The screen to render the food on.
    """
    size = self._energy / 10
    if size <= 1:
      size = 1
    pygame.draw.circle(screen, self._color, (self._x, self._y), size)
    pygame.draw.circle(screen, self._sec_color, (self._x, self._y), size * 0.6)

  def behave(self, entity_lists: "EntityListContainer", width: int, height: int):
    """
    Contains the food behavior. Basically only floats the food into a single direction.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    :param width: The width of the scene screen.
    :param height: The height of the scene screen.
    """
    self.performMovement(entity_lists, width, height, 0)
    return self.checkAlive()

  def kill(self, entity_lists: "EntityListContainer"):
    """
    Kills the food and removes it from all lists.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    """
    entity_lists.entity_list.remove(self)
    entity_lists.food_list.remove(self)

  def __str__(self):
    return f"<Food {int(self._x)}:{int(self._y)}>"

  def __repr__(self):
    return self.__str__()