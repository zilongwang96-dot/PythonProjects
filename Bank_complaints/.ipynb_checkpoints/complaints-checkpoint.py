import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path 

# Concatenate data from 2019 to 2025
desktop = (Path.home() / "Desktop"/"data analysis practice"/"Consumer Banking Complaints")

year_2019 = pd.read_csv(desktop/ "2019_year.csv")
year_2020 = pd.read_csv(desktop/ "2020_year.csv")
year_2021 = pd.read_csv(desktop/ "2021_year.csv")
year_2022 = pd.read_csv(desktop/ "2022_year.csv")
year_2023 = pd.read_csv(desktop/ "2023_year.csv")
year_2024 = pd.read_csv(desktop/ "2024_year.csv")
year_2025 = pd.read_csv(desktop/ "2025_year.csv")

complaints = pd.concat([year_2019,
                year_2020,
                year_2021,
                year_2022,
                year_2023,
                year_2024,
                year_2025,
                ])

# Create a copy of orignial data
clean_complaints = complaints.copy()

# Replace spaces with "_" in columns 
clean_complaints.columns = clean_complaints.columns.str.replace(" ", "_")
                                                         

# convert date recived to date time format
clean_complaints["Date_received"] = pd.to_datetime(clean_complaints["Date_received"])

# 
#print(clean_complaints.shape)   # 299997 rows, 16 columns
#print(clean_complaints.info())

# Check for duplicates 
#print(clean_complaints.duplicated().sum())

# Check for missing values
#print(clean_complaints.isna().sum())   # State missing 5874 values

# Convert "Timely_response?" column to binary values
clean_complaints["Timely_response?"] = clean_complaints["Timely_response?"].replace({"Yes": 1, "No": 0})

clean_complaints = clean_complaints.drop(columns = ["Product",
                                                    "Sub-product",
                                                    "Consumer_complaint_narrative",
                                                    "Company_public_response",
                                                    "Tags",
                                                    "Date_sent_to_company",
                                                    ])

# include only valid states in the data
valid_states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC"
]

state_abbreviations = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut",
    "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida",
    "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
    "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky",
    "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
    "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"
}
clean_complaints = clean_complaints[
    clean_complaints["State"].isin(valid_states)].copy()

clean_complaints["State"] = clean_complaints["State"].map(state_abbreviations)

"""
print(clean_complaints.head().T)
print(clean_complaints["Company"].value_counts())
print(clean_complaints["Issue"].value_counts())
print(clean_complaints["Company_response_to_consumer"].value_counts())
print(clean_complaints["Timely_response?"].value_counts())
print(clean_complaints["Submitted_via"].value_counts())
print(clean_complaints["State"].value_counts())
print(clean_complaints["Sub-issue"].value_counts())
"""


# Population by state
pop_2019 = pd.read_excel(desktop/ "2010_2019_population.xlsx", 
                         header = [2,3])
pop_2020_2025 = pd.read_excel(desktop/ "2020_2025_population.xlsx", 
                              header = [2,3])

pop_2019.columns = [
    "_".join(
        str(part).strip()
        for part in column
        if "Unnamed" not in str(part)
    )
    for column in pop_2019.columns
]

# Replace spaces with "_" and convert to lower case
pop_2019.columns = (pop_2019.columns
                    .str.replace(" ", "_")
                    .str.replace("-", "_")
                    .str.lower())

# Rename the columns to match the years
pop_2019 = pop_2019.rename(columns = {"population_estimate_(as_of_july_1)_2019" : "2019"})

# Remove the "." from the geographic_area column
pop_2019["geographic_area"] = pop_2019["geographic_area"].str.strip(".")

# Select only the geographic_area and 2019 columns
pop_2019 = pop_2019[["geographic_area", "2019"]]

# iloc[] select rows or columns by their number position. .reset_index(drop=True) rests the index number so it starts at 0 again.
pop_2019 = pop_2019.iloc[5:-7].reset_index(drop=True)

# Cleaning the 2020-2025 population data
pop_2020_2025.columns = [
    "_".join(
        str(part).strip()
        for part in column
        if "Unnamed" not in str(part)
    )
    for column in pop_2020_2025.columns
]
# Replace spaces with "_" and convert to lower case
pop_2020_2025.columns = (pop_2020_2025.columns
                    .str.replace(" ", "_")
                    .str.replace("-", "_")
                    .str.lower())

# rename the columns to match the years
pop_2020_2025 = pop_2020_2025.rename(columns = {"population_estimate_(as_of_july_1)_2020" : "2020"})
pop_2020_2025 = pop_2020_2025.rename(columns = {"population_estimate_(as_of_july_1)_2021" : "2021"})
pop_2020_2025 = pop_2020_2025.rename(columns = {"population_estimate_(as_of_july_1)_2022" : "2022"})
pop_2020_2025 = pop_2020_2025.rename(columns = {"population_estimate_(as_of_july_1)_2023" : "2023"})
pop_2020_2025 = pop_2020_2025.rename(columns = {"population_estimate_(as_of_july_1)_2024" : "2024"})
pop_2020_2025 = pop_2020_2025.rename(columns = {"population_estimate_(as_of_july_1)_2025" : "2025"})

pop_2020_2025 = (pop_2020_2025.iloc[5:-8]
                              .drop(columns = ["april_1,_2020_estimates_base","geographic_area"])
                              .reset_index(drop=True))

# concatenate the two population dataframes
population = pd.concat([pop_2019,
                        pop_2020_2025
                        ], axis = 1)

#export the cleaned population data to an excel file
population.to_excel(desktop/ "clean_population.xlsx", index = False)

"""
# horizontal bar chart of complaints by state
state_count = clean_complaints["State"].value_counts().sort_values(ascending = True)
plt.barh(state_count.index, state_count.values)
plt.tight_layout()
plt.title("Number of Complaints by State")
plt.xlabel("Number of Complaints")
plt.ylabel("State")

plt.show()
"""

results = []

for year in range(2019,2026): 

    # Filter the complaints data for the current year
    complaints_year = clean_complaints[clean_complaints["Date_received"].dt.year == year]
    
    # Count the number of complaints by state for the current year
    state_count_year = (
    complaints_year["State"]
    .value_counts()
    .reset_index()
    )
    # renames the columns
    state_count_year.columns = ["State", "Complaints"]

    # Merge with that year's population
    yearly_data = state_count_year.merge(
        population[["geographic_area", str(year)]],
        left_on="State",
        right_on="geographic_area"
    )

    # Calculate complaints per 100k
    yearly_data["Complaints_per_100k"] = (
        yearly_data["Complaints"]
        / yearly_data[str(year)]
        * 100000
    )

    yearly_data["Year"] = year

    # Keep only the columns you actually want
    yearly_data = yearly_data[
        ["State", "Year", "Complaints_per_100k"]
    ]

    results.append(yearly_data)

complaints_per_capita = pd.concat(
    results,
    ignore_index=True
)

print(complaints_per_capita)
 
state_avg = complaints_per_capita["Complaints_per_100k"].mean()
state_medium = complaints_per_capita["Complaints_per_100k"].median()

print(state_avg)
print(state_medium)