from operations import functions

operations = {
    'Saisir Note Examen': functions.saisir_note_examen,
    'Saisir Note Examen Sans Anonymat': functions.saisir_note,
    'Saisir Note CC': functions.saisir_note,
    'Moyenne EC - Session 1':functions.calculer_moyenne_ec_session_1,
    'Matiere à repasser - Session 1': functions.generer_matiere_a_repasser_session_1,
    'Generer note - Session 2':functions.generer_note_session_2,
    'Moyenne UE - Session 1':functions.calculer_moyenne_ue_session_1,
    'Moyenne UE - Session 2':functions.calculer_moyenne_ue_session_2,
    'Admission - Session 1':functions.admission_session_1,
    'Admission - Session 2':functions.admission_session_2,
    'Quitter': functions.quitter
}
