from pymongo import Connection
from pymongo.objectid import ObjectId
from config import config

class DB(object):
    '''Provides a connection to our mongo db'''

    def getDB(self):
        host = config['DB']['host']
        port = config['DB']['port']
        db = config['DB']['name']
        return Connection(host=host, port=port)[db]

class Model(DB):
    '''A base model defining methods all db accessors need'''

    def getCollection(self):
        db = self.getDB()
        return db[self.collection]

    def asJSON(self):
        json = vars(self)
        if not self._id:
            json.pop('_id')
        return json

    def save(self):
        db = self.getDB()
        self._id = db[self.collection].save(self.asJSON())
        return self._id

class BaseFinder(DB):
    '''Find everything by _id'''

    def find(self, id):
        db = self.getDB()
        if isinstance(id, ObjectId):
            return db[self.collection].find_one({"_id": id})
        else:
            return db[self.collection].find_one({"_id": ObjectId(id)})
