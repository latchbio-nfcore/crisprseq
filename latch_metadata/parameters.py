
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'analysis': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description='Type of analysis to perform. Targeted for targeted CRISPR experiments and screening for CRISPR screening experiments.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'overrepresented': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='targeted pipeline steps',
        description='Trim overrepresented sequences from reads (cutadapt)',
    ),
    'umi_clustering': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='If the sample contains umi-molecular identifyers (UMIs), run the UMI extraction, clustering and consensus steps.',
    ),
    'umi_bin_size': NextflowParameter(
        type=typing.Optional[int],
        default=1,
        section_title='UMI parameters',
        description='Minimum size of a UMI cluster.',
    ),
    'medaka_model': NextflowParameter(
        type=typing.Optional[str],
        default='r941_min_high_g360',
        section_title=None,
        description='Medaka model (-m) to use according to the basecaller used.',
    ),
    'aligner': NextflowParameter(
        type=typing.Optional[str],
        default='minimap2',
        section_title='Targeted parameters',
        description='Aligner program to use.',
    ),
    'protospacer': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Provide the same protospacer sequence for all samples. Will override protospacer sequences provided by an input samplesheet.',
    ),
    'vsearch_minseqlength': NextflowParameter(
        type=typing.Optional[int],
        default=55,
        section_title='Vsearch parameters',
        description='Vsearch minimum sequence length.',
    ),
    'vsearch_maxseqlength': NextflowParameter(
        type=typing.Optional[int],
        default=57,
        section_title=None,
        description='Vsearch maximum sequence length.',
    ),
    'vsearch_id': NextflowParameter(
        type=typing.Optional[float],
        default=0.99,
        section_title=None,
        description='Vsearch pairwise identity threshold.',
    ),
    'mle_design_matrix': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Screening parameters',
        description='Design matrix used for MAGeCK MLE to call essential genes under multiple conditions while considering sgRNA knockout efficiency',
    ),
    'rra_contrasts': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Comma-separated file with the conditions to be compared. The first one will be the reference (control)',
    ),
    'count_table': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Please provide your count table if the mageck test should be skipped.',
    ),
    'library': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='sgRNA and targetting genes, tab separated',
    ),
    'crisprcleanr': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='sgRNA library annotation for crisprcleanR',
    ),
    'cutadapt': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='cut adapter for screening analysis',
    ),
    'min_reads': NextflowParameter(
        type=typing.Optional[float],
        default=30.0,
        section_title=None,
        description='a filter threshold value for sgRNAs, based on their average counts in the control sample',
    ),
    'min_targeted_genes': NextflowParameter(
        type=typing.Optional[float],
        default=3.0,
        section_title=None,
        description='Minimal number of different genes targeted by sgRNAs in a biased segment in order for the corresponding counts to be corrected for CRISPRcleanR',
    ),
    'bagel_reference_essentials': NextflowParameter(
        type=typing.Optional[str],
        default='https://raw.githubusercontent.com/hart-lab/bagel/master/CEGv2.txt',
        section_title=None,
        description='Core essential gene set for BAGEL2',
    ),
    'bagel_reference_nonessentials': NextflowParameter(
        type=typing.Optional[str],
        default='https://raw.githubusercontent.com/hart-lab/bagel/master/NEGv1.txt',
        section_title=None,
        description='Non essential gene set  for BAGEL2',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'reference_fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to the reference FASTA file. Will override reference sequences provided by an input sample sheet.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

