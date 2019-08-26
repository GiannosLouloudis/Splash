# The Splash pipeline was created at the Hellenic Center of Marine Research (HMCR), in Crete (August 2019).
# It's developers were John Louloudis, Tereza Manousaki and Alexandros Tsakogiannis.

# Import libraries.
import pandas as pd
import sys

# List all fasta files in the directory and set the in a variable.
input_filename = sys.argv[1].split('.')[0].split('_')[0]


# Import the CPC2-produced table and open fasta file.
table = pd.read_csv( input_filename + '_CPC2.tbl', sep = ',')
fasta = open( input_filename + '_LO.fasta', 'r')
fasta_list = fasta.read().splitlines()
fasta.close()

# Create two lists to store the ids and sequences.
fasta_ids = []
fasta_seqs = []

# Loop through every element of the fasta-list.
for element in fasta_list:
    # If the element starts with ">" then its is the id.
    if element.startswith('>'):
        fasta_ids.append(element)
    # Else it is the sequence.
    elif element.startswith('A') or element.startswith('T') or element.startswith('G') or element.startswith('C'):
        fasta_seqs.append(element)

# ------------ Create a list of the coding ids. ------------
coding_ids = []

# For line in column seven of table.
for status_num in range(len(table.iloc[:, 7])):
    # If the line's column seven says coding ...
    if table.iloc[status_num, 7] == 'coding':
        # Append the id, to the coding_ids list.
        coding_ids.append(table.iloc[status_num, 0])

print("Coding transcript percentage: " + str(len(coding_ids)*100 / len(table.iloc[:, 7])) + "%", file=sys.stderr)

# ------------ Parse through the list of fasta ids and remove the id and sequence that match those in the coding ids file. ------------
to_remove = []

# Loop through the fasta_ids and fasta_seqs, and if an id is in the coding_ids list, append both the ID and Seq to the to_remove list.
for id_num in range(len(fasta_ids)):
    print(fasta_ids[id_num]+'\n')
    for cd_id in coding_ids:
        if fasta_ids[id_num] ==  ">"+cd_id:
            to_remove.append(fasta_ids[id_num])
            to_remove.append(fasta_seqs[id_num])

# If an element exists in the to_remove list, remove it from the fasta list.
for removal in to_remove:
    print(removal)
    for element in fasta_list:
        if removal == element:
            fasta_list.remove(element)

# Write the resulting list in a file.
result_file = open(input_filename + '_NC.fasta', 'w+')
for item in range(len(fasta_list)):
    result_file.write(fasta_list[item] + '\n')
result_file.close()
