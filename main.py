# INF601 - Advanced Programming in Python
# Rachel White
# Mini Project 3

import os

import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "us_average_prices_item_summary.csv"
CHARTS_DIR = "charts"

# Exact item name in the CSV -> short name used in tables and charts
ITEMS = {
    "Ground beef, 100% beef": "Ground Beef",
    "Gasoline, unleaded regular": "Regular Unleaded Gasoline",
    "Coffee, 100%, ground roast, all sizes": "Coffee",
}

COLORS = {
    "Ground Beef": "#D55E00",
    "Regular Unleaded Gasoline": "#0072B2",
    "Coffee": "#009E73",
}

# Columns this program needs from the CSV
REQUIRED_COLUMNS = ["item", "first_date", "last_date", "first_price", "last_price"]


def load_data():
    # Load the CSV file into a DataFrame
    df = pd.read_csv(DATA_FILE)

    print("Original DataFrame:")
    print(df.head())
    print("\nDataFrame information:")
    df.info()

    return df


def prepare_data(df):

    # make column names easier to work with
    df.columns = df.columns.str.strip()

    # display column names so the CSV structure is easier to inspect
    print("\nColumns in the dataset:")
    print(df.columns.tolist())

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Convert dates and prices to proper types
    df["first_date"] = pd.to_datetime(df["first_date"], errors="coerce")
    df["last_date"] = pd.to_datetime(df["last_date"], errors="coerce")
    df["first_price"] = pd.to_numeric(df["first_price"], errors="coerce")
    df["last_price"] = pd.to_numeric(df["last_price"], errors="coerce")

    # remove rows with missing values
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # keep only requested years
    df = df[
        (df["first_date"].dt.year >= 2015)
        & (df["last_date"].dt.year <= 2026)]

    # keep only the three products being analyzed
    df = df[df["item"].isin(ITEMS)].copy()

    missing_items = set(ITEMS) - set(df["item"])
    if missing_items:
        raise ValueError(f"Items not found in the data: {sorted(missing_items)}")

    # use the short item names and rename the important columns so the program is easier to read
    df["item"] = df["item"].map(ITEMS)
    df = df.rename(
        columns={
            "item": "Item",
            "first_date": "First Date",
            "last_date": "Last Date",
            "first_price": "First Price",
            "last_price": "Last Price",
        }
    )

    # keep just the columns we need, in the order the items were listed
    df = (
        df[["Item", "First Date", "Last Date", "First Price", "Last Price"]]
        .set_index("Item")
        .loc[list(ITEMS.values())]
        .reset_index()
    )

    return df


def calculate_changes(df):
    
    changes = df.copy()

    changes["Dollar Change"] = changes["Last Price"] - changes["First Price"]
    changes["Percent Change"] = changes["Dollar Change"] / changes["First Price"] * 100

    # Years between the first and last recorded price
    changes["Years"] = (changes["Last Date"] - changes["First Date"]).dt.days / 365.25

    # Compound average yearly percent change
    changes["Yearly Percent Change"] = (
        (changes["Last Price"] / changes["First Price"]) ** (1 / changes["Years"]) - 1
    ) * 100

    return changes


def create_price_trend_chart(changes):
   
    plt.figure(figsize=(12, 7))

    for _, row in changes.iterrows():
        item = row["Item"]

        plt.plot(
            [row["First Date"], row["Last Date"]],
            [row["First Price"], row["Last Price"]],
            marker="o",
            linewidth=2.5,
            color=COLORS[item],
            label=item,
        )

        # Label the price at each end of the line
        plt.annotate(
            f"${row['First Price']:.2f}",
            (row["First Date"], row["First Price"]),
            textcoords="offset points", xytext=(-10, 0), ha="right", va="center",
        )
        plt.annotate(
            f"${row['Last Price']:.2f}",
            (row["Last Date"], row["Last Price"]),
            textcoords="offset points", xytext=(10, 0), ha="left", va="center",
        )

    first_year = changes["First Date"].min().year
    last_year = changes["Last Date"].max().year

    plt.title(f"U.S. Average Prices: {first_year}–{last_year}")
    plt.xlabel("Date")
    plt.ylabel("Average Price (USD per lb. for beef and coffee, per gallon for gasoline)")
    plt.ylim(bottom=0)
    plt.margins(x=0.08)
    plt.grid(True, alpha=0.3)
    plt.legend(loc="upper left")
    plt.tight_layout()

    output_file = os.path.join(CHARTS_DIR, "price_trends.png")
    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"Saved: {output_file}")


def create_percent_change_chart(changes):
    
    plt.figure(figsize=(12, 7))

    ordered = changes.sort_values("Percent Change")

    bars = plt.barh(
        ordered["Item"],
        ordered["Percent Change"],
        color=[COLORS[item] for item in ordered["Item"]],
    )

    # Label each bar with the total change and the average yearly change
    for bar, (_, row) in zip(bars, ordered.iterrows()):
        plt.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{row['Percent Change']:+.1f}% total ({row['Yearly Percent Change']:.1f}% per year)",
            va="center",
        )

    first_year = changes["First Date"].min().year
    last_year = changes["Last Date"].max().year

    plt.title(f"Total Price Change: {first_year}–{last_year}")
    plt.xlabel("Percentage Change (%)")
    plt.xlim(0, ordered["Percent Change"].max() * 1.45)
    plt.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(CHARTS_DIR, "price_percent_change.png")
    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"Saved: {output_file}")


def print_summary(changes):
    
    print("\n===== PRICE CHANGES =====")
    print(changes.to_string(index=False, float_format="{:.2f}".format))

    print("\n===== FIRST TO LAST CHANGE =====")

    for _, row in changes.iterrows():
        print(
            f"{row['Item']}: "
            f"${row['First Price']:.2f} ({row['First Date']:%b %Y}) -> "
            f"${row['Last Price']:.2f} ({row['Last Date']:%b %Y}) | "
            f"Change: ${row['Dollar Change']:.2f} "
            f"({row['Percent Change']:.2f}%)"
        )


def main():
    """Run the grocery price analysis."""

    # Create the charts directory if it does not already exist.
    os.makedirs(CHARTS_DIR, exist_ok=True)

    # Load the CSV into a Pandas DataFrame.
    df = load_data()

    # Clean and filter the DataFrame.
    df = prepare_data(df)

    print("\n===== CLEANED DATA =====")
    print(df.to_string(index=False))

    # Calculate the price changes.
    changes = calculate_changes(df)

    # Print numerical results.
    print_summary(changes)

    # Generate charts.
    create_price_trend_chart(changes)
    create_percent_change_chart(changes)

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
