import argparse
import pathlib


def parse_args() -> argparse.Namespace:
    # Get command line args
    parser = argparse.ArgumentParser(
        prog="snvis",
        description="Create and view a graph representation of a social network.")
    parser.add_argument(
        "-n",
        type=str,
        help="label of the column containing the name (default: 'name')",
        metavar="LABEL",
        default="name"
    )
    parser.add_argument(
        "-c",
        type=str,
        help="label of the column containing the connections (default: 'connections')",
        metavar="LABEL",
        default="connections"
    )
    parser.add_argument(
        "-o",
        type=pathlib.Path,
        help="name of the output file (default: 'graph.svg')",
        metavar="FILE",
        default="graph.svg"
    )
    parser.add_argument(
        "-v",
        help="enable verbose logging",
        action="store_true"
    )
    parser.add_argument(
        "input",
        type=pathlib.Path,
        help="tab separated values file",
        metavar="SPREADSHEET"
    )
    args = parser.parse_args()
    return args
