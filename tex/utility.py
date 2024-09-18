#!/usr/bin/env python3
# This file contains functions to fill placeholder in a tex file from a json file
#
#
from os.path import exists
import re
import subprocess
import os
import typing

def process_releve_de_note(header_data, main_texfile, body_texfile):
    '''
    How does this suppose to work?
    In the texfile, there are specific placeholder inserted throughout the text,
    inside the content of the file.
    The format of the placeholder is like the following:
    \textit{[[[matricule]]]} => \textit{10ISST245-FGCI/GINFO}
    In the placeholder, [[[matricule]]], matricule will be retrieved from the json file
    '''

    # For the filename
    annee_univ = header_data['annee']
    nom = header_data['nom'].replace(' ','-')
    prenoms = header_data['prenoms'].replace(' ','-')
    header_data ['bodyText'] = f'body-{annee_univ}-{nom}-{prenoms}.tex'

    # Open the body tex file and rename it
    # It will be included in the main tex file
    # Open the body tex file for reading first
    with open(body_texfile, 'r') as btf:
        generated_body_tex = btf.read()

    with open(f"releve/{header_data['bodyText']}", 'w') as body_tex:
        body_tex.write(generated_body_tex)
        body_tex.close()

    # Open the tex file for reading
    with open(main_texfile, 'r') as tex_file:
        tex = tex_file.read()

    # Function to replace placeholders with their corresponding values from the JSON file
    def replace_placeholder(match):
        placeholder = match.group(1)  # Extract the placeholder name from the match
        return header_data.get(placeholder, match.group(0))  # Get the corresponding value from the JSON file, or return the original string if not found

    # Replace the placeholders in the header
    processed_texfile = re.sub(r'\[\[\[(.*?)\]\]\]', replace_placeholder, tex)

    # this is the filename of the relevé de note
    releve_filename = f"releve/releve-{annee_univ}-{nom}-{prenoms}.tex"

    # Write back the processed tex file
    with open(releve_filename, 'w') as processed_tex:
        processed_tex.write(processed_texfile)
        processed_tex.close()

    output_directory = 'releve'

    # Check if the file exists before trying to compile it
    while not os.path.exists(releve_filename):
        print(f'Checking for the file {releve_filename} to be compiled in {os.getcwd()}...')

    # Compile the latex file
    try:
        print(f'Generation du relevé de: {nom}-{prenoms}...')
        subprocess.run(['pdflatex', '-output-directory=' + output_directory, releve_filename],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f'Relevé de note généré: {nom}-{prenoms}')
    except subprocess.CalledProcessError as e:
        print('Error: ', e.stderr)
