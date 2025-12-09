from dataclasses import dataclass
@dataclass
class Connesione:
    r1 : int
    r2 : int
    anno : float
    distanza : float
    difficolta: str

    def __eq__(self, other):
        return isinstance(other, Connesione) and self.r1 == other.r1 and self.r2 == other.r2

    def __str__(self):


        return f"Connessione: {self.r1} | {self.r2}"

    def __repr__(self):
        return f"Connessione: {self.r1} | {self.r2}"