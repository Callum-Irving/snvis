import argparse
import os
import subprocess
from shutil import which

import igraph
from thefuzz import fuzz

from snvis.log import logger as loggydoo


def main(args: argparse.Namespace) -> int:
    logger = loggydoo(args.v)

    # Read spreadsheet
    logger.status_msg("Parsing file")

    student_matches = {}
    past_names = []

    def check_name_match(name):
        for past_name in past_names:
            ratio = fuzz.ratio(name, past_name)
            if 100 > ratio > 80:
                logger.custom_msg(
                    "NAME MATCHER", f"{name} is similar to {past_name}")
                return past_name

        past_names.append(name)
        return name

    with open(args.input) as f:
        # First line contains labels
        labels = f.readline().strip().split("\t")
        name_col = labels.index(args.n)
        matches_col = labels.index(args.c)

        for line in f.readlines():
            cols = line.strip().split("\t")
            name = cols[name_col].strip()
            name = check_name_match(name)

            try:
                matches = cols[matches_col].split(",")
                matches = list(map(lambda x: x.strip(), matches))

                for i in range(len(matches)):
                    matches[i] = check_name_match(matches[i])
            except:
                matches = []

            student_matches[name] = matches

    # Add people to graph
    logger.status_msg("Generating graph")
    students = igraph.Graph()
    students.add_vertices(len(student_matches))
    students.vs["name"] = list(student_matches.keys())

    # Create graph edges
    for student in student_matches:
        from_student = students.vs.find(name=student).index
        for match in student_matches[student]:
            to_student = students.vs.find(name=match).index
            students.add_edge(from_student, to_student)

            # Stops us from adding duplicated edges
            # TODO: Make edges thick if they go both ways
            if student in student_matches[match]:
                student_matches[match].remove(student)

    # Plot graph
    logger.status_msg("Writing graph to file")
    students.vs["label"] = students.vs["name"]
    layout = students.layout("kk")
    igraph.plot(students, str(args.o), margin=20, layout=layout)

    # Show graph using default program from system
    if os.sys.platform.startswith("linux"):
        if which("xdg-open"):
            logger.status_msg("Opening file with xdg-open")
            subprocess.run(["xdg-open", str(args.o)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            logger.error_msg("xdg-open is not installed")
            return 1
    # Following are UNTESTED
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
