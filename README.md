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

python elections_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202" vysledky_UH.csv

Průbeh stahování:
-----------------
Zpracovavam obec: Babice (kod: 592013)
Zpracovavam obec: Bánov (kod: 592021)
Zpracovavam obec: Bílovice (kod: 592030)
Zpracovavam obec: Bojkovice (kod: 592048)
Zpracovavam obec: Boršice (kod: 592064)
.
.
.
Zpracovavam obec: Vyškovec (kod: 592838)
Zpracovavam obec: Záhorovice (kod: 592846)
Zpracovavam obec: Zlámanec (kod: 592854)
Zpracovavam obec: Zlechov (kod: 592862)
Zpracovavam obec: Žítková (kod: 592871)

Hotovo! Data ulozena v souboru vysledky_uh.csv

ČÁSTEČNÝ VÝSTUP
---------------
kod	obec	registrovani	obalky	platne	Občanská demokratická strana	Řád národa - Vlastenecká unie	CESTA ODPOVĚDNÉ SPOLEČNOSTI	Česká str.sociálně demokrat.	Radostné Česko	STAROSTOVÉ A NEZÁVISLÍ	Komunistická str.Čech a Moravy	Strana zelených	ROZUMNÍ-stop migraci,diktát.EU	Strana svobodných občanů	Blok proti islam.-Obran.domova	Občanská demokratická aliance	Česká pirátská strana	Referendum o Evropské unii	TOP 09	ANO 2011	Dobrá volba 2016	SPR-Republ.str.Čsl. M.Sládka	Křesť.demokr.unie-Čs.str.lid.	REALISTÉ	SPORTOVCI	Dělnic.str.sociální spravedl.	Svob.a př.dem.-T.Okamura (SPD)	Strana Práv Občanů
592013	Babice	1452	873	866	79	0	0	60	0	55	66	5	6	3	0	2	74	0	23	254	1	0	95	5	1	0	133	4
592021	Bánov	1707	1070	1063	92	2	1	75	0	117	62	10	1	11	1	2	71	1	11	293	1	0	148	6	0	0	156	2
592030	Bílovice	1473	1018	1008	98	0	0	67	1	66	80	10	5	14	0	1	90	0	28	264	0	2	147	4	3	1	92	35
592048	Bojkovice	3635	2183	2170	290	6	0	165	1	79	225	23	7	20	1	1	134	4	37	612	0	3	208	16	1	3	322	12
592064	Boršice	1788	1141	1131	103	0	0	74	1	61	136	14	3	14	0	0	95	0	33	279	2	0	199	4	1	1	108	3
592056	Boršice u Blatnice	660	407	404	49	0	0	24	0	13	59	1	3	8	0	0	25	1	9	95	0	2	73	1	1	0	39	1

