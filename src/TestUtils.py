#!/usr/bin/env python3
#
# A collection of methods and elements useful for unit testing.
#
#############################################################################

from src.Scene import Scene

def load_dummy_scene_config():
  """
  Returns a default dummy scene configuration dict.
  """
  return {
    "background_color": [20, 20, 20],
    "screen_width": 1900,
    "screen_height": 1200,
    "min_food_available": 10,
    "mean_food_energy": 230,
    "mean_food_speed": 3,
    "start_obstacle_number": 0,
    "food_type_ratio": [0.5, 0.5]
  }

def load_dummy_queen_config():
  """
  Returns a dummy queens configuration list with one element.
  """
  return [
    {
      "birth_energy_threshold": 1000,
      "energy": 100,
      "energy_reduction_rate": 0.2,
      "worker_spawn_cost": 3,
      "max_energy": 1000,
      "speed": 3,
      "color": [0, 100, 100],
      "start_worker_number": 50,
      "worker_type": {
        "behavior": "SimpleWorker",
        "mean_energy": 50,
        "mean_speed": 5,
        "speed_range": 1,
        "energy_range": 1
      }
    }
  ]

def load_fast_dying_entity_config():
  """
  Returns a dummy queens configuration list with one element.
  This one dies very fast after a few milliseconds.
  """
  return [
    {
      "birth_energy_threshold": 1000,
      "energy": 10,
      "energy_reduction_rate": 1,
      "worker_spawn_cost": 3,
      "max_energy": 1000,
      "speed": 3,
      "color": [0, 100, 100],
      "start_worker_number": 50,
      "worker_type": {
        "behavior": "SimpleWorker",
        "mean_energy": 0.1,
        "mean_speed": 5,
        "speed_range": 1,
        "energy_range": 1
      }
    }
  ]

def load_dummy_scene_config_missing_field():
  """
  Returns a default dummy scene configuration dict.
  The field mean_food_speed is missing.
  """
  return {
    "background_color": [20, 20, 20],
    "screen_width": 1900,
    "screen_height": 1200,
    "min_food_available": 10,
    "mean_food_energy": 230,
    "start_obstacle_number": 0,
    "food_type_ratio": [0.5, 0.5]
  }

def load_dummy_queen_config_missing_field():
  """
  Returns a dummy queens configuration list with one element.
  The field worker_spawn_cost is missing.
  """
  return [
    {
      "birth_energy_threshold": 1000,
      "energy": 100,
      "worker_spawn_cost": 3,
      "max_energy": 1000,
      "speed": 3,
      "color": [0, 100, 100],
      "start_worker_number": 50,
      "worker_type": {
        "behavior": "SimpleWorker",
        "mean_energy": 50,
        "mean_speed": 5,
        "speed_range": 1,
        "energy_range": 1
      }
    }
  ]

def load_dummy_scene_config_invalid_array_field():
  """
  Returns a default dummy scene configuration dict.
  The food_type_ratio is greater than 1.
  """
  return {
    "background_color": [20, 20, 20],
    "screen_width": 1900,
    "screen_height": 1200,
    "min_food_available": 3,
    "mean_food_energy": 230,
    "start_obstacle_number": 0,
    "food_type_ratio": [0.5, 0.7]
  }

def load_dummy_queen_config_invalid_array_field():
  """
  Returns a dummy queens configuration list with one element.
  The color has only 2 values.
  """
  return [
    {
      "birth_energy_threshold": 1000,
      "energy": 100,
      "worker_spawn_cost": 3,
      "max_energy": 1000,
      "speed": 3,
      "color": [0, 100],
      "start_worker_number": 50,
      "worker_type": {
        "behavior": "SimpleWorker",
        "mean_energy": 50,
        "mean_speed": 5,
        "speed_range": 1,
        "energy_range": 1
      }
    }
  ]

def start_dummy_scene():
  """
  Starts a dummy scene without rendering on a separate thread and returns
  a reference to the scene.
  """
  scene_config = load_dummy_scene_config()
  scene = Scene(scene_config, False)
  scene.startScene(True)
  return scene