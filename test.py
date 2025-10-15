from functions import random_graph, branching
from calctemps import get_time, get_calctime

def stressTest(algo):
    graphs = [[], [], []]
    index = 0
    for i in range(2, 9, 3):
        gl = 10
        for _ in range(3):
            graphs[index].append([[random_graph(x, i)] for x in range(gl)])
            gl *= 2
        index += 1
    
    print(f"Starting the test for algorithm {algo.__name__}...")
    print("Easy section...")
    t = get_time()
    for g in graphs[0]:
        algo(g)
    f = get_calctime(t)
    print(f"Finished in {f} seconds!")
    print("Medium section...")
    t = get_time()
    for g in graphs[0]:
        algo(g)
    f = get_calctime(t)
    print(f"Finished in {f} seconds!")
    print("Hard section...")
    t = get_time()
    for g in graphs[0]:
        algo(g)
    f = get_calctime(t)
    print(f"Finished in {f} seconds!")
    

if __name__ == "__main__":
    stressTest(branching)