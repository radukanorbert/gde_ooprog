import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from abc import ABC, abstractmethod
import json

DATA_DIR = "data"
JARATOK_FILE = os.path.join(DATA_DIR, "jaratok.json")
FOGLALASOK_FILE = os.path.join(DATA_DIR, "foglalasok.json")
LEGITARSASAG_FILE = os.path.join(DATA_DIR, "legitarsasag.txt")

class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = int(jegyar)

    @abstractmethod
    def info(self):
        pass

class BelfoldiJarat(Jarat):
    def info(self):
        return f"[Belföldi] {self.jaratszam} - {self.celallomas} ({self.jegyar} Ft)"

class NemzetkoziJarat(Jarat):
    def info(self):
        return f"[Nemzetközi] {self.jaratszam} - {self.celallomas} ({self.jegyar} Ft)"

class JegyFoglalas:
    def __init__(self, utas_nev, jaratszam):
        self.utas_nev = utas_nev
        self.jaratszam = jaratszam

    def to_dict(self):
        return {"utas_nev": self.utas_nev, "jaratszam": self.jaratszam}

class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []
        self.foglalasok = []
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(JARATOK_FILE):
                with open(JARATOK_FILE, 'r') as jf:
                    jaratok = json.load(jf)
                    for j in jaratok:
                        if j['tipus'] == "Belfoldi":
                            self.jaratok.append(BelfoldiJarat(j['jaratszam'], j['celallomas'], j['jegyar']))
                        elif j['tipus'] == "Nemzetkozi":
                            self.jaratok.append(NemzetkoziJarat(j['jaratszam'], j['celallomas'], j['jegyar']))
            if os.path.exists(FOGLALASOK_FILE):
                with open(FOGLALASOK_FILE, 'r') as ff:
                    foglalasok = json.load(ff)
                    for f in foglalasok:
                        self.foglalasok.append(JegyFoglalas(f['utas_nev'], f['jaratszam']))
        except Exception as e:
            print(f"Hiba betöltéskor: {e}")

    def save_data(self):
        try:
            with open(JARATOK_FILE, 'w') as jf:
                jaratok = []
                for j in self.jaratok:
                    tipus = "Belfoldi" if isinstance(j, BelfoldiJarat) else "Nemzetkozi"
                    jaratok.append({
                        "tipus": tipus,
                        "jaratszam": j.jaratszam,
                        "celallomas": j.celallomas,
                        "jegyar": j.jegyar
                    })
                json.dump(jaratok, jf, indent=4)

            with open(FOGLALASOK_FILE, 'w') as ff:
                foglalasok = [f.to_dict() for f in self.foglalasok]
                json.dump(foglalasok, ff, indent=4)
        except Exception as e:
            print(f"Hiba mentéskor: {e}")

    def foglalas(self, utas_nev, jaratszam):
        for jarat in self.jaratok:
            if jarat.jaratszam == jaratszam:
                self.foglalasok.append(JegyFoglalas(utas_nev, jaratszam))
                self.save_data()
                return jarat.jegyar
        return None

    def lemondas(self, utas_nev, jaratszam):
        for f in self.foglalasok:
            if f.utas_nev == utas_nev and f.jaratszam == jaratszam:
                self.foglalasok.remove(f)
                self.save_data()
                return True
        return False

    def listaz_foglalasok(self):
        return [f"{f.utas_nev} - {f.jaratszam}" for f in self.foglalasok]

    def listaz_jaratok(self):
        return [j.info() for j in self.jaratok]

def gui():
    def foglalas():
        nev = simpledialog.askstring("Foglalás", "Név:")
        jaratszam = simpledialog.askstring("Foglalás", "Járatszám:")
        if not nev or not jaratszam:
            messagebox.showerror("Hiba", "Minden mezőt ki kell tölteni!")
            return
        ar = airline.foglalas(nev, jaratszam)
        if ar:
            messagebox.showinfo("Siker", f"Foglalás sikeres! Ár: {ar} Ft")
        else:
            messagebox.showerror("Hiba", "Nincs ilyen járat.")

    def lemondas():
        nev = simpledialog.askstring("Lemondás", "Név:")
        jaratszam = simpledialog.askstring("Lemondás", "Járatszám:")
        if not nev or not jaratszam:
            messagebox.showerror("Hiba", "Minden mezőt ki kell tölteni!")
            return
        if airline.lemondas(nev, jaratszam):
            messagebox.showinfo("Siker", "Foglalás törölve.")
        else:
            messagebox.showerror("Hiba", "Foglalás nem található.")

    def listaz_foglalasok():
        foglalasok = airline.listaz_foglalasok()
        if foglalasok:
            messagebox.showinfo("Foglalások", '\n'.join(foglalasok))
        else:
            messagebox.showinfo("Foglalások", "Nincsenek foglalások.")

    def listaz_jaratok():
        jaratok = airline.listaz_jaratok()
        if jaratok:
            messagebox.showinfo("Járatok", '\n'.join(jaratok))
        else:
            messagebox.showinfo("Járatok", "Nincsenek elérhető járatok.")

    root = tk.Tk()
    root.title("Repülőjegy Foglalási Rendszer")
    root.geometry("400x400")

    tk.Label(root, text="Repülőjegy Foglalási Rendszer", font=("Helvetica", 16)).pack(pady=20)
    tk.Button(root, text="Jegy Foglalása", width=30, command=foglalas).pack(pady=5)
    tk.Button(root, text="Foglalás Lemondása", width=30, command=lemondas).pack(pady=5)
    tk.Button(root, text="Foglalások Listázása", width=30, command=listaz_foglalasok).pack(pady=5)
    tk.Button(root, text="Járatok Listázása", width=30, command=listaz_jaratok).pack(pady=5)
    tk.Button(root, text="Kilépés", width=30, command=root.quit).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(LEGITARSASAG_FILE, 'w') as lf:
        lf.write("PythonAir")

    airline = LegiTarsasag("PythonAir")
    print("Program elindult")
    print(f"Betöltött járatok száma: {len(airline.jaratok)}")

    if not airline.jaratok:
        airline.jaratok = [
            BelfoldiJarat("HUN123", "Budapest", 15000),
            BelfoldiJarat("HUN456", "Debrecen", 12000),
            NemzetkoziJarat("INT789", "Berlin", 60000)
        ]
        airline.save_data()

    print("GUI indul...")
    gui()
