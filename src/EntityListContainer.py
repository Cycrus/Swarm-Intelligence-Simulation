#!/usr/bin/env python3
#
# A container managed by the scene, which contains all entity lists.
#
#############################################################################

class EntityListContainer:
  def __init__(self):
    self.entity_list = []
    self.food_list = []
    self.worker_list = []
    self.queen_list = []
    self.obstacle_list = []