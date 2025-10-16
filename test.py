from functions import random_graph
from calctemps import get_time, get_calctime

from functions import branching, algo_couplage, algo_glouton


def makeTestGraphBySize(m, n, p, increment):
    """
    Make a list of graphs with probability of p and size from m to n with increment(for the size).
    Can probably used to make a graph for statistics.
    """
    grahps = []
    for i in range(m, n + 1, increment):
        grahps.append(random_graph(i, p))
    return grahps

def makeStressTestGraphBySize(m, n, increment):
    """
    Make a list of graphs with probability of 0.2, 0.5 and 0.8 and size from m to n with increment(for the size).
    Can probably used to make a graph for statistics.
    """
    graphs = [[], [], []]  # Easy, Medium, Hard
    index = 0
    for i in range(2, 9, 3):
        graphs[index].append(makeTestGraphBySize(m, n, i * 0.1, increment))
        index += 1
    
    return graphs

def testSection(algo, graphs):
    results = []
    print(f"Starting the test for algorithm {algo.__name__}...")
    for G in graphs:
        print(f"Testing graph with {len(G.nodes())} nodes and {len(G.edges())} edges...")
        t = get_time()
        res = algo(G)
        f = get_calctime(t)
        results.append((len(G.nodes()), len(G.edges()), f, res))
        print(f"Finished in {f} seconds.")
    return results

def stressTest(algos, m=5, n=20, increment=5):
    graphs = makeStressTestGraphBySize(m, n, increment)
    
    sections = [("Easy", 0.2), ("Medium", 0.5), ("Hard", 0.8)]
    # For algos. Each list inside will have 3 lists for each section
    results = [[f"{x.__name__}"] for x in algos]
    print(f"Each section have graphs having size ranging from {m} to {n}, with the size increment of {increment}, which makes {(n - m) // increment} graphs...")
    for algonum, algo in enumerate(algos):
        print(f"\n\n\n================ Testing sections with the algo {algo.__name__} ================")
        if algo is None:
            continue
        for i in range(3):
            print(f"\n--- Testing {sections[i][0]} section with p={sections[i][1]} ---")
            for G in graphs[i]:
                results[algonum].append(testSection(algo, G))

    return results



def printResultsByAlgo(results):
    for result in results:
        # Each algorithm and their results
        print(f"\n\nAlgorithm: {result[0]}")
        for algores in result[1]:
            print(f"Nodes: {algores[0]}, Edges: {algores[1]}, Time: {algores[2]}, Result size: {len(algores[3])}")

def printResultsByTest(results):
    length = len(results[0]) - 1
    for i in range(length):
        print("\n\n==========================")
        for algo in results:
            print(f"Algorithm: {algo[0]}")
            print(f"Nodes: {algo[1][i][0]}, Edges: {algo[1][i][1]}, Time: {algo[1][i][2]}, Result size: {len(algo[1][i][3])}")

    

if __name__ == "__main__":
    # NOTE: EDGES MAKE A BIG JUMP AT EACH GRAPH, ALMOST DOUBLING. IT INCREASES REALLY QUICKLY
    # WE MIGHT NEED A WAY TO SAVE DATA, LIKE GRAPHS OR RESULTS
    # AND WE DEFINITELY NEED THE PLOTS
    algos = [algo_glouton, algo_couplage, branching]
    results = stressTest(algos)
    for result in results:
        for res in result:
            print(res)
    printResultsByAlgo(results)
    printResultsByTest(results)