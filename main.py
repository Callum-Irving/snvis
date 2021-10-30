import argparse
import os
import pathlib
import subprocess
import sys
from shutil import which

from thefuzz import fuzz
import igraph
from log import logger

# Get command line args
parser = argparse.ArgumentParser(
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

logger = logger(args.v)

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
        sys.exit(1)
# Following are UNTESTED
elif os.sys.platform == "win32":
    logger.status_msg("Opening SVG with default program")
    subprocess.run(["start", str(args.o)])
elif os.sys.platform == "darwin":
    logger.status_msg("Opening SVG with default program")
    subprocess.run(["open", str(args.o)])
else:
    logger.error_msg(f"Unsupported platform: {os.sys.platform}")
    sys.exit(1)

logger.status_msg("Exited succesfully")
