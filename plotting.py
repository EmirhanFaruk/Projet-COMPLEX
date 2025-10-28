from matplotlib import pyplot as plt

def makePlotForMoyennesNFixed(algomoyennes):
    algoname = algomoyennes[0]
    moyennesetsommets = algomoyennes[1:]
    probas = [x[0] for x in moyennesetsommets]
    moyennes = [x[1] for x in moyennesetsommets]
    print(algoname)
    print(probas)
    print(moyennes)
    plt.plot(probas, moyennes)
    plt.xlabel("Probabilité")
    plt.ylabel("Temps")
    
    plt.title(f"{algoname}, n fixé")
    plt.show()


def makePlotForMoyennes(algomoyennes):
    algoname = algomoyennes[0]
    moyennesetsommets = algomoyennes[1:]
    nbsommets = [x[0] for x in moyennesetsommets]
    moyennes = [x[1] for x in moyennesetsommets]
    print(algoname)
    print(nbsommets)
    print(moyennes)
    plt.plot(nbsommets, moyennes)
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Temps")
    
    plt.title(f"{algoname}, p fixé")
    plt.show()
    
def plotStressTest(refined_results_for_algo):
    """
    refined_results_for_algo: 
    [
        ["algo_name", 
            [(size1, [easy, medium, hard]), 
            ...]
        ]
    """
    for results in refined_results_for_algo:
        algoname = results[0]
        print("===============================")
        ress = results[1]
        for el in results[1]:
            print(el)
        sizes = [x[0] for x in ress[0]]
        easy_times = [x[1] for x in ress[0]]
        medium_times = [x[1] for x in ress[1]]
        hard_times = [x[1] for x in ress[2]]
        print(algoname)
        print(sizes)
        print(easy_times)
        print(medium_times)
        print(hard_times)

        plt.plot(sizes, easy_times, label="Easy (p=0.2)")
        plt.plot(sizes, medium_times, label="Medium (p=0.5)")
        plt.plot(sizes, hard_times, label="Hard (p=0.8)")
        plt.xlabel("Nombre de sommets")
        plt.ylabel("Temps moyen (s)")
        plt.title(f"{algoname}, Stress Test")
        plt.legend()
        plt.show()