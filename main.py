#!/usr/bin/env python3
#
# The main script and entry point of the program. Sets up all data and starts
# the simulation.
#
#############################################################################

import random
from src.Menu import Menu
from src.Scene import Scene
from src.ConfigManager import ConfigManager
from src.ErrorPopup import ErrorPopup

def setWorkingDirectoryToFileDirectory():
  """
  Sets the current working directory to the directory of the file for general
  callability out of any directory.
  """
  import sys
  import os
  script_dir = os.path.dirname(os.path.abspath(__file__))
  os.chdir(script_dir)
  sys.path.insert(0, script_dir)

def startScene():
  """
  Loads all configuration files and starts the main menu in order to
  play the configured scene.
  """
  config_manager = ConfigManager()
  scene_config = config_manager.loadSceneConfig()
  queens_list = config_manager.loadQueensConfig()
  scene_config_valid = config_manager.validateSceneConfig(scene_config)
  queens_list_valid = config_manager.validateQueensList(queens_list)

  can_run_scene = True
  if not scene_config_valid or not queens_list_valid:
    if not scene_config_valid:
      print("[ERROR] Exit program due to invalid scene config file.")
    if not queens_list_valid:
      print("[ERROR] Exit program due to invalid queens config file.")
    can_run_scene = False

  if not can_run_scene:
    return False

  width = scene_config["screen_width"]
  height = scene_config["screen_height"]

  try:
    scene = Scene(scene_config, True)
    for queen in queens_list:
      x = random.randint(0, width)
      y = random.randint(0, height)
      scene.spawnQueen(x, y, queen)
    scene.startScene(False)
  except Exception as e:
    print(f"[ERROR] {e}")
    return False
  return True

def main():
  """
  Main function. Entry point.
  """
  setWorkingDirectoryToFileDirectory()

  running = True
  while running:
    menu = Menu()
    play_scene = menu.start()
    show_error = False

    if play_scene:
      show_error = not startScene()
    else:
      running = False

    if show_error:
      popup = ErrorPopup("Error starting the scene.", "Your configs are probably malformed.\nLook at the terminal for more info.\n")
      popup.show()


if __name__ == "__main__":
  main()
