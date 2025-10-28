from functions import random_graph
from calctemps import get_time, get_calctime
from math import sqrt
from typing import Any, Callable, List, Optional, Tuple
from plotting import makePlotForMoyennes, makePlotForMoyennesNFixed, plotStressTest
from debug import sprint, DEBUG

from functions import branching, algo_couplage, algo_glouton


def makeTestGraphBySize(m: int, n: int, p: float, increment: int) -> List[Any]:
    """
    Make a list of graphs with probability of p and size from m to n with increment(for the size) for 10 each.
    Can probably used to make a graph for statistics.
    Example:
    [
        [G1_size_m, G2_size_m, ..., G10_size_m],
        [G1_size_m+increment, G2_size_m+increment, ..., G10_size_m+increment],
        ...
        [G1_size_n, G2_size_n, ..., G10_size_n]
    ]
    """
    grahps = []
    for i in range(m, n + 1, increment):
        grahps.append([random_graph(i, p) for _ in range(10)])  # 10 graphs per size
    return grahps

def makeStressTestGraphBySize(m: int, n: int, increment: int) -> List[List[List[Any]]]:
    """
    Make a list of graphs with probability of 0.2, 0.5 and 0.8 and size from m to n with increment(for the size).
    Can probably used to make a graph for statistics.
    Example:
    [
        [  # Easy (p=0.2)
            [G1_size_m, G2_size_m, ..., G10_size_m],
            [G1_size_m+increment, G2_size_m+increment, ..., G10_size_m+increment],
            ...
            [G1_size_n, G2_size_n, ..., G10_size_n]
        ],
        [  # Medium (p=0.5)
            [G1_size_m, G2_size_m, ..., G10_size_m],
            [G1_size_m+increment, G2_size_m+increment, ..., G10_size_m+increment],
            ...
            [G1_size_n, G2_size_n, ..., G10_size_n]
        ],
        [  # Hard (p=0.8)
            [G1_size_m, G2_size_m, ..., G10_size_m],
            [G1_size_m+increment, G2_size_m+increment, ..., G10_size_m+increment],
            ...
            [G1_size_n, G2_size_n, ..., G10_size_n]
        ]
    ]
    """
    graphs = [[], [], []]  # Easy, Medium, Hard
    probs = [0.2, 0.5, 0.8]
    
    for index, p in enumerate(probs):
        size_graphs_list = makeTestGraphBySize(m, n, p, increment)  # returns [[G1..G10], [G2..]]
        graphs[index] = size_graphs_list  # no extra append
    return graphs

def testSection(algo: Callable[[Any], Any], graphs: List[Any]) -> List[Tuple[int, int, float, Any]]:
    """
    Tests the graphs with the given algorithm. 
    The graphs should be like:
    [
        G1, G2, ..., Gn
    ]
    
    Returns the results in this format:
    [
        (node number, edge number, time it took to execute, the result),
        ...
    ]
    """
    results = []
    sprint(f"Starting the test for algorithm {algo.__name__}...")
    for G in graphs:
        sprint(f"Testing graph with {len(G.nodes())} nodes and {len(G.edges())} edges...")
        t = get_time()
        res = algo(G)
        f = get_calctime(t)
        results.append((len(G.nodes()), len(G.edges()), f, res))
        sprint(f"Finished in {f} seconds.")
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
        [[(5, 6, 0.00123, res_obj), ... x10], [(10, 18, 0.00234, res_obj), ... x 0], ...], # Easy
        [...],  # Medium
        [...]   # Hard
    ],
    ...
    ]
    """
    graphs = makeStressTestGraphBySize(m, n, increment)
    """
    [
        [  # Easy (p=0.2)
            [G1_size_m, G2_size_m, ..., G10_size_m],
            [G1_size_m+increment, G2_size_m+increment, ..., G10_size_m+increment],
            ...
            [G1_size_n, G2_size_n, ..., G10_size_n]
        ],
        [  # Medium (p=0.5)
            [G1_size_m, G2_size_m, ..., G10_size_m],
            [G1_size_m+increment, G2_size_m+increment, ..., G10_size_m+increment],
            ...
            [G1_size_n, G2_size_n, ..., G10_size_n]
        ],
        [  # Hard (p=0.8)
            [G1_size_m, G2_size_m, ..., G10_size_m],
            [G1_size_m+increment, G2_size_m+increment, ..., G10_size_m+increment],
            ...
            [G1_size_n, G2_size_n, ..., G10_size_n]
        ]
    ]
    """
    
    sections = [("Easy", 0.2), ("Medium", 0.5), ("Hard", 0.8)] # just to print
    # For algos. Each list inside will have 3 lists for each section
    results = [[f"{x.__name__}"] for x in algos]
    sprint(f"Each section have graphs having size ranging from {m} to {n}, with the size increment of {increment}, which makes {(n - m) // increment} graphs...")
    for algonum, algo in enumerate(algos):
        sprint(f"\n\n\n================ Testing sections with the algo {algo.__name__} ================")
        if algo is None:
            continue
        for i in range(3):
            """
            graphs[i]:
            [  # Section i(ex: Easy)
                [G1_size_m, G2_size_m, ..., G10_size_m],
                [G1_size_m+increment, G2_size_m+increment, ..., G10_size_m+increment],
                ...
                [G1_size_n, G2_size_n, ..., G10_size_n]
            ]
            """
            sprint(f"\n--- Testing {sections[i][0]} section with p={sections[i][1]} ---")
            results[algonum].append([])  # for this section
            for size_graphs in graphs[i]:  # size_graphs = list of 10 graphs
                results_for_size = testSection(algo, size_graphs)
                results[algonum][i + 1].append(results_for_size)

    """
    results:
    [
        ["algo_glouton",
            [ # Easy
                [(5, 6, 0.00123, res_obj), ... x10], 
                [(10, 18, 0.00234, res_obj) ... x10], ... x (n-m)/increment],
                ...
            ],
            [...],  # Medium
            [...]   # Hard
        ],
        ...
    ]
    """
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
    sprint(f"Each section have graphs having size {n}, with p ranging from 0.1 to 0.9, on 10 classes with 10 graphs each...")
    for algonum, algo in enumerate(algos):
        sprint(f"\n\n\n================ Testing sections with the algo {algo.__name__} ================")
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
    sprint(f"Each section have graphs having size ranging from {m} to {n}, with the size increment of {m}, on 10 classes with 10 graphs each...")
    for algonum, algo in enumerate(algos):
        sprint(f"\n\n\n================ Testing sections with the algo {algo.__name__} ================")
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


def getAvgTime(reslist: List[Tuple[int, int, float, Any]]) -> float:
    res = sum([x[2] for x in reslist]) / len(reslist)
    # print("Average time calculated:", res)
    return res


def stressTestMoyenne(results):
    # Tests faites, mtn il faut avoir les moyennes
    """
    results:
    [
        ["algo_glouton",
            [ # Easy
                [(5, 6, 0.00123, res_obj), ... x10], 
                [(10, 18, 0.00234, res_obj) ... x10], ... x (n-m)/increment],
                ...
            ],
            [...],  # Medium
            [...]   # Hard
        ],
        ...
    ]
    """
    
    res = []

    for algonum, algo_data in enumerate(results):
        """
        algo_data:
        ["algo_glouton",
            [ # Easy
                [(5, 6, 0.00123, res_obj), ... x10], 
                [(10, 18, 0.00234, res_obj) ... x10], ... x (n-m)/increment],
                ...
            ],
            [...],  # Medium
            [...]   # Hard
        ]
        """
        algo_name = algo_data[0]
        averaged_algo = [algo_name]
        """
        averaged_algo:
        [
            "algo_glouton",
            [
                (size, temps_moyenne_easy),
                (size, temps_moyenne_medium),
                (size, temps_moyenne_hard)
            ]
        ]
        """
        
        moyennes = [[[] for _ in range(len(algo_data[1][0]))] for _ in range(3)]  # Easy, Medium, Hard
        print(len(moyennes))
        """
        moyennes:
        [
            [ # Easy
                (size, moyenne),
                (size, moyenne),
                ...
            ],
            [ # Medium
                (size, moyenne),
                (size, moyenne),
                ...
            ],
            [ # Hard
                (size, moyenne),
                (size, moyenne),
                ...
            ]
        ]
        """
        print("================================")
        print(f"Sections of algo_data: {len(algo_data[1:])}")
        for i, section in enumerate(algo_data[1:]):
            print("\n\n", i, section)
        for size_index, res_by_size_list_list in enumerate(algo_data[1:]):
            """
            res_by_size_list:
            [ # Easy
                [(5, 6, 0.00123, res_obj), ... x10], 
                [(10, 18, 0.00234, res_obj) ... x10], ... x (n-m)/increment],
            ]
            """
            print("================================")
            print(size_index, res_by_size_list_list)
            print(len(moyennes))
            moyennes[size_index] = ([(l[0][0], getAvgTime(l)) for l in res_by_size_list_list])
            print("--------------------------------")
            print(moyennes)
            print("--------------------------------")

        averaged_algo.append(moyennes)
        res.append(averaged_algo)

    """
    res:
    [
        ["algo_glouton",
            [
                [ # Easy
                    (size, moyenne),
                    (size, moyenne),
                    ...
                ],
                [ # Medium
                    (size, moyenne),
                    (size, moyenne),
                    ...
                ],
                [ # Hard
                    (size, moyenne),
                    (size, moyenne),
                    ...
                ]
            ]
        ],
        ...
    """
    print("Final averaged results:")
    print(res)
    for r in res:
        print(r)
    return res


            
def printResultsByAlgoAndLevel(results: List[List[Any]]) -> None:
    for result in results:
        sprint(f"\n\nAlgorithm: {result[0]}")
        for l, level in enumerate(["easy", "medium", "hard"]):
            sprint(f"Level {level}")
            for res in result[l + 1]:
                sprint(f"Nodes: {res[0]}, Edges: {res[1]}, Time: {res[2]}, Result size: {len(res[3])}")


def leveledResultsGroupedBySize(results_leveled):
    refined_results = []

    for algo_data in results_leveled:
        algo_name = algo_data[0]
        data_lists = algo_data[1:]

        # Flatten all the lists
        all_results = [item for sublist in data_lists for item in sublist]

        # Group by node size using a list instead of a dict
        grouped_list = []
        seen_sizes = []
        for r in all_results:
            nodes = r[0]
            if nodes not in seen_sizes:
                seen_sizes.append(nodes)
                grouped_list.append((nodes, [r]))
            else:
                # append to the correct size
                for idx, (size, results_for_size) in enumerate(grouped_list):
                    if size == nodes:
                        grouped_list[idx][1].append(r)
                        break
        
        refined_results.append((algo_name, grouped_list))
    
    return refined_results
                

def testLevels(algos: List[Optional[Callable[[Any], Any]]], m: int = 5, n: int = 14, increment: int = 5) -> None:
    """
    Applies the stressTest to the given algos, 
    then makes graphs by the size of the graphs,
    using the mean value of them.
    """
    increment = (n - m) // 10
    if increment == 0:
        increment = 1
    results_leveled = stressTest(algos, m, n, increment)
    refined_results = stressTestMoyenne(results_leveled)
    #refined_results = leveledResultsGroupedBySize(results_leveled)
    sprint("Printing moyennes for stress test...")
    for moyenne in refined_results:
        print("===============================")
        for m in moyenne:
            sprint(m)
    
    plotStressTest(refined_results)
    
    
                
    

def testFixedP(algos: List[Callable[[Any], Any]]) -> None:
    results = pFixedTest(algos, 14)
    for result in results:
        for res in result:
            sprint(res)
    moyennes = FixedPTestMoyenne(results)
    print("Printing moyennes")
    for moyenne in moyennes:
        sprint(moyenne)
    
    # show plot
    for moyenne in moyennes:
        makePlotForMoyennes(moyenne)

def testFixedN(algos: List[Callable[[Any], Any]]) -> None:
    results = nFixedTest(algos, 14)
    for result in results:
        for res in result:
            sprint(res)
    moyennes = FixedNTestMoyenne(results)
    sprint("Printing moyennes")
    for moyenne in moyennes:
        sprint(moyenne)
    # show plot
    for moyenne in moyennes:
        makePlotForMoyennesNFixed(moyenne)
    


if __name__ == "__main__":
    # NOTE: EDGES MAKE A BIG JUMP AT EACH GRAPH, ALMOST DOUBLING. IT INCREASES REALLY QUICKLY
    # WE MIGHT NEED A WAY TO SAVE DATA, LIKE GRAPHS OR RESULTS
    # AND WE DEFINITELY NEED THE PLOTS
    algos = [algo_glouton, algo_couplage, branching]
    #testLevels(algos)
    #testFixedP(algos)
    #testFixedN(algos)
    testLevels(algos)