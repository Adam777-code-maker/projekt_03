# repozitar

POPIS PROJEKTU Č. 3 - ELECTIONS SCRAPER
---------------------------------------
Tento projekt slouží k extrahování výsledků z parlamentních voleb 2017. Odkaz k prohlédnutí nalaznete zde: 
https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

INSTALACE KNIHOVEN
------------------
Knihovny, které jsou použity v kódu, jsou uloženy v souboru requirements.txt. Po instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

$ pip3 --version                      # overim verzi manazeru
$ pip3 install -r requirements.txt    # nainstaluji knihovny

SPUŠTĚNÍ PROJEKTU
-----------------
1. Spouštění souboru "python elections_scraper.py" v rámci příkazového řádku, požaduje dva povinné argumenty:
2. Zadání URL pro scraping, např.: "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202"
3. Zadání názvu souboru, do kterého budou vyscrapovány výsledky. Pozor, za názvem souboru je potřeba zadat příponu ".csv", tedy např.: "vysledky_UH.csv".

Následně se Vám stáhnou výsledky, jako soubor s příponou .csv.

UKÁZKA PROJEKTU
---------------
Výsledky hlasování pro okres Uherské Hradiště:

1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202
2. argument: vysledky_UH.csv

Průbeh stahování:
-----------------
Zadejte URL pro scraping: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202
💾 Zadejte název výstupního CSV souboru (např. vysledky.csv): vysledky_UH.csv

📌 Zpracovávám data z URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202
📍 Zpracovávám obec: Babice (kód: 592013)
📍 Zpracovávám obec: Bánov (kód: 592021)
📍 Zpracovávám obec: Bílovice (kód: 592030)
📍 Zpracovávám obec: Bojkovice (kód: 592048)
📍 Zpracovávám obec: Boršice (kód: 592064)
.
.
.

Výsledky byly úspěšně uloženy do souboru vysledky_UH.csv

ČÁSTEČNÝ VÝSTUP
---------------
kód	obec	registrovaní	obálky	platné	1	Občanská demokratická strana	Řád národa - Vlastenecká unie	CESTA ODPOVĚDNÉ SPOLEČNOSTI	Česká str.sociálně demokrat.	Radostné Česko	STAROSTOVÉ A NEZÁVISLÍ
592013	Babice	1452	873	866	100.0	79	0	0	60	0	55
592021	Bánov	1707	1070	1063	0	92	2	1	75	0	117
592030	Bílovice	1473	1018	1008	0	98	0	0	67	1	66
592048	Bojkovice	3635	2183	2170	0	290	6	0	165	1	79
592064	Boršice	1788	1141	1131	0	103	0	0	74	1	61
