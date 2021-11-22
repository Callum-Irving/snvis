import logging
import os
from operator import itemgetter

from thefuzz import fuzz


def parse_file(file_path, name_col, cons_col):
    # Check input file exists
    if not os.path.isfile(file_path):
        logging.error(f"Could not find file: '{file_path}'")
        return 1

    # Read spreadsheet
    logging.info("Parsing file")

    rows = {}
    with open(file_path) as f:
        labels = f.readline().strip().split("\t")
        if not name_col < len(labels):
            logging.error(f"Column number '{name_col}' is too large")
            return 1
        elif not cons_col < len(labels):
            logging.error(f"Column number '{cons_col}' is too large")
            return 1
        elif name_col == cons_col:
            logging.error(
                f"Name and connections columns cannot be the same")
            return 1
        for row, line in enumerate(f.readlines()):
            cols = line.strip().split("\t")
            try:
                name = cols[name_col].strip()
            except IndexError:
                logging.error(f"Name column at row {row+2} is empty")
                return 1
            try:
                cons = cols[cons_col].split(",")
                cons = [x.strip() for x in cons]
            except IndexError:
                cons = []
            rows[name] = cons

    def check_name_match(name):
        others = list(rows.keys())
        if name in others:
            return name
        ratios = [(fuzz.ratio(name, to_check), to_check)
                  for to_check in others]
        closest_match = max(ratios, key=itemgetter(0))
        if 100 > closest_match[0] > 80:
            # TODO: Log row
            logging.info(
                f"Replacing {name} with {closest_match[1]}")
            return closest_match[1]
        return None

    for name, cons in rows.items():
        cons = [check_name_match(con) for con in cons]
        cons = [con for con in cons if con != None]
        rows[name] = cons

    return rows
