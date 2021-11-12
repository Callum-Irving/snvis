import argparse
import pathlib

from snvis import __version__


def parse_args() -> argparse.Namespace:
    # Get command line args
    parser = argparse.ArgumentParser(
        prog="snvis",
        description="Create and view a graph representation of a social network.")
    parser.add_argument(
        "-n",
        type=int,
        help="number of the column containing the name (default: 0)",
        metavar="COLUMN",
        default=0
    )
    parser.add_argument(
        "-c",
        type=int,
        help="number of the column containing the connections (default: 1)",
        metavar="COLUMN",
        default=1
    )
    parser.add_argument(
        "-o",
        type=pathlib.Path,
        help="name of the output file (default: 'graph.svg')",
        metavar="FILE",
        default="graph.svg"
    )
    parser.add_argument(
        "-q",
        help="stop logging to stdout",
        action="store_true"
    )
    parser.add_argument(
        "input",
        type=pathlib.Path,
        help="tab separated values file",
        metavar="SPREADSHEET"
    )
    parser.add_argument(
        "-v",
        "--view",
        help="view the output using default system tool",
        action="store_true"
    )
    parser.add_argument(
        "-s",
        "--simplify",
        help="remove unconnected people and self-loops",
        action="store_true"
    )
    parser.add_argument(
        "--version",
        help="show the version of snvis that is installed",
        action="version",
        version=f"{parser.prog} {__version__}"
    )
    args = parser.parse_args()
    return args
