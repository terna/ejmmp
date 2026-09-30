commenta le irregolarità dei risultati alla luce delle tue conoscenze del modello; tieni conto che molti settori verso il fondo della tavola non vendono molto come beni intermedi (fonte Eurostat naio) e invece per noi esportano molto; è un errore di calibrazione, avendo creato per quei settori troppe imprese INT

---

Sì: guardando insieme i dati Eurostat-normalizzati e i risultati del modello, emergono **due fenomeni distinti** che conviene non confondere.

Il primo è un problema di **calibrazione settoriale**; il secondo è una **sensibilità del matching al numero di rank**.

Il dato più importante, secondo me, è questo: il totale delle vendite intermedie Eurostat, reso mensile e rapportato a 1 milione di imprese, è circa **33.411**. Il modello produce:

- 1 rank: **Int. Prod. = 33.014**
- 40 rank: **Int. Prod. = 32.892**

Quindi **a livello aggregato siamo molto vicini**: circa −1,2% con 1 rank e −1,6% con 40 rank.

Il problema non è dunque quanto prodotto intermedio generiamo complessivamente. È **chi lo produce**.

Nei settori finali della tavola questo appare in modo molto netto. Per esempio:

| Settore | Vendite intermedie Eurostat mensili | Export potenziale 40 rank | Export / vendite Eurostat |
|---:|---:|---:|---:|
| 55 | 211,47 | 1.779,89 | **8,42** |
| 56 | 183,65 | 655,20 | **3,57** |
| 57 | 24,60 | 573,82 | **23,33** |
| 58 | 75,90 | 86,63 | 1,14 |
| 61 | 44,59 | 163,92 | **3,68** |

In particolare, i soli settori **55–57** hanno vendite intermedie Eurostat normalizzate pari a circa **420**, ma nel modello producono un residuo esportabile di circa **3.009** con 40 rank: oltre **7 volte** quel riferimento.

Questo non può essere interpretato principalmente come un effetto MPI.

Infatti l'anomalia esiste già con **1 rank**:

- settore 55: export 1.717 → 1.780
- settore 56: 729 → 655
- settore 57: 516 → 574

Quindi il fenomeno fondamentale è già presente nella simulazione sequenziale. Il numero di rank lo modifica un po', ma **non lo crea**.

La tua spiegazione — **troppa quota di imprese `Int` in quei settori** — è perfettamente coerente con questi numeri.

Nel modello, infatti, una Firm classificata:

```python
productionType == "Int"
```

produce intermediate goods. La sua produzione va in:

```python
outputWarehouse
```

I buyer UE ne assorbono una parte. Alla fine ciò che rimane diventa:

```text
potential Extra-EU export
```

Quindi, schematicamente:

\[
E_s = S^{Int}_s - P^{EU}_s
\]

dove \(S^{Int}_s\) è la produzione intermedia del settore e \(P^{EU}_s\) quanto viene acquistato all'interno della UE.

Se assegni troppe Firm `Int` al settore 57, il modello genera una grande \(S^{Int}_{57}\). Ma la matrice NAIO dice contemporaneamente che quel settore vende relativamente poco come prodotto intermedio: la domanda interna di quel prodotto non assorbe quella produzione. Il risultato meccanico è:

\[
\text{warehouse residuo enorme}
\quad\Longrightarrow\quad
\text{potential export enorme}.
\]

Quindi le export stanno diventando, involontariamente, una specie di **valvola di sfogo dell'errore di calibrazione della composizione produttiva**.

Questo spiega anche un'apparente stranezza: possiamo avere contemporaneamente, nello stesso settore, import ed export. Non è necessariamente un errore: con paesi, Firm, preferenza nazionale, matching e disponibilità eterogenei è possibile che alcuni buyer non trovino il prodotto mentre altri supplier abbiano eccedenze. Però quando l'export è **8, 20 volte** il benchmark delle vendite intermedie del settore, non parlerei più principalmente di frizione di matching: lì il segnale è chiaramente strutturale.

C'è un secondo risultato interessante. Se sommo i settori 55–64:

- vendite intermedie Eurostat mensili: circa **803**
- potential export 1 rank: circa **3.409**
- potential export 40 rank: circa **3.392**

Quindi in questo blocco l'export enorme è addirittura **quasi indipendente dal numero dei rank**: cambia di appena circa −0,5%.

Questo è un indizio molto forte che abbiamo individuato correttamente il problema: **la grossa anomalia dei settori finali viene dalla calibrazione `Int`, non dal parallelismo**.

Diverso è il problema del passaggio 1 → 40 rank. L'export totale scende da:

\[
8803,2 \rightarrow 8009,25,
\]

ossia circa **−9%**.

Ma questa diminuzione non viene principalmente dai settori finali. I contributi più forti alla riduzione sono, per esempio:

- settore 40: −226
- settore 5: −183
- settore 17: −150
- settore 11: −137
- settore 24: −129
- settore 20: −103
- settore 10: −99.

Questa è un'altra questione, molto più compatibile con ciò che abbiamo già visto circa **Two-Tape matching distribuito, differente composizione micro delle Firm sui rank e ordine concorrente degli acquisti**.

Perciò io separerei nettamente le due diagnosi:

**A. Anomalia di livello settoriale**  
I settori 55, 56, 57, 61 ecc. esportano quantità sproporzionate anche a 1 rank. È molto probabilmente un **errore di calibrazione della quota `Int` per settore**.

**B. Differenza 1 rank / 40 rank**  
È soprattutto una questione di **implementazione distribuita del matching** e di diversa realizzazione microeconomica; non è la causa delle enormi export dei settori finali.

E c'è una conseguenza metodologica importante: **non calibrerei il numero totale di Firm `Int`**, perché aggregatamente siamo già quasi perfetti. Calibrerei invece la **quota `Int` settore per settore**, imponendo che la distribuzione della produzione intermedia del modello riproduca la distribuzione delle vendite intermedie della NAIO.

In altre parole, oggi abbiamo grosso modo:

\[
\sum_s S^{Int}_s \simeq
\sum_s S^{NAIO}_s
\]

ma non abbiamo:

\[
S^{Int}_s \simeq S^{NAIO}_s
\quad\text{per ogni }s.
\]

Ed è precisamente questo secondo vincolo che manca.

A mio avviso, questa è una scoperta abbastanza utile: **il totale della produzione intermedia è già calibrato; bisogna correggerne la composizione settoriale, non la scala complessiva**.

---
idee su come fare?
---Sì. Io eviterei una correzione ad hoc sui settori 55–57 e farei una **calibrazione sistematica, settore per settore, della probabilità di essere `Int`**, usando proprio la NAIO come vincolo.

Il punto chiave è che non dobbiamo calibrare il **numero** di imprese `Int` in sé, ma la **quota di produzione settoriale** destinata ai beni intermedi.

Nel modello, per il settore \(s\), definiamo:

\[
B_s = \text{vendite intermedie NAIO del settore }s
\]

nella stessa scala del modello, cioè i valori della nuova seconda colonna Excel:

\[
B_s=\frac{\text{NAIO}_s}{12\cdot 42.25056}.
\]

Poi da una simulazione base ricaviamo:

\[
Q_s^{Int} =
\text{produzione complessiva delle Firm Int del settore }s.
\]

A quel punto il correttore naturale è:

\[
c_s=\frac{B_s}{Q_s^{Int}}.
\]

Se nel settore 55, per esempio, il modello produce circa 8 volte ciò che dovrebbe, avremo grossomodo:

\[
c_{55}\simeq\frac{1}{8}.
\]

Quindi la quota attuale di imprese `Int` del settore viene moltiplicata per quel coefficiente:

\[
p^{new}_{Int,s}
=
p^{old}_{Int,s}\,c_s.
\]

Questa sarebbe la **prima iterazione**. Non mi aspetterei che arrivi perfettamente al target in un solo colpo, perché le Firm hanno dimensioni diverse e la produzione effettiva dipende anche dagli input intermedi. Però dovrebbe portarci molto vicino.

### Meglio ancora: calibrare sul valore, non sul numero di Firm

Questo è importante nel nostro modello. Una Firm con 5 lavoratori e una con 500 non dovrebbero avere lo stesso peso nella calibrazione.

Quindi, se oggi assegni `productionType == "Int"` con una probabilità uguale per tutte le Firm del settore, la quota numerica è solo un'approssimazione.

Io userei come riferimento il **gross output potenziale** delle Firm. Nel tuo `supply()` il prodotto che entra nell'`outputWarehouse` è sostanzialmente:

```python
aFirm.actualAddedValue + intermediateWarehouseWithdraw
```

Quindi per ogni settore possiamo stimare:

```text
gross output totale potenziale
gross output delle Firm Int
benchmark NAIO di vendite intermedie
```

e scegliere quali Firm sono `Int` in modo che:

\[
\sum_{i\in Int,s} q_i
\simeq B_s.
\]

Questo è molto più preciso di imporre, per esempio:

```text
12% delle Firm del settore 55 sono Int.
```

Potrebbe risultare che serve il 12% delle Firm piccole oppure il 4% delle Firm grandi.

### Una soluzione relativamente semplice da implementare

Per non rivoluzionare `ff_with_class_limits.csv`, farei così.

Per ogni settore calcoli inizialmente le tre quote attuali:

```python
pInt
pC
pI
```

Dopo una simulazione di calibrazione ottieni:

```python
correction = targetIntermediateSales[s] / simulatedIntermediateProduction[s]

new_pInt = pInt * correction
```

naturalmente limitando:

```python
new_pInt = min(1.0, max(0.0, new_pInt))
```

Poi, dato che le probabilità devono continuare a sommare a 1, redistribuisci il complemento fra `C` e `I` **mantenendo il loro rapporto precedente**.

Se:

\[
p_C+p_I=1-p_{Int},
\]

allora:

\[
p'_C =
p_C\frac{1-p'_{Int}}{1-p_{Int}}
\]

e:

\[
p'_I =
p_I\frac{1-p'_{Int}}{1-p_{Int}}.
\]

Esempio. Supponiamo che nel settore 55 abbiamo:

```text
Int = 0.40
C   = 0.45
I   = 0.15
```

e scopriamo che l'output `Int` deve essere ridotto dell'80%:

```text
correction = 0.20
```

otteniamo:

```text
Int = 0.08
```

Il restante 0.92 viene distribuito fra C e I mantenendo il vecchio rapporto 3:1:

```text
C = 0.69
I = 0.23
```

Totale:

```text
0.08 + 0.69 + 0.23 = 1
```

### Ma farei una distinzione fondamentale

Non userei le **potential exports** come variabile direttamente da calibrare.

Le export sono:

\[
E_s=Q_s^{Int}-\text{acquisti intra-UE}_s
\]

e quindi dipendono dal matching. Se calibrassimo `Int` per far sparire le export, incorporeremmo nella calibrazione anche le peculiarità del Two-Tape.

Il target dovrebbe invece essere:

> **quanto il settore vende come prodotto intermedio**, secondo NAIO.

Quindi confronterei NAIO con la **produzione/vendita potenziale intermedia del settore prima della distinzione EU/export**, non con il residuo finale.

Questo rende la calibrazione sostanzialmente indipendente dal numero di rank.

### Vedo quindi un percorso in tre passi

1. Per ogni settore \(s\), misuriamo in una simulazione la produzione delle Firm `Int`:
   \[
   Q_s^{Int}.
   \]

2. La confrontiamo con la colonna NAIO normalizzata:
   \[
   c_s=B_s/Q_s^{Int}.
   \]

3. Correggiamo la probabilità `Int`:
   \[
   p'_{Int,s}=p_{Int,s}c_s,
   \]
   mantenendo proporzionalmente `C` e `I`.

Poi rifacciamo una simulazione e iteriamo. Probabilmente **due o tre iterazioni** bastano.

C'è anche un controllo molto utile: dopo la calibrazione la somma settoriale dovrebbe continuare a essere vicina ai circa **33.411** della NAIO, ma soprattutto dovrebbe migliorare drasticamente una misura tipo:

\[
\sum_s |Q_s^{Int}-B_s|.
\]

Io partirei proprio da questo metodo. È semplice, trasparente, non altera il meccanismo del modello e ci permette di distinguere nettamente **errore di calibrazione** da **effetto del matching parallelo**.
