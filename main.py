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
        self.okno_vypis = None

        tk.Label(
            root,
            text="EVIDENCE ZVĚŘE",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Button(root, text="Přidat záznam", width=25,
                command=self.pridej_zaznam).pack(pady=5)

        tk.Button(root, text="Vypsat záznamy", width=25,
                command=self.vypis_zaznamy).pack(pady=5)
        
        tk.Button(root, text="Správa druhů", width=25, 
                command=self.sprava_druhu).pack(pady=5)
        
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
        dp_entry = DateEntry(okno, date_pattern="dd-mm-yyyy", locale="cs_CZ", state="readonly")
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
                du_entry.config(state="readonly")
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
        okno = self.okno_vypis
        
        okno = tk.Toplevel(self.root)
        okno.title("Výpis záznamů")
        okno.geometry("800x400")
        
        tk.Label(okno, text="Přehled záznamů", font=("Arial", 14, "bold")).pack(pady=10)

        # ---- FILTR ----
        filtr_frame = tk.Frame(okno)
        filtr_frame.pack(fill="x", padx=10, pady=5)

        # DRUH
        tk.Label(filtr_frame, text="Druh:").grid(row=0, column=0)
        druhy = ["Vše"] + [d[1] for d in self.nacti_druhy()]
        self.filtr_druh = tk.StringVar(value="Vše")
        ttk.Combobox(filtr_frame, values=druhy, textvariable=self.filtr_druh,
                    state="readonly", width=18).grid(row=0, column=1, padx=5)

        # VĚK
        tk.Label(filtr_frame, text="Věk:").grid(row=0, column=2)
        self.filtr_vek = tk.StringVar(value="Mladý → Starý")
        ttk.Combobox(
            filtr_frame,
            values=["Mladý → Starý", "Starý → Mladý"],
            textvariable=self.filtr_vek,
            state="readonly",
            width=10
        ).grid(row=0, column=3, padx=5)
        
        # POHLAVÍ
        tk.Label(filtr_frame, text="Pohlaví:").grid(row=0, column=4)
        self.filtr_pohlavi = tk.StringVar(value="Vše")
        ttk.Combobox(
            filtr_frame,
            values=["Vše", "samec", "samice"],
            textvariable=self.filtr_pohlavi,
            state="readonly",
            width=10
        ).grid(row=0, column=5, padx=5)

        # DATUM
        tk.Label(filtr_frame, text="Datum:").grid(row=0, column=6)
        self.filtr_datum = tk.StringVar(value="Nejnovější → Nejstarší")
        ttk.Combobox(
            filtr_frame,
            values=["Nejnovější → Nejstarší", "Nejstarší → Nejnovější"],
            textvariable=self.filtr_datum,
            state="readonly",
            width=22
        ).grid(row=0, column=7, padx=5) 

        self.filtr_druh.trace_add("write", lambda *args: self.aplikuj_filtry())
        self.filtr_pohlavi.trace_add("write", lambda *args: self.aplikuj_filtry())
        self.filtr_vek.trace_add("write", lambda *args: self.aplikuj_filtry())
        self.filtr_datum.trace_add("write", lambda *args: self.aplikuj_filtry())

            
        sloupce = ("id", "druh", "vek", "pohlavi", "dp", "du")
        self.tree_vypis = ttk.Treeview(okno, columns=sloupce, show="headings")
        self.tree_vypis.pack(fill="both", expand=True, padx=10, pady=10)

        hlavicky = ("ID", "Druh", "Věk", "Pohlaví", "Datum pozorování", "Datum ulovení")
        sirka = (50, 180, 60, 90, 140, 140)

        for col, text, w in zip(sloupce, hlavicky, sirka):
            self.tree_vypis.heading(col, text=text)
            self.tree_vypis.column(col, width=w, anchor="center")


        for id_, druh, vek, pohlavi, dp, du in zaznamy:

            # --- datum pozorování ---
            if isinstance(dp, (datetime,)):
                dp_text = dp.strftime("%d-%m-%Y")
            elif dp:
                dp_text = str(dp)
            else:
                dp_text = ""

            # --- datum ulovení ---
            if isinstance(du, (datetime,)):
                du_text = du.strftime("%d-%m-%Y")
            elif du:
                du_text = str(du)
            else:
                du_text = ""

            self.tree_vypis.insert(
                "",
                "end",
                values=(id_, druh, vek, pohlavi, dp_text, du_text)
            )


        frame = tk.Frame(okno)
        frame.pack(pady=5)

        tk.Button(frame, text="Upravit", width=15, command=self.uprav_zaznam).pack(side="left", padx=5)
        tk.Button(frame, text="Zavřít", width=15, command=okno.destroy).pack(side="left", padx=5)
        tk.Button(frame, text="Smazat", width=15, command=self.smazat_zaznam).pack(side="left", padx=5)

    def uprav_zaznam(self):
        vyber = self.tree_vypis.selection()
        if not vyber:
            messagebox.showwarning("Pozor", "Nejdříve vyber záznam.")
            return

        hodnoty = self.tree_vypis.item(vyber[0], "values")
        zaznam_id, druh, vek, pohlavi, dp, du = hodnoty

        okno = tk.Toplevel(self.root)
        okno.title("Upravit záznam")
        okno.geometry("350x450")

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

        # ---- DATA ----
        tk.Label(okno, text="Datum pozorování:").pack(anchor="w", padx=20, pady=(10, 0))
        dp_entry = DateEntry(okno, date_pattern="dd-mm-yyyy",state="readonly", locale="cs_CZ")
        dp_entry.set_date(datetime.strptime(dp, "%d-%m-%Y"))
        dp_entry.pack(fill="x", padx=20)

        tk.Label(okno, text="Datum ulovení (nepovinné):").pack(anchor="w", padx=20, pady=(10, 0))

        # Checkbox pro aktivaci/neaktivaci
        du_var = tk.BooleanVar(value=bool(du))  # True pokud datum ulovení existuje
        du_checkbox = tk.Checkbutton(okno, text="Vyplnit datum ulovení", variable=du_var)
        du_checkbox.pack(anchor="w", padx=20)

        du_entry = DateEntry(okno, date_pattern="dd-mm-yyyy", locale="cs_CZ",
                            state="readonly" if du else "disabled")
        if du:
            du_entry.set_date(datetime.strptime(du, "%d-%m-%Y"))
        du_entry.pack(fill="x", padx=20)

        # Aktivace/Deaktivace DateEntry podle checkboxu
        def du_toggle():
            if du_var.get():
                du_entry.config(state="readonly")
                if not du:
                    du_entry.set_date(datetime.today())  # pokud nebylo datum, nastav dnešní
            else:
                du_entry.config(state="disabled")
                du_entry.set_date(datetime.today())  # hodnota se nepoužije

        du_var.trace_add("write", lambda *args: du_toggle())

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
            du_new = du_entry.get() if du_var.get() else None  # <--- tady

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

        tk.Button(okno, text="Uložit", width=20, command=ulozit).pack(pady=20)

    def smazat_zaznam(self):
        vyber = self.tree_vypis.selection()

        if not vyber:
            messagebox.showwarning("Chyba", "Nejprve vyber záznam ke smazání.")
            return

        hodnoty = self.tree_vypis.item(vyber[0], "values")
        zaznam_id = hodnoty[0]

        if not messagebox.askyesno(
            "Potvrzení",
            "Opravdu chceš tento záznam smazat?"
        ):
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM zaznamy WHERE id = ?", (zaznam_id,))
        conn.commit()
        conn.close()

        self.tree_vypis.delete(vyber[0])

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

    def sprava_druhu(self):
        okno = tk.Toplevel(self.root)
        okno.title("Správa druhů zvěře")
        okno.geometry("350x300")

        tk.Label(okno, text="Druhy zvěře", font=("Arial", 14, "bold")).pack(pady=10)

        listbox = tk.Listbox(okno)
        listbox.pack(fill="both", expand=True, padx=10)

        def nacti():
            listbox.delete(0, tk.END)
            for _, nazev in self.nacti_druhy():
                listbox.insert(tk.END, nazev)

        nacti()

        def smazat():
            vyber = listbox.curselection()
            if not vyber:
                messagebox.showwarning("Chyba", "Vyber druh.")
                return

            nazev = listbox.get(vyber[0])

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT id FROM druhy_zvere WHERE nazev=?", (nazev,))
            druh_id = cur.fetchone()[0]

            cur.execute(
                "SELECT COUNT(*) FROM zaznamy WHERE druh_id=?",
                (druh_id,)
            )

            if cur.fetchone()[0] > 0:
                messagebox.showerror(
                    "Nelze smazat",
                    "Druh je použit v záznamech."
                )
                conn.close()
                return

            if not messagebox.askyesno(
                "Potvrzení",
                f"Opravdu smazat '{nazev}'?"
            ):
                conn.close()
                return

            cur.execute("DELETE FROM druhy_zvere WHERE id=?", (druh_id,))
            conn.commit()
            conn.close()

            nacti()

        tk.Button(okno, text="Smazat vybraný druh", command=smazat).pack(pady=10)

    def aplikuj_filtry(self):
        # vymazání tabulky
        for i in self.tree_vypis.get_children():
            self.tree_vypis.delete(i)

        podminky = []
        parametry = []

        # DRUH
        if self.filtr_druh.get() != "Vše":
            podminky.append("d.nazev = ?")
            parametry.append(self.filtr_druh.get())

        # POHLAVÍ
        if self.filtr_pohlavi.get() != "Vše":
            podminky.append("z.pohlavi = ?")
            parametry.append(self.filtr_pohlavi.get())

        where_sql = ""
        if podminky:
            where_sql = "WHERE " + " AND ".join(podminky)

        # ŘAZENÍ VĚK
        order_sql = ""
        if self.filtr_vek.get() == "Mladý → Starý":
            order_sql = "ORDER BY z.vek ASC"
        else:
            order_sql = "ORDER BY z.vek DESC"

        # ŘAZENÍ DATUM
        if self.filtr_datum.get() == "Nejnovější → Nejstarší":
            order_sql = "ORDER BY z.datum_pozorovani DESC"
        else:
            order_sql = "ORDER BY z.datum_pozorovani ASC"

        sql = f"""
            SELECT z.id, d.nazev, z.vek, z.pohlavi,
                z.datum_pozorovani, z.datum_uloveni
            FROM zaznamy z
            JOIN druhy_zvere d ON z.druh_id = d.id
            {where_sql}
            {order_sql}
        """

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, parametry)
        data = cursor.fetchall()
        conn.close()

        for r in data:
            self.tree_vypis.insert("", "end", values=r)

if __name__ == "__main__":
    init_db()
    init_druhy()

    root = tk.Tk()
    app = EvidenceZvereApp(root)
    root.mainloop()



