from database import init_db, init_druhy
from database import ziskej_vsechny_druhy, pridej_druh
from database import get_connection
from models import Zver
from storage import uloz_zaznam
from storage import nacti_vse
from storage import uloz_vse
from datetime import datetime

def vypis_zaznamy():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT z.id, d.nazev, z.vek, z.pohlavi,
                z.datum_pozorovani, z.datum_uloveni
        FROM zaznamy z
        JOIN druhy_zvere d ON z.druh_id = d.id
        ORDER BY z.id
    """)

    zaznamy = cursor.fetchall()
    conn.close()

    if not zaznamy:
        print("Žádné záznamy.")
        return

    for i, z in enumerate(zaznamy, start=1):
        print(f"{i}. {z[1]}, věk {z[2]}, {z[3]}, "
            f"pozorování {z[4]}, ulovení {z[5]}")

def smaz_zaznam():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT  z.id, d.nazev, z.vek, z.pohlavi,
                z.datum_pozorovani, z.datum_uloveni
        FROM zaznamy z
        JOIN druhy_zvere d ON z.druh_id = d.id
        ORDER BY z.id
    """)
    
    zaznamy = cursor.fetchall()
    conn.close()
    
    if not zaznamy:
        print("Není co mazat.")
        return
    
    print("\nZáznamy k dispozici:")
    for i, z in enumerate(zaznamy, start=1):
        print(f"{i}. ID: {z[0]} | {z[1]}, věk {z[2]}, {z[3]}, "
            f"pozorování {z[4]}, ulovení {z[5]}")
    
    try:
        cislo = int(input("\nZadej číslo záznamu ke smazání: "))
        zaznam_id = zaznamy[cislo - 1][0]  # Skutečné DB ID
        
        if cislo < 1 or cislo > len(zaznamy):
            print("Neplatné číslo.")
            return
        
        potvrzeni = input(f"Opravdu chceš smazat záznam ID {zaznam_id}? (a/n): ")
        
        if potvrzeni.lower() == "a":
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM zaznamy WHERE id = ?", (zaznam_id,))
            conn.commit()
            conn.close()
            print(f"Záznam ID {zaznam_id} byl smazán.")
        else:
            print("Mazání zrušeno.")
    
    except ValueError:
        print("Musíš zadat číslo.")
    except IndexError:
        print("Neplatné číslo záznamu.")


def uprav_zaznam():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT z.id, d.nazev, z.vek, z.pohlavi,
                z.datum_pozorovani, z.datum_uloveni
        FROM zaznamy z
        JOIN druhy_zvere d ON z.druh_id = d.id
        ORDER BY z.id
    """)
    zaznamy = cursor.fetchall()
    conn.close()

    if not zaznamy:
        return

    volba = input("Vyber číslo záznamu k úpravě: ")

    if not volba.isdigit():
        print("Neplatná volba.")
        return

    index = int(volba) - 1
    if index < 0 or index >= len(zaznamy):
        print("Neexistující záznam.")
        return

    zaznam = zaznamy[index]
    zaznam_id = zaznam[0]

    druh, vek, pohlavi, dp, du = zaznam[1:]

    while True:
        print("\nCo chceš upravit?")
        print(f"1 - Druh: {druh}")
        print(f"2 - Věk: {vek}")
        print(f"3 - Pohlaví: {pohlavi}")
        print(f"4 - Datum pozorování: {dp}")
        print(f"5 - Datum ulovení: {du}")
        print("0 - Uložit a zpět")

        volba = input("Volba: ")

        if volba == "1":
            druh_id = vyber_druh()
            conn = get_connection()
            conn.execute("UPDATE zaznamy SET druh_id=? WHERE id=?", (druh_id, zaznam_id))
            conn.commit()
            conn.close()
            print("Druh upraven.")

        elif volba == "2":
            while True:
                novy = input("Nový věk: ")
                if novy.isdigit():
                    vek = int(novy)
                    break
            conn = get_connection()
            conn.execute("UPDATE zaznamy SET vek=? WHERE id=?", (vek, zaznam_id))
            conn.commit()
            conn.close()

        elif volba == "3":
            pohlavi = vyber_pohlavi()
            conn = get_connection()
            conn.execute("UPDATE zaznamy SET pohlavi=? WHERE id=?", (pohlavi, zaznam_id))
            conn.commit()
            conn.close()

        elif volba == "4":
            dp = nacti_datum("Nové datum pozorování: ")
            conn = get_connection()
            conn.execute(
                "UPDATE zaznamy SET datum_pozorovani=? WHERE id=?",
                (dp, zaznam_id)
            )
            conn.commit()
            conn.close()

        elif volba == "5":
            du = nacti_datum("Nové datum ulovení: ", povol_prazdne=True)
            conn = get_connection()
            conn.execute(
                "UPDATE zaznamy SET datum_uloveni=? WHERE id=?",
                (du, zaznam_id)
            )
            conn.commit()
            conn.close()

        elif volba == "0":
            print("Změny uloženy.")
            break

        else:
            print("Neplatná volba.")

def vyber_druh():
    while True:
        druhy = ziskej_vsechny_druhy()

        print("\nVyber druh zvěře:")
        print("0 - Přidat nový druh")

        for i, (_, nazev) in enumerate(druhy, start=1):
            print(f"{i} - {nazev}")

        volba = input("Zadej číslo: ")

        if not volba.isdigit():
            print("Zadej číslo.")
            continue

        volba = int(volba)

        if volba == 0:
            novy = input("Zadej název nového druhu: ").strip()
            if novy:
                pridej_druh(novy)
                print("Druh přidán.")
            else:
                print("Název nesmí být prázdný.")
            continue

        index = volba - 1
        if 0 <= index < len(druhy):
            return druhy[index][0]  
        else:
            print("Neplatná volba.")

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
    druh_id = vyber_druh()

    while True:
        vek = input("Věk: ")
        if vek.isdigit():
            vek = int(vek)
            break
        print("Věk musí být číslo.")

    pohlavi = vyber_pohlavi()

    datum_pozorovani = nacti_datum("Datum pozorování: ")
    datum_uloveni = nacti_datum("Datum ulovení (Enter = žádné): ", povol_prazdne=True)

    zver = Zver(
        druh=druh_id,
        vek=vek,
        pohlavi=pohlavi,
        datum_pozorovani=datum_pozorovani,
        datum_uloveni=datum_uloveni
    )

    #uloz_zaznam
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO zaznamy (druh_id, vek, pohlavi, datum_pozorovani, datum_uloveni)
        VALUES (?, ?, ?, ?, ?)
    """, (druh_id, vek, pohlavi, datum_pozorovani, datum_uloveni))
    conn.commit()
    conn.close()

    print("Záznam uložen.")

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
    init_db()
    init_druhy()
    hlavni_menu()


