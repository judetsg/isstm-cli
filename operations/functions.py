# Saisie des notes d'examen
import os
from decimal import Decimal

import questionary
# import inquirer
from rethinkdb import RethinkDB
from data import db, redis_client
from operations import utility_functions
from utilities import chooser

r = RethinkDB()
# connect to the Rethinkdb database
conn = r.connect(db=db)

def saisir_note_examen():
    # while True:
    """
    0. Choisir l'année universitaire
    1. Choisir le niveau
    2. Choisir le semestre
    3. Choisir l'EC
    4. Choisir si on veut saisir les codes ou les notes
    5. Revenir au menu principal
    """
    # 0. Choisir l'année universitaire
    annee_choices = utility_functions.select_annee(conn)
    annee_choisi = chooser.selector("Choisissez une année universitaire", annee_choices)
    redis_client.set('annee', annee_choisi)

    # 1. Choisir le niveau
    niveaux_choices = utility_functions.select_niveau(conn)
    niveau_choisi = chooser.selector("Choisissez un niveau", niveaux_choices)
    # Sauver sur redis
    redis_client.set('niveau_choisi', niveau_choisi)

    # 2. choisir le semestre
    niveau_choisi = redis_client.get('niveau_choisi').decode()
    semestre_choisi = chooser.selector('Choisissez un semestre', utility_functions.select_semestre(conn, niveau_choisi))
    redis_client.set('semestre_choisi', semestre_choisi)
    # print(f" Semestre: {(redis_client.get('semestre_choisi')).decode()}")

    # 3. choisir l'ec
    semestre_choisi = redis_client.get('semestre_choisi').decode()
    ec_choisi = chooser.selector('Choisissez un EC', utility_functions.select_ec(conn, semestre_choisi))
    redis_client.set('ec_choisi', ec_choisi)
    # print(f"EC: {(redis_client.get('ec_choisi')).decode()}")

    # choisir la session
    session = chooser.selector('Session', [
        questionary.Choice(title='Session 1', value=1),
        questionary.Choice(title='Session 2', value=2)
    ])
    redis_client.set('session', session)

    # 4. choisir si on veut saisir les codes ou les notes
    activite = chooser.selector('Type de Saisie', [
        questionary.Choice(title='Anonymat', value='saisie_code'),
        questionary.Choice(title='Correction Anonymat', value='correction_anonymat'),
        questionary.Choice(title='Note',value='saisie_note')
    ])
    # redis_client.set('activite', activite)

    # recuperer les variables nécessaires sur redis
    annee = redis_client.get('annee').decode()
    niveau = redis_client.get('niveau_choisi').decode()
    semestre = redis_client.get('semestre_choisi').decode()
    ec = redis_client.get('ec_choisi').decode()
    session = redis_client.get('session').decode()

    if activite == 'saisie_code':

        # Saisir les lettres du code si on veut saisir les Anonymats
        lettre_code = questionary.text(message='Entrez les lettres du code').ask()
        # redis_client.set('lettre_code', lettre_code)

        # afficher la liste des étudiants en utilisant le niveau choisi
        while True:
            try:
                os.system('clear')
                etudiant_id = chooser.tuple_selector('Choisir un étudiant: ', utility_functions.select_etudiant(conn, niveau_choisi))

                # saisir le rang
                rang = questionary.text('Rang:').ask()

                # saisir les anonymats
                """
                Pour saisir les anonymats, il nous faut l'année universitaire, le niveau, l'ec, le semestre et l'id de l'etudiant.
                Nous allons utiliser et afficher les etudiants, en choisir un entrer son anonymat et ainsi de suite,
                jusqu'à ce que nous cassons la boucle
                """
                r.table('notes').insert({
                    'id': r.uuid(),
                    'id_annee': annee,
                    'niveau': niveau,
                    'semestre': semestre,
                    'etudiant_id': etudiant_id,
                    'id_ec': ec,
                    'session': session,
                    'anonymat': lettre_code + rang,
                }).run(conn)
            except KeyboardInterrupt:
                break

    if activite == 'correction_anonymat':

        # Saisir les lettres du code si on veut saisir les Anonymats
        lettre_code = questionary.text(message='Entrez les lettres du code').ask()
        # redis_client.set('lettre_code', lettre_code)

        # afficher la liste des étudiants en utilisant le niveau choisi
        while True:
            try:
                os.system('clear')
                etudiant_id = chooser.tuple_selector('Choisir un étudiant: ', utility_functions.select_etudiant(conn, niveau_choisi))

                # saisir le rang
                rang = questionary.text('Rang:').ask()

                # saisir les anonymats
                """
                Pour saisir les anonymats, il nous faut l'année universitaire, le niveau, l'ec, le semestre et l'id de l'etudiant.
                Nous allons utiliser et afficher les etudiants, en choisir un entrer son anonymat et ainsi de suite,
                jusqu'à ce que nous cassons la boucle
                """
                r.table('notes')\
                    .filter((r.row['etudiant_id'] == etudiant_id) & (r.row['anonymat'].match(f'^{lettre_code}')))\
                    .update({
                    'anonymat': lettre_code + rang
                }).run(conn)
            except KeyboardInterrupt:
                break

    if activite == 'saisie_note':
        """
        1. Récuperer les anonymats correspondants et les afficher en liste comme la liste des etudiants
        2. Saisir les notes correspondantes
        """
        while True:
            try:
                os.system('clear')
                anonymat_id = chooser.tuple_selector('Choisir anonymat: ',
                                                        utility_functions.select_note(conn, annee, niveau, semestre, ec, session))
                print(f"Anonymat: {anonymat_id}")
                # saisir la note
                note = questionary.text('Note:').ask()
                try:
                    decimal_note = Decimal(note)
                    r.table('notes').get(anonymat_id).update({
                        'note': float(decimal_note),
                        'type': 'EX'
                    }).run(conn)
                except ValueError:
                    print(f"Erreur: tapez un nombre ({ValueError})")
            except KeyboardInterrupt:
                break

def quitter():
    print("Tapez Ctrl+C pour quitter")


def saisir_note_cc():
    """
        0. Choisir l'année universitaire
        1. Choisir le niveau
        2. Choisir le semestre
        3. Choisir l'EC
        4. Saisir les notes
        5. Revenir au menu principal
        """
    # 0. Choisir l'année universitaire
    annee_choices = utility_functions.select_annee(conn)
    annee_choisi = chooser.selector("Choisissez une année universitaire", annee_choices)
    redis_client.set('annee', annee_choisi)

    # 1. Choisir le niveau
    niveaux_choices = utility_functions.select_niveau(conn)
    niveau_choisi = chooser.selector("Choisissez un niveau", niveaux_choices)
    # Sauver sur redis
    redis_client.set('niveau_choisi', niveau_choisi)

    # 2. choisir le semestre
    niveau_choisi = redis_client.get('niveau_choisi').decode()
    semestre_choisi = chooser.selector('Choisissez un semestre', utility_functions.select_semestre(conn, niveau_choisi))
    redis_client.set('semestre_choisi', semestre_choisi)
    # print(f" Semestre: {(redis_client.get('semestre_choisi')).decode()}")

    # 3. choisir l'ec
    semestre_choisi = redis_client.get('semestre_choisi').decode()
    ec_choisi = chooser.selector('Choisissez un EC', utility_functions.select_ec(conn, semestre_choisi))
    redis_client.set('ec_choisi', ec_choisi)
    # print(f"EC: {(redis_client.get('ec_choisi')).decode()}")

    # choisir la session
    session = '1' # il n'y a pas de note de CC à la session 2
    redis_client.set('session', session)

    # recuperer les variables nécessaires sur redis
    annee = redis_client.get('annee').decode()
    niveau = redis_client.get('niveau_choisi').decode()
    semestre = redis_client.get('semestre_choisi').decode()
    ec = redis_client.get('ec_choisi').decode()
    session = redis_client.get('session').decode()

    # Saisir les notes
    # afficher la liste des étudiants en utilisant le niveau choisi
    while True:
        try:
            os.system('clear')
            etudiant_id = chooser.tuple_selector('Choisir un étudiant: ',
                                                 utility_functions.select_etudiant(conn, niveau_choisi))

            # saisir la note
            note = questionary.text('Note:').ask()
            decimal_note = Decimal(note)

            # saisir les anonymats
            """
            Pour saisir les anonymats, il nous faut l'année universitaire, le niveau, l'ec, le semestre et l'id de l'etudiant.
            Nous allons utiliser et afficher les etudiants, en choisir un entrer son anonymat et ainsi de suite,
            jusqu'à ce que nous cassons la boucle
            """
            r.table('notes').insert({
                'id': r.uuid(),
                'id_annee': annee,
                'niveau': niveau,
                'semestre': semestre,
                'etudiant_id': etudiant_id,
                'id_ec': ec,
                'session': session,
                'note': float(decimal_note),
                'type': 'CC'
            }).run(conn)
        except KeyboardInterrupt:
            break