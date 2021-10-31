import argparse
from operator import itemgetter
import os
import subprocess
from shutil import which

import igraph
from thefuzz import fuzz

from snvis.log import logger as logger_generator


def main(args: argparse.Namespace) -> int:
    logger = logger_generator(args.v)

    # Read spreadsheet
    logger.status_msg("Parsing file")

    rows: dict[str, list[str]] = {}

    with open(args.input) as f:
        labels = f.readline().strip().split("\t")
        name_col = labels.index(args.n)
        cons_col = labels.index(args.c)

        for line in f.readlines():
            cols = line.strip().split("\t")
            name = cols[name_col].strip()
            try:
                cons = cols[cons_col].split(",")
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
        for i, con in enumerate(cons):
            closest_match = check_name_match(con)
            if closest_match == None:
                logger.error_msg(
                    f"Unknown name in connections to {name}: {cons[i]}")
                return 1
            cons[i] = closest_match
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
    igraph.plot(people, str(args.o), margin=30, layout=layout)

    # Show graph using default program from system
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
