#!/usr/bin/env python3
#
# The basic abstraction of any entity present in the simulation scene.
# Equipped with basic operations and properties most entities could need.
# Also provides an interface which can be used to define custom behavior.
# All entities come with a position, movement direction, energy value, and color.
# Additionally, all entites can be equipped with a shadow.
#
#############################################################################

import pygame
import random
import math
import typing


class Entity:
  def __init__(self, x: int, y: int):
    """
    Constructor. Sets all default values for an entity and places it to
    a specified position.
    :param x: The initial x position of the entity.
    :param y: The initial y position of the entity.
    """
    self._x = x
    self._y = y
    self._direction = [0, 0]
    self._speed = 0
    self._energy = 100
    self._color = (255, 255, 255)
    self._shadow_color = (40, 40, 40)
    self._shadow_distance = 7

  def setPosition(self, x: int, y: int):
    """
    Sets the position of the entity.
    :param x: The new x position of the entity.
    :param y: The new y position of the entity.
    """
    self._x = x
    self._y = y

  def setRandomDirection(self):
    """
    Randomly sets a movement direction of the entity.
    """
    self._direction = [random.uniform(-1, 1), random.uniform(-1, 1)]

  def setRandomSpeed(self, min: int, max: int):
    """
    Randomly sets the movement speed of the entity in a designated range.
    :param min: The min boundary of the speed.
    :param max: The max boundary of the speed.
    """
    self._speed = random.randint(int(min), int(max))

  def setRandomEnergy(self, min: int, max: int):
    """
    Randomly sets the energy of the entity in a designated range.
    :param min: The min boundary of the energy.
    :param max: The max boundary of the energy.
    """
    self._energy = random.randint(int(min), int(max))

  def reduceEnergy(self, reduction: float) -> bool:
    """
    Reduces the energy of the entity by a certain value to minimum 0.
    :param reduction: The value to reduce the energy.
    :return: True if entity is still alive.
    """
    if self._energy <= 0:
      return False

    self._energy -= reduction
    return True

  def increaseEnergy(self, increase: float):
    """
    Increases the energy of the entity by a certain value.
    :param increase: The value to increase the energy.
    """
    self._energy += increase

  def computeDistance(self, target_entity: "Entity") -> float:
    """
    Computes the distance between this entity and another entity in pixels.
    :param target_entity: The entity to compute the distance to.
    :return: The distance between both objects.
    """
    return math.sqrt((self._x - target_entity._x) ** 2 + (self._y - target_entity._y) ** 2)

  def computeDirection(self, target_entity: "Entity") -> list[int, int]:
    """
    Computes the direction from this entity and another entity as a cartesian vector.
    :param target_entity: The entity to compute the direction to.
    :return: The direction of the entity to the other.
    """
    dx = target_entity._x - self._x
    dy = target_entity._y - self._y

    length = math.sqrt(dx ** 2 + dy ** 2)

    if length != 0:
      normalized_direction = [dx / length, dy / length]
    else:
      normalized_direction = [0, 0]

    return normalized_direction

  def performMovement(self, entity_lists: "EntityListContainer", width: int, height: int, jitter: int):
    """
    Performs a single movement step based on current speed and direction.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    :param width: The width of the scene screen.
    :param height: The height of the scene screen.
    :param jitter: The strength of movement jitter. A random value the direction of the movement
                   is skewed to. Gives movements a more natural feeling. If set to 0, there is no
                   movement jitter.
    """
    new_x = self._x + (self._direction[0] * self._speed + random.randint(0, jitter) * random.randint(-1, 1))
    new_y = self._y + (self._direction[1] * self._speed + random.randint(0, jitter) * random.randint(-1, 1))

    if new_x < 0 or new_x > width:
      self._direction[0] *= -1
    new_x = max(0, min(width, new_x))

    if new_y < 0 or new_y > height:
      self._direction[1] *= -1
    new_y = max(0, min(height, new_y))

    for obstacle in entity_lists.obstacle_list:
      if obstacle.checkCollision(self):
        top_dist = abs(new_y - (obstacle._y - obstacle._half_size))
        right_dist = abs(new_x - (obstacle._x + obstacle._half_size))
        bottom_dist = abs(new_y - (obstacle._y + obstacle._half_size))
        left_dist = abs(new_x - (obstacle._x - obstacle._half_size))
        
        if min(top_dist, bottom_dist) < min(right_dist, left_dist):
          self._direction[1] *= -1
          if top_dist < bottom_dist:
            new_y = obstacle._y - obstacle._half_size
          else:
            new_y = obstacle._y + obstacle._half_size
        else:
          self._direction[0] *= -1
          if left_dist < right_dist:
            new_x = obstacle._x - obstacle._half_size
          else:
            new_x = obstacle._x + obstacle._half_size

    self._x, self._y = new_x, new_y

  def render(self, screen: "pygame.Screen"):
    """
    Interface for the rendering method. Called by the scene every frame.
    :param screen: The pygame screen object to render to.
    """
    pygame.draw.rect(screen, self._color, (self._x, self._y), 10, 10)

  def checkAlive(self):
    """
    Checks if the entity is still alive (if energy > 0).
    :return: True if still alive.
    """
    return self._energy > 0

  def getEnergy(self) -> int:
    """
    Getter for the energy of the entity.
    :return: The energy 
    """
    return self._energy

  def getColor(self) -> "tuple[int]":
    """
    Getter for the color of the entity.
    :return: The RGB color as a tuple with three elements.
    """
    return self._color

  def kill(self, entity_lists: "EntityListContainer"):
    """
    Interface for killing the entity. Must be adapted to be removed from the lists it was included in.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    """
    entity_lists.entity_list.remove(self)

  def behave(self, entity_lists: "EntityListContainer", width: int, height: int):
    """
    Interface for the behavior of the entity. Is called every frame.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    :param width: The width of the scene screen.
    :param height: The height of the scene screen.
    """
    pass

  def __str__(self):
    return f"<Default Entity {self._x}:{self._y}>"

  def __repr__(self):
    return self.__str__()