from rethinkdb import RethinkDB
import redis  # for storing global application state

# create a redis connection
redis_client = redis.Redis(host='localhost')

# rethinkdb database connection
r = RethinkDB()

# Main menu choices
choices = [
    "Saisir Note Examen",
    "Saisir Note Examen Sans Anonymat",
    "Saisir Note CC",
    "Quitter"
]

# database names
db = "isstm"
