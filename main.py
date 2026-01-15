from models import Zver
from storage import uloz_zaznam
from storage import nacti_vse
from storage import uloz_vse
from datetime import datetime

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

def uprav_zaznam():
    data = nacti_vse()

    if not data:
        print("Nejsou žádné záznamy k úpravě.")
        return
    
    vypis_zaznamy()

    try:
        cislo = int(input("Zadej číslo záznamu k úpravě: "))
        index = cislo - 1

        if index < 0 or index >= len(data):
            print("Neplatné číslo.")
            return

        zaznam = data[index]

        while True:
            print("\nCo chceš upravit?")
            print(f"1 - Druh: {zaznam['druh']}")
            print(f"2 - Věk: {zaznam['vek']}")
            print(f"3 - Pohlaví: {zaznam['pohlavi']}")
            print(f"4 - Datum pozorování: {zaznam['datum_pozorovani']}")
            print(f"5 - Datum ulovení: {zaznam['datum_uloveni'] if zaznam['datum_uloveni'] else '—'}")
            print("0 - Uložit a zpět")


            volba = input("Vyber možnost: ")

            if volba == "1":
                zaznam["druh"] = input("Nový druh: ")

            elif volba == "2":
                zaznam["vek"] = nacti_vek()

            elif volba == "3":
                zaznam["pohlavi"] = vyber_pohlavi()

            elif volba == "4":
                zaznam["datum_pozorovani"] = nacti_datum("Nové datum pozorování: ")

            elif volba == "5":
                zaznam["datum_uloveni"] = nacti_datum(
                    "Nové datum ulovení (nebo Enter): ", True
                )

            elif volba == "0":
                uloz_vse(data)
                print("Záznam byl uložen.")
                break

            else:
                print("Neplatná volba.")
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

def nacti_datum(vyzva, povol_prazdne=False):
    formáty = [
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%Y-%m-%d",
        "%Y.%m.%d",
        "%d/%m/%Y",
        "%Y/%m/%d"
    ]

    while True:
        vstup = input(vyzva)

        if povol_prazdne and vstup == "":
            return None

        for fmt in formáty:
            try:
                datum = datetime.strptime(vstup, fmt)
                return datum.strftime("%d-%m-%Y")
            except ValueError:
                pass

        print("Neplatný formát data. Zkus např. 13-01-2026 nebo 2026/01/13")


def pridej_zaznam():
    while True:
        druh = input("Druh zvěře: ").strip()
        if druh:
            break
        print("Druh nesmí být prázdný.")
    vek = nacti_vek()
    pohlavi = vyber_pohlavi()
    datum_pozorovani = nacti_datum("Datum pozorování: ")
    datum_uloveni = nacti_datum("Datum ulovení (nebo Enter): ", True)
    
    zver = Zver(
        druh=druh,
        vek=vek,
        pohlavi=pohlavi,
        datum_pozorovani=datum_pozorovani,
        datum_uloveni=datum_uloveni
    )
    
    uloz_zaznam(zver)

    print("Záznam byl úspěšně uložen.")


def hlavni_menu():
    print("\n--- EVIDENCE ZVĚŘE ---")
    while True:
        print("1 - Přidat nový záznam")
        print("2 - Vypsat všechny záznamy")
        print("3 - Smazat záznam")
        print("4 - Upravit záznam")
        print("0 - Konec")

        volba = input("Vyber možnost: ")

        if volba == "1":
            pridej_zaznam()
        elif volba == "2":
            vypis_zaznamy()
        elif volba == "3":
            smaz_zaznam()
        elif volba == "4":
            uprav_zaznam()
        elif volba == "0":
            print("Ukončuji program.")
            break
        else:
            print("Neplatná volba, zkus to znovu.")

if __name__ == "__main__":
    hlavni_menu()

