import random
import time


def generate_matrix(n, low=-10.0, high=10.0):
    """Genera una matrice n x n con valori float casuali."""
    return [
        [random.uniform(low, high) for _ in range(n)]
        for _ in range(n)
    ]


def identity_matrix(n):
    """Restituisce una matrice identità n x n."""
    return [
        [1.0 if i == j else 0.0 for j in range(n)]
        for i in range(n)
    ]


def invert_matrix(A):
    """
    Inverte una matrice quadrata A usando Gauss-Jordan
    con pivoting parziale.
    """
    n = len(A)

    M = [row[:] for row in A]
    I = identity_matrix(n)

    for col in range(n):

        # Pivoting parziale
        pivot_row = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot_row][col]) < 1e-12:
            raise ValueError("Matrice singolare o quasi singolare")

        if pivot_row != col:
            M[col], M[pivot_row] = M[pivot_row], M[col]
            I[col], I[pivot_row] = I[pivot_row], I[col]

        pivot = M[col][col]

        # Normalizzazione riga pivot
        for j in range(n):
            M[col][j] /= pivot
            I[col][j] /= pivot

        # Eliminazione
        for row in range(n):
            if row != col:
                factor = M[row][col]
                for j in range(n):
                    M[row][j] -= factor * M[col][j]
                    I[row][j] -= factor * I[col][j]

    return I


def multiply_matrices(A, B):
    """Moltiplicazione matriciale (per verifica)."""
    n = len(A)
    result = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += A[i][k] * B[k][j]
            result[i][j] = s
    return result


def main():
    n = 1000

    print("Generazione matrice...")
    A = generate_matrix(n)

    print("Calcolo inversa...")
    t0 = time.perf_counter()
    A_inv = invert_matrix(A)
    t1 = time.perf_counter()

    elapsed = t1 - t0
    print(f"Tempo impiegato per inversione {n}x{n}: {elapsed:.4f} secondi")

    """
    print("Verifica A * A_inv ≈ I (prime 5 righe)...")
    check = multiply_matrices(A, A_inv)
    for i in range(5):
        print([round(x, 3) for x in check[i][:5]])
    """

if __name__ == "__main__":
    main()