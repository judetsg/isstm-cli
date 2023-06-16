import questionary
from data import r


# function to choose niveau
def select_niveau(rethinkdb_connection):
    niveaux = r.table('niveau').order_by('id').run(rethinkdb_connection)
    niveaux_choices = [
        questionary.Choice(title=niveau['niveau'], value=niveau['id']) for niveau in niveaux
    ]
    return niveaux_choices


# function to choose semetre
def select_semestre(rethinkdb_connection, niveau):
    semestres = r.table('semestre').order_by('id').filter({"niveau_id": niveau}).run(rethinkdb_connection)
    semestres_choices = [
        questionary.Choice(title=semestre['semestre'], value=semestre['id']) for semestre in semestres
    ]

    return semestres_choices


# function to choose ec
def select_ec(rethinkdb_connection, semestre):
    eCs = r.table('element_const').eq_join('ue_id', r.table('unite_ens')).without({'right': 'id'}).zip().filter({
        'semestre_id': semestre
    }).run(rethinkdb_connection)
    ecs_choices = [
        questionary.Choice(title=ec['appellation_ec'], value=ec['id']) for ec in eCs
    ]
    return ecs_choices


# function to return a list of students wrapped in tuples
def select_etudiant(rethinkdb_connection, niveau):
    etudiants = r.table('etudiant').order_by(index='nom')\
        .inner_join(r.table('inscriptions'),
                    lambda etudiant_row, inscriptions_row: etudiant_row['id'] == inscriptions_row['id_etudiant']).\
        without({'right': 'id'}).zip().filter({
        'id_niveau': niveau
    }).run(rethinkdb_connection)

    list_of_etudiants = [ (etudiant['id_etudiant'], etudiant['nom'], etudiant['prenoms'])
                          if etudiant.get('prenoms') is not None
                          else (etudiant['id_etudiant'], etudiant['nom'])
                                for etudiant in etudiants ]

    return list_of_etudiants

# This function extracts the first non-'Next' value from the given dictionary.
def extract_etudiant_from_dict(etudiant_dict):
    for value in etudiant_dict.values():
        if value != 'Next':
            return value
            break
    return None

def select_annee(rethinkdb_connection):
    annees = r.table('annee_universitaire').order_by('id').run(rethinkdb_connection)
    annee_choices = [
        questionary.Choice(title=annee['annee'], value=annee['id']) for annee in annees
    ]
    return annee_choices

def split_list(tuples):
    # calculate the size of each chunk
    chunk_size = len(tuples) // 3

    # create the 3 lists
    list1 = tuples[:chunk_size]
    list2 = tuples[chunk_size:2 * chunk_size]
    list3 = tuples[2 * chunk_size:]

    # if there are any remaining elements, add them to the lists
    remainder = len(tuples) % 3
    if remainder >= 1:
        list1.append(tuples[-remainder])
    if remainder == 2:
        list2.append(tuples[-2])

    return [ list1, list2, list3 ]


def select_note(rethinkdb_connection, annee, niveau, semestre, ec, session):
    notes = r.table('notes').order_by(index='anonymat')\
        .inner_join(r.table('element_const'),
                    lambda notes_row, ec_row: notes_row['id_ec'] == ec_row['id']).without(
        {'right': 'id'}).zip().filter(
        (r.row['id_annee'] == annee) & (r.row['niveau'] == niveau) & (r.row['semestre'] == semestre) &
        (r.row['session'] == session) & (r.row['id_ec'] == ec)
    ).run(rethinkdb_connection)

    # print(notes)

    list_of_notes = [
        (note['id'], note['anonymat'], note['appellation_ec']) for note in notes
    ]

    return list_of_notes