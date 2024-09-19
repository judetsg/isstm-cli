import pprint

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
    semestres = r.table('semestre').order_by('id').filter(
        {"niveau_id": niveau}).run(rethinkdb_connection)
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
def select_etudiant(rethinkdb_connection, niveau, annee):
    etudiants = r.table('etudiant').order_by(index='nom')\
        .inner_join(r.table('inscriptions'),
                    lambda etudiant_row, inscriptions_row: etudiant_row['id'] == inscriptions_row['id_etudiant']).\
        without({'right': 'id'}).zip().filter({
            'id_niveau': niveau,
            'id_annee': annee
        }).run(rethinkdb_connection)

    list_of_etudiants = [(etudiant['id_etudiant'], etudiant['nom'], etudiant['prenoms'])
                         if etudiant.get('prenoms') is not None
                         else (etudiant['id_etudiant'], etudiant['nom'])
                         for etudiant in etudiants]

    return list_of_etudiants

# renvoie la liste des étudiants ayant devant faire un repechage pour un EC


def select_etudiant_repechage(rethinkdb_connection, id_ec):
    etudiants = r.table("moyenne_ec").eq_join("id_etudiant", r.table("etudiant"))\
        .without({'right': 'id'}).zip().eq_join("id_ec", r.table("element_const"))\
        .without({'right': 'id'}).zip().order_by("nom")\
        .filter(r.and_(r.row["id_ec"].eq(id_ec), r.row["repasser"].eq(True)))\
        .run(rethinkdb_connection)

    list_of_etudiants = [(etudiant['id_etudiant'], etudiant['nom'], etudiant['prenoms'])
                         if etudiant.get('prenoms') is not None
                         else (etudiant['id_etudiant'], etudiant['nom'])
                         for etudiant in etudiants]
    return list_of_etudiants

# This function extracts the first non-'Next' value from the given dictionary.


def extract_etudiant_from_dict(etudiant_dict):
    for value in etudiant_dict.values():
        if value != 'Next':
            return value
            break
    return None


def select_annee(rethinkdb_connection):
    annees = r.table('annee_universitaire').order_by(
        'id').run(rethinkdb_connection)
    annee_choices = [
        questionary.Choice(title=annee['annee'], value=annee['id']) for annee in annees
    ]
    return annee_choices


def split_list(tuples):
    # Calculate the size of each chunk
    chunk_size = len(tuples) // 3

    # Create the 3 lists
    list1 = tuples[:chunk_size]
    list2 = tuples[chunk_size:2 * chunk_size]
    list3 = tuples[2 * chunk_size:]

    # If there are any remaining elements, add them to the last list (list3)
    remainder = len(tuples) % 3
    if remainder > 0:
        list3.extend(tuples[-remainder:])

    return [list1, list2, list3]


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


"""
Cette fonction permet d'avoir des données autres que l'id à partir d'une table
"""


def get_pretty_name(rethinkdb_connection, table, id, champ):
    raw_result = r.table(table).get(id).run(rethinkdb_connection)
    result = raw_result[champ]
    return result


def get_mention(note):
    mention = "Passable"
    if note >= 16:
        mention = "Très Bien"
    elif note >= 14:
        mention = "Bien"
    elif note >= 12:
        mention = "Assez Bien"

    return mention


def select_note_repechage(rethinkdb_connection, annee, semestre, ec, session):
    notes = r.table('moyenne_ec')\
        .eq_join('id_ec', r.table('element_const'))\
        .without({'right': 'id'}).zip().filter(
        (r.row['id_annee'] == annee) & (r.row['id_semestre'] == semestre) &
        (r.row['id_session'] == session) & (r.row['id_ec'] == ec)
    ).order_by(r.asc('anonymat')).run(rethinkdb_connection)

    # print(notes)

    list_of_notes = [
        (note['id'], note['anonymat'], note['appellation_ec']) for note in notes
    ]

    return list_of_notes


def get_note_session2(rethinkdb_connection, ec, etudiant_id, semestre):
    note = r.table('moyenne_ec').filter(
        r.and_(
            r.row['id_session'].eq('2'),
            r.row['id_etudiant'].eq(etudiant_id),
            r.row['id_ec'].eq(ec),
            r.row['id_semestre'].eq(semestre)
        )
    ).run(rethinkdb_connection)

    note_value = 0
    for value in note:
        # breakpoint()
        if value.get('note') == None:
            note_value = 0
        else:
            note_value = value['note']
    # breakpoint()
    return note_value


def est_valide_session1(rethinkdb_connection, ec, etudiant_id, niveau, semestre):
    note_brut = r.table('moyenne_ec').filter(
        r.and_(
            r.row['id_session'].eq('1'),
            r.row['id_etudiant'].eq(etudiant_id),
            r.row['id_niveau'].eq(niveau),
            r.row['id_ec'].eq(ec),
            r.row['id_semestre'].eq(semestre)
        )
    ).run(rethinkdb_connection)
    # breakpoint()
    est_valide = False
    for validation in note_brut:
        a_repasser = validation['repasser']
        if a_repasser:
            est_valide = False
        else:
            est_valide = True

    return est_valide


def get_note_session1(rethinkdb_connection, ec_id, etudiant_id, semestre):
    note = r.table('moyenne_ec').filter(
        r.and_(
            r.row['id_session'].eq('1'),
            r.row['id_etudiant'].eq(etudiant_id),
            r.row['id_ec'].eq(ec_id),
            r.row['id_semestre'].eq(semestre)
        )
    ).run(rethinkdb_connection)

    note_value = 0
    for value in note:
        # breakpoint()
        if value.get('note') == None:
            note_value = 0
        else:
            note_value = value['note']
    # breakpoint()
    return note_value

# Recuperer année universitaire à partir id


def recup_annee_univ(rethinkdb_connection, id_annee: int):
    annee = r.table('annee_universitaire').filter(
        {'id': id_annee}).run(rethinkdb_connection)
    return annee['annee']


def clear_lines(n=5):
    for _ in range(n):
        # Move the cursor up one line
        print('\033[F', end='')
        # Clear the line
        print('\033[K', end='')
