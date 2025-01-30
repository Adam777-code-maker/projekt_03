import requests
from bs4 import BeautifulSoup
import csv

def načti_url(url):
    """Načte HTML obsah dané stránky."""
    odpověď = requests.get(url)
    if odpověď.status_code == 200:
        return BeautifulSoup(odpověď.content, "html.parser")
    else:
        raise ConnectionError(f"❌ Chyba při načítání stránky {url} (HTTP {odpověď.status_code})")

def vyčisti_číslo(hodnota):
    """Převede číslo z formátu '1 000,00' na float/int."""
    hodnota = hodnota.replace("\xa0", "").replace(",", ".").strip()
    return float(hodnota) if "." in hodnota else int(hodnota)

def extrahuj_odkazy_na_obce(hlavní_url):
    """Extrahuje odkazy na všechny obce na stránce, i když jsou v různých sloupcích a tabulkách."""
    soup = načti_url(hlavní_url)
    tabulky = soup.find_all("table", class_="table")  # Najdeme všechny tabulky

    if not tabulky:
        raise ValueError("❌ Chyba: Nepodařilo se najít tabulky se seznamem obcí.")

    odkazy = []
    for tabulka in tabulky:
        for řádek in tabulka.find_all("tr")[2:]:  # Přeskočíme hlavičku
            buňky = řádek.find_all("td")
            if len(buňky) < 2:
                continue  # Přeskočíme neplatné řádky

            # Zpracujeme všechny sloupce, ne jen první
            for i in range(0, len(buňky), 3):  # Počítáme se třemi sloupci: číslo obce, název, odkaz na okrsky
                if i + 1 >= len(buňky):  # Ověříme, že existuje dostatek buněk
                    continue
                kód = buňky[i].text.strip()
                název = buňky[i+1].text.strip()
                odkaz = buňky[i].find("a")
                
                if odkaz:
                    relativní_url = odkaz["href"]
                    plná_url = f"https://www.volby.cz/pls/ps2017nss/{relativní_url}"
                    odkazy.append({"kód": kód, "název": název, "url": plná_url})

    return odkazy

def extrahuj_výsledky_voleb(obec_url):
    """Extrahuje volební výsledky pro danou obec."""
    soup = načti_url(obec_url)

    # 📊 Extrakce statistických údajů
    statistická_tabulka = soup.find("table", {"id": "ps311_t1"})
    if not statistická_tabulka:
        raise ValueError("❌ Chyba: Nepodařilo se najít tabulku se statistickými údaji.")

    statistický_řádek = statistická_tabulka.find_all("tr")[2]
    buňky = statistický_řádek.find_all("td")

    registrovaní = vyčisti_číslo(buňky[3].text)
    obálky = vyčisti_číslo(buňky[4].text)
    platné = vyčisti_číslo(buňky[7].text)

    # 📊 Extrakce výsledků stran
    výsledky_stran = {}
    tabulky_stran = soup.find_all("table", class_="table")

    for tabulka in tabulky_stran:
        for řádek in tabulka.find_all("tr")[2:]:
            buňky = řádek.find_all("td")
            if len(buňky) < 3:
                continue

            název_strany = buňky[1].text.strip()
            hlasy = vyčisti_číslo(buňky[2].text)
            výsledky_stran[název_strany] = hlasy

    return {
        "registrovaní": registrovaní,
        "obálky": obálky,
        "platné": platné,
        "strany": výsledky_stran
    }

def ulož_do_csv(výstupní_soubor, data):
    """Uloží výsledky voleb do CSV s oddělovačem středníkem."""
    strany = list(data[0]["strany"].keys())

    hlavička = ["kód", "obec", "registrovaní", "obálky", "platné"] + strany

    with open(výstupní_soubor, "w", newline="", encoding="utf-8-sig") as f:
        zapisovač = csv.writer(f, delimiter=";")
        zapisovač.writerow(hlavička)

        for záznam in data:
            řádek = [
                záznam["kód"],
                záznam["obec"],
                záznam["registrovaní"],
                záznam["obálky"],
                záznam["platné"]
            ] + [záznam["strany"].get(strana, 0) for strana in strany]
            zapisovač.writerow(řádek)

def hlavní():
    """Hlavní funkce pro scraping."""
    url = input("🔗 Zadejte URL pro scraping: ").strip()
    výstupní_soubor = input("💾 Zadejte název výstupního CSV souboru (např. vysledky.csv): ").strip()

    print(f"\n📌 Zpracovávám data z URL: {url}")
    
    try:
        obce = extrahuj_odkazy_na_obce(url)
        všechny_výsledky = []

        for obec in obce:
            print(f"📍 Zpracovávám obec: {obec['název']} (kód: {obec['kód']})")
            try:
                výsledek = extrahuj_výsledky_voleb(obec["url"])
                výsledek["kód"] = obec["kód"]
                výsledek["obec"] = obec["název"]
                všechny_výsledky.append(výsledek)
            except Exception as e:
                print(f"❌ Chyba při zpracování obce {obec['název']}: {e}")

        ulož_do_csv(výstupní_soubor, všechny_výsledky)
        print(f"\n✅ Výsledky byly úspěšně uloženy do souboru {výstupní_soubor}")

    except Exception as e:
        print(f"❌ Chyba: {e}")

if __name__ == "__main__":
    hlavní()
