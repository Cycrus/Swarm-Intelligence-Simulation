import pygame
import random
from .Entity import Entity

class Obstacle(Entity):
  def __init__(self, x: int, y: int, size: int):
    """
    Constructor. Sets up the food.
    :param x: Initial x position of food.
    :param y: Initial y position of food.
    :param size: The size of the obstacle.
    """
    super().__init__(x, y)
    self._size = size
    self._half_size = size // 2 + 7
    self._true_half_size = size // 2
    self._x = x
    self._y = y
    self._color = (92, 64, 51)
    self._darker_color = [c // 2 for c in self._color]
    self._energy = 1

  def renderShadow(self, screen: "pygame.Screen"):
    """
    Renders the shadow of the obstacle onto screen.
    :param screen: The screen to render the shadow on.
    """
    pygame.draw.rect(screen, self._shadow_color, ((self._x - self._true_half_size + self._shadow_distance, self._y - self._true_half_size + self._shadow_distance),
                                           (self._size, self._size)))

  def render(self, screen: "pygame.Screen"):
    """
    Renders the obstacle onto screen.
    :param screen: The screen to render the obstacle on.
    """
    pygame.draw.rect(screen, self._color, ((self._x - self._true_half_size, self._y - self._true_half_size),
                                           (self._size, self._size)))
    pygame.draw.rect(screen, self._darker_color, ((self._x - self._true_half_size * 0.7, self._y - self._true_half_size * 0.7),
                                                  (self._size * 0.7, self._size * 0.7)))

  def behave(self, entity_lists: "EntityListContainer", width: int, height: int):
    """
    Does nothing. An obstacle does not move around.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    :param width: The width of the scene screen.
    :param height: The height of the scene screen.
    """
    return True

  def checkCollision(self, entity: "Entity") -> bool:
    """
    Checks if a collision happened with this obstacle.
    :param entity: The other entity to check the collision with.
    :return: True if a collision was detected.
    """
    if entity._x > self._x - self._half_size and entity._x < self._x + self._half_size:
      if entity._y > self._y - self._half_size and entity._y < self._y + self._half_size:
        return True
    return False

  def kill(self, entity_lists: "EntityListContainer"):
    """
    Kills the obstacle and removes it from all lists.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    """
    entity_lists.entity_list.remove(self)
    entity_lists.obstacle_list.remove(self)

  def __str__(self):
    return f"<Obstacle {self._x}:{self._y}>"