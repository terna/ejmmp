#!/usr/bin/env python3
import time
import numpy as np

def main(n_iter: int = 10, n: int = 100, seed: int | None = None) -> None:
    rng = np.random.default_rng(seed)

    t0 = time.perf_counter()
    for i in range(1, n_iter + 1):
        print(f"[{i}/{n_iter}] genero matrice {n}x{n} e calcolo inversa...", flush=True)

        # Matrice casuale; aggiungo una piccola componente diagonale per stabilità numerica
        A = rng.random((n, n), dtype=np.float64)
        A += np.eye(n) * 1e-12

        try:
            invA = np.linalg.inv(A)
        except np.linalg.LinAlgError:
            # In caso (molto raro) di singolarità, rigenero e riprovo una volta
            print(f"  -> matrice singolare al ciclo {i}, rigenero e riprovo...", flush=True)
            A = rng.random((n, n), dtype=np.float64)
            A += np.eye(n) * 1e-12
            invA = np.linalg.inv(A)

        # Uso invA per evitare che venga ottimizzato via (non succede in Python, ma è ok)
        checksum = float(invA[0, 0])
        print(f"  -> completato ciclo {i}, checksum={checksum:.6g}", flush=True)

    t1 = time.perf_counter()
    print(f"Finito: {n_iter} inversioni di matrici {n}x{n} in {t1 - t0:.3f} s")

if __name__ == "__main__":
    main()