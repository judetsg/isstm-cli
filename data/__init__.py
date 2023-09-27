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
    'Moyenne EC - Session 1',
    'Matiere à repasser - Session 1',
    'Generer note - Session 2',
    'Moyenne UE - Session 1',
    'Moyenne UE - Session 2',
    'Admission - Session 1',
    'Admission - Session 2',
    "Saisir Note CC",
    "Quitter"
]

# database names
db = "isstm"
