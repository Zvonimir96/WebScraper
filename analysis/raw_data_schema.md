# raw_data Schema — Willhaben Apartments

Baza: `data/apartments.db` | Tablica: `apartments` | Ukupno: **2550 stanova**  
Kolona `raw_data` sadrži JSON s **~80 korisnih ključeva** (od 1967 ukupno — ostatak su unikatni naslovi oglasa).

---

## 1. Osnovni podaci (93–100%)

| Ključ | Popunjenost | Tip | Opis | Primjer |
|---|---|---|---|---|
| `url` | 100% | str | Link na oglas | `https://www.willhaben.at/iad/immobilien/d/...` |
| `id` | 100% | str | Willhaben ID | `1990832403` |
| `uuid` | 100% | str | UUID oglasa | `e32649a3-8c35-...` |
| `description` | 100% | str | Naslov oglasa | `Traumhafte 2-Zimmer-Gartenwohnung in Ruhelage` |
| `OWNAGETYPE` | 100% | str | Tip vlasništva | `Kauf` |
| `PRICE` | 100% | str | Cijena (numerički) | `180000` |
| `PRICE_FOR_DISPLAY` | 100% | str | Cijena (formatirano) | `€ 180.000` |
| `PROPERTY_TYPE` | 96% | str | Tip nekretnine | `Wohnung`, `Erdgeschoßwohnung`, `Penthousewohnung`, `Maisonette` |
| `PROPERTY_TYPE_ID` | 96% | str | ID tipa | `105`, `3` |
| `NO_OF_ROOMS` | 93% | str | Broj soba | `2`, `3,5` |
| `ESTATE_SIZE/LIVING_AREA` | 90% | str | Stambena površina (m²) | `44,5` |
| `ESTATE_SIZE` | 29% | str | Ukupna površina | `65` |
| `ESTATE_SIZE/USEABLE_AREA` | 14% | str | Korisna površina | `65` |
| `ESTATE_SIZE/GROSS_AREA` | 2% | str | Bruto površina | `65` |

## 2. Lokacija (59–97%)

| Ključ | Popunjenost | Tip | Opis | Primjer |
|---|---|---|---|---|
| `LOCATION/ADDRESS_1` | 59% | str | Ulica i broj | `Fontanestraße 8` |
| `LOCATION/ADDRESS_2` | 97% | str | Četvrt | `Wetzelsdorf` |
| `LOCATION/ADDRESS_3` | 97% | str | Grad | `Graz` |
| `LOCATION/ADDRESS_4` | 97% | str | Pokrajina | `Steiermark` |
| `COORDINATES` | 77% | str | GPS (lat,lon) | `47.051823,15.399733` |
| `AREA_ID` | 100% | str | Willhaben zona | `117467` |
| `REGION_AREA_ID` | 100% | str | Willhaben regija | `601` |
| `advertAddressDetails` | 97% | dict | Strukturirana adresa | `{postalCode, postalName, addressLines}` |
| `POSITION_RADIUS_METERS` | 15% | str | Radijus preciznosti GPS-a | `337` |

## 3. Energetika (51–86%)

| Ključ | Popunjenost | Tip | Opis | Primjer |
|---|---|---|---|---|
| `ENERGY_HWB` | 86% | str | Heizwärmebedarf (kWh/m²a) | `41,22` |
| `ENERGY_HWB_CLASS` | 72% | str | HWB klasa | `B`, `C`, `A` |
| `ENERGY_FGEE` | 70% | str | Gesamtenergieeffizienz | `0,64` |
| `ENERGY_FGEE_CLASS` | 51% | str | FGEE klasa | `A+`, `C` |
| `HEATING` | 70% | str | Tip grijanja | `Fernwärme`, `Zentralheizung`, `Fußbodenheizung` |

## 4. Zgrada (48–73%)

| Ključ | Popunjenost | Tip | Opis | Primjer |
|---|---|---|---|---|
| `BUILDING_CONDITION` | 73% | str | Stanje | `Neuwertig`, `Erstbezug`, `Renoviert`, `Sanierungsbedürftig` |
| `FLOOR` | 68% | str | Kat | `2`, `0`, `EG` |
| `BUILDING_TYPE` | 61% | str | Tip gradnje | `Neubau`, `Altbau` |
| `FLOOR_SURFACE` | 60% | str | Tip poda | `Parkett`, `Laminat`, `Fliesen` |
| `CONSTRUCTION_YEAR` | 48% | str | Godina gradnje | `2018`, `1999` |

## 5. Oprema i slobodne površine (73–95%)

| Ključ | Popunjenost | Tip | Opis | Primjer |
|---|---|---|---|---|
| `ESTATE_PREFERENCE` | 94% | list/str | Lista opreme | `['Einbauküche', 'Keller', 'Parkplatz']` |
| `FREE_AREA/FREE_AREA_TYPE` | 84% | list/str | Tipovi slobodnih površina | `['Terrasse', 'Garten']`, `Balkon` |
| `FREE_AREA/FREE_AREA_AREA` | 73% | list/str | Veličine (m²) | `['15,5', '32']` |
| `FREE_AREA/FREE_AREA_TYPE_AND_AREA` | 84% | list/str | Tip + veličina | `['Garten 32 m²', 'Terrasse 15,5 m²']` |
| `Ausstattung` | 75% | dict | Detaljna oprema | `{Terrassenanzahl, Bad mit Dusche, Einbauküche, Boden, Heizungsart, Möblierung...}` |
| `Flächen` | 34% | dict | Površine | `{Gesamtfläche, Gartenfläche, Kellerfläche}` |

## 6. Cijena — detalji (22–65%)

| Ključ | Popunjenost | Tip | Opis | Primjer |
|---|---|---|---|---|
| `Preis - Detailinformation` | 65% | dict | Troškovi | `{Nebenkosten, monatliche Kosten, Rücklage}` |
| `ADDITIONAL_COST/FEE` | 58% | str | Provizija | `3 % zzgl. 20% MwSt. vom Gesamtkaufpreis` |
| `ESTATE_PRICE/PRICE_SUGGESTION` | 95% | str | Predložena cijena | `180000` |
| `ESTATE_PRICE/MONTHCOSTS_GROSS` | 22% | str | Mjesečni troškovi bruto | `142,9` |
| `ESTATE_PRICE/HEATINGCOSTSNET` | 12% | str | Troškovi grijanja neto | `88,3` |
| `ESTATE_PRICE/PRICE_DESCRIPTION` | 23% | str | Opis cijene (free text) | `KP ist brutto inklusive TG...` |
| `OLD_PRICE` | 8% | str | Stara cijena (sniženje) | `305000` |
| `ADDITIONAL_COST/AMOUNT` | 8% | str | Iznos provizije | `94,29` |

## 7. Datumi (100%)

| Ključ | Popunjenost | Tip | Opis | Primjer |
|---|---|---|---|---|
| `createdDate` | 100% | str | Datum kreiranja | `2026-02-05T17:32:00+0100` |
| `changedDate` | 100% | str | Zadnja izmjena | `2026-03-12T17:35:00+0100` |
| `publishedDate` | 100% | str | Datum objave | `2026-03-12T17:33:00+0100` |
| `AVAILABLE_NOW` | 31% | str | Dostupnost | `ab sofort` |
| `AVAILABLE_DATE` | 29% | str | Datum dostupnosti | `16.03.2026` |
| `AVAILABLE_DATE_FREETEXT` | 28% | str | Dostupnost (free text) | `nach Vereinbarung`, `2 Quartal 2026` |

## 8. Kontakt / Agencija (80–93%)

| Ključ | Popunjenost | Tip | Opis | Primjer |
|---|---|---|---|---|
| `CONTACT/COMPANY` | 93% | str | Tvrtka | `Reichert Immobilien GmbH` |
| `CONTACT/COMPANYNAME` | 80% | str | Puni naziv | `Raiffeisen-Immobilien Steiermark GmbH` |
| `CONTACT/NAME` | 92% | str | Kontakt osoba | `Elisabeth Preitler` |
| `CONTACT/PHONE` | 93% | str | Telefon | `00436766215664` |
| `CONTACT/PHONE2` | 35% | str | Drugi telefon | `0043316803622700` |
| `CONTACT/URL` | 93% | list/str | Web stranica | `['https://www.reichert-immobilien.at']` |
| `CONTACT/ADDRESS_STREET` | 93% | str | Adresa agencije | `Quergasse 5/EG` |
| `CONTACT/ADDRESS_POSTCODE` | 93% | str | Poštanski broj | `8020` |
| `CONTACT/ADDRESS_TOWN` | 93% | str | Grad agencije | `Graz` |
| `ISPRIVATE` | 100% | str | Privatni oglas? | `0` (ne), `1` (da) |
| `DEALER` | 100% | str | Dealer? | `1` |

## 9. Projekt / Novogradnja (37–43%)

Prisutno samo kod stanova koji su dio većeg projekta.

| Ključ | Popunjenost | Tip | Opis | Primjer |
|---|---|---|---|---|
| `PROJECT_ID` | 39% | str | ID projekta | `1404793927` |
| `PROJECT_NAME` | 39% | str | Naziv projekta | `JAKOMINI VERDE` |
| `PROJECT/UNIT_COUNT_BUY` | 42% | str | Broj stanova za kupnju | `74` |
| `PROJECT/UNIT_PRICE_FROM` | 41% | str | Cijena od | `175000` |
| `PROJECT/UNIT_PRICE_TO` | 37% | str | Cijena do | `481000` |
| `PROJECT/UNIT_SIZE_FROM` | 43% | str | Površina od (m²) | `33,05` |
| `PROJECT/UNIT_SIZE_TO` | 43% | str | Površina do (m²) | `92,46` |
| `PROJECT/STATUS` | 37% | str | Status | `In Bau/Planung` |
| `PROJECT/FINISHED_BY` | 10% | str | Završetak | `01.07.2027` |
| `PROJECT/UNIT_CONFIGURATION_LEVEL` | 6% | str | Razina opreme | `Schlüsselfertig` |
| `UNIT_NUMBER` | 37% | str | Oznaka stana | `A1-09` |
| `UNIT_TITLE` | 37% | str | Naslov jedinice | `Etage 1/Top A1-09` |

## 10. Ugniježđeni dict-ovi (bogati podaci)

### `Zusatzinformationen` (76%)
Sadrži: Anzahl Etagen, Anzahl Badezimmer, Anzahl Stellplätze, Anzahl Wohneinheiten, Stellplatz (CARPORT/Tiefgarage), Gartennutzung, Energiepass gültig bis, Verfügbar ab...

### `Lage` (68%)
Sadrži: Laermbelastung (buka), Verkehrsanbindung (javni prijevoz), opis lokacije (free text).

### `Ausstattung` (75%)
Sadrži: Terrassenanzahl, Fläche Balkon/Terrassen, Bad mit Dusche/Wanne, Einbauküche, Boden, Heizung, Heizungsart, Möblierung...

### `Preis - Detailinformation` (65%)
Sadrži: Nebenkosten, monatliche Kosten (exkl./inkl. MWSt), Rücklage (exkl. MWSt).

### `Flächen` (34%)
Sadrži: Gesamtfläche, Gartenfläche, Kellerfläche, Balkonfläche...

### `Sonstiges` (23%)
Sadrži: einmalige Kaufnebenkosten (porez, notar, provizija).

---

## Korištenje s pandas

```python
import sqlite3, json
import pandas as pd

conn = sqlite3.connect('data/apartments.db')
df = pd.read_sql_query("SELECT * FROM apartments", conn)
conn.close()

# Parsiranje raw_data
raw = df['raw_data'].apply(json.loads)

# Ekstrakcija korisnih polja
df['construction_year'] = raw.apply(lambda x: x.get('CONSTRUCTION_YEAR'))
df['floor_num'] = raw.apply(lambda x: x.get('FLOOR'))
df['floor_surface'] = raw.apply(lambda x: x.get('FLOOR_SURFACE'))
df['energy_fgee'] = raw.apply(lambda x: x.get('ENERGY_FGEE'))
df['energy_fgee_class'] = raw.apply(lambda x: x.get('ENERGY_FGEE_CLASS'))
df['property_type'] = raw.apply(lambda x: x.get('PROPERTY_TYPE'))
df['free_areas'] = raw.apply(lambda x: x.get('FREE_AREA/FREE_AREA_TYPE_AND_AREA'))
df['preferences'] = raw.apply(lambda x: x.get('ESTATE_PREFERENCE'))
df['monthly_costs'] = raw.apply(lambda x: x.get('ESTATE_PRICE/MONTHCOSTS_GROSS'))
df['project_name'] = raw.apply(lambda x: x.get('PROJECT_NAME'))

# Ekstrakcija iz ugniježđenih dict-ova
df['n_bathrooms'] = raw.apply(lambda x: (x.get('Zusatzinformationen') or {}).get('Anzahl Badezimmer'))
df['n_parking'] = raw.apply(lambda x: (x.get('Zusatzinformationen') or {}).get('Anzahl Stellplätze'))
df['noise_level'] = raw.apply(lambda x: (x.get('Lage') or {}).get('Laermbelastung') if isinstance(x.get('Lage'), dict) else None)
df['reserve_fund'] = raw.apply(lambda x: (x.get('Preis - Detailinformation') or {}).get('Rücklage (exkl. MWSt)'))
```

---

---

## District Resolver (`analysis/district_resolver.py`)

Since 64% of apartments have only "Graz" as their district (no specific neighborhood),
a nearest-centroid GPS resolver was built to fill in the missing data.

### How it works

1. Computed average GPS coordinates (centroid) for each of the 18 Graz districts
   using 711 apartments that have both a known district and GPS coordinates.
2. For any apartment with unknown district but known GPS, calculates Haversine
   distance to all centroids and assigns the nearest one.

### Accuracy

Tested against 711 apartments with known districts and coordinates:

| Metric | Value |
|---|---|
| Correct | 655/711 (92.1%) |
| Wrong | 56/711 (7.9%) |
| Avg distance to centroid | 0.81 km |
| Max distance to centroid | 4.32 km |

All 56 misclassifications are between neighboring districts:

| Actual | Predicted | Count |
|---|---|---|
| Jakomini | Sankt Leonhard | 10 |
| Eggenberg | Wetzelsdorf | 7 |
| Geidorf | Lend | 5 |
| Liebenau | Jakomini | 5 |
| Geidorf | Sankt Leonhard | 3 |
| Straßgang | Wetzelsdorf | 3 |
| Andritz | Weinitzen | 2 |
| Jakomini | Innere Stadt | 2 |
| Waltendorf | Geidorf | 2 |
| Waltendorf | Ries | 2 |
| Waltendorf | Sankt Leonhard | 2 |
| Others (1 each) | | 13 |

No cross-city errors. All mistakes occur at district boundaries.

### Coverage after resolving

| Source | Apartments |
|---|---|
| Already had district | 859 |
| Resolved from GPS | 1260 |
| No district or GPS | 365 |
| **Total with district** | **2119/2550 (83.1%)** |

### Usage

```python
from analysis.district_resolver import resolve_district

resolve_district(47.051, 15.399)                        # => "Wetzelsdorf"
resolve_district(47.070, 15.440, return_distance=True)  # => ("Innere Stadt", 0.08)
```

### Limitations

- Boundary apartments may be assigned to the wrong neighboring district
- Centroids are based on listing distribution, not official district boundaries
- For higher accuracy, use GeoJSON district polygons with point-in-polygon

---

*Generated: 2026-04-03 | Source: 2550 apartments from willhaben.at*
