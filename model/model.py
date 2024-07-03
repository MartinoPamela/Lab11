import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._listYears = DAO.getYears()
        self._listColors = DAO.getColors()
        self._grafo = nx.Graph()
        self._idMap = {}
        self._solBest = []

    def buildGraph(self, color, anno):
        nodes = DAO.getAllNodes(color)
        self._grafo.add_nodes_from(nodes)
        for n in nodes:
            self._idMap[n._Product_number] = n

        for a in nodes:
            for b in nodes:
                if a != b:
                    peso = DAO.getAllEdges(a, b, anno)
                    if peso[0] > 0:
                        self._grafo.add_edge(a, b, weight=peso[0])

    def bestPath(self, v0):

        self._solBest = []
        parziale = []
        self.ricorsione(parziale, v0, 0)
        print("finale", len(self._solBest), [i[2]["weight"] for i in self._solBest])

    def ricorsione(self, parziale, nodoLast, livello):
        archiViciniAmmissibili = self.getArchiViciniAmm(nodoLast, parziale)

        if len(archiViciniAmmissibili) == 0:
            if len(parziale) > len(self._solBest):
                self._solBest = list(parziale)
                print(len(self._solBest), [ii[2]["weight"] for ii in self._solBest])

        for a in archiViciniAmmissibili:
            parziale.append(a)
            self.ricorsione(parziale, a[1], livello + 1)
            parziale.pop()

    def getArchiViciniAmm(self, nodoLast, parziale):
        archiVicini = self._grafo.edges(nodoLast, data=True)
        result = []
        for a1 in archiVicini:
            if self.isAscendent(a1, parziale) and self.isNovel(a1, parziale):
                result.append(a1)
        return result

    def isAscendent(self, e, parziale):
        if len(parziale) == 0:
            print("parziale is empty in isAscendent")
            return True
        return e[2]["weight"] >= parziale[-1][2]["weight"]

    def isNovel(self, e, parziale):
        if len(parziale) == 0:
            print("parziale is empty in isNovel")
            return True
        e_inv = (e[1], e[0], e[2])
        return (e_inv not in parziale) and (e not in parziale)

    def get_sorted_edges(self):
        return sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)

    def getYears(self):
        return self._listYears

    def getColors(self):
        return self._listColors

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def get_nodes(self):
        return self._grafo.nodes()

    def getObjFromId(self, idOggetto):
        return self._idMap[idOggetto]
