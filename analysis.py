"""
Life Expectancy and GDP Analysis (2000–2024)
===========================================
Investigates the relationship between Gross Domestic Product (GDP) and Life
Expectancy across six nations (Chile, China, Germany, Mexico, USA, Zimbabwe)
from 2000 to 2024 using data from the World Bank and the World Health Organization.

Includes two-era comparative analysis:
 - Era 1 (2000–2015): The Continuous Growth & Convergence Era (Codecademy baseline)
 - Era 2 (2016–2024): The Modern Disruption, COVID-19 Shock & Decoupling Era
"""

from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Ensure writable matplotlib cache in sandboxed/restricted environments
if "MPLCONFIGDIR" not in os.environ:
    os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

DATA_DIR = Path(__file__).parent
DATA_PATH_EXTENDED = DATA_DIR / "all_data_extended.csv"
DATA_PATH_BASELINE = DATA_DIR / "all_data.csv"
FIGURES_DIR = DATA_DIR / "figures"


def setup_plotting_theme():
    """Configure Seaborn and Matplotlib styling for high-quality figures."""
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams.update({
        "figure.titlesize": 14,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def load_data(extended: bool = True) -> pd.DataFrame:
    """Load dataset (extended 2000-2024 by default, or 2000-2015 baseline)."""
    path = DATA_PATH_EXTENDED if extended and DATA_PATH_EXTENDED.exists() else DATA_PATH_BASELINE
    df = pd.read_csv(path)
    df = df.rename(columns={"Life expectancy at birth (years)": "LEABY"})
    df["Country_Short"] = df["Country"].replace({"United States of America": "USA"})
    df["GDP_Trillions"] = df["GDP"] / 1e12
    df["GDP_Billions"] = df["GDP"] / 1e9
    df["log_GDP"] = np.log10(df["GDP"])
    return df


def compute_era_statistics(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute statistics for Era 1 (2000-2015) vs Era 2 (2016-2024)."""
    era1 = df[df["Year"] <= 2015]
    era2 = df[df["Year"] >= 2016]

    records_overall = []
    for country, grp in df.groupby("Country_Short"):
        g_sorted = grp.sort_values("Year")
        c_e1 = era1[era1["Country_Short"] == country]
        c_e2 = era2[era2["Country_Short"] == country]

        le_2000 = g_sorted[g_sorted["Year"] == 2000]["LEABY"].iloc[0]
        le_2015 = g_sorted[g_sorted["Year"] == 2015]["LEABY"].iloc[0]
        le_2019 = g_sorted[g_sorted["Year"] == 2019]["LEABY"].iloc[0] if 2019 in g_sorted["Year"].values else np.nan
        le_covid_low = g_sorted[g_sorted["Year"].isin([2020, 2021, 2022])]["LEABY"].min() if not c_e2.empty else np.nan
        le_2024 = g_sorted.iloc[-1]["LEABY"]

        gdp_2000 = g_sorted[g_sorted["Year"] == 2000]["GDP_Billions"].iloc[0]
        gdp_2024 = g_sorted.iloc[-1]["GDP_Billions"]

        r_e1 = c_e1["GDP"].corr(c_e1["LEABY"]) if not c_e1.empty else np.nan
        r_e2 = c_e2["GDP"].corr(c_e2["LEABY"]) if not c_e2.empty else np.nan

        records_overall.append({
            "Country": country,
            "LE_2000": le_2000,
            "LE_2015": le_2015,
            "LE_2019": le_2019,
            "LE_COVID_Low": le_covid_low,
            "COVID_Drop": le_covid_low - le_2019 if pd.notna(le_covid_low) and pd.notna(le_2019) else np.nan,
            "LE_Latest": le_2024,
            "GDP_2000_B": gdp_2000,
            "GDP_Latest_B": gdp_2024,
            "r_Era1 (00-15)": r_e1,
            "r_Era2 (16-24)": r_e2,
        })

    summary_df = pd.DataFrame(records_overall).sort_values(by="LE_Latest", ascending=False)
    return summary_df, df


def plot_distributions(df: pd.DataFrame, output_dir: Path = FIGURES_DIR):
    """Plot univariate distributions for GDP and Life Expectancy with histograms and KDE."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.histplot(df["GDP_Trillions"], kde=True, ax=axes[0], color="#2b5c8f", bins=15)
    axes[0].set_title(f"Distribution of GDP across Observations ({df['Year'].min()}–{df['Year'].max()})")
    axes[0].set_xlabel("GDP (Trillions of USD)")
    axes[0].set_ylabel("Frequency Count")
    axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:.1f}T"))

    sns.histplot(df["LEABY"], kde=True, ax=axes[1], color="#2ca02c", bins=15)
    axes[1].set_title(f"Distribution of Life Expectancy at Birth ({df['Year'].min()}–{df['Year'].max()})")
    axes[1].set_xlabel("Life Expectancy (Years)")
    axes[1].set_ylabel("Frequency Count")

    plt.tight_layout()
    output_path = output_dir / "1_distributions.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_country_averages(df: pd.DataFrame, output_dir: Path = FIGURES_DIR):
    """Plot mean GDP and mean Life Expectancy per country."""
    means = df.groupby("Country_Short")[["GDP_Trillions", "LEABY"]].mean().reset_index()
    palette = sns.color_palette("muted", n_colors=len(means))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    means_sorted_le = means.sort_values(by="LEABY", ascending=False)
    sns.barplot(
        data=means_sorted_le,
        x="LEABY",
        y="Country_Short",
        palette=palette,
        hue="Country_Short",
        legend=False,
        ax=axes[0],
    )
    axes[0].set_title(f"Mean Life Expectancy ({df['Year'].min()}–{df['Year'].max()})")
    axes[0].set_xlabel("Life Expectancy at Birth (Years)")
    axes[0].set_ylabel("")
    axes[0].set_xlim(0, 90)
    for p in axes[0].patches:
        width = p.get_width()
        axes[0].annotate(f"{width:.1f}y", (width + 1.2, p.get_y() + p.get_height() / 2),
                         va="center", fontsize=9, fontweight="bold")

    means_sorted_gdp = means.sort_values(by="GDP_Trillions", ascending=False)
    sns.barplot(
        data=means_sorted_gdp,
        x="GDP_Trillions",
        y="Country_Short",
        palette=palette,
        hue="Country_Short",
        legend=False,
        ax=axes[1],
    )
    axes[1].set_title(f"Mean Gross Domestic Product ({df['Year'].min()}–{df['Year'].max()})")
    axes[1].set_xlabel("GDP (Trillions of USD)")
    axes[1].set_ylabel("")
    axes[1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:.1f}T"))
    for p in axes[1].patches:
        width = p.get_width()
        axes[1].annotate(f"${width:.2f}T", (width + 0.2, p.get_y() + p.get_height() / 2),
                         va="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    output_path = output_dir / "2_country_averages.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_trends_over_time(df: pd.DataFrame, output_dir: Path = FIGURES_DIR):
    """Plot time-series trajectories for GDP and Life Expectancy with faceted scales."""
    # 1. Faceted GDP Trends
    g_gdp = sns.FacetGrid(
        df,
        col="Country_Short",
        col_wrap=3,
        hue="Country_Short",
        sharey=False,
        height=3.5,
        aspect=1.3,
    )
    g_gdp.map(sns.lineplot, "Year", "GDP_Trillions", marker="o", linewidth=2)
    g_gdp.set_axis_labels("Year", "GDP (Trillions USD)")
    g_gdp.set_titles(col_template="{col_name}", size=11)
    g_gdp.fig.subplots_adjust(top=0.9)
    g_gdp.fig.suptitle(f"GDP Trajectory by Nation ({df['Year'].min()}–{df['Year'].max()}) — Independent Scales", fontsize=14, fontweight="bold")
    gdp_path = output_dir / "3_gdp_trends_faceted.png"
    g_gdp.savefig(gdp_path)
    plt.close()
    print(f"Saved: {gdp_path}")

    # 2. Faceted Life Expectancy Trends (with COVID highlight)
    g_le = sns.FacetGrid(
        df,
        col="Country_Short",
        col_wrap=3,
        hue="Country_Short",
        sharey=False,
        height=3.5,
        aspect=1.3,
    )
    g_le.map(sns.lineplot, "Year", "LEABY", marker="s", linewidth=2, color="#d95f02")
    
    # Highlight COVID-19 period in each facet if data covers it
    if df["Year"].max() >= 2020:
        for ax in g_le.axes.flat:
            ax.axvspan(2019.8, 2021.5, color="red", alpha=0.15)
            
    g_le.set_axis_labels("Year", "Life Expectancy (Years)")
    g_le.set_titles(col_template="{col_name}", size=11)
    g_le.fig.subplots_adjust(top=0.9)
    g_le.fig.suptitle(f"Life Expectancy Trajectory ({df['Year'].min()}–{df['Year'].max()}) — Red Shading: COVID-19", fontsize=14, fontweight="bold")
    le_path = output_dir / "4_life_expectancy_trends_faceted.png"
    g_le.savefig(le_path)
    plt.close()
    print(f"Saved: {le_path}")

    # 3. Combined Macro Comparison
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    palette = sns.color_palette("tab10", n_colors=df["Country_Short"].nunique())

    sns.lineplot(
        data=df,
        x="Year",
        y="GDP_Trillions",
        hue="Country_Short",
        palette=palette,
        linewidth=2.5,
        marker="o",
        ax=axes[0],
    )
    axes[0].set_title(f"GDP Growth Comparison ({df['Year'].min()}–{df['Year'].max()})")
    axes[0].set_ylabel("GDP (Trillions of USD)")
    axes[0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:.0f}T"))

    sns.lineplot(
        data=df,
        x="Year",
        y="LEABY",
        hue="Country_Short",
        palette=palette,
        linewidth=2.5,
        marker="s",
        ax=axes[1],
    )
    if df["Year"].max() >= 2020:
        axes[1].axvspan(2019.8, 2021.5, color="red", alpha=0.12, label="COVID-19 Shock")
    axes[1].set_title(f"Life Expectancy Comparison ({df['Year'].min()}–{df['Year'].max()})")
    axes[1].set_ylabel("Life Expectancy at Birth (Years)")
    axes[1].set_ylim(40, 85)

    plt.tight_layout()
    macro_path = output_dir / "5_combined_macro_trends.png"
    plt.savefig(macro_path)
    plt.close()
    print(f"Saved: {macro_path}")


def plot_preston_curve_and_correlations(df: pd.DataFrame, output_dir: Path = FIGURES_DIR):
    """Demonstrate the Preston Curve relationship (Linear vs. Logarithmic scale)."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    countries = df["Country_Short"].unique()
    palette = dict(zip(countries, sns.color_palette("tab10", len(countries))))

    r_linear = df["GDP"].corr(df["LEABY"])
    for country in countries:
        c_data = df[df["Country_Short"] == country]
        axes[0].scatter(
            c_data["GDP_Trillions"],
            c_data["LEABY"],
            label=country,
            color=palette[country],
            s=45,
            alpha=0.85,
        )
    axes[0].set_title(f"Linear Scale: Raw GDP vs. Life Expectancy\n(Pooled Pearson r = {r_linear:.2f})")
    axes[0].set_xlabel("GDP (Trillions of USD)")
    axes[0].set_ylabel("Life Expectancy at Birth (Years)")
    axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:.0f}T"))
    axes[0].legend(title="Country", loc="lower right")

    r_log = df["log_GDP"].corr(df["LEABY"])
    for country in countries:
        c_data = df[df["Country_Short"] == country]
        axes[1].scatter(
            c_data["log_GDP"],
            c_data["LEABY"],
            label=country,
            color=palette[country],
            s=45,
            alpha=0.85,
        )

    m, b = np.polyfit(df["log_GDP"], df["LEABY"], 1)
    x_vals = np.linspace(df["log_GDP"].min(), df["log_GDP"].max(), 100)
    axes[1].plot(x_vals, m * x_vals + b, color="black", linestyle="--", alpha=0.7, label="Log Trendline")

    axes[1].set_title(f"Logarithmic Scale: The Preston Curve\n(Pooled Pearson r = {r_log:.2f} — Strong Log-Linear Law)")
    axes[1].set_xlabel("log10(GDP in USD)")
    axes[1].set_ylabel("Life Expectancy at Birth (Years)")
    axes[1].legend(title="Country / Trend", loc="lower right")

    plt.tight_layout()
    preston_path = output_dir / "6_preston_curve_analysis.png"
    plt.savefig(preston_path)
    plt.close()
    print(f"Saved: {preston_path}")


def plot_era_comparison_and_covid_shock(df: pd.DataFrame, output_dir: Path = FIGURES_DIR):
    """
    Dedicated figure visualizing the 2016-2024 era:
    1. Zoomed-in Life Expectancy trajectory (2015-2024) highlighting the COVID-19 dip.
    2. Comparison bar chart of Pearson correlations: Era 1 (2000-2015) vs. Era 2 (2016-2024).
    """
    if df["Year"].max() < 2020:
        return

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    modern_df = df[df["Year"] >= 2015]
    palette = sns.color_palette("tab10", n_colors=modern_df["Country_Short"].nunique())

    sns.lineplot(
        data=modern_df,
        x="Year",
        y="LEABY",
        hue="Country_Short",
        palette=palette,
        marker="o",
        linewidth=2.5,
        ax=axes[0],
    )
    axes[0].axvspan(2019.8, 2021.5, color="red", alpha=0.14, label="COVID-19 Shock")
    axes[0].set_title("The Modern Era (2015–2024): The COVID-19 Longevity Shock", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("Life Expectancy at Birth (Years)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylim(58, 83)
    axes[0].legend(loc="lower left", fontsize=9)

    era1 = df[df["Year"] <= 2015]
    era2 = df[df["Year"] >= 2016]

    corr_records = []
    for c in df["Country_Short"].unique():
        r1 = era1[era1["Country_Short"] == c]["GDP"].corr(era1[era1["Country_Short"] == c]["LEABY"])
        r2 = era2[era2["Country_Short"] == c]["GDP"].corr(era2[era2["Country_Short"] == c]["LEABY"])
        corr_records.append({"Country": c, "Era": "Era 1 (2000–2015: Growth)", "Correlation (r)": r1})
        corr_records.append({"Country": c, "Era": "Era 2 (2016–2024: Pandemic)", "Correlation (r)": r2})

    corr_df = pd.DataFrame(corr_records)
    sns.barplot(
        data=corr_df,
        x="Country",
        y="Correlation (r)",
        hue="Era",
        palette=["#2ca02c", "#d62728"],
        ax=axes[1],
    )
    axes[1].axhline(0, color="black", linestyle="--", alpha=0.6)
    axes[1].set_title("Health-Wealth Decoupling: Pearson r by Era", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Pearson Correlation Coefficient (r)")
    axes[1].set_xlabel("Country")
    axes[1].set_ylim(-0.5, 1.1)
    axes[1].legend(loc="lower left", fontsize=9)

    plt.tight_layout()
    output_path = output_dir / "7_era_comparison_covid_shock.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def run_full_pipeline():
    """Execute complete end-to-end data processing, reporting, and visualization."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    setup_plotting_theme()

    print("=" * 75)
    print(" LIFE EXPECTANCY & GDP: LONGITUDINAL & PANDEMIC SHOCK ANALYSIS (2000–2024)")
    print("=" * 75)

    df = load_data(extended=True)
    summary_df, _ = compute_era_statistics(df)

    print("\n--- Two-Era Comparison Table (2000–2015 vs. 2016–2024) ---")
    formatted_summary = summary_df.to_string(
        index=False,
        formatters={
            "LE_2000": "{:.1f}".format,
            "LE_2015": "{:.1f}".format,
            "LE_2019": "{:.1f}".format,
            "LE_COVID_Low": "{:.1f}".format,
            "COVID_Drop": "{:+.2f}y".format,
            "LE_Latest": "{:.1f}".format,
            "GDP_2000_B": "${:,.1f}B".format,
            "GDP_Latest_B": "${:,.1f}B".format,
            "r_Era1 (00-15)": "{:.3f}".format,
            "r_Era2 (16-24)": "{:+.3f}".format,
        },
    )
    print(formatted_summary)

    print("\n--- Generating Visualizations in ./figures/ ---")
    plot_distributions(df)
    plot_country_averages(df)
    plot_trends_over_time(df)
    plot_preston_curve_and_correlations(df)
    plot_era_comparison_and_covid_shock(df)

    print("\nAnalysis pipeline completed successfully.")
    print("=" * 75)


if __name__ == "__main__":
    run_full_pipeline()
