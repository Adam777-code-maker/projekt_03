"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Adam Směšný

email: adamsmesny@email.cz

discord: adams._25049

"""

import requests
from bs4 import BeautifulSoup
import csv

def nacti_url(url):
    """Načte HTML obsah dané stránky."""
    odpoved = requests.get(url)
    if odpoved.status_code == 200:
        return BeautifulSoup(odpoved.content, "html.parser")
    else:
        raise ConnectionError(f"Chyba pri nacteni stranky {url} (HTTP {odpoved.status_code})")

def vycisti_cislo(hodnota):
    """Prevede cislo z formatu '1 000,00' na float/int."""
    hodnota = hodnota.replace("\xa0", "").replace(",", ".").strip()
    return float(hodnota) if "." in hodnota else int(hodnota)

def extrahuj_odkazy_na_obce(hlavni_url):
    """Extrahuje odkazy na vsechny obce na strance, i kdyz jsou v ruznych sloupcich a tabulkach."""
    soup = nacti_url(hlavni_url)
    tabulky = soup.find_all("table", class_="table")

    if not tabulky:
        raise ValueError("Chyba: Nepodarilo se najit tabulky se seznamem obci.")

    odkazy = []
    for tabulka in tabulky:
        for radek in tabulka.find_all("tr")[2:]:  # Preskocime hlavicku
            bunky = radek.find_all("td")
            if len(bunky) < 2:
                continue  # Preskocime neplatne radky

            # Zpracujeme vsechny sloupce, ne jen prvni
            for i in range(0, len(bunky), 3):  # Pocitame se tremi sloupci: cislo obce, nazev, odkaz na okrsky
                if i + 1 >= len(bunky):  # Overime, ze existuje dostatek bunek
                    continue
                kod = bunky[i].text.strip()
                nazev = bunky[i+1].text.strip()
                odkaz = bunky[i].find("a")
                
                if odkaz:
                    relativni_url = odkaz["href"]
                    plna_url = f"https://www.volby.cz/pls/ps2017nss/{relativni_url}"
                    odkazy.append({"kod": kod, "nazev": nazev, "url": plna_url})

    return odkazy

def extrahuj_vysledky_voleb(obec_url):
    """Extrahuje volebni vysledky pro danou obec."""
    soup = nacti_url(obec_url)

    # Extrakce statistickych udaju
    statisticka_tabulka = soup.find("table", {"id": "ps311_t1"})
    if not statisticka_tabulka:
        raise ValueError("Chyba: Nepodarilo se najit tabulku se statistickymi udaji.")

    statisticke_radky = statisticka_tabulka.find_all("tr")
    if len(statisticke_radky) <= 2:
        raise ValueError("Chyba: Tabulka se statistickymi udaji neobsahuje ocekavany pocet radku.")

    statisticky_radek = statisticke_radky[2]
    bunky = statisticky_radek.find_all("td")
    if len(bunky) < 8:
        raise ValueError("Chyba: Radek ve statisticke tabulce neobsahuje ocekavany pocet bunek.")

    registrovani = vycisti_cislo(bunky[3].text)
    obalky = vycisti_cislo(bunky[4].text)
    platne = vycisti_cislo(bunky[7].text)

    # Extrakce vysledku stran
    vysledky_stran = {}
    tabulky_stran = soup.find_all("table", class_="table")

    for tabulka in tabulky_stran:
        radky = tabulka.find_all("tr")[2:]  # Preskocime prvni dva radky (hlavicky)
        if not radky:
            print("Upozorneni: Tabulka neobsahuje zadne radky s daty.")
            continue

        for radek in radky:
            bunky = radek.find_all("td")
            if len(bunky) < 3:  # Pokud neni dostatek bunek, preskocime tento radek
                print("Upozorneni: Radek neobsahuje ocekavany pocet bunek.")
                continue

            nazev_strany = bunky[1].text.strip()
            if nazev_strany == "1":  # Ignorujeme sloupec "1"
                continue

            hlasy = vycisti_cislo(bunky[2].text)
            vysledky_stran[nazev_strany] = hlasy

    return {
        "registrovani": registrovani,
        "obalky": obalky,
        "platne": platne,
        "strany": vysledky_stran
    }

def uloz_do_csv(vystupni_soubor, data):
    """Ulozi vysledky voleb do CSV s oddelovacem strednikem."""
    strany = list(data[0]["strany"].keys())

    hlavicka = ["kod", "obec", "registrovani", "obalky", "platne"] + strany

    with open(vystupni_soubor, "w", newline="", encoding="utf-8-sig") as f:
        zapisovac = csv.writer(f, delimiter=";")
        zapisovac.writerow(hlavicka)

        for zaznam in data:
            radek = [
                zaznam["kod"],
                zaznam["obec"],
                zaznam["registrovani"],
                zaznam["obalky"],
                zaznam["platne"]
            ] + [zaznam["strany"].get(strana, 0) for strana in strany]
            zapisovac.writerow(radek)

def hlavni():
    """Hlavni funkce pro scraping."""
    url = input("Zadejte URL pro scraping: ").strip()
    vystupni_soubor = input("Zadejte nazev vystupniho CSV souboru (napr. vysledky.csv): ").strip()

    print(f"\nZpracovavam data z URL: {url}")
    
    try:
        obce = extrahuj_odkazy_na_obce(url)
        vsechny_vysledky = []

        for obec in obce:
            print(f"Zpracovavam obec: {obec['nazev']} (kod: {obec['kod']})")
            try:
                vysledek = extrahuj_vysledky_voleb(obec["url"])
                vysledek["kod"] = obec["kod"]
                vysledek["obec"] = obec["nazev"]
                vsechny_vysledky.append(vysledek)
            except Exception as e:
                print(f"Chyba pri zpracovani obce {obec['nazev']}: {e}")

        uloz_do_csv(vystupni_soubor, vsechny_vysledky)
        print(f"\nVysledky byly uspesne ulozeny do souboru {vystupni_soubor}")

    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    hlavni()
