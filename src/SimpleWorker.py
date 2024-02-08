#!/usr/bin/env python3
#
# The class for the SimpleWorker, which uses global information to move around.
# Always directly moves to the closest entity of interest. Acts as upper bound
# baseline for other worker types.
#
#############################################################################

import pygame
import random
import typing
from .WorkerBase import WorkerBase




class SimpleWorker(WorkerBase):
  def __init__(self, x: int, y: int, energy: float, speed: int):
    """
    Constructor. Setup a default worker.
    :param x: The x position of the worker.
    :param y: The y position of the worker.
    :param energy: The starting energy of the worker.
    :param speed: The movement speed of the worker.
    """
    super().__init__(x, y, energy)
    self._direction = [0, 0]
    self._speed = speed
    self._food_color = None

  def render(self, screen: "pygame.Screen"):
    """
    Renders the worker on the screen.
    :param screen: The screen to render the worker on.
    """
    pygame.draw.circle(screen, self._color, (self._x, self._y), 4)
    if self._has_food and self._primary_food is not None:
      pygame.draw.circle(screen, self._food_color, (self._x, self._y + 3), 2)

  def moveToFood(self):
    """
    Changes direction to the primary food source.
    """
    self._direction = self.computeDirection(self._primary_food)

  def moveToQueen(self):
    """
    Changes direction to the primary queen.
    """
    self._direction = self.computeDirection(self._primary_queen)

  def takeFood(self):
    """
    Takes food if it touches food and has no food.
    """
    if self._primary_food is not None:
      if self.computeDistance(self._primary_food) <= 40:
        self._has_food = self._primary_food.reduceEnergy(1)
        self._food_color = self._primary_food.getColor()
        self._primary_food = None

  def giveFoodToQueen(self):
    """
    Feeds queen if it touches the queen and has food.
    """
    if self._primary_queen is not None:
      if self.computeDistance(self._primary_queen) <= 40:
        self._primary_queen.increaseEnergy(1)
        self._has_food = False
        self._primary_food = None

  def behave(self, entity_lists: "EntityListContainer", width: int, height: int):
    """
    Contains all methods required for the behavior of the simple workers. Called every frame.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    :param width: The width of the scene screen.
    :param height: The height of the scene screen.
    """
    if not self.queenAlive(entity_lists.queen_list):
      self._primary_queen = None

    if self._primary_queen is not None and self._primary_queen._energy <= self._primary_queen._max_energy:
      if not self.foodAlive(entity_lists.food_list):
        self.findFood(entity_lists.food_list)

      if self._has_food:
        if self.queenAlive(entity_lists.queen_list):
          self.moveToQueen()
        else:
          self.moveRandomly()
      else:
        if self.foodAlive(entity_lists.food_list):
          self.moveToFood()
        else:
          self.moveRandomly()
    else:
      self.moveRandomly()

    self.performMovement(entity_lists, width, height, 5)

    if self._primary_queen is not None:
      if self._has_food:
        self.giveFoodToQueen()
      else:
        self.takeFood()

      if self._has_food:
        self.giveFoodToQueen()
      else:
        self.takeFood()

    self.reduceEnergy(self._energy_reduction_rate)
    
    return self.checkAlive()

  def __str__(self):
    return f"<Simple Worker {int(self._x)}:{int(self._y)}>"