import networkx as nx
import random
import matplotlib.pyplot as plt
import os
from parsetxt import readFile, extractProps, reformatProps

def parseTxt(filename):
    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        lines = readFile(file_path)
        props = extractProps(lines)
        reprops = reformatProps(props)
        G = nx.parse_adjlist(reprops, nodetype=int)
    except:
        print("failure with first parse, using alt")
        G = parseTxt_alt(filename)
    return G

def parseTxt_alt(filename):  # experimental
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    edges = [tuple(map(int, line.split())) for line in lines[lines.index("Aretes") + 1:]]
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

def print_graph(G):
    print("Nodes:", G.nodes())
    print("Edges:", G.edges())    

def plot_graph(G, title=None):
    fig = plt.figure()
    nx.draw(G, with_labels=True)
    if title:
        try:
            fig.canvas.manager.set_window_title(title)
        except Exception:
            fig.suptitle(title)
    plt.show(block=False)





def remove_node_copy(G, n):
    H = G.copy()
    H.remove_node(n)
    return H

def degree_map(G) :
    return dict(G.degree())

def max_degree_vertex(G):
    degs = degree_map(G)
    if not degs:
        raise ValueError("max_degree_vertex: graph has no nodes")
    return max(degs, key=degs.get)

def random_graph(n,p):
    return nx.erdos_renyi_graph(n, p)

def random_graph_alt(n,p): # au cas ou le prof veut pas l'autre 
    G= nx.complete_graph(n)
    for u, v in list(G.edges()):
        if random.random() > p:
            G.remove_edge(u, v)
    return G


def algo_couplage(G):
    C = set()
    for edge in G.edges():
        if edge[0] not in C and edge[1] not in C:
            C.add(edge[0])
            C.add(edge[1])
    return C
#NOTE: l'énoncé est pas clair,
# je sais pas si c'est ça qu'il veut, ça dit "sortie: une couverture"
# mais au dessus: "un couplage est un ensemble d'arretes",
# on verra bien dans la suite si ça marche pas.

def algo_glouton(G):
    C = set()
    H = G.copy()
    while H.number_of_edges() > 0:
        v = max_degree_vertex(H)
        C.add(v)
        H.remove_node(v)
    return C



def branching(G):
    C = [] # le resultat
    pile = [(-1, G.copy(), [])] # le pile
    if len(G.edges()) == 0:
        return []
    while pile != []:
        courant = pile.pop()
        (_, Hc, solc) = courant
        if len(Hc.edges()) == 0:
            if C == []:
                C = solc.copy()
            else:
                if len(C) > len(solc):
                    C = solc.copy()
        else:
            arete = list(Hc.edges())[0]
            u, v = arete
            pile.append((u, remove_node_copy(Hc, u), solc + [u]))
            pile.append((v, remove_node_copy(Hc, v), solc + [v]))
                
    return C


if __name__ == "__main__":
    H = parseTxt("exemple.txt")
    print(dir(H))
    print(H.nodes)
    print(len(H.nodes()))
    print(H.size())
    print_graph(H)
    plot_graph(H, title="exemple")
    print("degree map:", degree_map(H))
    print("max degree vertex:", max_degree_vertex(H))
    print("couplage:", algo_couplage(H))
    print("glouton:", algo_glouton(H))
    
    G = random_graph(10, 0.3)
    plot_graph(G, title="random")
    
    C = branching(H)
    print("branching: ", C)
    

    input("'Enter' pour fermer les graphes...")


