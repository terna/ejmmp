import random

def main():
    N = 20
    lista = list(range(1, N+1))
    valore = random.uniform(0, N)

    print(f"Lista: {lista}")
    print(f"Valore casuale: {valore:.4f}")

    for i, num in enumerate(lista):
        if num > valore:
            print(f"Primo elemento maggiore di {valore:.4f}: {num} (posizione {i})")
            break
    else:
        print("Nessuna posizione trovata: il valore è ≥ dell'ultimo elemento della lista")

if __name__ == "__main__":
    main()