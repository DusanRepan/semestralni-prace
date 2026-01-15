from models import Zver
from storage import uloz_zaznam
from storage import nacti_vse
from storage import uloz_vse


def vypis_zaznamy():
    data = nacti_vse()

    if not data:
        print("Žádné záznamy nejsou uložené.")
        return

    for i, z in enumerate(data, start=1):
        print(f"{i}. Druh: {z['druh']}, "
            f"Věk: {z['vek']}, "
            f"Pohlaví: {z['pohlavi']}, "
            f"Pozorování: {z['datum_pozorovani']}, "
            f"Ulovení: {z['datum_uloveni']}")

def smaz_zaznam():
    data = nacti_vse()

    if not data:
        print("Není co mazat.")
        return

    vypis_zaznamy()

    try:
        cislo = int(input("Zadej číslo záznamu ke smazání: "))
        index = cislo - 1

        if index < 0 or index >= len(data):
            print("Neplatné číslo.")
            return

        potvrzeni = input("Opravdu chceš záznam smazat? (a/n): ")

        if potvrzeni.lower() == "a":
            smazany = data.pop(index)
            uloz_vse(data)
            print("Záznam byl smazán:", smazany["druh"])
        else:
            print("Mazání zrušeno.")

    except ValueError:
        print("Musíš zadat číslo.")

def vyber_pohlavi():
    while True:
        print("Vyber pohlaví:")
        print("1 - Samec")
        print("2 - Samice")

        volba = input("Zadej číslo: ")

        if volba == "1":
            return "samec"
        elif volba == "2":
            return "samice"
        else:
            print("Neplatná volba.")


def nacti_vek():
    while True:
        vstup = input("Věk: ")

        if not vstup.isdigit():
            print("Zadej celé číslo (např. 3).")
            continue

        vek = int(vstup)

        if vek < 0:
            print("Věk nemůže být záporný.")
            continue

        return vek


def pridej_zaznam():
    druh = input("Druh zvěře: ")
    vek = nacti_vek()
    pohlavi = vyber_pohlavi()
    datum_pozorovani = input("Datum pozorování (YYYY-MM-DD): ")
    datum_uloveni = input("Datum ulovení (nebo Enter): ")

    if datum_uloveni == "":
        datum_uloveni = None

    zver = Zver(
        druh=druh,
        vek=vek,
        pohlavi=pohlavi,
        datum_pozorovani=datum_pozorovani,
        datum_uloveni=datum_uloveni
    )

    uloz_zaznam(zver)
    print("Záznam uložen.")

def hlavni_menu():
    print("\n--- EVIDENCE ZVĚŘE ---")
    while True:
        print("1 - Přidat nový záznam")
        print("2 - Vypsat všechny záznamy")
        print("3 - Smazat záznam")
        print("0 - Konec")

        volba = input("Vyber možnost: ")

        if volba == "1":
            pridej_zaznam()
        elif volba == "2":
            vypis_zaznamy()
        elif volba == "3":
            smaz_zaznam()

        elif volba == "0":
            print("Ukončuji program.")
            break
        else:
            print("Neplatná volba, zkus to znovu.")

if __name__ == "__main__":
    hlavni_menu()

