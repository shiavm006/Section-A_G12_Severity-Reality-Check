# Data Dictionary: US Accidents (March 2023)

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | US Accidents (2016 - 2023) |
| Source | Kaggle (Sobhan Moosavi) |
| Raw file name | US_Accidents_March23.csv |
| Granularity | One row per reported traffic accident |

## Column Definitions

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `Severity` | int | Impact on traffic (1=Low, 4=High). **Not physical injury severity**. | 2 | Target, KPI | No missing values. Extracted a balanced sample representing all 4 levels. |
| `Start_Time` | datetime | When the accident occurred / traffic impact began. | 2016-02-08 05:46:00 | EDA, Derived | Formatted properly. Used to derive temporal features. |
| `End_Time` | datetime | When the traffic impact ended. | 2016-02-08 11:00:00 | EDA | Formatted properly. Used to derive Duration. |
| `Start_Lat` | float | Latitude of accident start. | 39.8651 | Location | Validated to be within US bounds (24-50). |
| `Start_Lng` | float | Longitude of accident start. | -84.0587 | Location | Validated to be within US bounds (-125 to -66). |
| `Distance_mi` | float | Length of road extent affected by accident. | 0.01 | EDA | Capped outliers at 99th percentile (~9.06 mi). Set negative to 0. |
| `Street` | string | Street name. | I-70 E | Location | Filled missing values with "Unknown". |
| `City` | string | City name. | Dayton | Location | Dropped 5 rows with missing City. |
| `County` | string | County name. | Montgomery | Location | - |
| `State` | string | State abbreviation. | OH | Location, Stratification | - |
| `Zipcode` | string | 5-digit ZIP code. | 45424 | Location | Trimmed to 5 characters. Filled few nulls with mode by City+State. |
| `Timezone` | string | US Timezone. | US/Eastern | Location | Filled missing values using a predefined State-to-Timezone mapping. |
| `Temperature_F` | float | Temperature in Fahrenheit. | 36.9 | EDA | Imputed using median by **State + Month + Hour**. |
| `Humidity_pct` | float | Humidity percentage. | 91.0 | EDA | Imputed using median by **State + Month**. |
| `Pressure_in` | float | Atmospheric pressure in inches. | 29.68 | EDA | Imputed using median by **State + Month**. |
| `Visibility_mi` | float | Visibility in miles. | 10.0 | EDA | Imputed using median by **Weather_Condition + Sunrise_Sunset**. |
| `Wind_Direction` | string | Wind direction. | SW | Weather | Imputed using mode by **State + Month**. |
| `Wind_Speed_mph` | float | Wind speed in mph. | 4.6 | EDA | Imputed using median by **Weather_Condition + State**. |
| `Weather_Condition` | string | Text description of weather. | Light Rain | EDA, KPI | Imputed using mode by **State + Month**. Used for Weather Category. |
| `Amenity` - `Traffic_Signal` | bool (int for Tableau) | Various road features near the accident. | 0 or 1 | EDA | Cast to int for Tableau. Kept as-is. |
| `Sunrise_Sunset` | string | Day or Night based on sunrise. | Night | EDA | Imputed from Hour (6-18=Day, else Night). |

## Derived Columns

| Derived Column | Logic | Business Meaning |
|---|---|---|
| `Year`, `Month`, `Day_of_Week`, `Hour` | Extracted from `Start_Time`. | Temporal trend analysis. Day_of_Week (0=Mon, 6=Sun). |
| `Day_Name` | Mon/Tue/Wed... from `Day_of_Week`. | Readable labels for charts. |
| `Is_Weekend` | True if Saturday or Sunday. | Identifies if accident happened on a weekend. |
| `Time_of_Day` | Morning (5-11), Afternoon (12-16), Evening (17-20), Night (21-4). | Grouping into business/non-business chunks. |
| `Season` | Winter/Spring/Summer/Fall from `Month`. | Identifies seasonal risk. |
| `Duration_min` | `(End_Time - Start_Time)` in minutes. | Represents total delay time. Capped negative/outliers, imputed missing. |
| `Road_Feature_Count` | Sum of all binary road feature flags. | Quantifies intersection/road complexity. |
| `Is_Rush_Hour` | True if Hour is 7-9 or 16-19. | Key identifier for Congestion Bias testing. |
| `Severity_Label` | 1="Low", 2="Moderate", 3="High", 4="Critical". | Tableau-friendly naming. |
| `Weather_Category` | Rolled up 52 conditions into ~8 categories. | Simplifies weather filtering in Tableau. |
| `State_Region` | Mapped States to Census Regions (Northeast, South, etc). | High-level geographic comparison. |

## Data Quality Notes

- **End_Lat, End_Lng**: Dropped completely (100% null).
- **Turning_Loop, Country**: Dropped (zero variance, 100% False / "US").
- **Wind_Chill, Precipitation**: Dropped due to extremely high missing rates (>50%).
- **Sampling Strategy**: The original 7.7M row dataset was extremely imbalanced. We created a ~100k stratified sample ensuring enough representation for Severity 1 and 4, while avoiding geographic bias by stratifying over State.
- **Null Imputation**: Rather than using global means, we filled weather variables contextually (e.g., finding the median temperature for a specific state, in a specific month, at a specific hour).
