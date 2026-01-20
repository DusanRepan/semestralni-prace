# Semestrální práce – Evidence zvěře a lovů

## 1. Úvod

Tato semestrální práce se zaměřuje na vytvoření desktopové aplikace v jazyce **Python**, která slouží k evidenci zvěře a lovů. Aplikace umožňuje uživateli přehledně ukládat, upravovat, mazat a filtrovat záznamy o jednotlivých kusech zvěře.

Cílem projektu bylo propojit objektově orientované programování, práci s databází a grafické uživatelské rozhraní do jednoho funkčního celku.

---

## 2. Použité technologie

* **Python 3.11** – hlavní programovací jazyk
* **Tkinter** – grafické uživatelské rozhraní (GUI)
* **SQLite** – relační databáze
* **JSON** – meziformát pro práci s daty / zálohy
* **tkcalendar** – výběr data v GUI

---

## 3. Architektura projektu

Projekt je rozdělen do několika samostatných souborů, aby byla zachována přehlednost a oddělení odpovědností:

```
semestralni-prace/
│
├── main.py          # hlavní aplikace a GUI
├── database.py      # práce s databází (SQLite)
├── models.py        # datové modely a struktury
├── storage.py       # práce s JSON (ukládání / načítání)
├── statistics.py    # statistiky (rozšíření projektu)
├── data.db          # databázový soubor
├── data.json        # JSON data (záloha / import)
└── README.md        # dokumentace projektu
```

---

## 4. Postup vývoje projektu

### 4.1 Python – základ aplikace

Projekt je napsán v jazyce Python, který jsem zvolil kvůli jeho jednoduchosti a dobré podpoře pro práci s databázemi i GUI.

Použit byl objektově orientovaný přístup – hlavní třída `EvidenceZvereApp` spravuje:

* okna aplikace
* filtry
* práci s databází
* reakce na uživatelské události

---

### 4.2 GUI – Tkinter

Grafické rozhraní bylo vytvořeno pomocí knihovny **Tkinter**.

GUI obsahuje:

* hlavní menu aplikace
* okno s výpisem záznamů (TreeView)
* dialogy pro přidání a úpravu záznamů
* filtrační panel

Použité prvky:

* `Tk`, `Toplevel`
* `Label`, `Button`, `Entry`
* `ttk.Treeview`
* `ttk.Combobox`
* `Radiobutton`, `Checkbutton`

---

### 4.3 Databáze – SQLite

Pro ukládání dat byla zvolena databáze **SQLite**, která je:

* jednoduchá
* nevyžaduje server
* ideální pro menší aplikace

Databáze obsahuje např. tabulky:

* `zaznamy` – jednotlivé záznamy zvěře
* `druhy_zvere` – seznam druhů

Ukázka dat v databázi:

* druh
* pohlaví (samec / samice)
* věk
* datum pozorování
* datum ulovení (volitelné)

---

### 4.4 JSON (počáteční fáze projektu)

* JSON byl použit v počáteční fázi vývoje aplikace

* Sloužil k ukládání a načítání záznamů bez databáze

* Umožnil rychlé ověření funkčnosti aplikace

* Později byl nahrazen databází SQLite kvůli lepší práci s daty

---

### 4.5 Filtrace a řazení dat

Aplikace umožňuje **živé filtrování** bez nutnosti restartu:

Filtry:

* druh zvěře
* pohlaví (samec / samice)
* řazení podle věku
* řazení podle data pozorování

Filtrace je realizována pomocí:

* `StringVar`
* `trace_add()`
* dynamického sestavení SQL dotazu
---

### 4.6 Úprava a mazání záznamů

Uživatel může:

* vybrat záznam v tabulce
* otevřít okno pro úpravu
* změnit hodnoty
* uložit změny zpět do databáze

Mazání záznamů je chráněno potvrzovacím dialogem.

---

## 5. Statistické rozšíření (bohužel jsem nestihnul)

Projekt je připraven na rozšíření o statistiky, například:

* počet kusů za období
* poměr samců a samic
* počet ulovených / neulovených kusů

---

## 6. Závěr

Cílem této semestrální práce bylo vytvořit aplikaci pro evidenci zvěře a lovů v jazyce Python s grafickým uživatelským rozhraním. Během vývoje aplikace jsem si osvojil práci s několika novými knihovnami a koncepty.

* využití Pythonu
* práce s databází
* tvorba GUI
* objektový návrh
* praktické využití

Aplikace je dále rozšiřitelná a může sloužit jako základ pro komplexnější evidenční systém.

---

## 7. Možná budoucí vylepšení

* export do CSV / PDF
* grafické statistiky
* uživatelské role
* automatické zálohování databáze

---

## 8. Poděkování testerům

* Zátěžový test provedl(co z programu nesnědl to rozbil):
* Honza Bartoň - velkayolanda

---

**Autor:** Dušan Repáň
**Rok:** 2026
