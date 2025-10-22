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
    
    plt.title(algoname)
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
    
    plt.title(algoname)
    plt.show()