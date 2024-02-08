#!/usr/bin/env python3
#
# The core of the program. Controls the whole simulation and, if required,
# renders all elements onto the screen.
#
#############################################################################

import pygame
import random
import threading
import copy
import itertools
import typing
from .Food import Food
from .Queen import Queen
from .Obstacle import Obstacle
from .EntityListContainer import EntityListContainer

class Scene:
  def __init__(self, scene_settings: dict, show_rendering: bool):
    """
    Constructor. Initializes the whole scene.
    :param scene_settings: The scene config dictionary.
    :param show_rendering: If True, the scene is rendered. If False, all
                           rendering is avoided.
    """
    self._show_rendering = show_rendering

    if self._show_rendering:
      pygame.init()
      pygame.display.set_caption("Swarm Intelligence Simulation")

    self._scene_settings = scene_settings
    self._min_food = scene_settings["min_food_available"]
    self._width = scene_settings["screen_width"]
    self._height = scene_settings["screen_height"]
    self._fps = 30
    self._bg_color = scene_settings["background_color"]
    self.plain_text_font = None
    self._do_render_legend = True

    self._food_type_ratio = scene_settings["food_type_ratio"]
    self._discrete_food_type_ratio = list(self._food_type_ratio)
    ratio_counter = 0
    for ratio_id in range(0, len(self._discrete_food_type_ratio)):
      self._discrete_food_type_ratio[ratio_id] *= 100
      ratio_counter += self._discrete_food_type_ratio[ratio_id]
      self._discrete_food_type_ratio[ratio_id] = ratio_counter

    if self._show_rendering:
      self._screen = pygame.display.set_mode((self._width, self._height))

    self._run_simulations = True
    self._running = True
    self._thread = None

    self._entity_lists = EntityListContainer()

    self.left_mouse_clicked = False
    self.right_mouse_clicked = False
    self.can_click_mouse = True
    self.dragged_entity = None

    self.spawnRandomFood(scene_settings["min_food_available"])
    self.spawnRandomObstacles(scene_settings["start_obstacle_number"])

  def spawnFood(self, x: int, y: int):
    """
    Spawns a single food source.
    :param x: X position of food.
    :param y: Y position of food.
    """
    food_type = 0
    food_random_value = random.randint(0,100)
    for ratio_id in range(0, len(self._discrete_food_type_ratio)):
      if ratio_id == len(self._discrete_food_type_ratio) - 1 or \
          food_random_value <= self._discrete_food_type_ratio[ratio_id]:
        food_type = ratio_id
        break
      
    food = Food(x, y, self._scene_settings["mean_food_energy"],
                self._scene_settings["mean_food_speed"], food_type)
    self._entity_lists.entity_list.append(food)
    self._entity_lists.food_list.append(food)

  def spawnObstacle(self, x: int, y: int):
    """
    Spawns a single obstacle.
    :param x: X position of obstacle.
    :param y: Y position of obstacle.
    """
    obstacle = Obstacle(x, y, 100)
    self._entity_lists.obstacle_list.append(obstacle)
    self._entity_lists.entity_list.append(obstacle)

  def spawnRandomObstacles(self, num_obstacles: int):
    """
    Spawns a number of randomly placed obstacles.
    :param num_obstacles: The number of obstacles to place.
    """
    for _ in range(num_obstacles):
      x = random.randint(0, self._width)
      y = random.randint(0, self._height)
      self.spawnObstacle(x, y)

  def spawnRandomFood(self, num_food: int):
    """
    Spawns a number of randomly placed food sources.
    :param num_food: The number of food sources to place.
    """
    for _ in range(num_food):
      x = random.randint(0, self._width)
      y = random.randint(0, self._height)
      self.spawnFood(x, y)

  def spawnQueen(self, x: int, y: int, queen_description: dict):
    """
    Spawns a single queen with a certain configuration.
    :param x: X position of queen.
    :param y: Y position of queen.
    :param queen_description: Configuration of queen.
    """
    worker_description = copy.copy(queen_description["worker_type"])
    worker_type = None
    if worker_description["behavior"] != "SimpleWorker" and \
        worker_description["behavior"] != "AdvancedWorker":
      print("[ERROR] Invalid behavior for worker type of one of your queen.")
      exit(1)

    queen = Queen(x, y, queen_description)
    self._entity_lists.entity_list.append(queen)
    self._entity_lists.queen_list.append(queen)
    queen.spawnWorker(queen_description["start_worker_number"], self._entity_lists.entity_list,
                      self._entity_lists.worker_list, self._width, self._height, 0, 300)

  def startScene(self, separate_thread: bool):
    """
    Launches the scene.
    :param separate_thread: If True, the scene is started in an separate thread allowing for
                            asynchronous simulation. Useful if code should interact with simulation.
    """
    if separate_thread:
      self._thread = threading.Thread(target = self._gameLoop)
      self._thread.start()
    else:
      self._thread = None
      self._gameLoop()

  def joinSceneThread(self):
    """
    Joins the scene thread, if launched in separate thread.
    """
    if self._thread is not None:
      self._thread.join()
      return True
    return False

  def render(self):
    """
    Renders all entites currently present in the scene.
    """
    self._screen.fill(self._bg_color)
    for entity in self._entity_lists.obstacle_list:
      entity.renderShadow(self._screen)
    for entity in self._entity_lists.food_list:
      entity.renderShadow(self._screen)
    for entity in self._entity_lists.queen_list:
      entity.renderShadow(self._screen)

    for entity in self._entity_lists.worker_list:
      entity.render(self._screen)
    for entity in self._entity_lists.obstacle_list:
      entity.render(self._screen)
    for entity in self._entity_lists.food_list:
      entity.render(self._screen)
    for entity in self._entity_lists.queen_list:
      entity.render(self._screen)

    self._renderLegend()
    self._renderQueenStats()

    pygame.display.flip()

  def behave(self):
    """
    Performs the behavioral simulations of all entites currently present in the scene.
    """
    for entity in self._entity_lists.entity_list:
      alive = entity.behave(self._entity_lists, self._width, self._height)
      if not alive:
        entity.kill(self._entity_lists)

  def registerMouseClick(self):
    """
    Registers a left or a right mouse click and stores it for later use.
    """
    if pygame.mouse.get_pressed()[0]:
      if self.can_click_mouse:
        self.left_mouse_clicked = True
        self.can_click_mouse = False
      else:
        self.left_mouse_clicked = False

    elif pygame.mouse.get_pressed()[2]:
      if self.can_click_mouse:
        self.right_mouse_clicked = True
        self.can_click_mouse = False
      else:
        self.right_mouse_clicked = False

    else:
      self.left_mouse_clicked = False
      self.right_mouse_clicked = False
      self.can_click_mouse = True

  def checkMouseClick(self):
    """
    Used a stored left or right mouse click to perform certain user-input actions.
    """
    def getClickedEntity(mouse_pos, distance):
      for entity in itertools.chain(*[self._entity_lists.obstacle_list, self._entity_lists.queen_list, self._entity_lists.food_list]):
        if mouse_pos[0] <= entity._x + distance and mouse_pos[0] >= entity._x - distance:
          if mouse_pos[1] <= entity._y + distance and mouse_pos[1] >= entity._y - distance:
            return entity
      return None

    mouse_pos = pygame.mouse.get_pos()
    mouse_held = pygame.mouse.get_pressed()[0]
    if self.left_mouse_clicked:
      clicked_entity = getClickedEntity(mouse_pos, 40)
      if clicked_entity is not None:
        print(f"[INFO] Dragging " + str(clicked_entity) + ".")
        self.dragged_entity = clicked_entity
      else:
        print(f"[INFO] Spawning in food at pos {mouse_pos[0]}:{mouse_pos[1]}.")
        self.spawnFood(mouse_pos[0], mouse_pos[1])

    if self.right_mouse_clicked:
      clicked_entity = getClickedEntity(mouse_pos, 40)
      if type(clicked_entity) is Obstacle:
        print(f"[INFO] Removing " + str(clicked_entity) + ".")
        clicked_entity.kill(self._entity_lists)
      else:
        print(f"[INFO] Spawning in obstacle at pos {mouse_pos[0]}:{mouse_pos[1]}.")
        self.spawnObstacle(mouse_pos[0], mouse_pos[1])

    if self.dragged_entity is not None and not mouse_held:
      self.dragged_entity = None

  def handleEntityDrag(self):
    """
    Performs operations, so that an entity can follow the mouse cursor if it is dragged.
    """
    if self.dragged_entity is not None:
      if self.dragged_entity._energy <= 0:
        self.dragged_entity = None
        return
      mouse_pos = pygame.mouse.get_pos()
      self.dragged_entity.setPosition(mouse_pos[0], mouse_pos[1])

  def getEntityNumbers(self) -> "tuple(int, int, int, int)":
    """
    Returns the number of all different entities currently present in the scene.
    :return: A tuple containing the numbers of all queens, workers, foods, obstacles, in this order.
    """
    return len(self._entity_lists.queen_list), len(self._entity_lists.worker_list),\
           len(self._entity_lists.food_list), len(self._entity_lists.obstacle_list)

  def getEntityLists(self) -> "EntityListContainer":
    """
    Returns a reference to the entity list container, which contains all entites currently
    present in the scene.
    """
    return self._entity_lists

  def exitScene(self):
    """
    Sets a flag to exit the scene.
    """
    self._running = False

  def _drawText(self, text: str, font: "pygame.Font", x: int = None, y: int = None, color: "tuple[int]" = (0, 0, 0)):
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
      text_surface = font.render(line, True, color)
      text_width, text_height = text_surface.get_size()
      if center_text:
        x = (self._width - text_width) // 2

      self._screen.blit(text_surface, (x, y + y_offset))
      y_offset += font.get_linesize()

  def _renderLegend(self):
    """
    Renders a legend for the user input to the upper left corner.
    """
    if not self._do_render_legend:
      return

    legend_text = "Control Scheme:\n\n" +\
                  "Escape - Exit\n" +\
                  "Space - Resume / Pause\n" +\
                  "Click left mouse - Spawn Food\n" +\
                  "Click right mouse - Spawn/Remove Obstacle\n" +\
                  "Drag entity with cursor - Move entity around\n" +\
                  "F1 / H - Toggle legend\n\n" +\
                  "Have fun experimenting ;)"

    width = 700
    height = 360
    x_pos = 10
    y_pos = 10

    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    transparent_surface.set_alpha(40)
    pygame.draw.rect(transparent_surface, (255, 255, 255), (0, 0, width, height))
    self._screen.blit(transparent_surface, (x_pos, y_pos))
    self._drawText(legend_text, self.plain_text_font, x_pos + 10, y_pos + 10)

  def _renderQueenStats(self):
    """
    Renders queen energy stats and counters for the different worker colonies to the right side of the screen.
    """

    width = 600
    height = 45 * len(self._entity_lists.queen_list)
    x_pos = self._width - width - 10
    y_pos = 20
    y_offset = 40

    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    transparent_surface.set_alpha(40)
    pygame.draw.rect(transparent_surface, (255, 255, 255), (0, 0, width, height))
    self._screen.blit(transparent_surface, (x_pos - 10, y_pos - 10))

    queen_counter = 0
    for queen in self._entity_lists.queen_list:
      counter_text = f"Queen {queen_counter} workers: {queen.getWorkerNum()} | energy: {int(queen.getEnergy())}"
      self._drawText(counter_text, self.plain_text_font, x_pos, y_pos, queen.getColor())

      y_pos += y_offset
      queen_counter += 1

  def _gameLoop(self):
    """
    Core loop of the simulation. Performs all actions and checks for all input.
    """
    clock = pygame.time.Clock()
    frame_counter = 0

    if self._show_rendering:
      self.plain_text_font = pygame.font.Font(None, 45)

    while self._running:
      if self._show_rendering:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.exitScene()
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              self.exitScene()
            if event.key == pygame.K_SPACE:
              self._run_simulations = not self._run_simulations
            if event.key == pygame.K_F1 or event.key == pygame.K_h:
              self._do_render_legend = not self._do_render_legend

        if frame_counter == 250:
          self._do_render_legend = False

      frame_counter += 1

      if self._run_simulations:
        self.behave()
        self._spawnPeriodicFood()

      if self._show_rendering:
        self.render()

      clock.tick(self._fps)

      if self._show_rendering:
        self.registerMouseClick()
        self.checkMouseClick()
        self.handleEntityDrag()

    pygame.quit()

  def _spawnPeriodicFood(self):
    """
    Spawns with a certain probability, if too few food sources are currently present.
    """
    if len(self._entity_lists.food_list) >= self._min_food:
      return

    if random.randint(0, 100) <= 8:
      self.spawnRandomFood(1)

