import argparse
import logging
import os
import pathlib
from shutil import which
import subprocess
import sys

import igraph

from snvis import core
from snvis import __version__


def parse_args() -> argparse.Namespace:
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


def main() -> int:
    FORMAT = "[%(levelname)s]: %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    args = parse_args()

    # Argument checking
    if args.n == args.c:
        logging.error("Name and connections columns cannot be equal")
        return 1

    rows = core.parsing.parse_file(
        args.input, args.n, args.c)

    if rows == 1:
        return 1

    graph = core.graphing.generate_igraph(rows, simplify=args.simplify)

    # Output graph
    logging.info("Writing graph to file")
    layout = graph.layout("kk")

    try:
        igraph.plot(graph, str(args.o), margin=30, layout=layout)
    except ValueError:
        logging.error(f"Could not write file. Do you have permissions?")
        return 1

    if not args.view:
        logging.info("Exited succesfully")
        return 0

    # Show graph using default program from system
    if os.sys.platform.startswith("linux"):
        if which("xdg-open"):
            logging.info("Opening file with xdg-open")
            subprocess.run(["xdg-open", str(args.o)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            logging.error("xdg-open is not installed")
            return 1
    # TODO: Following are UNTESTED
    elif os.sys.platform == "win32":
        logging.info("Opening SVG with default program")
        subprocess.run(["start", str(args.o)])
    elif os.sys.platform == "darwin":
        logging.info("Opening SVG with default program")
        subprocess.run(["open", str(args.o)])
    else:
        logging.error(f"Unsupported platform: {os.sys.platform}")
        return 1

    logging.info("Exited succesfully")


if __name__ == "__main__":
    sys.exit(main())
