#!/usr/bin/env python3

# Import libraries.
import re
import sys
import requests
import argparse
import pandas as pd

# Initialize parser.
parser = argparse.ArgumentParser(description='Get the name of the organism and/or the amino acid sequence, for the provided protein ID.')

# Add the parameters.
parser.add_argument("-i", "--input_file", help="Input the TopHits table file from the Splash pipeline or any tab-delimeted table where the second column has the protein IDs.")
parser.add_argument("-s", "--sequence", help="Output the sequence corresponding to each ID.", action="store_true")
parser.add_argument("-o", "--organism", help="Output the organism corresponding to each ID.", action="store_true")

# Parse the arguments.
args = parser.parse_args()

# Read the input table.
data = pd.read_csv(args.input_file, sep='\t', header=None)

# Keep the IDs' column. Create empty lists to store the organisms' names and sequences.
queries = data.iloc[:, 1]
organisms = []
sequences = []

#
def get_data(query):
    print(query)
    # Create the url for the corresponding protein.
    url = 'https://www.uniprot.org/uniprot/'+str(query)+'.fasta'
    # Get to the url's api.
    request = requests.get(url)
    # set a variable as the fasta text.
    hit = request.text
    if args.sequence==True and args.organism==True:
        organism_finder(hit)
        prot_seq_finder(hit)
    elif args.sequence==True and args.organism==False:
        prot_seq_finder(hit)
    elif args.sequence==False and args.organism==True:
        organism_finder(hit)
    else:
        pass


def organism_finder(hit):
    # If the query is in the line, keep the part of the line that contains the organism.
    organisms.append(re.search('OS=(.+?)OX=', hit).group(1))

def prot_seq_finder(hit):
    # Split fasta file lines.
    hit_lines = hit.splitlines()
    # Create empty string to store the sequence.
    sequence = ''
    # Store the sequence as one string.
    full_seq = sequence.join(hit_lines[1:])
    sequences.append(full_seq)

def loop(_range_):
    for i in range(_range_):
        get_data(queries[i])

loop(10)

results = open(args.input_file.split(".")[0] + '_API.results', 'w+')
if args.sequence==True and args.organism==True:
    for i in range(len(organisms)):
        results.write(queries[i] + '\t' + organisms[i] + '\t' + sequences[i] + '\n')
elif args.sequence==False and args.organism==True:
    for i in range(len(organisms)):
        results.write(queries[i] + '\t' + organisms[i] + '\n')
elif args.sequence==True and args.organism==False:
    for i in range(len(sequences)):
        results.write(queries[i] + '\t' + sequences[i] + '\n')
results.close()
