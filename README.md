# 🌍 Life Expectancy and GDP: Comparative Empirical Analysis (2000–2015)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13%2B-4c72b0)](https://seaborn.pydata.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An empirical investigation into the longitudinal relationship between Gross Domestic Product (GDP) and Life Expectancy at birth across six diverse nations (**Chile, China, Germany, Mexico, the United States, and Zimbabwe**) between **2000 and 2015**.

Based on observational data published by the **World Health Organization (WHO)** and the **World Bank**, this project evaluates univariate distributions, time-series growth trajectories, national health-wealth correlations, and tests the classical **Preston Curve** hypothesis.

---

## 📌 Executive Summary & Key Findings

| Country | Life Exp (2000) | Life Exp (2015) | Longevity Gain | GDP (2000) | GDP (2015) | GDP Growth (%) | GDP CAGR | Pearson Correlation ($r$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Germany** | 78.0 yrs | 81.0 yrs | **+3.0 yrs** | $1,950.0 B | $3,375.6 B | +73.1% | 3.7% | **0.933** |
| **Chile** | 77.3 yrs | 80.5 yrs | **+3.2 yrs** | $77.9 B | $242.5 B | +211.5% | 7.9% | **0.950** |
| **United States** | 76.8 yrs | 79.3 yrs | **+2.5 yrs** | $10,300.0 B | $18,100.0 B | +75.7% | 3.8% | **0.982** |
| **Mexico** | 74.8 yrs | 76.7 yrs | **+1.9 yrs** | $683.6 B | $1,152.3 B | +68.5% | 3.5% | **0.932** |
| **China** | 71.7 yrs | 76.1 yrs | **+4.4 yrs** | $1,211.3 B | $11,064.7 B | **+813.4%** | **15.9%** | **0.909** |
| **Zimbabwe** | 46.0 yrs | 60.7 yrs | **+14.7 yrs** | $6.7 B | $16.3 B | +143.7% | 6.1% | **0.966** |

### 🔍 Major Takeaways

1. **Within-Nation vs. Global Dynamics (The Preston Curve):**
   * Within every individual country, the correlation between GDP expansion and life expectancy gains is extraordinarily strong ($r \ge 0.91$).
   * However, pooling all nations together in a raw linear model yields a weak correlation of only **$r = 0.34$**, because wealth operates on orders of magnitude differences.
   * Applying a logarithmic transformation ($\log_{10}(\text{GDP})$) raises the pooled correlation to **$r = 0.79$**, confirming Samuel Preston's famous 1975 economic hypothesis: **diminishing marginal returns to health from GDP increases**.
2. **Zimbabwe's Historic Turnaround:**
   * After plummeting to a low of **44.3 years in 2004** amid the HIV/AIDS epidemic and socioeconomic instability, Zimbabwe achieved a remarkable recovery to **60.7 years by 2015** — an increase of **+16.4 years** from its nadir (+14.7 years overall).
3. **China's Unprecedented Economic Expansion:**
   * Following China's WTO entry in late 2001, GDP expanded from $1.21 Trillion to $11.06 Trillion (+813.4%, CAGR of 15.9%), raising life expectancy from 71.7 to 76.1 years.
4. **The Chile Paradox:**
   * Chile achieved a higher life expectancy in 2015 than the United States (**80.5 years vs. 79.3 years**), despite having a GDP that is less than 2% of the US economy. This highlights that national health systems, public health policy, and social safety nets play a crucial role beyond raw national wealth.

---

## 📊 Visualizations

### 1. Macro Trends (Shared Scales)
A side-by-side view illustrating the diverging economic scales alongside the steady convergence in human longevity:

![Combined Macro Trends](figures/5_combined_macro_trends.png)

---

### 2. The Preston Curve: Linear vs. Logarithmic Correlation
Demonstrating why a naive linear model misrepresents cross-country health economics, whereas a logarithmic model fits the diminishing returns of wealth on lifespan:

![Preston Curve Analysis](figures/6_preston_curve_analysis.png)

---

### 3. Country-by-Country Trajectories (Faceted Independent Scales)
Faceted time-series reveal the individual trajectories without smaller economies being compressed by US and Chinese GDP totals:

| GDP Evolution (2000–2015) | Life Expectancy Evolution (2000–2015) |
| :---: | :---: |
| ![Faceted GDP](figures/3_gdp_trends_faceted.png) | ![Faceted Life Expectancy](figures/4_life_expectancy_trends_faceted.png) |

---

### 4. Country Averages & Baseline Distributions

| Univariate Distributions | National 16-Year Averages |
| :---: | :---: |
| ![Distributions](figures/1_distributions.png) | ![Country Averages](figures/2_country_averages.png) |

---

## 📂 Project Structure

```text
life-expectancy-and-gdp/
├── all_data.csv                 # Raw dataset (WHO & World Bank)
├── life_expectancy_gdp.ipynb    # Comprehensive Jupyter Notebook analysis
├── analysis.py                  # Standalone CLI analysis script & figure generator
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Modern Python packaging configuration
├── .gitignore                   # Git ignore rules (clean repository standard)
├── figures/                     # High-resolution (300 DPI) exported visualizations
│   ├── 1_distributions.png
│   ├── 2_country_averages.png
│   ├── 3_gdp_trends_faceted.png
│   ├── 4_life_expectancy_trends_faceted.png
│   ├── 5_combined_macro_trends.png
│   └── 6_preston_curve_analysis.png
└── README.md                    # Project documentation
```

---

## 🛠️ Installation & Quickstart

### Prerequisites
* Python 3.9 or higher
* `pip` or any virtual environment manager (`venv`, `conda`, `uv`)

### 1. Clone the repository
```bash
git clone https://github.com/your-username/life-expectancy-and-gdp.git
cd life-expectancy-and-gdp
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the automated analysis
To generate all statistical summaries and re-export the figures:
```bash
python analysis.py
```

### 5. Launch the Jupyter Notebook
For an interactive, step-by-step walkthrough:
```bash
jupyter notebook life_expectancy_gdp.ipynb
```

---

## 📖 Methodology & Data Description

The dataset `all_data.csv` contains **96 rows** across **4 columns**:

| Column Name | Type | Description | Source |
| :--- | :--- | :--- | :--- |
| `Country` | string | Nation name (6 unique countries) | WHO / World Bank |
| `Year` | integer | Observation year (2000–2015) | — |
| `Life expectancy at birth (years)` | float | Average life expectancy at birth in years | [World Health Organization](http://apps.who.int/gho/data/node.main.688) |
| `GDP` | float | Gross Domestic Product in current U.S. Dollars | [World Bank](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD) |

### Analytical Techniques Used
* **Data Cleansing:** Standardized column names, scaled economic values into Billions/Trillions USD, created logarithmic transformations.
* **Univariate & Bivariate EDA:** Kernel Density Estimation (KDE), histograms, violin plots, and jittered strip plots.
* **Longitudinal Modeling:** Faceted time-series grids (`sns.FacetGrid`) with independent axis scaling.
* **Econometric Analysis:** Compound Annual Growth Rate (CAGR), Pearson product-moment correlation coefficients, and log-linear regression modeling (Preston Curve).

---

## 📚 References
* Preston, S. H. (1975). *The Changing Relation between Mortality and Level of Economic Development*. Population Studies, 29(2), 231–248.
* World Health Organization. (2018). *Global Health Observatory (GHO) data*.
* World Bank. (2018). *World Development Indicators: GDP (current US$)*.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
