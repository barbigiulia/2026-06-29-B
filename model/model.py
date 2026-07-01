import networkx as nx

from database.DAO import DAO
from model.track import Track


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.MapAlbum = {}

    def fillAlbum(self):
        return list(self._grafo.nodes)

    def getAlbumById(self, albumId):
        for a in self._grafo.nodes:
            if str(a.AlbumId) == str(albumId):
                return a
        return None

    def buildGraph(self):
        self._grafo.clear()
        nodi = []
        for a in DAO.getNodes():
            nodi.append(a)
        self._grafo.add_nodes_from(nodi)
        lista = DAO.getListaBrani()
        brani = {}
        for a,t,g in lista:
            if a not in brani:
                brani[a] = []
            brani[a].append(Track(t, g))
        for a in nodi:
            for aID in brani:
                 if a.AlbumId == aID:
                     a.listaBrani = brani.get(aID, [])

        for a in self._grafo.nodes:
            if a.AlbumId not in self.MapAlbum:
                self.MapAlbum[a.AlbumId] = a
        self.addEdges_python()


    def addEdges_con_query(self):
        archi = DAO.getEdges()
        for a1, a2 in archi:
            self._grafo.add_edge(self.MapAlbum[a1], self.MapAlbum[a2])


    def addEdges_python(self):
        coppie = DAO.getEdges1() # (AlbumId, GenreId)
        # LA TRACCIA NON SERVE!!!
        generiPerAlbum = {}
        for albumId,genreId in coppie:
            if albumId not in generiPerAlbum:
                generiPerAlbum[albumId] = set()
            generiPerAlbum[albumId].add(genreId)

        nodi = list(self._grafo.nodes)
        for i in range(len(nodi)):
            for j in range(i + 1, len(nodi)):
                album1 = nodi[i]
                album2 = nodi[j]

                generi1 = generiPerAlbum.get(album1.AlbumId, set())
                generi2 = generiPerAlbum.get(album2.AlbumId, set())

                if len(generi1 & generi2) > 0:  # intersezione non vuota
                    self._grafo.add_edge(album1, album2)


    def compConnesse(self):
        num = nx.number_connected_components(self._grafo)
        res = []
        for c in list(nx.connected_components(self._grafo)):
            res.append((c,len(c)))
        res.sort(key=lambda x: x[1], reverse=True)

        # res[0] è gia la tupla
        return num, res[0]    # perchè ho usato list(nx.connected_components(self._grafo))

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

# ===========metodi utili per la ricorsione =======================
    def get_componente_Connessa(self, album):
        # TROVA LA COMPONENTE CONNESSA DI UN NODO
        componenti = list(nx.connected_components(self._grafo))
        for c in componenti:
            if album in c:
                return c
        return None

    def get_album_con_piu_brani(self, componente):
        # SE DEVO SCEGLIERE UN SOLO ALBUM DA UNA COMPONENTE, TANTO VALE
        # SCEGLIERE QUELLO CON PIU BRANI
        best= None
        maxBrani = -1
        for album in componente:
            if len(album.listaBrani) > maxBrani:
                maxBrani = len(album.listaBrani)
                best = album
        return best

    def getTotBrani(self, albums):
        tot = 0
        for a in albums:
            tot+= len(a.listaBrani)
        return tot


    # ==================== ricorsione =================================
    def trovaSelezione(self, nodoStart, n):
        if nodoStart not in self._grafo.nodes:
            return None, 0
        if n <= 0:
            return None, 0
        componenti = list(nx.connected_components(self._grafo))
        compStart =  self.get_componente_Connessa(nodoStart)
        componenti.remove(compStart) # non posso riusare la componente di partenza

        self._bestPath = []
        self._maxBrani = 0
        self._ricorsione([nodoStart], n , componenti)
        if len(self._bestPath) != n:
            return None, 0 # nessuna sequenza trovata
        return self._bestPath, self._maxBrani


    def _ricorsione(self, parziale, n, componentiRimanenti):
        # caso base: ho selezionato n album
        if len(parziale) == n:
            totale = self.getTotBrani(parziale)
            if totale > self._maxBrani:
                self._maxBrani = totale
                self._bestPath = list(parziale)
            return

        # pruning --> se anche prendendo un album da OGNI componente rimasta
        #             non arrivo a n, questo ramo è inutile -> taglio subito
        if not componentiRimanenti or n-len(parziale)>len(componentiRimanenti):
            return
        proxComponente = componentiRimanenti[0]

        # 1) non prendo nessun album da questa componente
        self._ricorsione(parziale, n, componentiRimanenti[1:])

        #2) prendo il miglior album di questa componente
        candidato = self.get_album_con_piu_brani(proxComponente)
        if candidato is not None:
            parziale.append(candidato)
            self._ricorsione(parziale, n, componentiRimanenti[1:])
            parziale.pop()