from pyvis.network import Network
import networkx as nx

def generate_network(rows, simplify=True):
    graph = nx.Graph()

    for name in rows:
        graph.add_node(name)

    for name, cons in rows.items():
        for con in cons:
            graph.add_edge(name, con)

    if simplify:
        # Remove isolated nodes and self loops
        graph.remove_nodes_from(list(nx.isolates(graph)))
        graph.remove_edges_from(list(nx.selfloop_edges(graph)))

    # Write networkx graph to GML file
    print("writing GML file")
    nx.readwrite.write_gml(graph, "output.gml")

    net = Network(width="100%", height="100%")
    net.from_nx(graph)
    
    return net

