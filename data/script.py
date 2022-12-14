import re
import sys
from pathlib import Path
from Bio import Entrez
from Bio import SeqIO

from qpa_final_project.data.config import PATH_TO_DOCS_FROM_NCBI
from qpa_final_project.data.db_query import get_rna_string, get_protein_string
from qpa_final_project.data.config import EMAIL

Entrez.email = EMAIL


def convert_dna_to_rna(dna_string: str) -> str:
    """Function that convert DNA to RNA"""

    dna_to_convert = str(dna_string).upper()
    dna_pattern = '^[ACTG]*$'

    if re.findall(dna_pattern, dna_to_convert):
        rna = get_rna_string(dna_to_convert)
        return rna
    return "Please input correct sequence that contain only 'ATGC' letters"


def convert_rna_to_protein(rna_string: str) -> str:
    """Function that convert RNA to protein"""

    rna_to_convert = str(rna_string).upper()
    rna_pattern = '^[ACUG]*$'

    # try:
        # codon_step = range(0, len(rna_to_convert), 3)
        # aminoacids_list = [AMINOACID_DICT[rna_to_convert[i:i + 3]] for i in codon_step]
        # protein = ''.join(aminoacids_list)

    if re.findall(rna_pattern, rna_to_convert):
        if len(rna_to_convert) % 3 != 0:
            return "For translation to protein your sequence should be multiple by 3"
        protein = get_protein_string(rna_to_convert)
        return protein
    return "Please input correct sequence of the form 'AUUCG'"


def get_prefix(sequence_name: str) -> int:
    """Function that retrieve prefix from accession number"""
    sequence_search_pattern = '^[A-Z]{1,2}[_\d]{5,8}[\d.]{1,2}$'
    prefix_search_pattern = '^[A-Z]+'

    if re.search(sequence_search_pattern, sequence_name):
        prefix = len((re.search(prefix_search_pattern, sequence_name)).group(0))
        return prefix
    return 3


def fasta_creator(accession: str) -> Path:
    """Function that create fasta file with accession from nucleotide ncbi and return path to file"""
    with open(f'{PATH_TO_DOCS_FROM_NCBI}{accession}.fasta', 'w') as file:
        handle = Entrez.efetch(db="nucleotide", id=accession, rettype="fasta")
        record = SeqIO.read(handle, "fasta")
        reply = '>' + record.description + '\n' + str(record.seq)
        file.write(reply)

    path_to_download = Path().joinpath(f'{PATH_TO_DOCS_FROM_NCBI}{accession}.fasta')
    return path_to_download


if __name__ == "__main__":

    argument = sys.argv[1]
    search_algo_str = sys.argv[2]

    search_dict = {"DtR": convert_dna_to_rna, "RtP": convert_rna_to_protein}

    try:
        func = search_dict[search_algo_str]
        result = func(argument)
        print(result)
    except KeyError:
        print(f'{search_algo_str} is an unknown search algorithm')

# print(convert_dna_to_rna('ATTGATG'))
# print(convert_rna_to_protein('AUGGGCAA'))
