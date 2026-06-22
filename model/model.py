import copy
import itertools
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idMapTeams = None
        self._bestPath = []
        self._bestObjVal = 0

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._teams =  DAO.getTeamsOfYear(year)
        self._idMapTeams = {t.ID: t for t in self._grafo.nodes}
        return self._teams

    def getVicini(self, source):
        vicini = self._grafo.neighbors(source)
        viciniTuples =[]
        for v in vicini:
            viciniTuples.append(self._grafo[source][v]["weight"])
        viciniTuples.sort(key=lambda x: x[1], reverse= True) #le ordino per peso dell arco
        return viciniTuples

    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)
        # for u in self._grafo.nodes: //DOPPIO LOOP, NON CONVIENE
        #     for v in self._grafo.nodes:
        #         if u!=v:
        #             self._grafo.add_edge(u, v)
        myedges = list(itertools.combinations(self._teams, 2))

        self._grafo.add_edges_from(myedges)
        mapSalary = DAO.getSalariesTeam(year, self._idMapTeams) #dizionario che ha per ogni team il suo salario
        for e in self._grafo.edges:
            sal1 = mapSalary[e[0]] #salario del 1 team dell'arco
            sal2 = mapSalary[e[1]]
            peso = sal1+sal2
            self._grafo[e[0]][e[1]]["weight"] = peso
            #potevo direttamente dire
           # self._grafo[e[1]][e[0]]["weight"] = mapSalary[e[0]] + mapSalary[e[1]]

    def getPath(self, v0):
        self._bestPath = []
        self._bestObjVal =0
        parziale = [v0]
        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self.ricorsione(parziale)
            parziale.pop()

    def getPath2(self, v0):
        self._bestPath = []
        self._bestObjVal = 0
        parziale = [v0]
        listaVicini = self.getVicini(parziale[-1])
        parziale.append(listaVicini[0][0])
        self.ricorsione2(parziale)
        parziale.pop()
        return self._bestPath and self._bestObjVal

    #VERSIONE 1, TROPPO LENTA
    def ricorsione(self, parziale):
        #verifico se la soluzione è migliore del best
        #verifico se ha senso continuare o no
        #verifico se posso aggiungere qualcosa
        #1) CONDIZIONE DI OTTIMALITA': verifica che parziale sia migliore del best
        if self._score(parziale) < self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        #2) CONDIZIONE DI TEMRINAZIONE : non ne ho nessuna specificata
        #3) PASSO DIRETTAMENTE ALLA RICORSIONE
        for v in self._grafo.neighbors(parziale[-1]):
            pesoE = self._grafo[parziale[-1]][v]["weight"]

            if self._grafo[parziale[-2]][parziale[-1]]["weight"]> pesoE and  v not in parziale:
                parziale.append(v)
                self.ricorsione(parziale)
                parziale.pop()

     #VERSIONE 2
    def ricorsione2(self, parziale):
        # 1) CONDIZIONE DI OTTIMALITA': verifica che parziale sia migliore del best
        if self._score(parziale) < self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        # 2) CONDIZIONE DI TEMRINAZIONE : non ne ho nessuna specificata
        # 3) PASSO DIRETTAMENTE ALLA RICORSIONE
        # listaVicini = []
        # for v in self._grafo.neighbors(parziale[-1]):
        #     edgeV = self._grafo[parziale[-1]][v]["weight"]
        #     listaVicini.append((v, edgeV))
        # listaVicini.sort(key=lambda x: x[1], reverse= True)
        listaVicini = self.getVicini(parziale[-1])
        for v in listaVicini:
            if v[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > v[1]:
                parziale.append(v[0])
                self.ricorsione2(parziale)
                parziale.pop()
                return

    def _score(self, parziale):
        '''gli arriva una lista di nodi, sono sicura che questa lista di nodi è connessa da archi,
        prendo il peso dell'arco e lo sommo a score'''
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return score


    def  getRandomNodes(self):
        index = random.randint(0,len(self._teams))
        return self._teams[index]

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)