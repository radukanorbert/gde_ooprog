#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# Mappa és fájlnevek definiálása az adatok tárolására
DATA_DIR = "data"
JARATOK_FILE = os.path.join(DATA_DIR, "jaratok.txt")
FOGLALASOK_FILE = os.path.join(DATA_DIR, "foglalasok.txt")
LEGITARSASAG_FILE = os.path.join(DATA_DIR, "legitarsasag.txt")

# Járat osztály - egy járat alapvető adatait tárolja
class Jarat:
    def __init__(self, jaratszam, celallomas, jegyar, tipus):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = int(jegyar)
        self.tipus = tipus

    def __str__(self):
        return f"{self.tipus},{self.jaratszam},{self.celallomas},{self.jegyar}"

# JegyFoglalas osztály - egy foglalás adatait tárolja
class JegyFoglalas:
    def __init__(self, utas_nev, jaratszam):
        self.utas_nev = utas_nev
        self.jaratszam = jaratszam

    def __str__(self):
        return f"{self.utas_nev},{self.jaratszam}"

# LegiTarsasag osztály - a légitársaság járatait és foglalásait kezeli
class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []
        self.foglalasok = []
        self.load_data()  # Adatok betöltése fájlokból

    def load_data(self):
        # Járatok betöltése fájlból
        if os.path.exists(JARATOK_FILE):
            with open(JARATOK_FILE, 'r') as f:
                for line in f:
                    tipus, szam, cel, ar = line.strip().split(',')
                    self.jaratok.append(Jarat(szam, cel, ar, tipus))

        # Foglalások betöltése fájlból
        if os.path.exists(FOGLALASOK_FILE):
            with open(FOGLALASOK_FILE, 'r') as f:
                for line in f:
                    nev, szam = line.strip().split(',')
                    self.foglalasok.append(JegyFoglalas(nev, szam))

    def save_data(self):
        # Járatok mentése fájlba
        with open(JARATOK_FILE, 'w') as f:
            for j in self.jaratok:
                f.write(str(j) + '\n')

        # Foglalások mentése fájlba
        with open(FOGLALASOK_FILE, 'w') as f:
            for foglalas in self.foglalasok:
                f.write(str(foglalas) + '\n')

    # Új foglalás hozzáadása
    def foglalas(self, utas_nev, jaratszam):
        for jarat in self.jaratok:
            if jarat.jaratszam == jaratszam:
                self.foglalasok.append(JegyFoglalas(utas_nev, jaratszam))
                self.save_data()  # Módosítás mentése
                return jarat.jegyar
        return None

    # Foglalás törlése
    def lemondas(self, utas_nev, jaratszam):
        for f in self.foglalasok:
            if f.utas_nev == utas_nev and f.jaratszam == jaratszam:
                self.foglalasok.remove(f)
                self.save_data()  # Módosítás mentése
                return True
        return False

    # Foglalások listázása
    def listaz_foglalasok(self):
        return [f"{f.utas_nev} - {f.jaratszam}" for f in self.foglalasok]

# Grafikus felület létrehozása

def gui():
    # Jegy foglalása funkció
    def foglalas():
        nev = simpledialog.askstring("Foglalás", "Név:")
        jaratszam = simpledialog.askstring("Foglalás", "Járatszám:")
        ar = airline.foglalas(nev, jaratszam)
        if ar:
            messagebox.showinfo("Siker", f"Foglalás sikeres! Ár: {ar} Ft")
        else:
            messagebox.showerror("Hiba", "Nincs ilyen járat.")

    # Foglalás lemondása funkció
    def lemondas():
        nev = simpledialog.askstring("Lemondás", "Név:")
        jaratszam = simpledialog.askstring("Lemondás", "Járatszám:")
        if airline.lemondas(nev, jaratszam):
            messagebox.showinfo("Siker", "Foglalás törölve.")
        else:
            messagebox.showerror("Hiba", "Foglalás nem található.")

    # Foglalások megjelenítése
    def listaz():
        foglalasok = airline.listaz_foglalasok()
        if foglalasok:
            messagebox.showinfo("Foglalások", '\n'.join(foglalasok))
        else:
            messagebox.showinfo("Foglalások", "Nincsenek foglalások.")

    # GUI ablak létrehozása
    root = tk.Tk()
    root.title("Repülőjegy Foglalási Rendszer")

    # Gombok hozzáadása a GUI-hoz
    tk.Button(root, text="Jegy Foglalása", width=30, command=foglalas).pack(pady=10)
    tk.Button(root, text="Foglalás Lemondása", width=30, command=lemondas).pack(pady=10)
    tk.Button(root, text="Foglalások Listázása", width=30, command=listaz).pack(pady=10)
    tk.Button(root, text="Kilépés", width=30, command=root.quit).pack(pady=10)

    root.mainloop()

# Főprogram belépési pontja
if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)  # Data mappa létrehozása, ha nem létezik
    
    # Légitársaság nevének fájlba írása
    with open(LEGITARSASAG_FILE, 'w') as f:
        f.write("PythonAir")

    # Légitársaság példányosítása
    airline = LegiTarsasag("PythonAir")

    # Alapértelmezett járatok betöltése, ha még nincsenek mentve
    if not airline.jaratok:
        airline.jaratok = [
            Jarat("HUN123", "Budapest", 15000, "Belfoldi"),
            Jarat("HUN456", "Debrecen", 12000, "Belfoldi"),
            Jarat("INT789", "Berlin", 60000, "Nemzetkozi")
        ]
        airline.save_data()

    # GUI elindítása
    gui()