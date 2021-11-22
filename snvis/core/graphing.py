import logging

import igraph


def generate_igraph(rows, simplify=True):
    logging.info("Generating graph")
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

    if simplify:
        logging.info("Removing unconnected people and self-loops")
        people.vs.select(_degree=0).delete()
        people.simplify()

    return people
