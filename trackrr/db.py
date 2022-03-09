from tinydb import TinyDB, Query

DATABASE_NAME = "MTB.json"


def initialize_database():
    return TinyDB(DATABASE_NAME)
