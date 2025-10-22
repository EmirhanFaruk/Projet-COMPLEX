from matplotlib import pyplot as plt


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