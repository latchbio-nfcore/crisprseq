from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: typing.Optional[LatchFile], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], analysis: str, email: typing.Optional[str], multiqc_title: typing.Optional[str], overrepresented: typing.Optional[bool], umi_clustering: typing.Optional[bool], protospacer: typing.Optional[str], mle_design_matrix: typing.Optional[LatchFile], rra_contrasts: typing.Optional[LatchFile], count_table: typing.Optional[LatchFile], library: typing.Optional[LatchFile], crisprcleanr: typing.Optional[str], cutadapt: typing.Optional[str], genome: typing.Optional[str], reference_fasta: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[LatchFile], umi_bin_size: typing.Optional[int], medaka_model: typing.Optional[str], aligner: typing.Optional[str], vsearch_minseqlength: typing.Optional[int], vsearch_maxseqlength: typing.Optional[int], vsearch_id: typing.Optional[float], min_reads: typing.Optional[float], min_targeted_genes: typing.Optional[float], bagel_reference_essentials: typing.Optional[str], bagel_reference_nonessentials: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('analysis', analysis),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('overrepresented', overrepresented),
                *get_flag('umi_clustering', umi_clustering),
                *get_flag('umi_bin_size', umi_bin_size),
                *get_flag('medaka_model', medaka_model),
                *get_flag('aligner', aligner),
                *get_flag('protospacer', protospacer),
                *get_flag('vsearch_minseqlength', vsearch_minseqlength),
                *get_flag('vsearch_maxseqlength', vsearch_maxseqlength),
                *get_flag('vsearch_id', vsearch_id),
                *get_flag('mle_design_matrix', mle_design_matrix),
                *get_flag('rra_contrasts', rra_contrasts),
                *get_flag('count_table', count_table),
                *get_flag('library', library),
                *get_flag('crisprcleanr', crisprcleanr),
                *get_flag('cutadapt', cutadapt),
                *get_flag('min_reads', min_reads),
                *get_flag('min_targeted_genes', min_targeted_genes),
                *get_flag('bagel_reference_essentials', bagel_reference_essentials),
                *get_flag('bagel_reference_nonessentials', bagel_reference_nonessentials),
                *get_flag('genome', genome),
                *get_flag('reference_fasta', reference_fasta),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_crisprseq", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_crisprseq(input: typing.Optional[LatchFile], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], analysis: str, email: typing.Optional[str], multiqc_title: typing.Optional[str], overrepresented: typing.Optional[bool], umi_clustering: typing.Optional[bool], protospacer: typing.Optional[str], mle_design_matrix: typing.Optional[LatchFile], rra_contrasts: typing.Optional[LatchFile], count_table: typing.Optional[LatchFile], library: typing.Optional[LatchFile], crisprcleanr: typing.Optional[str], cutadapt: typing.Optional[str], genome: typing.Optional[str], reference_fasta: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[LatchFile], umi_bin_size: typing.Optional[int] = 1, medaka_model: typing.Optional[str] = 'r941_min_high_g360', aligner: typing.Optional[str] = 'minimap2', vsearch_minseqlength: typing.Optional[int] = 55, vsearch_maxseqlength: typing.Optional[int] = 57, vsearch_id: typing.Optional[float] = 0.99, min_reads: typing.Optional[float] = 30.0, min_targeted_genes: typing.Optional[float] = 3.0, bagel_reference_essentials: typing.Optional[str] = 'https://raw.githubusercontent.com/hart-lab/bagel/master/CEGv2.txt', bagel_reference_nonessentials: typing.Optional[str] = 'https://raw.githubusercontent.com/hart-lab/bagel/master/NEGv1.txt') -> None:
    """
    nf-core/crisprseq

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, analysis=analysis, email=email, multiqc_title=multiqc_title, overrepresented=overrepresented, umi_clustering=umi_clustering, umi_bin_size=umi_bin_size, medaka_model=medaka_model, aligner=aligner, protospacer=protospacer, vsearch_minseqlength=vsearch_minseqlength, vsearch_maxseqlength=vsearch_maxseqlength, vsearch_id=vsearch_id, mle_design_matrix=mle_design_matrix, rra_contrasts=rra_contrasts, count_table=count_table, library=library, crisprcleanr=crisprcleanr, cutadapt=cutadapt, min_reads=min_reads, min_targeted_genes=min_targeted_genes, bagel_reference_essentials=bagel_reference_essentials, bagel_reference_nonessentials=bagel_reference_nonessentials, genome=genome, reference_fasta=reference_fasta, multiqc_methods_description=multiqc_methods_description)

