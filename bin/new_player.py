#! /usr/bin/python

import sys
from pymongo import Connection
from pymongo.objectid import ObjectId

conn = Connection()
db = conn.foo

if (len(sys.argv) < 2):
    print "Usage:" + sys.argv[0] + " first_name last_name"
    sys.exit()

player = {
    "first": (sys.argv[1]).lower(),
    }

if (len(sys.argv > 2)):
    player["second"] = (sys.argv[2]).lower()

id = db.players.save(player)
print str(id)
