#! /usr/bin/python

import sys
import os
_root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, _root_dir)

from models.Player import Player

if (len(sys.argv) < 3):
    print "Usage:" + sys.argv[0] + " first_name last_name"
    sys.exit()

player = Player(sys.argv[1], sys.argv[2])
player.save()
