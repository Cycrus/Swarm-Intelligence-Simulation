#!/usr/bin/env python3
#
# The class for the AdvancedWorker, which uses the advanced swarm simulation
# algorithm based on auditory location information.
#
#############################################################################

import pygame
import random
import typing
from .WorkerBase import WorkerBase


class AdvancedWorker(WorkerBase):
  def __init__(self, x, y, energy, speed, shouting_radius):
    """
    Constructor. Setup a default worker.
    :param x: The x position of the worker.
    :param y: The y position of the worker.
    :param energy: The starting energy of the worker.
    :param shouting_radius: The radius in which the worker can shout.
    """
    super().__init__(x, y, energy)
    self._direction = [0, 0]
    self.setRandomDirection()
    self._speed = speed
    self._shouting_radius = shouting_radius
    self._adjacent_workers = []
    self._internal_queen_distance = 99999
    self._internal_food_distance = 99999

  def clearAdjacentWorkerList(self):
    """
    Clears the whole adjacent worker list, which contains all workers in shouting range.
    """
    self._adjacent_workers.clear()

  def addToAdjacentWorkerList(self, worker: "AdvancedWorker"):
    """
    adds a worker to the adjacend worker list, which contains all workers in shouting range.
    :param worker: The worker to add.
    """
    self._adjacent_workers.append(worker)

  def scoutFood(self, food_list: list["Food"]):
    """
    Detects a new food source, if the worker touches one.
    :param food_list: The list containing all food in the scene.
    """
    for food in food_list:
      if self.computeDistance(food) <= 40:
        self._internal_food_distance = 0

  def scoutQueen(self):
    """
    Detects its primary queen, if the worker touches it.
    """
    if self._primary_queen is None:
      return

    if self.computeDistance(self._primary_queen) <= 40:
      self._internal_queen_distance = 0

  def takeFood(self, food_list: list["Food"]):
    """
    Takes food bite if it touches any and if it does not hold food. Then turns around.
    :param food_list: The list containing all food in the scene.
    """
    if self._has_food:
      return

    for food in food_list:
      if self.computeDistance(food) <= 40:
        self._has_food = food.reduceEnergy(1)
        self._food_color = food.getColor()
        self.turnAround()

  def giveFoodToQueen(self):
    """
    Gives food to the queen if it touches it and holds food. Then turns around
    """
    if self._primary_queen is None:
      return
    if not self._has_food:
      return

    if self.computeDistance(self._primary_queen) <= 40:
      self._primary_queen.increaseEnergy(1)
      self._has_food = False
      self.turnAround()

  def turnAround(self):
    """
    Reversed the direction to turn around 180 degree.
    """
    self._direction[0] = -self._direction[0]
    self._direction[1] = -self._direction[1]

  def askForNextDirection(self):
    """
    Performs the core part of the advanced worker algorithm. Checks for all workers
    in listening (shouting) range if memorized distance to food or queen of any worker is
    lower than its own. If it found one, it stores this new value and turns into the direction
    of the other worker.
    """
    best_food_direction_signal_sender = None
    best_queen_direction_signal_sender = None

    for adjacent_worker in self._adjacent_workers:
      heard_food_distance = adjacent_worker._internal_food_distance +\
                            adjacent_worker._shouting_radius
      heard_queen_distance = adjacent_worker._internal_queen_distance +\
                             adjacent_worker._shouting_radius

      if heard_food_distance < self._internal_food_distance:
        self._internal_food_distance = heard_food_distance
        best_food_direction_signal_sender = adjacent_worker
        
      if heard_queen_distance < self._internal_queen_distance:
        self._internal_queen_distance = heard_queen_distance
        best_queen_direction_signal_sender = adjacent_worker

    if self._has_food and best_queen_direction_signal_sender is not None:
      self._direction = self.computeDirection(best_queen_direction_signal_sender)
    elif not self._has_food and best_food_direction_signal_sender is not None:
      self._direction = self.computeDirection(best_food_direction_signal_sender)

  def getShoutingRadius(self) -> int:
    """
    Returns the shouting radius of the worker.
    :return: The shouting radius.
    """
    return self._shouting_radius

  def increaseInternalDistanceRepresentations(self):
    """
    Increases all internal distances by the step size of the frame. This serves as an
    approximation how far away the worker is from the last entity of interest found or heard of.
    """
    self._internal_queen_distance += self._speed
    self._internal_food_distance += self._speed

  def render(self, screen: "pygame.Screen"):
    """
    Renders the worker on the screen.
    :param screen: The screen to render the worker on.
    """
    pygame.draw.circle(screen, self._color, (self._x, self._y), 4)
    if self._has_food:
      pygame.draw.circle(screen, self._food_color, (self._x, self._y + 3), 2)

  def behave(self, entity_lists: "EntityListContainer", width: int, height: int):
    """
    Contains all methods required for the behavior of the advanced workers. Called every frame.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    :param width: The width of the scene screen.
    :param height: The height of the scene screen.
    """
    if not self.queenAlive(entity_lists.queen_list):
      self._primary_queen = None

    self.increaseInternalDistanceRepresentations()

    self.performMovement(entity_lists, width, height, 5)

    self.scoutFood(entity_lists.food_list)
    self.scoutQueen()
    self.giveFoodToQueen()
    self.takeFood(entity_lists.food_list)

    if self._primary_queen is None or self._primary_queen._energy > self._primary_queen._max_energy:
      self.moveRandomly()
    else:
      self.askForNextDirection()

    self.clearAdjacentWorkerList()

    self.reduceEnergy(self._energy_reduction_rate)
    
    return self.checkAlive()

  def __str__(self):
    return f"<Advanced Worker {self._x}:{self._y}>"
