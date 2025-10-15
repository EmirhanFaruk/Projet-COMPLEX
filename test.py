from functions import random_graph, branching
from calctemps import get_time, get_calctime


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



def makeTestGraphs():
    """
    Make 3 graphs with the size 10, 20 and 40.
    First list have 0.2 p, second 0.5 and third 0.8.
    """
    graphs = [[], [], []]  # Easy, Medium, Hard
    index = 0
    for i in range(2, 9, 3):
        gl = 10
        for _ in range(3):
            graphs[index].append([random_graph(gl, i * 0.1)])
            gl *= 2
        index += 1
    
    return graphs


def testSection(algo, graphs):
    results = []
    print(f"Starting the test for algorithm {algo.__name__}...")
    for G in graphs:
        for g in G:
            print(f"Testing graph with {len(g.nodes())} nodes and {len(g.edges())} edges...")
            t = get_time()
            algo(g)
            f = get_calctime(t)
            results.append((len(g.nodes()), len(g.edges()), f))
    return results

def stressTest(algo1, algo2=None, m=10, n=50, increment=10):
    graphs = makeStressTestGraphBySize(m, n, increment)
    
    algos = [algo1, algo2]
    sections = [("Easy", 0.2), ("Medium", 0.5), ("Hard", 0.8)]
    # For algo 1 and algo 2.
    results = [[[], [], []], [[], [], []]] 
    print(f"Each section have graphs having size ranging from {m} to {n}, with the size increment of {increment}, which makes {(n - m) // increment} graphs...")
    for algo in algos:
        if algo is None:
            continue
        for i in range(3):
            print(f"\n\n--- Testing {sections[i][0]} section with p={sections[i][1]} ---")
            for G in graphs[i]:
                testSection(algo, G)
        """
        print(f"Starting the test for algorithm {algo.__name__}...")
        print(f"Easy section. ")
        tt = get_time()
        for G in graphs[0]:
            for g in G:
                print(f"Testing graph with {len(g.nodes())} nodes and {len(g.edges())} edges...")
                t = get_time()
                algo(g)
                f = get_calctime(t)
                results[0].append((len(g.nodes()), len(g.edges()), f))
        ft = get_calctime(t)
        results[0].append(("Total", "", ft))
        print(f"Finished in {ft} seconds!")
        
        
        print(f"Medium section. It has graphs with p=0.5 with size ranging from {m} to {n}, with the size increment of {increment}, which makes {(n - m) // increment} graphs...")
        t = get_time()
        for g in graphs[1]:
            algo(g)
        f = get_calctime(t)
        print(f"Finished in {f} seconds!")
        print(f"Hard section. It has graphs with p=0.8 with size ranging from {m} to {n}, with the size increment of {increment}, which makes {(n - m) // increment} graphs...")
        t = get_time()
        for g in graphs[2]:
            algo(g)
        f = get_calctime(t)
        print(f"Finished in {f} seconds!")
        """
    

if __name__ == "__main__":
    stressTest(branching)