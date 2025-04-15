import tkinter as tk
from tkinter import messagebox, simpledialog
import os

DATA_DIR = "data"
JARATOK_FILE = os.path.join(DATA_DIR, "jaratok.txt")
FOGLALASOK_FILE = os.path.join(DATA_DIR, "foglalasok.txt")
LEGITARSASAG_FILE = os.path.join(DATA_DIR, "legitarsasag.txt")

class Jarat:
    def __init__(self, jaratszam, celallomas, jegyar, tipus):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = int(jegyar)
        self.tipus = tipus

    def __str__(self):
        return f"{self.tipus},{self.jaratszam},{self.celallomas},{self.jegyar}"

class JegyFoglalas:
    def __init__(self, utas_nev, jaratszam):
        self.utas_nev = utas_nev
        self.jaratszam = jaratszam

    def __str__(self):
        return f"{self.utas_nev},{self.jaratszam}"

class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []
        self.foglalasok = []
        self.load_data()

    def load_data(self):
        if os.path.exists(JARATOK_FILE):
            with open(JARATOK_FILE, 'r') as jf:
                for line in jf:
                    tipus, szam, cel, ar = line.strip().split(',')
                    self.jaratok.append(Jarat(szam, cel, ar, tipus))

        if os.path.exists(FOGLALASOK_FILE):
            with open(FOGLALASOK_FILE, 'r') as ff:
                for line in ff:
                    nev, szam = line.strip().split(',')
                    self.foglalasok.append(JegyFoglalas(nev, szam))

    def save_data(self):
        with open(JARATOK_FILE, 'w') as jf:
            for j in self.jaratok:
                jf.write(str(j) + '\n')

        with open(FOGLALASOK_FILE, 'w') as ff:
            for f in self.foglalasok:
                ff.write(str(f) + '\n')

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

def gui():
    def foglalas():
        nev = simpledialog.askstring("Foglalás", "Név:")
        jaratszam = simpledialog.askstring("Foglalás", "Járatszám:")
        ar = airline.foglalas(nev, jaratszam)
        if ar:
            messagebox.showinfo("Siker", f"Foglalás sikeres! Ár: {ar} Ft")
        else:
            messagebox.showerror("Hiba", "Nincs ilyen járat.")

    def lemondas():
        nev = simpledialog.askstring("Lemondás", "Név:")
        jaratszam = simpledialog.askstring("Lemondás", "Járatszám:")
        if airline.lemondas(nev, jaratszam):
            messagebox.showinfo("Siker", "Foglalás törölve.")
        else:
            messagebox.showerror("Hiba", "Foglalás nem található.")

    def listaz():
        foglalasok = airline.listaz_foglalasok()
        if foglalasok:
            messagebox.showinfo("Foglalások", '\n'.join(foglalasok))
        else:
            messagebox.showinfo("Foglalások", "Nincsenek foglalások.")

    root = tk.Tk()
    root.title("Repülőjegy Foglalási Rendszer")

    tk.Button(root, text="Jegy Foglalása", width=30, command=foglalas).pack(pady=10)
    tk.Button(root, text="Foglalás Lemondása", width=30, command=lemondas).pack(pady=10)
    tk.Button(root, text="Foglalások Listázása", width=30, command=listaz).pack(pady=10)
    tk.Button(root, text="Kilépés", width=30, command=root.quit).pack(pady=10)

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
            Jarat("HUN123", "Budapest", 15000, "Belfoldi"),
            Jarat("HUN456", "Debrecen", 12000, "Belfoldi"),
            Jarat("INT789", "Berlin", 60000, "Nemzetkozi")
        ]
        airline.save_data()

    print("GUI indul...")
    gui()