from main import *
import time
import threading
import copy
from src.TestUtils import *
from src.AdvancedWorker import AdvancedWorker
from src.ConfigManager import ConfigManager


def test_scene_starting_configuration():
  print("\n[TEST SCENE] Checking functionality of starting parameters.")
  init_thread_count = threading.active_count()
  scene = start_dummy_scene()
  queen_number, worker_number, food_number, obstacle_number = scene.getEntityNumbers()
  added_thread_count = threading.active_count()
  scene.exitScene()
  scene.joinSceneThread()
  after_thread_count = threading.active_count()

  assert queen_number == 0
  assert worker_number == 0
  assert food_number == 10
  assert added_thread_count == init_thread_count + 1
  assert after_thread_count == added_thread_count - 1


def test_entity_spawning():
  print("\n[TEST SCENE] Checking spawning behavior.")
  scene = start_dummy_scene()
  queen_config = load_dummy_queen_config()
  scene.spawnRandomFood(5)
  scene.spawnQueen(100, 250, queen_config[0])
  scene.spawnQueen(800, 30, queen_config[0])
  queen_number, worker_number, food_number, obstacle_number = scene.getEntityNumbers()
  scene.exitScene()
  scene.joinSceneThread()

  assert queen_number == 2
  assert worker_number == 100
  assert food_number == 15

def test_worker_lists():
  print("\n[TEST SCENE] Checking correctness of worker lists.")
  scene = start_dummy_scene()
  queen_config = load_dummy_queen_config()
  scene.spawnRandomFood(5)
  scene.spawnQueen(100, 250, queen_config[0])
  scene.spawnQueen(800, 30, queen_config[0])

  entity_lists = scene.getEntityLists()
  worker_list_queen_a = entity_lists.queen_list[0].getWorkerList()
  worker_list_queen_b = entity_lists.queen_list[1].getWorkerList()
  queen_worker_lists = [worker_list_queen_a, worker_list_queen_b]

  every_worker_included_once = True

  for queen_list in queen_worker_lists:
    for queen_worker in queen_list:
      this_worker_contained = False
      if entity_lists.worker_list.count(queen_worker) != 1:
        every_worker_included_once = False
      if entity_lists.entity_list.count(queen_worker) != 1:
        every_worker_included_once = False
      if not every_worker_included_once:
        break

  scene.exitScene()
  scene.joinSceneThread()

  assert every_worker_included_once

def test_worker_queen_assignment():
  print("\n[TEST SCENE] Checking correctness of assigned queen for every worker.")
  scene = start_dummy_scene()
  queen_config = load_dummy_queen_config()
  scene.spawnQueen(100, 250, queen_config[0])
  scene.spawnQueen(800, 30, queen_config[0])

  entity_lists = scene.getEntityLists()
  worker_list_queen_a = entity_lists.queen_list[0].getWorkerList()
  worker_list_queen_b = entity_lists.queen_list[1].getWorkerList()
  queen_worker_lists = [worker_list_queen_a, worker_list_queen_b]

  every_worker_correct_queen = True

  for worker in worker_list_queen_a:
    if worker._primary_queen != entity_lists.queen_list[0]:
      every_worker_correct_queen = False

  for worker in worker_list_queen_b:
    if worker._primary_queen != entity_lists.queen_list[1]:
      every_worker_correct_queen = False

  scene.exitScene()
  scene.joinSceneThread()

  assert every_worker_correct_queen

def test_entity_death():
  print("\n[TEST ENTITY] Checking correct working of entity death mechanic.")
  scene = start_dummy_scene()
  queen_config = load_fast_dying_entity_config()
  scene.spawnQueen(100, 250, queen_config[0])

  queen_number_pre, worker_number_pre, food_number, obstacle_number = scene.getEntityNumbers()

  time.sleep(1.0)

  queen_number_post, worker_number_post, food_number, obstacle_number = scene.getEntityNumbers()

  scene.exitScene()
  scene.joinSceneThread()

  assert queen_number_pre == 1 
  assert worker_number_pre == 50

  assert queen_number_post == 0
  assert worker_number_post == 0

def test_entity_killing():
  print("\n[TEST ENTITY] Checking correct working of manual entity killing mechanic.")
  scene = start_dummy_scene()
  queen_config = load_dummy_queen_config()
  scene.spawnQueen(100, 250, queen_config[0])

  entity_lists = scene.getEntityLists()

  queen_number, worker_number, food_number, obstacle_number = scene.getEntityNumbers()
  assert worker_number == 50
  entity_lists.worker_list[0].kill(entity_lists)
  queen_number, worker_number, food_number, obstacle_number = scene.getEntityNumbers()
  assert worker_number == 49

  queen_number, worker_number, food_number, obstacle_number = scene.getEntityNumbers()
  assert food_number == 10
  entity_lists.food_list[0].kill(entity_lists)
  queen_number, worker_number, food_number, obstacle_number = scene.getEntityNumbers()
  assert food_number == 9

  queen_number, worker_number, food_number, obstacle_number = scene.getEntityNumbers()
  assert queen_number == 1
  entity_lists.queen_list[0].kill(entity_lists)
  queen_number, worker_number, food_number, obstacle_number = scene.getEntityNumbers()
  assert queen_number == 0

  time.sleep(0.1)

  assert worker_number == 49  
  for worker in entity_lists.worker_list:
    assert worker._primary_queen == None

  scene.exitScene()
  scene.joinSceneThread()

def test_entity_vector_operations():
  print("\n[TEST ENTITY] Checking correct working of distance and direction operations.")
  worker_x = AdvancedWorker(200, 200, 100, 0, 50)

  worker_north = AdvancedWorker(100, 200, 100, 0, 50)
  worker_east = AdvancedWorker(200, 300, 100, 0, 50)
  worker_south = AdvancedWorker(300, 200, 100, 0, 50)
  worker_west = AdvancedWorker(200, 100, 100, 0, 50)

  assert worker_x.computeDirection(worker_north) == [-1, 0]
  assert worker_x.computeDirection(worker_east) == [0, 1]
  assert worker_x.computeDirection(worker_south) == [1, 0]
  assert worker_x.computeDirection(worker_west) == [0, -1]

  assert worker_x.computeDistance(worker_north) == 100
  assert worker_x.computeDistance(worker_east) == 100
  assert worker_x.computeDistance(worker_south) == 100
  assert worker_x.computeDistance(worker_west) == 100

def test_scene_config_validation():
  print("\n[TEST CONFIG] Thorough test of scene configuration validation.")
  config_manager = ConfigManager()
  valid_scene_config = load_dummy_scene_config()

  # Test valid config
  assert config_manager.validateSceneConfig(valid_scene_config) == True

  # Test all possible missing fields in config
  for key in valid_scene_config.keys():
    invalid_scene_config = copy.deepcopy(valid_scene_config)
    del invalid_scene_config[key]
    assert config_manager.validateSceneConfig(invalid_scene_config) == False

  # Test all possible invalid fields in config
  for key in valid_scene_config.keys():
    invalid_scene_config = copy.deepcopy(valid_scene_config)
    invalid_scene_config[key] = "invalid_value"
    assert config_manager.validateSceneConfig(invalid_scene_config) == False

  # Test faulty array in config
  scene_config_faulty_array = load_dummy_scene_config_invalid_array_field()
  assert config_manager.validateSceneConfig(scene_config_faulty_array) == False

def test_queens_config_validation():
  print("\n[TEST CONFIG] Thorough test of queens configuration validation.")
  config_manager = ConfigManager()
  valid_queens_config = load_dummy_queen_config()

  # Test valid config
  assert config_manager.validateQueensList(valid_queens_config) == True

  # Test all possible missing fields in config
  for key in valid_queens_config[0].keys():
    invalid_queens_config = copy.deepcopy(valid_queens_config)
    del invalid_queens_config[0][key]
    assert config_manager.validateQueensList(invalid_queens_config) == False

  # Test all possible invalid fields in config
  for key in valid_queens_config[0].keys():
    invalid_queens_config = copy.deepcopy(valid_queens_config)
    invalid_queens_config[0][key] = "invalid_value"
    assert config_manager.validateQueensList(invalid_queens_config) == False

  # Test faulty array in config
  queens_config_faulty_array = load_dummy_queen_config_invalid_array_field()
  assert config_manager.validateQueensList(queens_config_faulty_array) == False