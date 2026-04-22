"""ETL pipeline for US Accidents (2016-2023) — DeliverIQ Capstone.

This module provides functions for:
  1. Balanced extraction from the ~7.7M-row raw dataset
  2. Intelligent cleaning with relationship-based imputation
  3. Feature engineering and Tableau-ready dataset preparation
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Column normalisation
# ---------------------------------------------------------------------------

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to a clean snake_case format."""
    cleaned = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    result = df.copy()
    result.columns = cleaned
    return result


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply a few safe default cleaning steps."""
    result = normalize_columns(df)
    result = result.drop_duplicates().reset_index(drop=True)

    for column in result.select_dtypes(include="object").columns:
        result[column] = result[column].astype("string").str.strip()

    return result


# ---------------------------------------------------------------------------
# Phase 1 — Balanced extraction
# ---------------------------------------------------------------------------

# Columns to drop immediately (justified in implementation plan)
COLUMNS_TO_DROP = [
    "ID", "End_Lat", "End_Lng", "Turning_Loop", "Country",
    "Description", "Wind_Chill(F)", "Precipitation(in)",
    "Weather_Timestamp", "Airport_Code", "Source",
]

# Target sample sizes per severity level (balanced for analysis)
# Actual counts: Sev1≈67K, Sev2≈6.15M, Sev3≈1.3M, Sev4≈205K
SEVERITY_TARGETS = {1: 10_000, 2: 35_000, 3: 35_000, 4: 20_000}


def extract_balanced_sample(
    raw_path: Path,
    output_path: Path,
    total_target: int = 100_000,
    chunk_size: int = 500_000,
    random_state: int = 42,
) -> pd.DataFrame:
    """Extract a severity-balanced, geographically diverse sample.

    Strategy (single-pass chunked collection + stratified sampling):
      - Severity 1: sample 10K (from ~67K available)
      - Severity 2: sample 35K (from ~6.15M available)
      - Severity 3: sample 35K (from ~1.3M available)
      - Severity 4: sample 20K (from ~205K available)
      - Within each severity, stratify by State for geographic diversity
    """
    print("Phase 1: Starting balanced extraction ...")
    print(f"  Reading {raw_path} in chunks of {chunk_size:,} rows")

    # --- Single pass: collect all rows grouped by severity -----------------
    severity_buckets: dict[int, list[pd.DataFrame]] = {1: [], 2: [], 3: [], 4: []}
    sev_counts: dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0}

    for i, chunk in enumerate(pd.read_csv(raw_path, chunksize=chunk_size)):
        vc = chunk["Severity"].value_counts()
        for sev in sev_counts:
            sev_counts[sev] += int(vc.get(sev, 0))
        # For sev 2 & 3 (very large), reservoir-sample within chunks
        for sev in [1, 4]:
            severity_buckets[sev].append(chunk[chunk["Severity"] == sev])
        for sev in [2, 3]:
            sev_chunk = chunk[chunk["Severity"] == sev]
            # Keep a random 5% of each chunk to limit memory
            if len(sev_chunk) > 0:
                frac = min(1.0, SEVERITY_TARGETS[sev] * 3 / sev_counts.get(sev, len(sev_chunk)))
                severity_buckets[sev].append(
                    sev_chunk.sample(frac=min(frac, 0.15), random_state=random_state + i)
                    if len(sev_chunk) > 1000 else sev_chunk
                )
        if (i + 1) % 5 == 0:
            print(f"    ... read {(i+1)*chunk_size:,} rows")

    print(f"  Full dataset severity counts: {sev_counts}")

    # --- Determine final targets (cap at available) -------------------------
    targets = dict(SEVERITY_TARGETS)
    for sev in targets:
        targets[sev] = min(targets[sev], sev_counts[sev])
    print(f"  Sampling targets: {targets}")

    # --- Stratified sampling for each severity ------------------------------
    rng = np.random.RandomState(random_state)
    sampled_chunks: list[pd.DataFrame] = []

    for sev in [1, 2, 3, 4]:
        target = targets[sev]
        all_sev = pd.concat(severity_buckets[sev], ignore_index=True)
        all_sev = all_sev.drop_duplicates().reset_index(drop=True)
        print(f"  Severity {sev}: {len(all_sev):,} rows available, target {target:,}")

        if len(all_sev) <= target:
            sampled_chunks.append(all_sev)
        else:
            # group-proportional sampling by State for geographic diversity
            state_groups = all_sev.groupby("State")
            state_fracs = state_groups.size() / len(all_sev)
            parts = []
            for state, grp in state_groups:
                n = max(1, int(np.round(target * state_fracs[state])))
                n = min(n, len(grp))
                parts.append(grp.sample(n=n, random_state=rng))
            sampled = pd.concat(parts, ignore_index=True)
            # trim or pad to exact target
            if len(sampled) > target:
                sampled = sampled.sample(n=target, random_state=rng)
            sampled_chunks.append(sampled)
        print(f"  Severity {sev}: sampled {len(sampled_chunks[-1]):,} rows")

    df = pd.concat(sampled_chunks, ignore_index=True).sample(frac=1, random_state=rng).reset_index(drop=True)
    print(f"  Total extracted: {len(df):,} rows")

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"  Saved to {output_path}")
    return df


# ---------------------------------------------------------------------------
# Phase 2 — Intelligent cleaning
# ---------------------------------------------------------------------------

# US State → Timezone mapping (for filling nulls)
STATE_TIMEZONE = {
    "AL": "US/Central", "AK": "US/Alaska", "AZ": "US/Mountain", "AR": "US/Central",
    "CA": "US/Pacific", "CO": "US/Mountain", "CT": "US/Eastern", "DE": "US/Eastern",
    "FL": "US/Eastern", "GA": "US/Eastern", "HI": "US/Hawaii", "ID": "US/Mountain",
    "IL": "US/Central", "IN": "US/Eastern", "IA": "US/Central", "KS": "US/Central",
    "KY": "US/Eastern", "LA": "US/Central", "ME": "US/Eastern", "MD": "US/Eastern",
    "MA": "US/Eastern", "MI": "US/Eastern", "MN": "US/Central", "MS": "US/Central",
    "MO": "US/Central", "MT": "US/Mountain", "NE": "US/Central", "NV": "US/Pacific",
    "NH": "US/Eastern", "NJ": "US/Eastern", "NM": "US/Mountain", "NY": "US/Eastern",
    "NC": "US/Eastern", "ND": "US/Central", "OH": "US/Eastern", "OK": "US/Central",
    "OR": "US/Pacific", "PA": "US/Eastern", "RI": "US/Eastern", "SC": "US/Eastern",
    "SD": "US/Central", "TN": "US/Central", "TX": "US/Central", "UT": "US/Mountain",
    "VT": "US/Eastern", "VA": "US/Eastern", "WA": "US/Pacific", "WV": "US/Eastern",
    "WI": "US/Central", "WY": "US/Mountain", "DC": "US/Eastern",
}

# US State → Census Region mapping
STATE_REGION = {
    "CT": "Northeast", "ME": "Northeast", "MA": "Northeast", "NH": "Northeast",
    "RI": "Northeast", "VT": "Northeast", "NJ": "Northeast", "NY": "Northeast",
    "PA": "Northeast",
    "IL": "Midwest", "IN": "Midwest", "MI": "Midwest", "OH": "Midwest",
    "WI": "Midwest", "IA": "Midwest", "KS": "Midwest", "MN": "Midwest",
    "MO": "Midwest", "NE": "Midwest", "ND": "Midwest", "SD": "Midwest",
    "DE": "South", "FL": "South", "GA": "South", "MD": "South",
    "NC": "South", "SC": "South", "VA": "South", "DC": "South",
    "WV": "South", "AL": "South", "KY": "South", "MS": "South",
    "TN": "South", "AR": "South", "LA": "South", "OK": "South", "TX": "South",
    "AZ": "West", "CO": "West", "ID": "West", "MT": "West",
    "NV": "West", "NM": "West", "UT": "West", "WY": "West",
    "AK": "West", "CA": "West", "HI": "West", "OR": "West", "WA": "West",
}

WEATHER_GROUPS = {
    "Clear": ["Fair", "Clear", "Fair / Windy"],
    "Cloudy": ["Cloudy", "Mostly Cloudy", "Partly Cloudy", "Overcast",
               "Scattered Clouds", "Cloudy / Windy", "Mostly Cloudy / Windy",
               "Partly Cloudy / Windy"],
    "Rain": ["Light Rain", "Rain", "Heavy Rain", "Light Drizzle", "Drizzle",
             "Rain Showers", "Light Rain Showers", "Heavy Rain Showers",
             "Rain / Windy", "Light Rain / Windy", "Heavy Rain / Windy",
             "Light Drizzle / Windy", "Showers in the Vicinity"],
    "Snow": ["Light Snow", "Snow", "Heavy Snow", "Light Snow / Windy",
             "Snow / Windy", "Heavy Snow / Windy", "Blowing Snow",
             "Blowing Snow / Windy", "Snow and Sleet", "Light Snow and Sleet",
             "Snow Grains", "Light Ice Pellets", "Ice Pellets",
             "Wintry Mix", "Wintry Mix / Windy", "Sleet", "Light Sleet",
             "Freezing Rain", "Light Freezing Rain", "Heavy Sleet",
             "Light Freezing Drizzle", "Freezing Drizzle"],
    "Fog": ["Fog", "Haze", "Mist", "Shallow Fog", "Patches of Fog",
            "Light Freezing Fog", "Haze / Windy", "Fog / Windy"],
    "Storm": ["Thunderstorm", "T-Storm", "Heavy T-Storm", "Thunderstorms and Rain",
              "Light Thunderstorms and Rain", "Heavy Thunderstorms and Rain",
              "T-Storm / Windy", "Heavy T-Storm / Windy",
              "Thunderstorm / Windy"],
    "Wind": ["Windy", "Blowing Dust", "Blowing Dust / Windy",
             "Blowing Sand", "Dust Whirls"],
    "Smoke": ["Smoke", "Smoke / Windy", "Volcanic Ash", "Widespread Dust"],
}

_WEATHER_CATEGORY_MAP: dict[str, str] = {}
for cat, conditions in WEATHER_GROUPS.items():
    for c in conditions:
        _WEATHER_CATEGORY_MAP[c] = cat


def _group_impute(df: pd.DataFrame, col: str, group_cols: list[str],
                  method: str = "median") -> pd.Series:
    """Impute missing values using grouped aggregation (relationship-based)."""
    s = df[col].copy()
    if s.isnull().sum() == 0:
        return s

    if method == "median":
        fill_vals = df.groupby(group_cols)[col].transform("median")
    else:
        fill_vals = df.groupby(group_cols)[col].transform(
            lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else np.nan
        )
    s = s.fillna(fill_vals)

    if method == "median":
        s = s.fillna(df[col].median())
    else:
        mode_val = df[col].mode()
        if len(mode_val) > 0:
            s = s.fillna(mode_val.iloc[0])
    return s


def _classify_time_of_day(hour: int) -> str:
    """Classify hour into time-of-day bucket."""
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"


def _get_season(month: int) -> str:
    """Map month number to season."""
    if month in (12, 1, 2):
        return "Winter"
    elif month in (3, 4, 5):
        return "Spring"
    elif month in (6, 7, 8):
        return "Summer"
    else:
        return "Fall"


def clean_accidents_data(df: pd.DataFrame) -> pd.DataFrame:
    """Full cleaning pipeline with relationship-based imputation.

    Steps:
      1. Drop unnecessary columns
      2. Parse datetimes and engineer temporal features
      3. Validate geographic coordinates
      4. Relationship-based imputation for weather variables
      5. Clean categorical columns
      6. Engineer derived features
      7. Final validation
    """
    print("\nPhase 2: Starting intelligent cleaning ...")
    result = df.copy()


    cols_to_drop = [c for c in COLUMNS_TO_DROP if c in result.columns]
    result.drop(columns=cols_to_drop, inplace=True, errors="ignore")
    print(f"  Dropped {len(cols_to_drop)} columns: {cols_to_drop}")

    result["Start_Time"] = pd.to_datetime(result["Start_Time"], errors="coerce")
    result["End_Time"] = pd.to_datetime(result["End_Time"], errors="coerce")

    result["Year"] = result["Start_Time"].dt.year
    result["Month"] = result["Start_Time"].dt.month
    result["Day_of_Week"] = result["Start_Time"].dt.dayofweek  # Mon=0
    result["Day_Name"] = result["Start_Time"].dt.day_name()
    result["Hour"] = result["Start_Time"].dt.hour
    result["Is_Weekend"] = result["Day_of_Week"].isin([5, 6])

    result["Time_of_Day"] = result["Hour"].apply(_classify_time_of_day)
    result["Season"] = result["Month"].apply(_get_season)


    result["Duration_min"] = (
        (result["End_Time"] - result["Start_Time"]).dt.total_seconds() / 60
    )

    result.loc[result["Duration_min"] < 0, "Duration_min"] = np.nan
    result.loc[result["Duration_min"] > 1440, "Duration_min"] = 1440
    result["Duration_min"] = _group_impute(
        result, "Duration_min", ["Severity"], "median"
    )

    print(f"  Temporal features engineered: Year, Month, Day_of_Week, Hour, etc.")

    lat_mask = result["Start_Lat"].between(24, 50)
    lng_mask = result["Start_Lng"].between(-125, -66)
    invalid_coords = (~lat_mask | ~lng_mask).sum()
    result = result[lat_mask & lng_mask].reset_index(drop=True)
    print(f"  Removed {invalid_coords} rows with invalid coordinates")

    dist_99 = result["Distance(mi)"].quantile(0.99)
    result.loc[result["Distance(mi)"] > dist_99, "Distance(mi)"] = dist_99
    result.loc[result["Distance(mi)"] < 0, "Distance(mi)"] = 0
    print(f"  Capped Distance at 99th percentile: {dist_99:.2f} mi")

    tz_null_mask = result["Timezone"].isnull()
    if tz_null_mask.any():
        result.loc[tz_null_mask, "Timezone"] = result.loc[tz_null_mask, "State"].map(STATE_TIMEZONE)
        print(f"  Filled {tz_null_mask.sum()} Timezone nulls from State mapping")

    null_before = result["Temperature(F)"].isnull().sum()
    result["Temperature(F)"] = _group_impute(
        result, "Temperature(F)", ["State", "Month", "Hour"], "median"
    )
    print(f"  Temperature(F): filled {null_before} nulls via State+Month+Hour median")

    null_before = result["Humidity(%)"].isnull().sum()
    result["Humidity(%)"] = _group_impute(
        result, "Humidity(%)", ["State", "Month"], "median"
    )
    print(f"  Humidity(%): filled {null_before} nulls via State+Month median")

    null_before = result["Pressure(in)"].isnull().sum()
    result["Pressure(in)"] = _group_impute(
        result, "Pressure(in)", ["State", "Month"], "median"
    )
    print(f"  Pressure(in): filled {null_before} nulls via State+Month median")

    null_before = result["Wind_Direction"].isnull().sum()
    result["Wind_Direction"] = _group_impute(
        result, "Wind_Direction", ["State", "Month"], "mode"
    )
    print(f"  Wind_Direction: filled {null_before} nulls via State+Month mode")

    null_before = result["Weather_Condition"].isnull().sum()
    result["Weather_Condition"] = _group_impute(
        result, "Weather_Condition", ["State", "Month"], "mode"
    )
    print(f"  Weather_Condition: filled {null_before} nulls via State+Month mode")


    ss_null = result["Sunrise_Sunset"].isnull()
    if ss_null.any():
        result.loc[ss_null, "Sunrise_Sunset"] = result.loc[ss_null, "Hour"].apply(
            lambda h: "Day" if 6 <= h < 18 else "Night"
        )
    for tw_col in ["Civil_Twilight", "Nautical_Twilight", "Astronomical_Twilight"]:
        tw_null = result[tw_col].isnull()
        if tw_null.any():
            result.loc[tw_null, tw_col] = result.loc[tw_null, "Hour"].apply(
                lambda h: "Day" if 6 <= h < 18 else "Night"
            )

    null_before = result["Visibility(mi)"].isnull().sum()
    result["Visibility(mi)"] = _group_impute(
        result, "Visibility(mi)", ["Weather_Condition", "Sunrise_Sunset"], "median"
    )
    print(f"  Visibility(mi): filled {null_before} nulls via Weather+DayNight median")

    null_before = result["Wind_Speed(mph)"].isnull().sum()
    result["Wind_Speed(mph)"] = _group_impute(
        result, "Wind_Speed(mph)", ["Weather_Condition", "State"], "median"
    )
    print(f"  Wind_Speed(mph): filled {null_before} nulls via Weather+State median")


    result["Zipcode"] = result["Zipcode"].astype(str).str[:5]
    result.loc[result["Zipcode"] == "nan", "Zipcode"] = np.nan
    if result["Zipcode"].isnull().any():
        result["Zipcode"] = _group_impute(result, "Zipcode", ["City", "State"], "mode")


    if result["Street"].isnull().any():
        result["Street"] = result["Street"].fillna("Unknown")


    road_features = ["Amenity", "Bump", "Crossing", "Give_Way", "Junction",
                     "No_Exit", "Railway", "Roundabout", "Station", "Stop",
                     "Traffic_Calming", "Traffic_Signal"]
    result["Road_Feature_Count"] = result[road_features].sum(axis=1)

    result["Is_Rush_Hour"] = result["Hour"].apply(
        lambda h: (7 <= h <= 9) or (16 <= h <= 19)
    )

    print(f"  Derived features added: Road_Feature_Count, Is_Rush_Hour")

    before = len(result)
    result = result.drop_duplicates().reset_index(drop=True)
    print(f"  Removed {before - len(result)} duplicate rows")

    remaining_nulls = result.isnull().sum()
    total_nulls = remaining_nulls.sum()
    if total_nulls > 0:
        print(f"\n  ⚠ Remaining nulls ({total_nulls} total):")
        for col, cnt in remaining_nulls[remaining_nulls > 0].items():
            print(f"    {col}: {cnt}")
        result = result.dropna().reset_index(drop=True)
        print(f"  Dropped remaining null rows. Final shape: {result.shape}")
    else:
        print(f"  ✓ Zero nulls remaining. Final shape: {result.shape}")

    return result


# ---------------------------------------------------------------------------
# Phase 5 — Tableau-ready preparation
# ---------------------------------------------------------------------------

def prepare_tableau_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Add KPI columns and format for Tableau import."""
    print("\nPhase 5: Preparing Tableau-ready dataset ...")
    result = df.copy()

    # Severity labels
    sev_labels = {1: "Low", 2: "Moderate", 3: "High", 4: "Critical"}
    result["Severity_Label"] = result["Severity"].map(sev_labels)

    # Weather category
    result["Weather_Category"] = result["Weather_Condition"].map(_WEATHER_CATEGORY_MAP)
    result["Weather_Category"] = result["Weather_Category"].fillna("Other")

    # State region
    result["State_Region"] = result["State"].map(STATE_REGION)
    result["State_Region"] = result["State_Region"].fillna("Other")

    # Clean column names for Tableau (readable, no special chars)
    col_rename = {
        "Distance(mi)": "Distance_mi",
        "Temperature(F)": "Temperature_F",
        "Humidity(%)": "Humidity_pct",
        "Pressure(in)": "Pressure_in",
        "Visibility(mi)": "Visibility_mi",
        "Wind_Speed(mph)": "Wind_Speed_mph",
    }
    result = result.rename(columns=col_rename)

    # Format datetime columns as strings for Tableau
    for col in ["Start_Time", "End_Time"]:
        if col in result.columns:
            result[col] = pd.to_datetime(result[col], errors="coerce")
            result[col] = result[col].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Convert booleans to int for Tableau compatibility
    bool_cols = result.select_dtypes(include="bool").columns
    for col in bool_cols:
        result[col] = result[col].astype(int)

    print(f"  Added Severity_Label, Weather_Category, State_Region")
    print(f"  Final Tableau dataset shape: {result.shape}")
    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_clean_dataset(input_path: Path) -> pd.DataFrame:
    """Read a raw CSV file and return a cleaned dataframe."""
    df = pd.read_csv(input_path)
    return basic_clean(df)


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    """Write the cleaned dataframe to disk, creating the parent folder if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the DeliverIQ ETL pipeline.")
    parser.add_argument(
        "--input", required=True, type=Path,
        help="Path to the raw CSV file in data/raw/.",
    )
    parser.add_argument(
        "--output", required=True, type=Path,
        help="Path to the cleaned CSV file in data/processed/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cleaned_df = build_clean_dataset(args.input)
    save_processed(cleaned_df, args.output)
    print(f"Processed dataset saved to: {args.output}")
    print(f"Rows: {len(cleaned_df)} | Columns: {len(cleaned_df.columns)}")


if __name__ == "__main__":
    main()
