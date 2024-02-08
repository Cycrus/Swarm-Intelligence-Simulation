#!/usr/bin/env python3
#
# Handles the configuration files for scene and queens.
# Is capable of loading a config, validating it, and saving a default
# config.
#
#############################################################################

import json
import typing

class ConfigManager:
  def __init__(self):
    pass

  def loadSceneConfig(self) -> dict:
    """
    Loads the scene config file. (No validation.)
    :return: The configuration parsed into a dictionary.
    """
    try:
      data = self.__loadGeneralConfig("config/scene_config.json")
    except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
      print(f"[ERROR] Cannot read scene config: {e}")
      data = None
    return data

  def loadQueensConfig(self) -> list[dict]:
    """
    Loads the queens config file. (No validation.)
    :return: All different queen configurations parsed into a list of dictionaries.
    """
    try:
      data = self.__loadGeneralConfig("config/queen_config.json")["queens"]
    except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
      print(f"[ERROR] Cannot read queens config: {e}")
      data = None
    except KeyError as e:
      print(f"[ERROR] Cannot find the \"queens\" field in the queens config.")
      data = None
    return data

  def __loadGeneralConfig(self, path: str) -> dict:
    """
    A general purpose method to load any json formatted configuration into a dict.
    :param path: The path of the configuration file.
    :return: The configuration parsed into a dictionary.
    """
    file = open(path)
    data = json.load(file)
    return data

  def validateSceneConfig(self, config: dict) -> bool:
    """
    Completely checks for validity of schene config.
    """
    if not self.validSceneConfigSchema(config):
      return False
    if not self.validSceneConfigValues(config):
      return False
    return True

  def validSceneConfigSchema(self, config: dict) -> bool:
    """
    Roughly validates a loaded scene configuration dictionary. Basically checks
    if all required fields are present in the dictionary.
    :param config: The config dict to validate.
    :return: True if the config is valid.
    """
    if config is None:
      return False

    required_keys = ["background_color", "screen_width", "screen_height", "min_food_available", "start_obstacle_number",
                     "mean_food_energy", "mean_food_speed", "food_type_ratio"]

    for key in required_keys:
      if key not in config:
        print(f"[ERROR] Cannot find field <{key}> in scene config file.")
        return False

    return True

  def validSceneConfigValues(self, config: dict) -> bool:
    """
    More precise configuration check. Checks if all fields contain valid vlaues.
    :return: True if the config is valid.
    """
    if type(config["background_color"]) is not list:
      print("[ERROR] Invalid background_color value detected in scene config. Must be a list with RGB values.")
      return False
    if len(config["background_color"]) != 3:
      print("[ERROR] Invalid background_color value detected in scene config. Must be a list with RGB values.")
      return False
    for color in config["background_color"]:
      if not self.checkNumberString(color, 0, 255,
                                    "[ERROR] Invalid background_color value detected in scene config."): return False

    if not self.checkNumberString(config["screen_width"], 0, None,
                                  "[ERROR] Invalid screen_width value detected in scene config."): return False
    if not self.checkNumberString(config["screen_height"], 0, None,
                                  "[ERROR] Invalid screen_height value detected in scene config."): return False
    if not self.checkNumberString(config["min_food_available"], 0, None,
                                  "[ERROR] Invalid min_food_available value detected in scene config."): return False
    if not self.checkNumberString(config["start_obstacle_number"], 0, None,
                                  "[ERROR] Invalid start_obstacle_number value detected in scene config."): return False
    if not self.checkNumberString(config["mean_food_energy"], 0, None,
                                  "[ERROR] Invalid mean_food_energy value detected in scene config."): return False
    if not self.checkNumberString(config["mean_food_speed"], 0, None,
                                  "[ERROR] Invalid mean_food_speed value detected in scene config."): return False

    if type(config["food_type_ratio"]) is not list:
      print("[ERROR] Invalid food_type_ratio value detected in scene config.")
      return False
    if len(config["food_type_ratio"]) > 3:
      print("[ERROR] Invalid food_type_ratio value detected in scene config.")
      return False
    counter = 0.0
    for food in config["food_type_ratio"]:
      if not self.checkNumberString(food, 0, 1.0,
                                    "[ERROR] Invalid background_color value detected in scene config."): return False
      counter += self.toNumber(food)
    if counter > 1.01 or counter < 0.99:
      print("[ERROR] Invalid food_type_ratio value detected in scene config. All values must add up to 1.0")
      return False
    
    return True

  def validateQueensList(self, config: list[dict]) -> bool:
    """
    Completely checks for validity of queens config list.
    """
    if not self.validQueensListSchema(config):
      return False
    if not self.validQueensListValues(config):
      return False
    return True

  def validQueensListSchema(self, queen_list: list[dict]) -> bool:
    """
    Roughly validates a loaded queens configuration dictionaries in the queens list. Basically checks
    if all required fields are present in the dictionary.
    :param config: The config dict to validate.
    :return: True if the config is valid.
    """
    if queen_list is None:
      return False

    required_keys = ["birth_energy_threshold", "energy", "max_energy", "energy_reduction_rate", "worker_spawn_cost",
                     "speed", "color", "start_worker_number", "worker_type"]
    required_worker_keys = ["behavior", "mean_energy", "energy_range", "mean_speed", "speed_range"]

    queen_counter = 0
    for queen_config in queen_list:
      for key in required_keys:
        if key not in queen_config:
          print(f"[ERROR] Cannot find field <{key}> in queen config nr. {queen_counter}.")
          return False
      for key in required_worker_keys:
        if key not in queen_config["worker_type"]:
          print(f"[ERROR] Cannot find field <{key}> in worker_type config of queen nr. {queen_counter}.")
          return False
      if queen_config["worker_type"]["behavior"] == "SimpleWorker":
        pass
      elif queen_config["worker_type"]["behavior"] == "AdvancedWorker":
        if "shouting_radius" not in queen_config["worker_type"]:
          print(f"[ERROR] Cannot find field <shouting_radius> in worker_type config of queen nr. {queen_counter}.")
          return False
      else:
        print(f"[ERROR] Invalid worker_type behavior found. Please choose only between \"SimpleWorker\" or \"AdvancedWorker\"")
        return False
        
      queen_counter += 1

    return True

  def validQueensListValues(self, queen_list: list[dict]) -> bool:
    """
    More precise configuration check. Checks if all fields contain valid vlaues.
    :return: True if the config is valid.
    """
    queen_counter = 0
    for queen_config in queen_list:
      if not self.checkNumberString(queen_config["birth_energy_threshold"], 0, None,
                                    f"[ERROR] Invalid birth_energy_threshold value detected for queen {queen_counter}."): return False
      if not self.checkNumberString(queen_config["energy"], 0, None,
                                    f"[ERROR] Invalid energy value detected for queen {queen_counter}."): return False
      if not self.checkNumberString(queen_config["max_energy"], 0, None,
                                    f"[ERROR] Invalid max_energy value detected for queen {queen_counter}."): return False
      if not self.checkNumberString(queen_config["energy_reduction_rate"], 0, None,
                                    f"[ERROR] Invalid energy_reduction_rate value detected for queen {queen_counter}."): return False
      if not self.checkNumberString(queen_config["worker_spawn_cost"], 0, None,
                                    f"[ERROR] Invalid worker_spawn_cost value detected for queen {queen_counter}."): return False
      if not self.checkNumberString(queen_config["speed"], 0, None,
                                    f"[ERROR] Invalid speed value detected for queen {queen_counter}."): return False

      if type(queen_config["color"]) is not list:
        print(f"[ERROR] Invalid color value detected for queen {queen_counter}.")
        return False
      if len(queen_config["color"]) != 3:
        print(f"[ERROR] Invalid color value detected for queen {queen_counter}.")
        return False
      for color in queen_config["color"]:
        if not self.checkNumberString(color, 0, 255,
                                      f"[ERROR] Invalid color value detected for queen {queen_counter}."): return False

      if not self.checkNumberString(queen_config["start_worker_number"], 0, None,
                                    f"[ERROR] Invalid start_worker_number value detected for queen {queen_counter}."): return False

      worker_type = queen_config["worker_type"]
      if type(worker_type) is not dict:
        print(f"[ERROR] Invalid worker_type detected for queen {queen_counter}.")
        return False

      if worker_type["behavior"] != "SimpleWorker" and worker_type["behavior"] != "AdvancedWorker":
        print(f"[ERROR] Invalid behavior detected for worker_type of queen {queen_counter}.")
        return False

      if not self.checkNumberString(worker_type["mean_energy"], 0, None,
                                    f"[ERROR] Invalid mean_energy detected for worker_type of queen {queen_counter}."): return False
      if not self.checkNumberString(worker_type["energy_range"], 0, None,
                                    f"[ERROR] Invalid energy_range detected for worker_type of queen {queen_counter}."): return False
      if not self.checkNumberString(worker_type["mean_speed"], 0, None,
                                    f"[ERROR] Invalid mean_speed detected for worker_type of queen {queen_counter}."): return False
      if not self.checkNumberString(worker_type["speed_range"], 0, None,
                                    f"[ERROR] Invalid speed_range detected for worker_type of queen {queen_counter}."): return False

      queen_counter += 1

    return True

  def toNumber(self, string: str) -> bool:
    """
    Casts a string into a number. If not possible it returns None.
    """
    number = 0
    try:
      number = float(string)
    except:
      return None
    return number  

  def checkNumberString(self, string: str, min_value: int, max_value: int, err_msg: str) -> bool:
    num_value = self.toNumber(string)
    if (num_value is None) or \
       (min_value is not None and num_value < min_value) or \
       (max_value is not None and num_value > max_value):
      print(err_msg)
      return False
    return True

  def setDefaultSceneConfig(self):
    """
    Overwrites the scene config file with a default config. Invoked by the user if config is faulty.
    """
    print("[INFO] Regenerated default scene config.")

    data = {
      "background_color": [
        20,
        20,
        20
      ],
      "screen_width": 1900,
      "screen_height": 1200,
      "min_food_available": 6,
      "start_obstacle_number": 10,
      "mean_food_speed": 4,
      "mean_food_energy": 230,
      "food_type_ratio": [
          1.0
      ]
    }

    file_path = "config/scene_config.json"

    with open(file_path, 'w') as json_file:
      json.dump(data, json_file, indent = 4)


  def setDefaultQueensConfig(self):
    """
    Overwrites the queens config file with a default config. Invoked by the user if config is faulty.
    """
    print("[INFO] Regenerated default queens config.")

    data = {
      "queens": [
        {
            "birth_energy_threshold": 300,
            "energy": 300,
            "max_energy": 1000,
            "energy_reduction_rate": 0.2,
            "worker_spawn_cost": 3,
            "speed": 8,
            "color": [
                200,
                0,
                150
            ],
            "start_worker_number": 300,
            "worker_type": {
                "behavior": "AdvancedWorker",
                "mean_energy": 150,
                "energy_range": 10,
                "mean_speed": 20,
                "speed_range": 0,
                "shouting_radius": 70
            }
        },
        {
            "birth_energy_threshold": 300,
            "energy": 300,
            "max_energy": 1000,
            "energy_reduction_rate": 0.2,
            "worker_spawn_cost": 8,
            "speed": 8,
            "color": [
                200,
                200,
                150
            ],
            "start_worker_number": 100,
            "worker_type": {
                "behavior": "SimpleWorker",
                "mean_energy": 150,
                "energy_range": 10,
                "mean_speed": 15,
                "speed_range": 5
            }
        }
      ]
    }

    file_path = "config/queen_config.json"

    with open(file_path, 'w') as json_file:
      json.dump(data, json_file, indent = 4)