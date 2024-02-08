#!/usr/bin/env python3
#
# The base class which all worker types are derived from. Offers useful
# methods the workers need to work.
#
#############################################################################

import pygame
import random
import typing
from .Entity import Entity
from .Food import Food

class WorkerBase(Entity):
  def __init__(self, x: int, y: int, energy: float):
    """
    Constructor. Setup a default worker.
    :param x: The x position of the worker.
    :param y: The y position of the worker.
    :param energy: The starting energy of the worker.
    """
    super().__init__(x, y)
    self._energy = energy
    self._energy_reduction_rate = 0.1
    self._primary_queen = None
    self._primary_food = None
    self._color = (100, 100, 100)
    self._lifetime = 0
    self._has_food = False
    self._food_color = None

  def queenAlive(self, queen_list: list["Queen"]):
    """
    Checks if the primary queen of the worker is still alive.
    :param queen_list: The list containing all queens in the scene.
    :return: True if the primary queen is still alive.
    """
    return self._primary_queen in queen_list

  def foodAlive(self, food_list: list["Food"]):
    """
    Checks if the current primary food of the worker still exists.
    :param food_list: The list containing all food in the scene.
    :return: True if the primary food still exists.
    """
    return self._primary_food in food_list

  def moveRandomly(self):
    """
    Sets a random direction for the next movement.
    """
    self.setRandomDirection()

  def selectFood(self, food: "Food"):
    """
    Assigns a new primary food for the worker.
    """
    self._primary_food = food

  def selectQueen(self, queen: "Queen"):
    """
    Assigns a new primary queen for the worker.
    """
    if self._primary_queen:
      self._primary_queen.removeWorker(self)
    self._primary_queen = queen
    if not self in self._primary_queen.getWorkerList():
      self._primary_queen.addWorker(self)
    if self._primary_queen is not None:
      self._color = self._primary_queen.getColor()

  def findFood(self, food_list: list["Food"]):
    """
    Finds the closest food and assigns it as the primary food.
    :param food_list: The list containing all food in the scene.
    """
    self.selectFood(self.findClosestEntity(food_list))

  def findQueen(self, queen_list: list["Queen"]):
    """
    Finds the closest queen and assigns it as the primary queen.
    :param queen_list: The list containing all queens in the scene.
    """
    self.selectQueen(self.findClosestEntity(queen_list))

  def findClosestEntity(self, entity_list: list["Entity"]) -> "Entity":
    """
    Finds the closest instance of an entity in any entity list.
    :param entity_list: The list in which the closest entity should be looked for.
    :return: The closest entity if one has been found. If not None.
    """
    closest_entity = None
    closest_entity_distance = None
    for entity in entity_list:
      if closest_entity is None:
        closest_entity = entity
        closest_entity_distance = self.computeDistance(entity)
        continue

      new_entity_distance = self.computeDistance(entity)
      if new_entity_distance < closest_entity_distance:
        closest_entity_distance = new_entity_distance
        closest_entity = entity

    return closest_entity

  def kill(self, entity_lists: "EntityListContainer"):
    """
    Kills the worker and removes it from all lists.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    """
    entity_lists.entity_list.remove(self)
    entity_lists.worker_list.remove(self)
    if self._primary_queen is not None:
      self._primary_queen.removeWorker(self)
