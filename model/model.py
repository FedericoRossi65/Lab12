import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._nodes = None

        self._rifugi = {}
        for r in DAO.get_rifugio():
            self._rifugi[r.id] = r #id --> Nome

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # 1. Pulizia: Se il grafo esiste già, lo svuoto
        self.G.clear()
        self._nodes = set()


        # 2. Recupero tutti i rifugi (nodi) dal DB
        all_rifugi = DAO.get_rifugio()

        # 3. Aggiungo i nodi al grafo
        for rifugio in all_rifugi:
            # Salvo nella mappa per recuperare l'oggetto dato l'ID
            self._nodes.add(rifugio.nome)
            # Aggiungo il nodo al grafo (passo l'intero oggetto)
            self.G.add_node(rifugio)

        # 4. Recupero tutte le tratte (archi potenziali)
        all_connessioni = DAO.get_connesione()

        # 5. Aggiungo gli archi
        peso = None
        for c in all_connessioni:
            # Controllo che entrambi i rifugi esistano (sicurezza)
            if c.anno <= int(year):#condizione per aggiungere i nodi
                r1 = c.r1
                r2 = c.r2

                if r1 in self._rifugi and r2 in self._rifugi:
                    u = self._rifugi[r1]
                    v = self._rifugi[r2]
                    if c.difficolta == 'facile':
                        peso = float(c.distanza) * 1
                    elif c.difficolta == 'media':
                        peso = float(c.distanza) * 1.5
                    elif c.difficolta == 'difficile':
                        peso = float(c.distanza) * 2


                    self.G.add_edge(u, v, weight=peso)

        # 6. PULIZIA DEL GRAFO
        # "I nodi rappresentano i rifugi collegati da almeno un sentiero fino all'anno selezionato."
        # Questo significa rimuovere i nodi con grado 0.
        # Copia dei nodi da rimuovere
        nodi_isolati = [node for node in self.G.nodes() if self.G.degree(node) == 0]
        self.G.remove_nodes_from(nodi_isolati)

        # Aggiorno la lista interna dei nodi attivi
        self._nodes = set(self.G.nodes())




    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        all_weight = [s[2]['weight'] for s in self.G.edges(data= True)]
        min_weight = min(all_weight)
        max_weight = max(all_weight)
        return min_weight, max_weight



    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        minori = []
        maggiori = []
        all_edges = self.G.edges(data= True)
        for edge in all_edges:
            if edge[2]['weight'] < soglia:
                minori.append(edge)
            elif edge[2]['weight'] > soglia:
                maggiori.append(edge)
        return len(minori), len(maggiori)



    """Implementare la parte di ricerca del cammino minimo"""
    def get_minimo_cammino_bfs(self,S):
        # creazione di un grafo 'temporaneo' con solo i archi e nodi che rispettano la soglia
        Gf = nx.Graph()
        Gf.add_nodes_from(self.G.nodes(data=True))

        for u, v, data in self.G.edges(data=True):
            if data["weight"] > S:
                Gf.add_edge(u, v, weight=data["weight"])
        miglior_cammino = None
        miglior_peso = float("inf")  # peso iniziale molto grande

        # provo tutte le possibili coppie di nodi (nodo_partenza, nodo_arrivo)
        for nodo_partenza in Gf.nodes:
            for nodo_arrivo in Gf.nodes:
                if nodo_partenza == nodo_arrivo:
                    continue  # non considero cammini dallo stesso nodo a se stesso

                try:
                    # calcolo il cammino minimo tra partenza e arrivo
                    cammino = nx.dijkstra_path(
                        Gf,
                        nodo_partenza,
                        nodo_arrivo,
                        weight="weight"
                    )

                    # controllo che il cammino abbia almeno 3 nodi --> 2 archi
                    if len(cammino) < 3:
                        continue

                    # calcolo il peso totale del cammino
                    peso = nx.path_weight(Gf, cammino, weight="weight")

                    # se è il migliore finora, lo salvo
                    if peso < miglior_peso:
                        miglior_peso = peso
                        miglior_cammino = cammino

                except nx.NetworkXNoPath:
                    # non esiste un cammino valido tra questa coppia → ignoro
                    pass
        coppie = []
        for i in range(len(miglior_cammino) - 1):
                u = miglior_cammino[i]
                v = miglior_cammino[i+1]
                coppie.append([{'id': u.id, 'nome': u.nome, 'localita': u.localita},
                              {'id':v.id,'nome':v.nome,'localita':v.localita}])


        return coppie





