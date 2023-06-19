from operations import functions

operations = {
    'Saisir Note Examen': functions.saisir_note_examen,
    "Saisir Note Examen Sans Anonymat": functions.saisir_note('EX'),
    'Saisir Note CC': functions.saisir_note('CC'),
    'Quitter': functions.quitter
}
