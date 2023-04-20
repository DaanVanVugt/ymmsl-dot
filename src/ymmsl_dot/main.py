"""Command-line tools for ymmsl."""
import subprocess
from pathlib import Path
from typing import Sequence, Union

import click
import pydot
import ymmsl
from ymmsl import PartialConfiguration

from .model_to_dot import plot_model_graph


@click.group()
def main() -> None:
    """This command provides various functions for analysing yMMSL coupled simulations.

    Use ymmsl <command> --help for help with individual commands.
    """
    pass


@main.command(short_help="Print a graphical representation of this workflow")
@click.argument(
    "ymmsl_files",
    nargs=-1,
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        allow_dash=True,
        resolve_path=True,
    ),
)
@click.option(
    "-o",
    "--out",
    nargs=1,
    required=False,
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=False,
        allow_dash=True,
        resolve_path=True,
    ),
    help="Output file (default ./output.format)",
)
@click.option(
    "-f",
    "--fmt",
    type=click.Choice(pydot.Dot().formats, case_sensitive=False),
    required=False,
    help="Set output format (default svg).",
)
@click.option(
    "-w",
    "--viewer",
    nargs=1,
    required=False,
    type=str,
    help="Open with specified viewer (try xdg-open)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Show more info (prints the generated dot syntax)",
)
@click.option("-p", "--ports", is_flag=True, help="Explicitly draw component ports.")
@click.option("-l", "--legend", is_flag=True, help="Show a legend (only with --ports).")
@click.option(
    "-s",
    "--simple-edges",
    is_flag=True,
    help="Only indicate conduit direction, not port types.",
)
@click.option(
    "--portlabels",
    is_flag=True,
    help="Never simplify matching port labels along an edge.",
)
def graph(
    ymmsl_files: Sequence[str],
    out: Union[Path, None],
    fmt: str,
    viewer: str,
    verbose: bool,
    ports: bool,
    legend: bool,
    simple_edges: bool,
    portlabels: bool,
) -> None:
    """Plot a graphical representation of the passed yMMSL files.

    To help develop or understand about a coupled simulation it may
    be useful to view a graphical representation.

    If multiple yMMSL files are given, then they will be combined left
    to right, i.e. if there are conflicting declarations, the one from
    the file last given is used.

    Result:

      A graph is displayed or saved to disk, containing all the defined
    components and the connections between them.

    Examples:

      muscle3 graph simulation.ymmsl

    """
    partial_config = _load_ymmsl_files(ymmsl_files)

    graph = plot_model_graph(
        partial_config,
        simplify_edge_labels=not portlabels,
        draw_ports=ports,
        simple_edges=simple_edges,
        show_legend=legend,
    )

    if fmt is None:
        fmt = "svg"
    if out is None:
        out = "output." + fmt

    if out == "-" and fmt == "dot":
        print(graph)  # noqa:T201
    elif out == "-":
        print(graph.create(format=fmt))  # noqa:T201
    else:
        if verbose:
            print(graph)  # noqa:T201

        graph.write(out, format=fmt)

    if viewer is not None and out != "-":
        subprocess.run([viewer, out])


def _load_ymmsl_files(ymmsl_files: Sequence[str]) -> PartialConfiguration:
    """Load and merge yMMSL files."""
    configuration = PartialConfiguration()
    for path in ymmsl_files:
        with open(path, "r") as f:
            configuration.update(ymmsl.load(f))
    return configuration


if __name__ == "__main__":
    main()
