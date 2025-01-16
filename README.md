# FIIT STU ZS 2024/25: Klastrovanie bodov

### Téma: Implementácia aglomeratívneho klastrovacieho algoritmu

**Autor:** Martin Kvietok, Slovenská technická univerzita v Bratislave

---

## **Popis projektu**

Cieľom projektu je implementovať algoritmus na klastrovanie bodov v dvojrozmernom priestore s rozsahom súradníc od -5000 do +5000. Projekt zahŕňa:
- Generovanie 20 referenčných bodov a následných 20 000 bodov s náhodným posunom.
- Klastrovanie bodov pomocou aglomeratívneho algoritmu s využitím centroidov a medoidov.
- Grafickú vizualizáciu klastrov, kde sú zhluky farebne odlíšené a ich centrá zvýraznené.

---

## **Kľúčové koncepty**

### 1. **Aglomeratívny algoritmus**
- Hierarchická metóda klastrovania (bottom-up prístup).
- Spojovanie dvojíc klastrov na základe minimálnej euklidovskej vzdialenosti medzi stredmi klastrov.
- Proces sa opakuje, kým sa nesplnia kritériá na maximálnu vzdialenosť (500).

### 2. **Centroid**
- Reprezentuje priemernú polohu bodov v klastru (abstraktný bod).
- Citlivý na odľahlé hodnoty (outliery), ktoré môžu skresliť presnosť.

### 3. **Medoid**
- Skutočný bod v klastru, ktorý minimalizuje kumulatívnu vzdialenosť k ostatným bodom.
- Menej citlivý na odľahlé hodnoty a vhodný na homogénne klastre.

### 4. **Postup klastrovania**
1. **Inicializácia klastrov:**
   - Generovanie počiatočných bodov a priradenie bodov k príslušným klastrom.
   - Výpočet centroidov alebo medoidov.
2. **Tvorba matice vzdialeností:**
   - Matica vzdialeností medzi klastrami (len horná trojuholníková časť).
3. **Zhlukovanie klastrov:**
   - Spájanie klastrov na základe minimálnej vzdialenosti a aktualizácia matice.
   - Podmienka na maximálnu priemernú vzdialenosť medzi bodmi (500).

---

## **Finálne testovanie a výsledky**

### **Optimalizácia vzdialenosti:**
- Maximálna akceptovateľná vzdialenosť: 800 (najlepší kompromis medzi kompaktnosťou klastrov a počtom bodov).

### **Časová náročnosť:**
- Optimalizované algoritmom redukujúcim aktualizácie matice.
- Časy pre rôzne počty bodov:
  - 5 000 bodov: do 10 sekúnd.
  - 10 000 bodov: do 30 sekúnd.
  - 20 000 bodov: do 2–3 minút.

### **Porovnanie centroidov a medoidov:**
- Centroidy sú výpočtovo rýchlejšie, no menej odolné voči odľahlým bodom.
- Medoidy poskytujú homogénnejšie klastre, ale výsledky závisia od počiatočnej voľby bodov.

---

## **Použitie programu**

1. Spustite súbor `Zadanie2c_klastrovanie.py` v prostredí Visual Studio 2022.
2. Po spustení:
   - Zadajte počet bodov a metódu klastrovania (centroid/medoid).
   - Program vypíše čas výpočtov a zobrazí grafické znázornenie klastrov.

---

## **Záver**

Navrhnutý algoritmus dosahuje vysokú efektivitu pri klastrovaní veľkých množín dát. Optimalizáciou výpočtov sa podarilo výrazne znížiť časovú náročnosť. Algoritmus je vhodný na spracovanie dát s kompaktnými klastrami, pričom jeho úspech závisí od vhodne nastavených parametrov, najmä maximálnej vzdialenosti medzi bodmi.
