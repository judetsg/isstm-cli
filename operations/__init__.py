from operations import functions

operations = {
    'Saisir Note Examen': functions.saisir_note_examen,
    'Saisir Note Examen Sans Anonymat': functions.saisir_note,
    'Saisir Note CC': functions.saisir_note,
    'Moyenne EC - Session 1':functions.calculer_moyenne_ec_session_1,
    'Matiere à repasser - Session 1': functions.generer_matiere_a_repasser_session_1,
    'Quitter': functions.quitter
}
