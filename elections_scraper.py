"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Adam Směšný

email: adamsmesny@email.cz

discord: adams._25049

"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

def nacti_url(url):
    odpoved = requests.get(url)
    if odpoved.status_code == 200:
        return BeautifulSoup(odpoved.content, "html.parser")
    else:
        raise ConnectionError(f"Chyba pri nacitani stranky {url} (HTTP {odpoved.status_code})")

def vycisti_cislo(hodnota):
    """Prevede cislo z formatu '1 000,00' nebo '-' na int/float nebo 0"""
    hodnota = hodnota.replace("\xa0", "").replace(",", ".").strip()
    if hodnota in ["-", ""]:
        return 0
    return float(hodnota) if "." in hodnota else int(hodnota)

def extrahuj_odkazy_na_obce(hlavni_url):
    soup = nacti_url(hlavni_url)
    odkazy = []
    tabulky = soup.find_all("table", class_="table")

    for tabulka in tabulky:
        for radek in tabulka.find_all("tr")[2:]:
            bunky = radek.find_all("td")
            for i in range(0, len(bunky), 3):
                if i + 1 >= len(bunky):
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
    soup = nacti_url(obec_url)
    statisticka_tabulka = soup.find("table", {"id": "ps311_t1"})
    statisticky_radek = statisticka_tabulka.find_all("tr")[2]
    bunky = statisticky_radek.find_all("td")
    registrovani = vycisti_cislo(bunky[3].text)
    obalky = vycisti_cislo(bunky[4].text)
    platne = vycisti_cislo(bunky[7].text)

    vysledky_stran = {}
    tabulky_stran = soup.find_all("table", class_="table")

    for tabulka in tabulky_stran:
        radky = tabulka.find_all("tr")[2:]
        for radek in radky:
            bunky = radek.find_all("td")
            if len(bunky) < 3:
                continue

            nazev_strany = bunky[1].text.strip()
            if not nazev_strany or nazev_strany in ["-", "0", "1"] or nazev_strany.isdigit():
                continue
            if not any(c.isalpha() for c in nazev_strany):
                continue

            hlasy = vycisti_cislo(bunky[2].text)
            vysledky_stran[nazev_strany] = hlasy

    return {
        "registrovani": registrovani,
        "obalky": obalky,
        "platne": platne,
        "strany": vysledky_stran
    }

def uloz_do_csv(soubor, data):
    strany = list(data[0]["strany"].keys())
    hlavicka = ["kod", "obec", "registrovani", "obalky", "platne"] + strany

    with open(soubor, "w", newline="", encoding="utf-8-sig") as f:
        zapisovac = csv.writer(f, delimiter=";")
        zapisovac.writerow(hlavicka)
        for zaznam in data:
            radek = [zaznam["kod"], zaznam["obec"], zaznam["registrovani"], zaznam["obalky"], zaznam["platne"]]
            radek += [zaznam["strany"].get(strana, 0) for strana in strany]
            zapisovac.writerow(radek)

def main():
    if len(sys.argv) != 3:
        print("Chyba: Musíš zadat 2 argumenty: <URL> <výstupní_soubor.csv>")
        sys.exit(1)

    url = sys.argv[1]
    vystupni_soubor = sys.argv[2]

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
        print(f"\nHotovo! Data ulozena v souboru {vystupni_soubor}")

    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    main()