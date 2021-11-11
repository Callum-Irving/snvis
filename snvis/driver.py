import argparse
from operator import itemgetter
import os
import subprocess
from shutil import which

import igraph
from thefuzz import fuzz

from snvis.log import logger as logger_generator


def main(args: argparse.Namespace) -> int:
    logger = logger_generator(args.q)

    # Check input file exists
    if not os.path.isfile(args.input):
        logger.error_msg(f"Could not find file: '{args.input}'")
        return 1

    # Read spreadsheet
    logger.status_msg("Parsing file")

    rows: dict[str, list[str]] = {}

    with open(args.input) as f:
        labels = f.readline().strip().split("\t")
        if not args.n < len(labels):
            logger.error_msg(f"Column number '{args.n}' is too large")
            return 1
        elif not args.c < len(labels):
            logger.error_msg(f"Column number '{args.c}' is too large")
            return 1
        elif args.n == args.c:
            logger.error_msg(
                f"Name and connections columns cannot be the same")
            return 1

        for row, line in enumerate(f.readlines()):
            cols = line.strip().split("\t")

            try:
                name = cols[args.n].strip()
            except IndexError:
                logger.error_msg(f"Name column at row {row+2} is empty")
                return 1

            try:
                cons = cols[args.c].split(",")
                cons = [x.strip() for x in cons]
            except IndexError:
                cons = []

            rows[name] = cons

    # Name matching
    def check_name_match(name):
        others = list(rows.keys())
        if name in others:
            return name

        ratios = [(fuzz.ratio(name, to_check), to_check)
                  for to_check in others]

        closest_match = max(ratios, key=itemgetter(0))
        if 100 > closest_match[0] > 80:
            logger.custom_msg(
                "NAME MATCHER", f"{name} is similar to {closest_match[1]}")
            return closest_match[1]

        return None

    for name, cons in rows.items():
        cons = [check_name_match(con) for con in cons]
        cons = [con for con in cons if con != None]
        rows[name] = cons

    # Generate graph
    logger.status_msg("Generating graph")
    people = igraph.Graph()
    people.add_vertices(len(rows))
    people.vs["label"] = list(rows.keys())

    for name, cons in rows.items():
        edge_from = people.vs.find(label=name).index
        for con in cons:
            edge_to = people.vs.find(label=con).index
            people.add_edge(edge_from, edge_to)

            # Stop duplicates
            if name in rows[con]:
                rows[con].remove(name)

    # Plot graph
    logger.status_msg("Writing graph to file")
    layout = people.layout("kk")

    if args.simplify:
        logger.status_msg("Removing unconnected people and self-loops")
        people.vs.select(_degree=0).delete()
        people.simplify()

    try:
        igraph.plot(people, str(args.o), margin=30, layout=layout)
    except ValueError:
        logger.error_msg(f"Could not write file. Do you have permissions?")

    # Show graph using default program from system
    if not args.view:
        return 0

    if os.sys.platform.startswith("linux"):
        if which("xdg-open"):
            logger.status_msg("Opening file with xdg-open")
            subprocess.run(["xdg-open", str(args.o)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            logger.error_msg("xdg-open is not installed")
            return 1
    # TODO: Following are UNTESTED
    elif os.sys.platform == "win32":
        logger.status_msg("Opening SVG with default program")
        subprocess.run(["start", str(args.o)])
    elif os.sys.platform == "darwin":
        logger.status_msg("Opening SVG with default program")
        subprocess.run(["open", str(args.o)])
    else:
        logger.error_msg(f"Unsupported platform: {os.sys.platform}")
        return 1

    logger.status_msg("Exited succesfully")
    return 0
