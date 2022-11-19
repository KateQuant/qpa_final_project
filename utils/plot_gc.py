import logging
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from Bio import Entrez, SeqIO

from ticks_gc import ticks_mapper
from qpa_final_project.data.config import EMAIL

Entrez.email = EMAIL


def get_sequence(seq_name: str):  # NC_007366.1
    """Function to retrieve the dna sequence in fasta format"""

    handle = Entrez.efetch(db="nucleotide", id=seq_name, rettype="fasta")
    record = SeqIO.read(handle, "fasta")

    return str(record.seq)


def gc_content_plot(string: str, step=100):
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

    plt.savefig("gc_plot.png")


if __name__ == "__main__":
    dna_seq = get_sequence('NR_036570.1')  # NM_021257.4  MN908947.3
    gc_content_plot(dna_seq)

