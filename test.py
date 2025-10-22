from functions import random_graph
from calctemps import get_time, get_calctime
from math import sqrt
from typing import Any, Callable, List, Optional, Tuple
from plotting import makePlotForMoyennes, makePlotForMoyennesNFixed
from savegraph import saveGraphToFile

from functions import branching, algo_couplage, algo_glouton


def makeTestGraphBySize(m: int, n: int, p: float, increment: int) -> List[Any]:
    """
    Make a list of graphs with probability of p and size from m to n with increment(for the size).
    Can probably used to make a graph for statistics.
    """
    grahps = []
    for i in range(m, n + 1, increment):
        grahps.append(random_graph(i, p))
    return grahps

def makeStressTestGraphBySize(m: int, n: int, increment: int) -> List[List[List[Any]]]:
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

def testSection(algo: Callable[[Any], Any], graphs: List[Any]) -> List[Tuple[int, int, float, Any]]:
    """
    Tests the graphs with the given algorithm. returns the results including:
    [node number, edge number, time it took to execute, the result]
    """
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

def stressTest(algos: List[Optional[Callable[[Any], Any]]], m: int = 5, n: int = 20, increment: int = 5) -> List[List[Any]]:
    """
    For each algorithm in `algos`, this function generates sets of random graphs
    across three fixed edge-probability levels: Easy (p=0.2), Medium (p=0.5),
    and Hard (p=0.8). For each difficulty, graphs of sizes from `m` to `n`
    (inclusive) are created using the given `increment`, and the algorithm is
    executed and timed on each graph.

    Parameters
    - algos (list[callable]): List of algorithm callables that accept a single
    graph parameter and return a result. Each callable should have a
    `__name__` attribute for logging. Elements equal to None are skipped.
    - m (int): Minimum number of nodes for generated graphs (default 5).
    - n (int): Maximum number of nodes for generated graphs (default 20).
    - increment (int): Step size between successive graph sizes (default 5).

    Side effects
    - Prints progress and timing information to stdout.
    - Uses `makeStressTestGraphBySize` to generate graphs and `testSection`
    (which uses `get_time()` / `get_calctime()`) to time executions.

    Returns
    - list: One entry per algorithm. Each algorithm entry is a list:
        [algo_name: str, easy_results: list, medium_results: list, hard_results: list]
    where each difficulty-results list contains tuples:
        (num_nodes: int, num_edges: int, elapsed_seconds: float, result: Any)

    Example
    [
    ["algo_glouton",
        [(5, 6, 0.00123, res_obj), (10, 18, 0.00234, res_obj), ...],
        [...],  # Medium
        [...]   # Hard
    ],
    ...
    ]
    """
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


def nFixedTest(algos: List[Optional[Callable[[Any], Any]]], n: int = 20) -> None:
    """
    Tests for variant p.
    Applies the algos on those graphs, 10 for each class.
    """
    
    graphs = []
    index = 0
    for p in range(10):
        graphs.append([])
        for _ in range(10): #  par class
            graphs[index].append(random_graph(n, p * 0.1))
        index += 1

    """
    index = 0
    for graph in graphs:
        index += 1
        saveGraphToFile(graph[0], f"nFixedTest_{str(index).zfill(3)}_{len(graph[0].nodes())}_{len(graph[0].edges())}.txt")
    """
    
    results = [[f"{x.__name__}"] for x in algos]
    print(f"Each section have graphs having size {n}, with p ranging from 0.1 to 0.9, on 10 classes with 10 graphs each...")
    for algonum, algo in enumerate(algos):
        print(f"\n\n\n================ Testing sections with the algo {algo.__name__} ================")
        if algo is None:
            continue
        for G in graphs:
            results[algonum].append(testSection(algo, G))
    
    return results

def pFixedTest(algos: List[Optional[Callable[[Any], Any]]], n: int = 20, p: Optional[float] = None) -> None:
    """
    Tests for Nmax/10 etc. for given p.
    Applies the algos on those graphs, 10 for each class.
    """
    if p == None:
        p = 1/sqrt(n)
    m = n//10
    graphs = []
    index = 0
    for i in range(m, n + 1, m):
        graphs.append([])
        for _ in range(10): #  par class
            graphs[index].append(random_graph(i, p))
        index += 1
    
    """
    index = 0
    for graph in graphs:
        index += 1
        saveGraphToFile(graph[0], f"pFixedTest_{str(index).zfill(3)}_{len(graph[0].nodes())}_{len(graph[0].edges())}.txt")
    """
    
    results = [[f"{x.__name__}"] for x in algos]
    print(f"Each section have graphs having size ranging from {m} to {n}, with the size increment of {m}, on 10 classes with 10 graphs each...")
    for algonum, algo in enumerate(algos):
        print(f"\n\n\n================ Testing sections with the algo {algo.__name__} ================")
        if algo is None:
            continue
        for G in graphs:
            results[algonum].append(testSection(algo, G))
    
    return results
    
def FixedNTestMoyenne(results):
    # Tests faites, mtn il faut avoir les moyennes
    
    res = []
        
    for i, algo in enumerate(results):
        # start each algorithm entry with its name
        res.append([algo[0]])
        # iterate over probability-class results (skip the name at index 0)
        for j, class_results in enumerate(algo[1:]):
            if not class_results:
                # if no data for this class, append zero average
                res[i].append([j * 0.1, 0.0])
                continue
            partie_list = [resultat[2] for resultat in class_results]
            pm = sum(partie_list) / len(partie_list)
            # j corresponds to the class index (0 -> p=0.0, 1 -> p=0.1, ...)
            res[i].append([j * 0.1, pm])
                
            
    return res

def FixedPTestMoyenne(results):
    # Tests faites, mtn il faut avoir les moyennes
    
    res = []
        
    for i, algo in enumerate(results):
        for algores in algo:
            if isinstance(algores, str):
                res.append([algores])
                continue
            partie_list= [resultat[2] for resultat in algores]
            pm = sum(partie_list) / len(partie_list)
            res[i].append([algores[0][0], pm])
                
            
    return res

            
def printResultsByAlgoAndLevel(results: List[List[Any]]) -> None:
    for result in results:
        print(f"\n\nAlgorithm: {result[0]}")
        for l, level in enumerate(["easy", "medium", "hard"]):
            print(f"Level {level}")
            for res in result[l + 1]:
                print(f"Nodes: {res[0]}, Edges: {res[1]}, Time: {res[2]}, Result size: {len(res[3])}")

def testLevels(algos: List[Callable[[Any], Any]]) -> None:
    """
    Applies the stressTest to the given algos, 
    then prints them using printResultsByAlgoAndLevel.
    """
    results_leveled = stressTest(algos)
    for result in results_leveled:
        for res in result:
            print(res)
    printResultsByAlgoAndLevel(results_leveled)
    #printResultsByTest(results_leveled)

def testFixedP(algos: List[Callable[[Any], Any]]) -> None:
    results = pFixedTest(algos, 14)
    for result in results:
        for res in result:
            print(res)
    moyennes = FixedPTestMoyenne(results)
    print("Printing moyennes")
    for moyenne in moyennes:
        print(moyenne)
    
    # show plot
    for moyenne in moyennes:
        makePlotForMoyennes(moyenne)

def testFixedN(algos: List[Callable[[Any], Any]]) -> None:
    results = nFixedTest(algos, 14)
    for result in results:
        for res in result:
            print(res)
    moyennes = FixedNTestMoyenne(results)
    print("Printing moyennes")
    for moyenne in moyennes:
        print(moyenne)
    
    # show plot
    for moyenne in moyennes:
        makePlotForMoyennesNFixed(moyenne)
    


if __name__ == "__main__":
    # NOTE: EDGES MAKE A BIG JUMP AT EACH GRAPH, ALMOST DOUBLING. IT INCREASES REALLY QUICKLY
    # WE MIGHT NEED A WAY TO SAVE DATA, LIKE GRAPHS OR RESULTS
    # AND WE DEFINITELY NEED THE PLOTS
    algos = [algo_glouton, algo_couplage, branching]
    #testLevels(algos)
    testFixedP(algos)
    testFixedN(algos)