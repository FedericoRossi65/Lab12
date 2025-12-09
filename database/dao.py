from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione import Connesione


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    @staticmethod
    def get_rifugio() -> list[Rifugio]|None:
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM rifugio"""
        try:
            cursor.execute(query)
            for row in cursor:
                rifugio = Rifugio(
                    id=row["id"],
                    nome=row["nome"],
                    localita=row["localita"],
                    altitudine=row["altitudine"],
                    capienza=row["capienza"],
                    aperto = row['aperto']

                )

                result.append(rifugio)
                print(rifugio)
        except Exception as e:
            print(f"Errore durante la query get_rifugio: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
    @staticmethod
    def get_connesione() -> list[Connesione] | None:
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT  LEAST(id_rifugio1,id_rifugio2) AS r1,
                            GREATEST(id_rifugio1,id_rifugio2) AS r2, 
                            anno,
                            distanza,
                            difficolta
                    FROM connessione
                    """

        try:
            cursor.execute(query)
            for row in cursor:
                connessione = Connesione(
                    r1=row['r1'],
                    r2 = row['r2'],
                    anno = row['anno'],
                    distanza = row['distanza'],
                    difficolta = row['difficolta']

                    )

                result.append(connessione)
                print(connessione)
        except Exception as e:
            print(f"Errore durante la query get_connessione: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
#l = DAO.get_rifugio()
#k = DAO.get_connesione()