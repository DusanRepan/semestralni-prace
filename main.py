import tkinter as tk
from tkinter import messagebox
from database import init_db, init_druhy
from tkinter import ttk
from database import get_connection, pridej_druh
from datetime import datetime
from tkcalendar import DateEntry

class EvidenceZvereApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidence zvěře")
        self.root.geometry("400x300")

        tk.Label(
            root,
            text="EVIDENCE ZVĚŘE",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Button(root, text="Přidat záznam", width=25,
                command=self.pridej_zaznam).pack(pady=5)

        tk.Button(root, text="Vypsat záznamy", width=25,
                command=self.vypis_zaznamy).pack(pady=5)

        tk.Button(root, text="Smazat záznam", width=25,
                command=self.smaz_zaznam).pack(pady=5)

        tk.Button(root, text="Konec", width=25,
                command=root.quit).pack(pady=15)

    def pridej_zaznam(self):
        okno = tk.Toplevel(self.root)
        okno.title("Přidat záznam")
        okno.geometry("350x450")

        tk.Label(okno, text="Přidání záznamu", font=("Arial", 14, "bold")).pack(pady=10)

        # ---------- DRUH ----------
        tk.Label(okno, text="Druh zvěře:").pack(anchor="w", padx=20)

        druhy = self.nacti_druhy()
        nazvy = ["➕ Přidat nový druh"] + [d[1] for d in druhy]

        self.druh_var = tk.StringVar()
        combo = ttk.Combobox(okno, values=nazvy, textvariable=self.druh_var, state="readonly")
        combo.current(0)
        combo.pack(fill="x", padx=20)

        def zmena_druhu(event):
            if self.druh_var.get() == "➕ Přidat nový druh":
                self.okno_novy_druh(okno, combo)

        combo.bind("<<ComboboxSelected>>", zmena_druhu)

        # ---------- VĚK ----------
        tk.Label(okno, text="Věk:").pack(anchor="w", padx=20, pady=(10, 0))
        vek_entry = tk.Entry(okno)
        vek_entry.pack(fill="x", padx=20)

        # ---------- POHLAVÍ ----------
        tk.Label(okno, text="Pohlaví:").pack(anchor="w", padx=20, pady=(10, 0))
        pohlavi_var = tk.StringVar(value="samec")
        tk.Radiobutton(okno, text="Samec", variable=pohlavi_var, value="samec").pack(anchor="w", padx=40)
        tk.Radiobutton(okno, text="Samice", variable=pohlavi_var, value="samice").pack(anchor="w", padx=40)

        # ---------- DATA ----------
        tk.Label(okno, text="Datum pozorování:").pack(anchor="w", padx=20, pady=(10, 0))
        dp_entry = DateEntry(okno, date_pattern="dd-mm-yyyy", locale="cs_CZ")
        dp_entry.pack(fill="x", padx=20)

        tk.Label(okno, text="Datum ulovení (nepovinné):").pack(anchor="w", padx=20, pady=(10, 0))

        du_var = tk.BooleanVar(value=False)  # Checkbox stav
        du_checkbox = tk.Checkbutton(okno, text="Vyplnit datum ulovení", variable=du_var)
        du_checkbox.pack(anchor="w", padx=20)

        du_entry = DateEntry(okno, date_pattern="dd-mm-yyyy", locale="cs_CZ", state="disabled")
        du_entry.pack(fill="x", padx=20)

        # Aktivace/Deaktivace DateEntry podle checkboxu
        def du_toggle():
            if du_var.get():
                du_entry.config(state="normal")
            else:
                du_entry.config(state="disabled")
                du_entry.set_date(datetime.today())  # jen aby měl nějakou validní hodnotu, nepoužije se

        du_var.trace_add("write", lambda *args: du_toggle())

        # ---------- ULOŽENÍ ----------
        def uloz_zaznam():
            nazev_druhu = self.druh_var.get()
            if nazev_druhu == "➕ Přidat nový druh":
                messagebox.showerror("Chyba", "Vyber nebo vytvoř druh.")
                return

            druh_id = next(d[0] for d in druhy if d[1] == nazev_druhu)

            vek_text = vek_entry.get()
            if not vek_text.isdigit():
                messagebox.showerror("Chyba", "Věk musí být číslo.")
                return
            vek = int(vek_text)

            pohlavi = pohlavi_var.get()
            dp = dp_entry.get()
            du = du_entry.get() if du_var.get() else None

            if not dp:
                messagebox.showerror("Chyba", "Datum pozorování je povinné.")
                return

            # uložíme do DB
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO zaznamy (druh_id, vek, pohlavi, datum_pozorovani, datum_uloveni)
                VALUES (?, ?, ?, ?, ?)
            """, (druh_id, vek, pohlavi, dp, du))
            conn.commit()
            conn.close()

            messagebox.showinfo("Hotovo", "Záznam byl uložen.")
            okno.destroy()

        tk.Button(okno, text="Uložit", width=20, command=uloz_zaznam).pack(pady=20)
        
    def vypis_zaznamy(self):
        zaznamy = self.nacti_zaznamy()

        okno = tk.Toplevel(self.root)
        okno.title("Výpis záznamů")
        okno.geometry("900x400")

        tk.Label(okno, text="Přehled záznamů", font=("Arial", 14, "bold")).pack(pady=10)

        sloupce = ("id", "druh", "vek", "pohlavi", "dp", "du")

        tree = ttk.Treeview(okno, columns=sloupce, show="headings")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Nastavení hlaviček
        tree.heading("id", text="ID")
        tree.heading("druh", text="Druh")
        tree.heading("vek", text="Věk")
        tree.heading("pohlavi", text="Pohlaví")
        tree.heading("dp", text="Datum pozorování")
        tree.heading("du", text="Datum ulovení")

        # Nastavení šířky sloupců
        tree.column("id", width=40, anchor="center")
        tree.column("druh", width=150, anchor="w")
        tree.column("vek", width=50, anchor="center")
        tree.column("pohlavi", width=80, anchor="center")
        tree.column("dp", width=120, anchor="center")
        tree.column("du", width=120, anchor="center")

        # Vložení dat
        for z in zaznamy:
            tree.insert("", "end", values=z)

        frame = tk.Frame(okno)
        frame.pack(pady=5)

        tk.Button(frame, text="Upravit", width=15,
                command=self.uprav_zaznam).pack(side="left", padx=5)

        tk.Button(frame, text="Zavřít", width=15,
                command=okno.destroy).pack(side="left", padx=5)


    def uprav_zaznam(self):
        vyber = self.tree.selection()

        if not vyber:
            messagebox.showwarning("Pozor", "Nejdříve vyber záznam.")
            return

        hodnoty = self.tree.item(vyber[0], "values")
        zaznam_id, druh, vek, pohlavi, dp, du = hodnoty

        okno = tk.Toplevel(self.root)
        okno.title("Upravit záznam")
        okno.geometry("350x400")

        tk.Label(okno, text="Úprava záznamu", font=("Arial", 14, "bold")).pack(pady=10)

        # ---- DRUH ----
        tk.Label(okno, text="Druh zvěře:").pack(anchor="w", padx=20)
        druhy = self.nacti_druhy()
        nazvy = [d[1] for d in druhy]

        druh_var = tk.StringVar(value=druh)
        combo = ttk.Combobox(okno, values=nazvy, textvariable=druh_var, state="readonly")
        combo.pack(fill="x", padx=20)

        # ---- VĚK ----
        tk.Label(okno, text="Věk:").pack(anchor="w", padx=20, pady=(10, 0))
        vek_entry = tk.Entry(okno)
        vek_entry.insert(0, vek)
        vek_entry.pack(fill="x", padx=20)

        # ---- POHLAVÍ ----
        tk.Label(okno, text="Pohlaví:").pack(anchor="w", padx=20, pady=(10, 0))
        pohlavi_var = tk.StringVar(value=pohlavi)
        tk.Radiobutton(okno, text="Samec", variable=pohlavi_var, value="samec").pack(anchor="w", padx=40)
        tk.Radiobutton(okno, text="Samice", variable=pohlavi_var, value="samice").pack(anchor="w", padx=40)

        # ---- DATA v úpravě ----
        tk.Label(okno, text="Datum pozorování:").pack(anchor="w", padx=20, pady=(10, 0))
        dp_entry = DateEntry(okno, date_pattern="dd-mm-yyyy", locale="cs_CZ")
        dp_entry.set_date(datetime.strptime(dp, "%d-%m-%Y"))
        dp_entry.pack(fill="x", padx=20)

        tk.Label(okno, text="Datum ulovení:").pack(anchor="w", padx=20, pady=(10, 0))
        du_entry = DateEntry(okno, date_pattern="dd-mm-yyyy", locale="cs_CZ")
        if du:
            du_entry.set_date(datetime.strptime(du, "%d-%m-%Y"))
        du_entry.pack(fill="x", padx=20)

        # ---- ULOŽIT ----
        def ulozit():
            nazev_druhu = druh_var.get()
            druh_id = next(d[0] for d in druhy if d[1] == nazev_druhu)
            if not vek_entry.get().isdigit():
                messagebox.showerror("Chyba", "Věk musí být číslo.")
                return

            vek = int(vek_entry.get())
            pohlavi = pohlavi_var.get()
            dp_new = dp_entry.get()
            du_new = du_entry.get() or None

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE zaznamy
                SET druh_id=?, vek=?, pohlavi=?, datum_pozorovani=?, datum_uloveni=?
                WHERE id=?
            """, (druh_id, vek, pohlavi, dp_new, du_new, zaznam_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Hotovo", "Záznam byl upraven.")
            okno.destroy()

    def smaz_zaznam(self):
        messagebox.showinfo("Info", "Mazání záznamu – zatím prázdné")

    def okno_novy_druh(self, parent, combobox):
            win = tk.Toplevel(parent)
            win.title("Nový druh zvěře")
            win.geometry("300x140")
            win.resizable(False, False)

            tk.Label(win, text="Název druhu:").pack(pady=5)
            entry = tk.Entry(win)
            entry.pack(fill="x", padx=20)

            def uloz():
                nazev = entry.get().strip()
                if not nazev:
                    messagebox.showerror("Chyba", "Název nesmí být prázdný.")
                    return

                pridej_druh(nazev)

                druhy = self.nacti_druhy()
                hodnoty = ["➕ Přidat nový druh"] + [d[1] for d in druhy]
                combobox["values"] = hodnoty
                combobox.set(nazev)

                win.destroy()

            tk.Button(win, text="Uložit", command=uloz).pack(pady=10)
            
    def nacti_zaznamy(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT  
                z.id,
                d.nazev,
                z.vek,
                z.pohlavi,
                z.datum_pozorovani,
                z.datum_uloveni
            FROM zaznamy z
            JOIN druhy_zvere d ON z.druh_id = d.id
            ORDER BY z.id DESC
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    def validuj_datum(self, text, povol_prazdne=False):
        if povol_prazdne and text.strip() == "":
            return None

        formaty = [
            "%d-%m-%Y",
            "%d.%m.%Y",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%Y/%m/%d"
        ]

        for fmt in formaty:
            try:
                d = datetime.strptime(text.strip(), fmt)
                return d.strftime("%d-%m-%Y")
            except ValueError:
                pass

        return False

    def nacti_druhy(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nazev FROM druhy_zvere ORDER BY nazev")
        data = cursor.fetchall()
        conn.close()
        return data





if __name__ == "__main__":
    init_db()
    init_druhy()

    root = tk.Tk()
    app = EvidenceZvereApp(root)
    root.mainloop()



