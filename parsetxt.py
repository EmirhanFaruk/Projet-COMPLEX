

def readFile(filename):
    try:
        file = open(filename, "r")
        lines = file.readlines()
        return lines
    except:
        print("Erreur pendant lecture de fichier")
        raise FileNotFoundError

def extractProps(lines):
    nbsommets = 0
    sommets = []
    nbaretes = 0
    aretes = []
    status = 0 
    """
    1 -> nb sommets
    2 -> sommets
    3 -> nb aretes
    4 -> aretes
    """
    for line in lines:
        line = line.strip()
        if (line == "" or line[0] in [i for i in range(10)]) and status == 0:
            continue
        if line[0] in [str(i) for i in range(10)]:
            if status == 1:
                try:
                    nbsommets = int(line)
                except:
                    print(f"Erreur pendant lecture de nb sommet {line}")
                    raise ValueError
                status = 0
            elif status == 2:
                try:
                    sommets.append(line) # Change ici pour avoir string a la place d'entier
                except:
                    print(f"Erreur pendant lecture de sommet {line}")
                    raise ValueError
            elif status == 3:
                try:
                    nbaretes = int(line)
                except:
                    print(f"Erreur pendant lecture de nb arete {line}")
                    raise ValueError
                status = 0
            elif status == 4:
                try:
                    narete = line.split(" ") 
                    if len(narete) != 2:
                        raise ValueError
                    aretes.append(narete)
                except:
                    print(f"Erreur pendant lecture de arete {line}")
                    raise ValueError
        else:
            if line == "Nombre de sommets":
                status = 1
            elif line == "Sommets":
                status = 2
            elif line == "Nombre d aretes":
                status = 3
            elif line == "Aretes":
                status = 4
        
    return nbsommets, sommets[:nbsommets], nbaretes, aretes[:nbaretes]


def reformatProps(props):
    sommets = dict()
    for sommet in props[1]:
        sommets[sommet] = ""
    for arete in props[3]:
        sommets[arete[0]] = sommets[arete[0]] + " " + arete[1]
        sommets[arete[0]] = sommets[arete[0]].strip()
    return [(sommet + " " + aretes).strip() for sommet, aretes in sommets.items()]


def test(filename):
    lines = readFile("exemple.txt")
    props = extractProps(lines)
    reprops = reformatProps(props)
    print(reprops)

if __name__ == "__main__":
    test("exemple.txt")
