# Price Analysis — Graz Apartments

Data: 2550 apartments scraped from willhaben.at (March 2026).

## 1. Average Price per m² by District

Apartments with known district, price, and living area: 1867

| District | Avg €/m² | Median €/m² | Count |
|---|---:|---:|---:|
| Sankt Peter | 6,215 | 6,276 | 116 |
| Geidorf | 5,985 | 6,069 | 165 |
| Andritz | 5,807 | 5,890 | 146 |
| Waltendorf | 5,767 | 6,090 | 83 |
| Sankt Leonhard | 5,745 | 5,952 | 104 |
| Mariatrost | 5,734 | 6,510 | 70 |
| Weinitzen | 5,362 | 4,840 | 4 |
| Straßgang | 5,146 | 5,470 | 82 |
| Jakomini | 5,074 | 5,137 | 205 |
| Liebenau | 5,041 | 5,177 | 81 |
| Ries | 4,756 | 4,394 | 40 |
| Puntigam | 4,566 | 4,630 | 106 |
| Gries | 4,534 | 4,763 | 288 |
| Eggenberg | 4,319 | 4,304 | 117 |
| Gösting | 4,193 | 4,205 | 54 |
| Lend | 3,909 | 3,429 | 133 |
| Innere Stadt | 3,737 | 3,750 | 24 |
| Wetzelsdorf | 3,567 | 3,373 | 49 |
| **Graz (total)** | **5,047** | **5,032** | **1867** |

## 2. Neubau vs Altbau — Price per m² by District

Only apartments with known `building_type`: 1152 Neubau, 123 Altbau.

| District | Neubau €/m² | Neubau n | Altbau €/m² | Altbau n | Δ €/m² |
|---|---:|---:|---:|---:|---:|
| Geidorf | 6,290 | 105 | 4,873 | 6 | +1,417 |
| Sankt Peter | 6,239 | 101 | 2,980 | 1 | +3,259 |
| Sankt Leonhard | 6,218 | 65 | 5,008 | 19 | +1,211 |
| Waltendorf | 5,848 | 61 | — | — | — |
| Mariatrost | 5,770 | 37 | — | — | — |
| Andritz | 5,669 | 83 | 3,333 | 2 | +2,336 |
| Liebenau | 5,212 | 74 | — | — | — |
| Jakomini | 5,199 | 176 | 3,614 | 8 | +1,585 |
| Straßgang | 5,096 | 40 | — | — | — |
| Gries | 4,842 | 114 | 2,969 | 26 | +1,873 |
| Puntigam | 4,783 | 53 | 2,733 | 1 | +2,050 |
| Ries | 4,775 | 39 | — | — | — |
| Gösting | 4,732 | 28 | 3,328 | 4 | +1,404 |
| Weinitzen | 4,691 | 3 | — | — | — |
| Eggenberg | 4,623 | 66 | 3,096 | 14 | +1,527 |
| Lend | 4,557 | 69 | 3,166 | 26 | +1,391 |
| Innere Stadt | 3,919 | 9 | 3,624 | 11 | +295 |
| Wetzelsdorf | 3,617 | 29 | 3,445 | 5 | +172 |
| **Graz (total)** | **5,328** | **1152** | **3,569** | **123** | **+1,760** |

## 3. Parking / Garage — Price Impact

Apartments without any parking-related keyword in `ESTATE_PREFERENCE` are considered
to have no parking. This is a rough estimate — the price difference reflects both the
parking itself and the general quality of apartments that come with parking.

| Metric | With Parking (n=1246) | Without Parking (n=1030) | Difference |
|---|---:|---:|---:|
| Average price | €401,502 | €325,787 | +€75,715 |
| Median price | €339,000 | €263,212 | +€75,788 |

Note: This is not the isolated price of a parking spot. Apartments with parking
tend to be newer and larger, which inflates the difference. To estimate the pure
parking premium, a regression controlling for size, district, and building type
would be needed.

## 4. Regression Analysis — Isolating Price Factors

Simple comparison of apartments with/without parking (Section 3) is misleading because
apartments with parking also tend to be larger and newer. Linear regression separates
these effects by estimating each factor's contribution independently.

**Model:** `price = intercept + b1×area + b2×neubau + b3×parking + district_dummies`

N = 1,867 apartments | R² = 0.633 (model explains 63% of price variation)

### Main coefficients

| Variable | Coefficient | Interpretation |
|---|---:|---|
| Intercept | -€37,361 | Base price |
| Living area (m²) | +€4,514 | Each additional m² adds this to price |
| Neubau | +€42,909 | New construction premium |
| **Parking/Garage** | **+€29,619** | **Estimated price of a parking spot** |

### District premiums (vs Gries as reference)

| District | Premium | District | Premium |
|---|---:|---|---:|
| Sankt Peter | +€144,296 | Puntigam | +€2,160 |
| Mariatrost | +€122,299 | Eggenberg | -€1,984 |
| Andritz | +€104,922 | Gösting | -€20,311 |
| Geidorf | +€104,734 | Lend | -€39,860 |
| Sankt Leonhard | +€102,928 | Innere Stadt | -€50,821 |
| Waltendorf | +€90,558 | Wetzelsdorf | -€70,852 |
| Weinitzen | +€47,120 | | |
| Straßgang | +€37,112 | | |
| Jakomini | +€26,111 | | |
| Liebenau | +€18,299 | | |
| Ries | +€6,941 | | |

### How to read this

Comparing two apartments in Gries, both 70m², both Altbau:
- Without parking: -€37,361 + 70×€4,514 = **€278,619**
- With parking: €278,619 + €29,619 = **€308,238**

Same apartment but Neubau in Sankt Peter with parking:
- -€37,361 + 70×€4,514 + €42,909 + €29,619 + €144,296 = **€495,443**

### Limitations

- R² = 0.633 — 37% of price variation is unexplained (floor, condition, energy rating, amenities)
- Neubau coefficient includes apartments where `building_type` is unknown (treated as non-Neubau)
- Parking detection is keyword-based, may miss some cases
- Linear model assumes constant €/m² across all sizes (in reality, larger apartments may have lower €/m²)
