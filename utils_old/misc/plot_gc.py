# import logging
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from Bio import Entrez, SeqIO

from qpa_final_project.utils_old.misc.ticks_gc import ticks_mapper
from qpa_final_project.data.config import EMAIL
from qpa_final_project.data.config import PATH_TO_DOCS_FROM_NCBI


Entrez.email = EMAIL


def get_sequence(seq_name: str):  # NC_007366.1
    """Function to retrieve the dna sequence in fasta format"""

    handle = Entrez.efetch(db="nucleotide", id=seq_name, rettype="fasta")
    record = SeqIO.read(handle, "fasta")

    return str(record.seq)


def gc_content_plot(string: str, file_name, step=100):
    """Function that plots DNA sequence GC-content distribution"""

    gc_count = lambda dna_string: ((dna_string.count('G') + dna_string.count('C')) / len(dna_string)) * 100

    partitions_list = [string[i: i + step] for i in range(0, len(string), step)]
    partition_gc = list(map(gc_count, partitions_list))
    genome_position = [i * step for i in range(1, len(partition_gc) + 1)]

    gc_dataframe = pd.DataFrame({'GC content': partition_gc,
                                 'Genome position': genome_position})

    x_ticks = None
    xtick_labels = None
    if len(genome_position) > 20:
        x_ticks, xtick_labels = ticks_mapper(genome_position, gc_dataframe)

    plt.figure(figsize=(15, 8))
    ax = sns.barplot(x='Genome position', y='GC content', data=gc_dataframe, color=(0.7, 0.3, 0.2))
    ax.axes.set_title('GC content distribution', fontsize=20)
    ax.set_xlabel("Genome position", fontsize=20)
    ax.set_ylabel("GC content", fontsize=20)
    ax.tick_params(labelsize=10)
    if x_ticks:
        ax.set(xticks=x_ticks)
        ax.set(xticklabels=xtick_labels)

    picture = f"{PATH_TO_DOCS_FROM_NCBI}/{file_name}.png"
    plt.savefig(picture)
    path_to_picture = Path().joinpath(picture)

    return path_to_picture


if __name__ == "__main__":

    seq_name = sys.argv[1]

    try:
        seq_str = get_sequence(seq_name)
        picture_path = gc_content_plot(seq_str, seq_name)
        print(f"Your plot picture saved in {picture_path}")
    except KeyError:
        print(f'{seq_name} is incorrect')

