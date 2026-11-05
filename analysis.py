"""
Life Expectancy and GDP Analysis
================================
Investigates the relationship between Gross Domestic Product (GDP) and Life
Expectancy across six nations (Chile, China, Germany, Mexico, USA, Zimbabwe)
from 2000 to 2015 using data from the World Bank and the World Health Organization.
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

DATA_PATH = Path(__file__).parent / "all_data.csv"
FIGURES_DIR = Path(__file__).parent / "figures"


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


def load_and_preprocess_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the raw CSV dataset and apply standard column transformations."""
    df = pd.read_csv(path)
    df = df.rename(columns={"Life expectancy at birth (years)": "LEABY"})
    # Normalize long country name for cleaner plot legends
    df["Country_Short"] = df["Country"].replace({"United States of America": "USA"})
    df["GDP_Trillions"] = df["GDP"] / 1e12
    return df


def compute_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute summary statistics per country including CAGR, gains, and correlation."""
    records = []
    for country, group in df.groupby("Country"):
        g_sorted = group.sort_values("Year")
        gdp_start = g_sorted["GDP"].iloc[0]
        gdp_end = g_sorted["GDP"].iloc[-1]
        le_start = g_sorted["LEABY"].iloc[0]
        le_end = g_sorted["LEABY"].iloc[-1]
        le_min = g_sorted["LEABY"].min()
        n_years = g_sorted["Year"].iloc[-1] - g_sorted["Year"].iloc[0]

        # Compound Annual Growth Rate (CAGR)
        cagr_gdp = ((gdp_end / gdp_start) ** (1 / n_years) - 1) * 100
        corr_pearson = group["GDP"].corr(group["LEABY"])

        records.append({
            "Country": country,
            "LE_2000": le_start,
            "LE_2015": le_end,
            "LE_Gain": le_end - le_start,
            "LE_Min": le_min,
            "GDP_2000_B": gdp_start / 1e9,
            "GDP_2015_B": gdp_end / 1e9,
            "GDP_Growth_%": ((gdp_end - gdp_start) / gdp_start) * 100,
            "GDP_CAGR_%": cagr_gdp,
            "Correlation_r": corr_pearson,
        })

    summary_df = pd.DataFrame(records).sort_values(by="LE_2015", ascending=False)
    return summary_df


def plot_distributions(df: pd.DataFrame, output_dir: Path = FIGURES_DIR):
    """Plot univariate distributions for GDP and Life Expectancy with histograms and KDE."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # GDP distribution
    sns.histplot(df["GDP_Trillions"], kde=True, ax=axes[0], color="#2b5c8f", bins=15)
    axes[0].set_title("Distribution of GDP across Observations (2000–2015)")
    axes[0].set_xlabel("GDP (Trillions of USD)")
    axes[0].set_ylabel("Frequency Count")
    axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:.1f}T"))

    # Life Expectancy distribution
    sns.histplot(df["LEABY"], kde=True, ax=axes[1], color="#2ca02c", bins=15)
    axes[1].set_title("Distribution of Life Expectancy at Birth (2000–2015)")
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

    # Average Life Expectancy
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
    axes[0].set_title("Mean Life Expectancy (2000–2015)")
    axes[0].set_xlabel("Life Expectancy at Birth (Years)")
    axes[0].set_ylabel("")
    axes[0].set_xlim(0, 90)
    for p in axes[0].patches:
        width = p.get_width()
        axes[0].annotate(f"{width:.1f}y", (width + 1.2, p.get_y() + p.get_height() / 2),
                         va="center", fontsize=9, fontweight="bold")

    # Average GDP
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
    axes[1].set_title("Mean Gross Domestic Product (2000–2015)")
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
    g_gdp.fig.suptitle("GDP Trajectory by Nation (2000–2015) — Independent Scales", fontsize=14, fontweight="bold")
    gdp_path = output_dir / "3_gdp_trends_faceted.png"
    g_gdp.savefig(gdp_path)
    plt.close()
    print(f"Saved: {gdp_path}")

    # 2. Faceted Life Expectancy Trends
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
    g_le.set_axis_labels("Year", "Life Expectancy (Years)")
    g_le.set_titles(col_template="{col_name}", size=11)
    g_le.fig.subplots_adjust(top=0.9)
    g_le.fig.suptitle("Life Expectancy Trajectory by Nation (2000–2015) — Independent Scales", fontsize=14, fontweight="bold")
    le_path = output_dir / "4_life_expectancy_trends_faceted.png"
    g_le.savefig(le_path)
    plt.close()
    print(f"Saved: {le_path}")

    # 3. Combined Macro Comparison (Side-by-side macro view)
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
    axes[0].set_title("GDP Growth Comparison (Combined Scale)")
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
    axes[1].set_title("Life Expectancy Comparison (2000–2015)")
    axes[1].set_ylabel("Life Expectancy at Birth (Years)")
    axes[1].set_ylim(40, 85)

    plt.tight_layout()
    macro_path = output_dir / "5_combined_macro_trends.png"
    plt.savefig(macro_path)
    plt.close()
    print(f"Saved: {macro_path}")


def plot_preston_curve_and_correlations(df: pd.DataFrame, output_dir: Path = FIGURES_DIR):
    """
    Demonstrate the Preston Curve relationship:
    Plot Raw GDP vs. Life Expectancy alongside Log(GDP) vs. Life Expectancy.
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    countries = df["Country_Short"].unique()
    palette = dict(zip(countries, sns.color_palette("tab10", len(countries))))

    # 1. Linear Scale (Raw GDP)
    r_linear = df["GDP"].corr(df["LEABY"])
    for country in countries:
        c_data = df[df["Country_Short"] == country]
        axes[0].scatter(
            c_data["GDP_Trillions"],
            c_data["LEABY"],
            label=country,
            color=palette[country],
            s=50,
            alpha=0.85,
        )
    axes[0].set_title(f"Linear Scale: Raw GDP vs. Life Expectancy\n(Overall r = {r_linear:.2f})")
    axes[0].set_xlabel("GDP (Trillions of USD)")
    axes[0].set_ylabel("Life Expectancy at Birth (Years)")
    axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:.0f}T"))
    axes[0].legend(title="Country", loc="lower right")

    # 2. Logarithmic Scale (The Preston Curve)
    df["log_GDP"] = np.log10(df["GDP"])
    r_log = df["log_GDP"].corr(df["LEABY"])

    for country in countries:
        c_data = df[df["Country_Short"] == country]
        axes[1].scatter(
            c_data["log_GDP"],
            c_data["LEABY"],
            label=country,
            color=palette[country],
            s=50,
            alpha=0.85,
        )

    # Fit overall trendline on log scale
    m, b = np.polyfit(df["log_GDP"], df["LEABY"], 1)
    x_vals = np.linspace(df["log_GDP"].min(), df["log_GDP"].max(), 100)
    axes[1].plot(x_vals, m * x_vals + b, color="black", linestyle="--", alpha=0.7, label="Log Trendline")

    axes[1].set_title(f"Logarithmic Scale: The Preston Curve\n(Overall r = {r_log:.2f} — Strong Log-Linear Correlation)")
    axes[1].set_xlabel("log10(GDP in USD)")
    axes[1].set_ylabel("Life Expectancy at Birth (Years)")
    axes[1].legend(title="Country / Trend", loc="lower right")

    plt.tight_layout()
    preston_path = output_dir / "6_preston_curve_analysis.png"
    plt.savefig(preston_path)
    plt.close()
    print(f"Saved: {preston_path}")


def run_full_pipeline():
    """Execute complete end-to-end data processing, reporting, and visualization."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    setup_plotting_theme()

    print("=" * 70)
    print(" LIFE EXPECTANCY & GDP: COMPARATIVE ANALYSIS (2000–2015)")
    print("=" * 70)

    df = load_and_preprocess_data()
    summary = compute_statistics(df)

    print("\n--- Summary Statistics by Nation ---")
    formatted_summary = summary.to_string(
        index=False,
        formatters={
            "LE_2000": "{:.1f}".format,
            "LE_2015": "{:.1f}".format,
            "LE_Gain": "+{:.1f}".format,
            "LE_Min": "{:.1f}".format,
            "GDP_2000_B": "${:,.1f}B".format,
            "GDP_2015_B": "${:,.1f}B".format,
            "GDP_Growth_%": "+{:.1f}%".format,
            "GDP_CAGR_%": "{:.1f}%".format,
            "Correlation_r": "{:.3f}".format,
        },
    )
    print(formatted_summary)

    print("\n--- Generating Visualizations in ./figures/ ---")
    plot_distributions(df)
    plot_country_averages(df)
    plot_trends_over_time(df)
    plot_preston_curve_and_correlations(df)

    print("\nAnalysis pipeline completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    run_full_pipeline()

