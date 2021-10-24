


#                                   PROJET COMPLEX 2021 GROUPE 3
#                                       COUVERTURE DE GRAPHE
#                                   Almehdi KRISNI , Alessia LOI






#######################################################################################################
# LIBRAIRIES PYTHON
#######################################################################################################

import copy
import random
import networkx as nx
import matplotlib.pyplot as plt
import time
import datetime
import math



#######################################################################################################
# OUTILS
#######################################################################################################


# Méthode permettant d'obtenir une liste d'arêtes à partir d'un graphe G (utile pour la partie 3)
def aretesGrapheToList(G) :
    E = []
    for s1 in G.keys() :
        for s2 in G[s1] :
            if (s2,s1) not in E :
                E.append((s1,s2))
    return E

#------------------------------------------------------------------------------------------------------

# Méthode permettant d'acquérir un graphe G (modelisation : dictionnaire) depuis un fichier texte
def acquisitionGraphe(nomFichier):
    G = {}
    phase = 0
    with open(nomFichier, 'r') as fichier:
        for ligne in fichier:
            if ligne.startswith('Nombre de sommets') or ligne.startswith('Nombre d aretes'):
                phase = 0
                continue
            if ligne.startswith('Sommets'):
                phase = 1
                continue
            if ligne.startswith('Aretes'):
                phase = 2
                continue
            
            if phase == 1:
                G[ligne.strip()] = []
            if phase == 2:
                e = ligne.strip().split()
                if len(e) == 2:
                    (s1, s2) = e
                    G[s1].append(s2)
                    G[s2].append(s1)
                else :
                    print("Format de fichier invalide : chaque arete doit etre constituée de exactement 2 sommets")

    return G   

#------------------------------------------------------------------------------------------------------

# Méthode permettant d'afficher à l'écran un graphe non orienté et, éventuellement, un titre
def showGraphe(G, titre = "G"):
    newG = nx.Graph()
    newG.add_nodes_from(list(G.keys()))
    for v1 in G.keys() :
        for v2 in G.keys() :
            if (v2, v1) not in newG.edges and v2 in G[v1]:
                newG.add_edge(v1, v2)

    plt.title(titre)
    nx.draw(newG, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.circular_layout(G))

    plt.show()   

#------------------------------------------------------------------------------------------------------

# Méthode permettant d'afficher un graphique de comparaison des performances ("temps de calcul" et "qualité des Solutions") de l'algorithme choisi
def plotPerformances(p, nbIterations, secondesMaxAutorises, mode, verbose = False, save = False):
    """ p : la probabilité qu'une arete entre 2 sommets soit crée, p E ]0,1[
        nbIterations : nombre d'éxecutions de l'algorithme, dans le but d'en déduir une performance moyenne
        secondesMaxAutorises : temps maximum autorisé pour l'éxecution de l'algorithme
        nbNoeuds : nombre de nodes allant etre créées au maximum dans le graphe
        mode : valeur déterminant l'algorithme allant etre utilisé
        verbose : "True" pour afficher le détail des itérations
        save : "True" pour enregistrer le tracé en format jpg
    """

    # Calcul de la taille nMaxAGlouton pour l'algorithme (G)
    # nMax : taille jusqu'à laquelle l'algorithme tourne rapidement, i.e temps G(nMax,p) < secondesMaxAutorises
    nMax = 0
    t = 0
    while t < secondesMaxAutorises :
        nMax += 1
        
        # Méthode permettant de générer des graphes aléatoires
        G = randomGraphe(nMax, p)

        t1 = time.time()

        # Selection du mode (algorithme allant etre utilisé)
        if (mode == 1) :
            res = algoCouplage(G)
        elif (mode == 2) :
            res = algoGlouton(G)
        elif (mode == 3) :
            res = branchement(G)
        elif (mode == 4) :
            res = branchementBornesCouplage(G)
        elif (mode == 5) :
            res = branchementOptimiseCouplage(G)
        elif (mode == 6) :
            res = branchementOptimiseCouplage_uDegreMax(G)
        else :
            print("Aucun mode ne correspond à la valeur passée en paramètre. Veuillez choisir une autre valeur de mode.")
            return

        t2 = time.time()
        t = t2-t1

    if verbose :
        print("nMax = ", nMax, "\n")

    y1 = []  # axe des ordonnées : liste des temps de calcul moyen, pour l'algorithme sélectionné(G)
    y2 = []  # axe des ordonnées : liste des tailles des couplages (nombre de sommets) moyen, pour l'algorithme sélectionné(G)
    x = []   # axe des abscisses : liste de "nombre de sommets" {1/10 nbIterations, 2/10 nbIterations, ... , nbIterations}
    
    # Pour chaque 1/10 de nMax
    for i in range(1, 11) :

        tabTemps = []
        moyTemps = 0
        resAlgo = []
        moyQualiteSolutions = 0

        # Pour chacune des nbIterations démandées en paramètre
        for ite in range(nbIterations):

            # Méthode permettant de générer des graphes aléatoires
            G = randomGraphe(int(nMax * (i / 10)), p)

            # Execution et recueil statistiques de l'algorithme (G)
            t1 = time.time()
            
            # Selection du mode (algorithme allant etre utilisé)
            if (mode == 1) :
                res = algoCouplage(G)
            elif (mode == 2) :
                res = algoGlouton(G)
            elif (mode == 3) :
                res = branchement(G)
            elif (mode == 4) :
                res = branchementBornesCouplage(G)
            elif (mode == 5) :
                res = branchementOptimiseCouplage(G)
            elif (mode == 6) :
                res = branchementOptimiseCouplage_uDegreMax(G)
            else :
                print("Aucun mode ne correspond à la valeur passée en paramètre. Veuillez choisir une autre valeur de mode.")
                return

            t2 = time.time()
            t = t2-t1

            tabTemps.append(t) # temps de calcul de l'algorithme pour l'itération courante
            resAlgo.append(len(res)) # qualité des solutions pour l'itération courante

            if verbose : 
                print("x = ", i, "/10 nMax, iteration n.", ite+1, ":", "\n\t\ttabTemps =", tabTemps, "\n\t\tresAlgo =", resAlgo, "\n")

        # Calcul et stockage du temps d'execution moyen et de la qualité des solutions moyenne par rapport aux 'nbIterations' éxecutions
        moyTemps = sum(tabTemps)/len(tabTemps)
        moyQualiteSolutions = int(sum(resAlgo)/len(resAlgo))

        y1.append(moyTemps)
        y2.append(moyQualiteSolutions)
        x.append(int(nMax * (i / 10)))

        if verbose : 
            print("\nx = ", i, "/10 nMax (" + str(int(nbIterations * i/10)) + ") : moyTemps =", moyTemps, "moyQualiteSolutions =", moyQualiteSolutions)
            print("----------------------------------------------------------------------------------------------\n")

    # Selection du nom de l'algorithme
    if (mode == 1) :
        nomAlgo = "algo_Couplage"
    elif (mode == 2) :
        nomAlgo = "algo_Glouton"
    elif (mode == 3) :
        nomAlgo = "branchement"
    elif (mode == 4) :
        nomAlgo = "branchement_Bornes_Couplage"
    elif (mode == 5) :
        nomAlgo = "branchement_Optimise_Couplage"
    elif (mode == 6) :
        nomAlgo = "branchement_Optimise_Couplage_uDegreMax"
    else :
        print("Aucun mode ne correspond à la valeur passée en paramètre. Veuillez choisir une autre valeur de mode.")
        return

    # Affichage graphique
    plt.figure(figsize = (10, 10))
    plt.suptitle("Performances de l'algorithme " + nomAlgo + " avec nMax =" + str(nMax) + " nodes dans le graphe\n", color = 'red', size = 15)
    plt.rc('xtick', labelsize=10)    # fontsize of the tick labels

    # Construction et affichage du tracé "temps de calcul"
    plt.subplot(2, 1, 1)
    plt.title("Analyse du temps de calcul en fonction du nombre de sommets n")
    plt.xlabel("n") # nombre de sommets du graphe G
    plt.ylabel("t(n)") # temps de calcul en fonction du nombre de sommets du graphe G
    plt.plot(x, y1, color = 'blue')

    # Construction et affichage du tracé "qualité des solutions"
    plt.subplot(2, 1, 2)
    plt.title("Analyse de la qualité des solutions en fonction du nombre de sommets n")
    plt.xlabel("n") # nombre de sommets du graphe G
    plt.ylabel("q(n)") # qualité des solutions (taille du couplage) en fonction du nombre de sommets du graphe G
    plt.plot(x, y2, color = 'green')

    # Sauvegarde du tracé
    if (save) :
        plt.savefig("TestResults/" + nomAlgo + "_" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)

    plt.show()




#######################################################################################################
# METHODES PARTIE 2
#######################################################################################################

# Méthode permet de supprimer un sommet d'un graphe G et d'obtenir le graphe G' résultant de la suppression du sommet v
def suppSommet(initG, v) :
    if v not in initG.keys() :
        print("\nLe sommet", v, "n'est pas dans le graphe G : le graphe G'=G\{v} est équivalent à G.\n")
        return initG

    # On réalise une copie de initG pour ne pas le modifier
    G = copy.deepcopy(initG)

    # On retire le sommet v
    del G[v]

    # On retire les aretes liées au sommet v en créant une nouvelle liste de jointures
    for s in G.keys() :
        l = []
        for e in G[s] :
            if (e != v) :
                l.append(e)
        G[s] = l

    # On retire de G' les clés contenant des listes vides
    cleanG = []
    for k in G.keys() :
        if G[k] == []:
            cleanG.append(k)

    for s in cleanG:
        del G[s]
        
    # On retourne G'
    return G

#------------------------------------------------------------------------------------------------------

# Méthode permettant de supprimer plusieurs sommets à la fois d'un graphe G et d'obtenir le graphe G' résultant de la suppression des sommets
def multSuppSommet(G, ensv) :
    modifG = copy.deepcopy(G)

    for v in ensv :
        modifG = suppSommet(modifG, v)

    return modifG

#------------------------------------------------------------------------------------------------------

# Méthode renvoyant un tableau (dictionnaire) contenant les degres de chaque sommet du graphe G
def degresSommet(G) :

    # Création d'un dictionnaire 'tab' contenant les degres de chaque sommet du graphe G
    tab = dict()
    for v in G.keys() :
        tab[v] = len(list(G[v]))

    return tab

#------------------------------------------------------------------------------------------------------

# Méthode permettant de retourner le sommet ayant le degre maximal dans le graphe G
def sommetDegresMax(G) :
    deg = degresSommet(G) # deg est un dictionnaire { nbSommet : sommetsAdjacents }
    degres = list(deg.values())
    v = list(deg.keys())
    return v[degres.index(max(degres))]

#------------------------------------------------------------------------------------------------------

# Méthode permettant de retourner le degre du sommet ayant le degre maximum dans le graphe G
def valeurDegresMax(G) :
    deg = degresSommet(G) # deg est un dictionnaire { nbSommet : sommetsAdjacents }
    degres = list(deg.values())
    return max(degres)

#------------------------------------------------------------------------------------------------------

# Méthode permettant de générer des graphes aléatoires
def randomGraphe(n, p) :
    """ n : nombre de sommets, n > 0
        p : la probabilité qu'une arete entre 2 sommet soit créée, p E ]0,1[
    """
    if n < 1 :
        print("Il faut que n soit supérieur ou égal à 1 (n = nombre de sommets).\n")
        return ([],[])

    # Création du graphe
    G = dict()

    # Creation de la liste des sommets
    for i in range(n) :
        G[i] = []
    
    # Creation de la liste des aretes, ajoutées au graphe G suivant une probabilité p de présence
    for v1 in G.keys() :
        for v2 in G.keys() :
            if v1 != v2 :
                if random.uniform(0,1) < p :
                    if (v2 not in G[v1]) and (v1 not in G[v2]) :
                        G[v1].append(v2)
                        G[v2].append(v1)
    
    # On organise les listes de sommets adjacents pour faciliter la lecture
    for s in G :
        G[s].sort()

    return G





#######################################################################################################
# METHODES PARTIE 3
#######################################################################################################

# Couplage = ensemble d'arêtes n'ayant pas d'extrémité en commun

# Méthode representant l'algorithme de couplage sur le graphe G
def algoCouplage(G) :
    C = list()  # C = liste de sommets représentant le couplage

    for s1 in list(G.keys()) :
        for s2 in list(G[s1]) :
            if (s1 not in C) and (s2 not in C) :
                C.append(s1)
                C.append(s2)
                break

    return C

#------------------------------------------------------------------------------------------------------

# Méthode représentant l'algorithme glouton de couplage sur le graphe G
def algoGlouton(G) :
    C = []  # C = liste de sommets représentant le couplage

    # On réalise une copie de G afin de ne pas modifier l'original
    copyG = copy.deepcopy(G)
    E = aretesGrapheToList(copyG) # Liste des arêtes du graphe G

    while E != [] :

        # On determine le sommet de degrès maximal et on le supprime du graphe
        v = sommetDegresMax(copyG)
        copyG = suppSommet(copyG, v)

        # On ajoute le sommet à la couverture
        C.append(v)

        # On supprime les arêtes couvertes par le sommet v
        E = [e for e in E if v not in e]

    return C



#######################################################################################################
# METHODES PARTIE 4
#######################################################################################################

# Méthode réalisant le branchement de manière impartiale (sans indice)
def branchement(G, randomSelection=False, verbose=False) :
    nbNoeudsGeneres = 1 # nombre de noeuds générés
    optiC = None # optiC = ensemble de sommets représentant la solution optimale (on cherche à minimiser la taille de la couverture)

    if (aretesGrapheToList(G) != []) :
        areteInitiale = aretesGrapheToList(G)[0] # On récupère la première arete du graphe si elle existe
    else :
        return [n for n in G.keys()] # Sinon on renvoie l'ensemble des nodes de G

    # Un état est de la forme [ Couverture C actuelle, Dictionnaire de graphe G ]
    statesToStudy = [] # Pile des états du branchement à étudier
    statesToStudy.append([[areteInitiale[0]], suppSommet(G, areteInitiale[0])])
    statesToStudy.append([[areteInitiale[1]], suppSommet(G, areteInitiale[1])])

    # Début de l'algorithme de branchement
    while (statesToStudy != []) :

        # Choix de la méthode de sélection d'état
        if (randomSelection) :
            # On récupère un état aléatoire de la liste d'états à étudier
            state = statesToStudy.pop(random.randint(0, len(statesToStudy) - 1))
        else :
            # On récupère la tete de la pile et on la supprime de statesToStudy
            state = statesToStudy.pop(0)

        # Cas où G (state[1]) est un graphe sans aretes
        if (aretesGrapheToList(state[1]) == []) :
            if (optiC == None) or (len(state[0]) < len(optiC)) :
                optiC = state[0]

        # Cas où G (state[1]) n'est pas un graphe sans aretes
        else :
            # On récupère une arete aléatoire
            areteEtude = aretesGrapheToList(state[1])[0] # On récupère la première arete du graphe
            leftNode = areteEtude[0]
            rightNode = areteEtude[1]
            nbNoeudsGeneres += 1

            # On ajoute deux feuilles à la liste (on priorise le fils de gauche, soit le premier élément de l'arete étudiée)
            statesToStudy.insert(0, [state[0] + [rightNode], suppSommet(state[1], rightNode)])
            statesToStudy.insert(0, [state[0] + [leftNode], suppSommet(state[1], leftNode)])
        
    if (verbose) :
        print("Nombre de noeuds générés avec la méthode 'branchement' :", nbNoeudsGeneres)

    # On retourne la meilleure couverture trouvée
    return optiC

#------------------------------------------------------------------------------------------------------

# Méthode permettant de calculer le max parmi les bornes b1, b2 et b3
def calculBorneInf(G, verbose=False) :
    b1 = 0 # Partie entière supérieure de m / delta (m = nombre aretes de G, delta = degrès maximum sommets du graphe)
    b2 = 0 # Cardinalité de M (M un couplage de G)
    b3 = 0 # Formule
    l = []

    # Calcul de M
    M = algoCouplage(G) # M est un couplage de G
    C = branchement(G, randomSelection=False) # C est une couverture de G

    # Calcul de n, m et c
    n = len(list(G.keys())) # nombre de sommets
    m = len(aretesGrapheToList(G)) # nombre d'aretes
    c = len(C) # cardinalite de la couverture minimale

    # Calcul de b1
    b1 = math.ceil(m / valeurDegresMax(G)) # Partie entière superieure de (m / valeurDegresMax)
    l.append(b1)

    # Calcul de b2
    b2 = (len(M) / 2)
    l.append(b2)
    
    # Calcul de b3
    b3 = (2*n-1-(math.sqrt( ((2*n-1)**2)-8*m) ))/2
    l.append(b3)
    
    # Valeur maximale entre les bi
    maxB = max(l)
    if (verbose) :
        print("b1 =", b1, "\nb2 =", b2, "\nb3 =", b3, "\n|C| =", c, "\n|C| >= max{b1,b2,b3} :\t", c, ">=", maxB)

    # On retourne la valeur maximale
    return maxB

#------------------------------------------------------------------------------------------------------

# Fonction réalisant le branchement2, qui insère le calcul en chaque noeud d'une solution réalisable et le calcul d'une borne inférieure
def branchementBornesCouplage(G, verbose=False) :
    nbNoeudsGeneres = 1 # nombre de noeuds générés

    if G == {} :
        return "Le graphe est vide, C = {}"

    # On calcule la borne inférieure et la borne supérieure pour la racine
    rootBorneInf = calculBorneInf(G)
    rootBorneSup = len(algoCouplage(G))

    # Dans le cas où les deux bornes sont égales, on retourne immédiatement la solution
    if (rootBorneInf >= rootBorneSup) :
        return algoCouplage(G)

    # optiC = ensemble de sommets représentant la solution optimale (on cherche à minimiser la taille de la couverture)
    optiC = algoCouplage(G)
    # print("optic =", optiC)

    #  On récupère la première arete du graphe
    areteInitiale = aretesGrapheToList(G)[0]
    # print("on choisit l'arete initiale", areteInitiale)

    # Un état est de la forme [ Couverture C actuelle, Dictionnaire de graphe G , Borne Inf , Borne Sup]
    statesToStudy = list() # Pile des états du branchement à étudier

    # CONDITION POUR ELAGUER : (BORNE SUP < BORNE INF) ou (BORNE INF > TAILLE OPTI_C)
    # CONDITIONS DE REUSSITE : (BORNE SUP >= BORNE INF) ou (BORNE INF <= TAILLE OPTI_C)

    # Création des informations du noeud de droite
    newGraphe = copy.deepcopy(G)
    newGraphe = suppSommet(newGraphe, areteInitiale[1])
    
    if not (newGraphe == {}):
        newBorneInf = calculBorneInf(newGraphe) + 1
        newBorneSup = len(algoCouplage(newGraphe))
    else :
        newBorneInf = None
        newBorneSup = None
    # print("niveau node droite I : arete =", areteInitiale, "v =", areteInitiale[1], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

    if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
        statesToStudy.insert(0, [[areteInitiale[1]], newGraphe, newBorneInf, newBorneSup])
        # print("on ajoute ce noeud droit")

    # Création des informations du noeud de gauche
    newGraphe = copy.deepcopy(G)
    newGraphe = suppSommet(newGraphe, areteInitiale[0])

    if not (newGraphe == {}):
        newBorneInf = calculBorneInf(newGraphe) + 1
        newBorneSup = len(algoCouplage(newGraphe))
    else :
        newBorneInf = None
        newBorneSup = None
    # print("niveau node gauche I : arete =", areteInitiale, "u =", areteInitiale[0], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

    if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
        statesToStudy.insert(0, [[areteInitiale[0]], newGraphe, newBorneInf, newBorneSup])
        # print("on ajoute ce noeud gauche")


    # Début de l'algorithme de branchement
    i = 0    
    while (len(statesToStudy) != 0) :
        i+=1
        # print("\niteration n.", i)

        # On récupère la tete de la pile et on la supprime de statesToStudy
        state = statesToStudy.pop(0)

        # Cas où G (state[1]) est un graphe sans aretes
        if (aretesGrapheToList(state[1]) == []) :
            if (optiC == None) or (len(state[0]) < len(optiC)) :
                optiC = state[0]
                # print(">>> c est une feuille, plus d aretes dans E, optiC =", optiC)

        # Cas où G (state[1]) n'est pas un graphe sans aretes
        else :

            # print(">>> G it.", i, ":", state[1] )

            # On récupère la première arete du branchement
            areteEtude = aretesGrapheToList(state[1])[0] # On récupère la première arete du graphe
            # print("areteEtude", areteEtude)

            # Calcul des informations du noeud de droite
            newGraphe = copy.deepcopy(state[1])
            newGraphe = suppSommet(newGraphe, areteEtude[1])
 
            if not (newGraphe == {}):
                newBorneInf = calculBorneInf(newGraphe)
                newBorneSup = len(algoCouplage(newGraphe))
            else :
                newBorneInf = None
                newBorneSup = None
            # print("niveau node droite it.", i, ": arete =", areteEtude, "v =", areteEtude[1], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

            if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
                statesToStudy.insert(0, [state[0] + [areteEtude[1]], newGraphe, newBorneInf, newBorneSup])
                nbNoeudsGeneres += 1
                # print("on ajoute ce noeud droit")

            # Calcul des informations du noeud de gauche
            newGraphe = copy.deepcopy(state[1])
            newGraphe = suppSommet(newGraphe, areteEtude[0])

            if not (newGraphe == {}):
                newBorneInf = calculBorneInf(newGraphe)
                newBorneSup = len(algoCouplage(newGraphe))
            else :
                newBorneInf = None
                newBorneSup = None
            # print("niveau node gauche it.", i, ": arete =", areteEtude, "u =", areteEtude[0], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

            if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
                statesToStudy.insert(0, [state[0] + [areteEtude[0]], newGraphe, newBorneInf, newBorneSup])
                nbNoeudsGeneres += 1
                # print("on ajoute ce noeud gauche")


    if (verbose) :
        print("Nombre de noeuds générés avec la méthode 'branchement2' :", nbNoeudsGeneres)

    # On retourne C
    return optiC

#------------------------------------------------------------------------------------------------------

# Fonction réalisant le branchement2, qui insère le calcul en chaque noeud d'une solution réalisable et le calcul d'une borne inférieure
def branchementOptimiseCouplage(G, verbose=False) :
    nbNoeudsGeneres = 1 # nombre de noeuds générés

    if G == {} :
        return "Le graphe est vide, C = {}"

    # On calcule la borne inférieure et la borne supérieure pour la racine
    rootBorneInf = calculBorneInf(G)
    rootBorneSup = len(algoCouplage(G))

    # Dans le cas où les deux bornes sont égales, on retourne immédiatement la solution
    if (rootBorneInf >= rootBorneSup) :
        return algoCouplage(G)

    # optiC = ensemble de sommets représentant la solution optimale (on cherche à minimiser la taille de la couverture)
    optiC = algoCouplage(G)
    print("optic =", optiC)

    #  On récupère la première arete du graphe
    areteInitiale = aretesGrapheToList(G)[0]
    print("on choisit l'arete initiale", areteInitiale)

    # Un état est de la forme [ Couverture C actuelle, Dictionnaire de graphe G , Borne Inf , Borne Sup]
    statesToStudy = list() # Pile des états du branchement à étudier

    # CONDITION POUR ELAGUER : (BORNE SUP < BORNE INF) ou (BORNE INF > TAILLE OPTI_C)
    # CONDITIONS DE REUSSITE : (BORNE SUP >= BORNE INF) ou (BORNE INF <= TAILLE OPTI_C)

    # Création des informations du noeud de droite
    newGraphe = copy.deepcopy(G)

    voisinsU = newGraphe[areteInitiale[0]]
    print("voisinsU", voisinsU)

    newGraphe = suppSommet(newGraphe, areteInitiale[0])
    for s in voisinsU:
        newGraphe = suppSommet(newGraphe, s)
    
    if not (newGraphe == {}):
        newBorneInf = calculBorneInf(newGraphe) + 1
        newBorneSup = len(algoCouplage(newGraphe))
    else :
        newBorneInf = None
        newBorneSup = None
    print("niveau node droite I : arete =", areteInitiale, "v =", areteInitiale[1], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

    if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
        statesToStudy.insert(0, [[areteInitiale[1]] + voisinsU, newGraphe, newBorneInf, newBorneSup])
        print("on ajoute ce noeud droit, c =", statesToStudy[0][0])

    # Création des informations du noeud de gauche
    newGraphe = copy.deepcopy(G)
    newGraphe = suppSommet(newGraphe, areteInitiale[0])

    if not (newGraphe == {}):
        newBorneInf = calculBorneInf(newGraphe) + 1
        newBorneSup = len(algoCouplage(newGraphe))
    else :
        newBorneInf = None
        newBorneSup = None
    print("niveau node gauche I : arete =", areteInitiale, "u =", areteInitiale[0], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

    if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
        statesToStudy.insert(0, [[areteInitiale[0]], newGraphe, newBorneInf, newBorneSup])
        print("on ajoute ce noeud gauche")


    # Début de l'algorithme de branchement
    i = 0    
    while (len(statesToStudy) != 0) :
        i+=1
        print("\niteration n.", i)

        # On récupère la tete de la pile et on la supprime de statesToStudy
        state = statesToStudy.pop(0)

        # Cas où G (state[1]) est un graphe sans aretes
        if (aretesGrapheToList(state[1]) == []) :
            if (optiC == None) or (len(state[0]) < len(optiC)) :
                optiC = state[0]
                print(">>> c est une feuille, plus d aretes dans E, optiC =", optiC)

        # Cas où G (state[1]) n'est pas un graphe sans aretes
        else :

            print(">>> G it.", i, ":", state[1] )

            # On récupère la première arete du branchement
            areteEtude = aretesGrapheToList(state[1])[0] # On récupère la première arete du graphe
            print("areteEtude", areteEtude)

            # Calcul des informations du noeud de droite
            newGraphe = copy.deepcopy(state[1])
            voisinsU = newGraphe[areteEtude[0]]

            for s in voisinsU:
                newGraphe = suppSommet(newGraphe, s)

            if not (newGraphe == {}):
                newBorneInf = calculBorneInf(newGraphe)
                newBorneSup = len(algoCouplage(newGraphe))
            else :
                newBorneInf = None
                newBorneSup = None
            print("niveau node droite it.", i, ": arete =", areteEtude, "v =", areteEtude[1], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

            if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
                statesToStudy.insert(0, [[state[0] + [areteEtude[1]] + voisinsU], newGraphe, newBorneInf, newBorneSup])
                nbNoeudsGeneres += 1
                print("on ajoute ce noeud droit")

            # Calcul des informations du noeud de gauche
            newGraphe = copy.deepcopy(state[1])
            newGraphe = suppSommet(newGraphe, areteEtude[0])

            if not (newGraphe == {}):
                newBorneInf = calculBorneInf(newGraphe)
                newBorneSup = len(algoCouplage(newGraphe))
            else :
                newBorneInf = None
                newBorneSup = None
            print("niveau node gauche it.", i, ": arete =", areteEtude, "u =", areteEtude[0], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

            if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
                statesToStudy.insert(0, [state[0] + [areteEtude[0]], newGraphe, newBorneInf, newBorneSup])
                nbNoeudsGeneres += 1
                print("on ajoute ce noeud gauche")


    if (verbose) :
        print("Nombre de noeuds générés avec la méthode 'branchementBornesCouplage' :", nbNoeudsGeneres)

    # On retourne C
    return optiC

#------------------------------------------------------------------------------------------------------

# Fonction réalisant le branchement2, qui insère le calcul en chaque noeud d'une solution réalisable et le calcul d'une borne inférieure
def branchementOptimiseCouplage_uDegreMax(G, verbose=False) :
    nbNoeudsGeneres = 1 # nombre de noeuds générés

    if G == {} :
        return "Le graphe est vide, C = {}"

    # On calcule la borne inférieure et la borne supérieure pour la racine
    rootBorneInf = calculBorneInf(G)
    rootBorneSup = len(algoCouplage(G))

    # Dans le cas où les deux bornes sont égales, on retourne immédiatement la solution
    if (rootBorneInf >= rootBorneSup) :
        return algoCouplage(G)

    # optiC = ensemble de sommets représentant la solution optimale (on cherche à minimiser la taille de la couverture)
    optiC = algoCouplage(G)
    print("optic =", optiC)

    #  On récupère la premiere arete du graphe
    uDegreMax = sommetDegresMax(G)
    Gprime = {}
    Gprime[uDegreMax] = G[uDegreMax]
    areteInitiale = aretesGrapheToList(Gprime)[0]
    print("on choisit l'arete initiale", areteInitiale)

    # Un état est de la forme [ Couverture C actuelle, Dictionnaire de graphe G , Borne Inf , Borne Sup]
    statesToStudy = list() # Pile des états du branchement à étudier

    # CONDITION POUR ELAGUER : (BORNE SUP < BORNE INF) ou (BORNE INF > TAILLE OPTI_C)
    # CONDITIONS DE REUSSITE : (BORNE SUP >= BORNE INF) ou (BORNE INF <= TAILLE OPTI_C)

    # Création des informations du noeud de droite
    newGraphe = copy.deepcopy(G)
    print("G init :", newGraphe)
    newGraphe = suppSommet(newGraphe, areteInitiale[1])
    print("G modif1 :", newGraphe)

    if not newGraphe == {}:
        voisinsU = newGraphe[areteInitiale[0]]
        print("voisinsU", voisinsU)
        for s in voisinsU:
            print("on enleve le voisin de u ", s)
            if s in newGraphe:
                newGraphe = suppSommet(newGraphe, s)
    else :
        voisinsU = None

    if not (newGraphe == {}):
        newBorneInf = calculBorneInf(newGraphe) + 1
        newBorneSup = len(algoCouplage(newGraphe))
    else :
        newBorneInf = None
        newBorneSup = None
    print("niveau node droite I : arete =", areteInitiale, "v =", areteInitiale[1], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

    if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
        if voisinsU != None:
            statesToStudy.insert(0, [[[areteInitiale[1]] + voisinsU], newGraphe, newBorneInf, newBorneSup])
        else:
            statesToStudy.insert(0, [[areteInitiale[1]], newGraphe, newBorneInf, newBorneSup])
        print("on ajoute ce noeud droit, c =", statesToStudy[0][0])


    # Création des informations du noeud de gauche
    newGraphe = copy.deepcopy(G)
    newGraphe = suppSommet(newGraphe, areteInitiale[0])

    if not (newGraphe == {}):
        newBorneInf = calculBorneInf(newGraphe) + 1
        newBorneSup = len(algoCouplage(newGraphe))
    else :
        newBorneInf = None
        newBorneSup = None
    print("niveau node gauche I : arete =", areteInitiale, "u =", areteInitiale[0], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

    if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
        statesToStudy.insert(0, [[areteInitiale[0]], newGraphe, newBorneInf, newBorneSup])
        print("on ajoute ce noeud gauche")


    # Début de l'algorithme de branchement
    i = 0    
    while (len(statesToStudy) != 0) :
        i+=1
        print("\niteration n.", i)

        # On récupère la tete de la pile et on la supprime de statesToStudy
        state = statesToStudy.pop(0)

        # Cas où G (state[1]) est un graphe sans aretes
        if (aretesGrapheToList(state[1]) == []) :
            if (optiC == None) or (len(state[0]) < len(optiC)) :
                optiC = state[0]
                print(">>> c est une feuille, plus d aretes dans E, optiC =", optiC)

        # Cas où G (state[1]) n'est pas un graphe sans aretes
        else :

            print(">>> G it.", i, ":", state[1] )

            # On récupère la première arete du branchement
            uDegreMax = sommetDegresMax(state[1])
            Gprime = {}
            Gprime[uDegreMax] = (state[1])[uDegreMax]
            areteEtude = aretesGrapheToList(Gprime)[0] # On récupère la  arete du graphe avec max d
            print("areteEtude", areteEtude)

            # Calcul des informations du noeud de droite
            newGraphe = copy.deepcopy(state[1])
            newGraphe = suppSommet(newGraphe, areteEtude[1])
            print("G modif sans v =", areteEtude[1], "G =", newGraphe)

            if not newGraphe == {}:
                voisinsU = newGraphe[areteEtude[0]]
                print("voisinsU", voisinsU)
                for s in voisinsU:
                    print("on enleve le voisin de u ", s)
                    if s in newGraphe:
                        newGraphe = suppSommet(newGraphe, s)
                print("G modif2 :", newGraphe)
            else :
                voisinsU = None
 
            if not (newGraphe == {}):
                newBorneInf = calculBorneInf(newGraphe) + 1
                newBorneSup = len(algoCouplage(newGraphe))
            else :
                newBorneInf = None
                newBorneSup = None
            print("niveau node droite I : arete =", areteEtude, "v =", areteEtude[1], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

            if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
                if voisinsU != None:
                    statesToStudy.insert(0, [[state[0] + [areteEtude[1]] + voisinsU], newGraphe, newBorneInf, newBorneSup])
                else:
                    statesToStudy.insert(0, [[state[0] + [areteEtude[1]]], newGraphe, newBorneInf, newBorneSup])
                print("on ajoute ce noeud droit, c =", statesToStudy[0][0])


            # Calcul des informations du noeud de gauche
            newGraphe = copy.deepcopy(state[1])
            newGraphe = suppSommet(newGraphe, areteEtude[0])

            if not (newGraphe == {}):
                newBorneInf = calculBorneInf(newGraphe)
                newBorneSup = len(algoCouplage(newGraphe))
            else :
                newBorneInf = None
                newBorneSup = None
            print("niveau node gauche it.", i, ": arete =", areteEtude, "u =", areteEtude[0], "newG =", newGraphe, "bornes Inf sup =", newBorneInf, newBorneSup )

            if (newBorneInf != None and not(newBorneSup < newBorneInf or newBorneInf > len(optiC))) :
                statesToStudy.insert(0, [state[0] + [areteEtude[0]], newGraphe, newBorneInf, newBorneSup])
                nbNoeudsGeneres += 1
                print("on ajoute ce noeud gauche")


    if (verbose) :
        print("Nombre de noeuds générés avec la méthode 'branchement2' :", nbNoeudsGeneres)

    # On retourne C
    return optiC

#######################################################################################################
# TESTS
#######################################################################################################

# Instanciation d'un graphe G (modelisation : dictionnaire)
# G = {0 : [1, 2, 3], 1 : [0, 2], 2 : [0, 1], 3 : [0]}
# showGraphe(convertGraph(G))

# Instanciation d'un graphe G (modelisation : librairie graphe networkx)
# V = [0, 1, 2, 3]
# E = [(0,1), (0,2), (0,3), (1,2)]

# G = nx.Graph()
# G.add_nodes_from(V) # sommets
# G.add_edges_from(E) # aretes
# showGraphe(G)

#------------------------------------------------------------------------------------------------------

# Test méthode suppSommet
# print("Graphe G\n", G, "\n")
# newG = suppSommet(G, 0)
# print("Graphe G'\n", newG, "\n")

#------------------------------------------------------------------------------------------------------

# Test méthode multSuppSommet
# newG = multSuppSommet(G, [0, 1])
# print("Graphe G'\n", newG, "\n")

#------------------------------------------------------------------------------------------------------

# Tests des méthodes degresSommet et sommetDegresSommet
# print(degresSommet(G))
# print(sommetDegresMax(G))

#------------------------------------------------------------------------------------------------------

# Tests sur la génération aléatoire de graphe
# randG = randomGraphe(8, 0.1)
# print("Graphe G\n", randG, "\n")
# showGraphe(convertGraph(randG))

#------------------------------------------------------------------------------------------------------

# Tests sur l'algorithme de couplage
# G = randomGraphe(8, 0.2)
# print(algoCouplage(G))
# print(aretesGrapheToList(G))
# showGraphe(convertGraph(G))

#------------------------------------------------------------------------------------------------------

# Tests sur l'algorithme de couplage glouton
# G = randomGraphe(20, 0.5)
# print(algoGlouton(G))
# showGraphe(convertGraph(G))

#------------------------------------------------------------------------------------------------------

# Tests de comparaison d'efficacité des 2 algorithmes

#------------------------------------------------------------------------------------------------------

# Test méthode acquisitionGraphe depuis un fichier texte
G = acquisitionGraphe("exempleinstance.txt")
print("G = ", G, "\n")
showGraphe(G)

#------------------------------------------------------------------------------------------------------

# Test méthodes plotPerformances sur Couplage et Glouton
# plotPerformances(0.3, 15, 0.01, 1, verbose=True, save=True)
# plotPerformances(0.3, 15, 0.01, 2, verbose=True, save=True)

#------------------------------------------------------------------------------------------------------

# Test sur la méthode de branchement
# print(branchement(acquisitionGraphe("exempleinstance.txt"), randomSelection=False))
# showGraphe(convertGraph(acquisitionGraphe("exempleinstance.txt")))

# print(valeurDegresMax(G))
# calculBornesInf(G)

#------------------------------------------------------------------------------------------------------

# Test méthodes plotPerformancesCouplage et plotPerformancesGlouton
# plotPerformances(0.2, 15, 0.01, 3, verbose=True, save=True)
# plotPerformances(0.5, 15, 0.01, 3, verbose=True, save=True)
# plotPerformances(0.9, 15, 0.01, 3, verbose=True, save=True)

#------------------------------------------------------------------------------------------------------

# Test sur la méthode de branchement utilisant les bornes et l'algorithme de couplage standart
# print(branchementBornesCouplage(acquisitionGraphe("exempleinstance.txt")))
# showGraphe(convertGraph(acquisitionGraphe("exempleinstance.txt")))
# print(valeurDegresMax(G))

#------------------------------------------------------------------------------------------------------

# Test sur la méthode de branchement utilisant les bornes et l'algorithme de couplage standart
# print(branchementOptimiseCouplage(acquisitionGraphe("exempleinstance.txt")))
#showGraphe(convertGraph(acquisitionGraphe("exempleinstance.txt")))

#------------------------------------------------------------------------------------------------------
# print("--------------------------------------------------------")
# Test sur la méthode de branchement utilisant les bornes et l'algorithme de couplage standart
# print(branchementOptimiseCouplage_uDegreMax(acquisitionGraphe("exempleinstance.txt")))
# showGraphe(convertGraph(acquisitionGraphe("exempleinstance.txt")))


#######################################################################################################
# EVALUATIONS
#######################################################################################################

# Dans cette partie, on s'occupe de l'évaluation des différents algorithmes
# Ces résultats seront présentés dans le rapport dans les parties désignées

# Méthode d'évaluation permettant de réaliser les tests
def evaluationAlgorithm(n, p, a) :
    # a = permet de choisir l'algorithme à utiliser

    # a = 1 - Test de branchement (4.1)
    if (a == 1) :
        print("EVALUATION - Algorithme : branchement (4.1).\nDébut de l'évaluation des performances pour :\nn =", n, "\tp =", p)
        testGraphe = randomGraphe(n,p)
        startTime = time.time()
        solution = branchement(testGraphe, verbose=True)
        endTime = time.time()
        execTime = endTime - startTime
        print("Temps d'exécution =", execTime, "secondes.\n")

    # a = 2 - Test de branchementBornesCouplage (4.2)
    elif (a == 2) :
        print("EVALUATION - Algorithme : branchementBornesCouplage (4.2).\nDébut de l'évaluation des performances pour :\nn =", n, "\tp =", p)
        testGraphe = randomGraphe(n,p)
        startTime = time.time()
        solution = branchementBornesCouplage(testGraphe, verbose=True)
        endTime = time.time()
        execTime = endTime - startTime
        print("Temps d'exécution =", execTime, "secondes.\n")

    # La valeur de a ne correspond à aucun algorithme
    else :
        print("EVALUATION - Aucun algorithme correspondant.\nVeuillez choisir une valeur de a différente.")

#------------------------------------------------------------------------------------------

# Evalutation de branchement (question 4.1)
# n = 20 # Il est recommandé de choisir une valeur de n divisible par d pour faciliter les calculs
# d = 20 # Facteur de division de la valeur de n (plus d est elevé, plus le nombre de tests est élevé)
# for i in range(d) :
#     numberOfNodes = (int)(n * ((i + 1) / d))
#     evaluationAlgorithm(numberOfNodes, 0.2, 1)