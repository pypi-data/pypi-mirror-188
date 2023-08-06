"""
Defines the rule ``syw__arxiv`` to generate a tarball for arXiv submission.

Runs the script :doc:`arxiv` to generate the tarball ``arxiv.tar.gz``.

"""
from showyourwork import paths


rule:
    """
    Generate a tarball for arXiv submission.

    """
    name:
        "syw__arxiv"
    message:
        "Generating the arXiv tarball..."
    input:
        config["ms_tex"],
        config["dependencies"][config["ms_tex"]],
        WORKFLOW_GRAPH,
        "showyourwork.yml",
        paths.user().flags / "SYW__CONDA"
    output:
        "arxiv.tar.gz",
        config["ms_pdf"],
        temp(config["tex_files_out"]),
        temp(config["stylesheet"]),
        temp(config["stylesheet_meta_file"]),
        directory(paths.user().compile.as_posix())
    script:
        "../scripts/arxiv.py"
