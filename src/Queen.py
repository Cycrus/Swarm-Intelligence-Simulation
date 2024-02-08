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
from .SimpleWorker import SimpleWorker
from .AdvancedWorker import AdvancedWorker


class Queen(Entity):
  def __init__(self, x: int, y: int, queen_description: dict):
    """
    Constructor. Initializes the queen and its worker type with the given configs.
    :param x: Initial x position.
    :param y: Initial y position.
    :param queen_description: The config for this queen.
    """
    super().__init__(x, y)
    self.setRandomDirection()
    self._speed = queen_description["speed"]
    self._energy_reduction_rate = queen_description["energy_reduction_rate"]
    self._birth_worker_threshold = queen_description["birth_energy_threshold"]
    self._start_energy = queen_description["energy"]
    self._energy = queen_description["energy"]
    self._max_energy = queen_description["max_energy"]
    self._color = queen_description["color"]
    self._sec_color = (self._color[0] / 2,
                       self._color[1] / 2,
                       self._color[2] / 2)
    self._worker_list = []
    self._sorted_worker_list = []
    self._worker_description = queen_description["worker_type"]
    self._worker_spawn_cost = 3
    self._frame_counter = 0

  def renderShadow(self, screen: "pygame.Screen"):
    """
    Renders the shadow of the queen onto screen.
    :param screen: The screen to render the shadow on.
    """
    size = self._energy / 10
    if size <= 1:
      size = 1
    pygame.draw.circle(screen, self._shadow_color, (self._x + self._shadow_distance, self._y + self._shadow_distance), size)

  def render(self, screen: "pygame.Screen"):
    """
    Renders the queen onto screen.
    :param screen: The screen to render the queen on.
    """
    size = self._energy / 10
    if size <= 1:
      size = 1
    pygame.draw.circle(screen, self._color, (self._x, self._y), size)
    pygame.draw.circle(screen, self._sec_color, (int(self._x - size * 0.5), self._y), size * 0.5)
    pygame.draw.circle(screen, self._sec_color, (int(self._x + size * 0.5), self._y), size * 0.5)

  def behave(self, entity_lists: "EntityListContainer", width: int, height: int):
    """
    Contains the queen behavior. Basically only floats the queen into random directions.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    :param width: The width of the scene screen.
    :param height: The height of the scene screen.
    """
    if self._frame_counter % 1 == 0:
      if self._worker_description["behavior"] == "AdvancedWorker":
        self.sortWorkerListByX()
        self.computeAdjacentWorkers()

    if(random.randint(0, 1000) <= 5):
      self.setRandomDirection()

    self.performMovement(entity_lists, width, height, 0)

    if self._energy > self._birth_worker_threshold:
      self.spawnWorker(1, entity_lists.entity_list, entity_lists.worker_list,
                       width, height, self._worker_spawn_cost, 40)

    energy_corrected_reduction = max(((self._energy - self._start_energy) / 1500), 0)
    self.reduceEnergy(self._energy_reduction_rate + energy_corrected_reduction)
    self._frame_counter += 1
    return self.checkAlive()

  def kill(self, entity_lists: "EntityListContainer"):
    """
    Kills the queen and removes it from all lists.
    :param entity_lists: The container of all entity lists which is managed by the Scene.
    """
    entity_lists.entity_list.remove(self)
    entity_lists.queen_list.remove(self)

  def spawnWorker(self, num_workers: int, entity_list: list["Entity"], worker_list: list["WorkerBase"],
                  width: int, height: int, cost: int, spawn_distance: int):
    """
    Spawns a number of workers around the queen.
    :param num_workers: The amount of workers to spawn.
    :param entity_list: The list of all entities in the EntityListContainer.
    :param worker_list: The list of all workers in the EntityListContainer.
    :param width: The width of the screen.
    :param height: The height of the screen.
    :param cost: The cost for the queen to spawn each of the workers.
    :param spawn_distance: The radius to spawn the workers around the queen.
    """
    for _ in range(num_workers):
      x = random.randint(max(0, int(self._x) - spawn_distance),
                         min(width, int(self._x) + spawn_distance))
      y = random.randint(max(0, int(self._y) - spawn_distance),
                         min(height, int(self._y) + spawn_distance))
                         
      starting_energy = random.randint(int(self._worker_description["mean_energy"] - max(self._worker_description["energy_range"], 1)),
                                       int(self._worker_description["mean_energy"] + self._worker_description["energy_range"]))
      speed = random.randint(int(self._worker_description["mean_speed"] - max(self._worker_description["speed_range"], 1)),
                             int(self._worker_description["mean_speed"] + self._worker_description["speed_range"]))

      if self._worker_description["behavior"] == "SimpleWorker":
        worker = SimpleWorker(x, y, starting_energy, speed)
      elif self._worker_description["behavior"] == "AdvancedWorker":
        shouting_radius = self._worker_description["shouting_radius"]
        worker = AdvancedWorker(x, y, starting_energy, speed, shouting_radius)

      entity_list.append(worker)
      worker_list.append(worker)
      self._worker_list.append(worker)
      worker.selectQueen(self)
      self.reduceEnergy(cost)

  def removeWorker(self, worker: list["WorkerBase"]):
    """
    Removes a worker from the worker list of the queen.
    """
    self._worker_list.remove(worker)

  def addWorker(self, worker: list["WorkerBase"]):
    """
    Adds a worker to the worker list of the queen.
    """
    self._worker_list.append(worker)

  def getWorkerList(self) -> list["WorkerBase"]:
    """
    Returns the list of all workers assigned to this queen.
    """
    return self._worker_list

  def getWorkerNum(self) -> int:
    """
    Returns the total number of all workers in this queens colony.
    """
    return len(self._worker_list)

  def sortWorkerListByX(self):
    """
    Sorts the worker list of this queen by the x axis. Used for optimizing the advanced worker
    shouting algorithm.
    """
    def getWorkerX(worker):
      return worker._x
    self._sorted_worker_list = sorted(self._worker_list, key = getWorkerX)

  def computeAdjacentWorkers(self):
    """
    Computes the adjacent workers for all workers assigned to this queen. Used for optimizing
    the advanced worker shouting algorithm.
    """
    while len(self._sorted_worker_list) > 0:
      worker = self._sorted_worker_list.pop(0)
      radius = worker.getShoutingRadius()

      for potential_partner in self._sorted_worker_list:
        if potential_partner._x - worker._x > radius:
          break

        if abs(potential_partner._y - worker._y) <= radius:
          worker.addToAdjacentWorkerList(potential_partner)
          potential_partner.addToAdjacentWorkerList(worker)

  def __str__(self):
    return f"<Queen {int(self._x)}:{int(self._y)}>"

  def __repr__(self):
    return self.__str__()