

class ContoBancario:
    def __init__(self, saldo_iniziale):
        self._saldo = saldo_iniziale # Attributo privato

    # 1. IL GETTER: Legge il valore
    @property
    def saldo(self):
        print("Lettura del saldo in corso...")
        return self._saldo

    # 2. IL SETTER: Modifica e convalida il valore
    @saldo.setter
    def saldo(self, nuovo_saldo):
        if nuovo_saldo >= 0:
            print(f"Modifica saldo a: {nuovo_saldo}")
            self._saldo = nuovo_saldo
        else:
            print("Errore: Il saldo non può essere negativo!")

# --- Utilizzo della classe ---
conto = ContoBancario(100)

# Esegue il GETTER
print(conto.saldo) # Stampa: 100

# Esegue il SETTER con valore valido
conto.saldo = 250 # Modifica il valore a 250

# Esegue il SETTER con valore NON valido
conto.saldo = -50 # Blocca la modifica e stampa l'errore
