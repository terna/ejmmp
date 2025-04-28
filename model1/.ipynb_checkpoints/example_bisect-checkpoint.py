import random
import bisect

def main():
    N = 20
    lista = list(range(1, N+1))
    valore = random.uniform(0, N)

    print(f"Lista: {lista}")
    print(f"Valore casuale: {valore:.4f}")

    pos = bisect.bisect_right(lista, valore)
    print(f"Posizione trovata con bisect: {pos}")

if __name__ == "__main__":
    main()