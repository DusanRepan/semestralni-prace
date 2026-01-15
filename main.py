from models import Zver
from storage import uloz_zaznam

def pridej_zaznam():
    druh = input("Druh zvěře: ")
    vek = int(input("Věk: "))
    pohlavi = input("Pohlaví (samec/samice): ")
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


if __name__ == "__main__":
    pridej_zaznam()
