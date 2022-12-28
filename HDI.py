# TASK 1. HDI data scrape from Wikipedia
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date

wikiurl = 'https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index'
table_class = "wikitable sortable plainrowheaders"
# Retrieve the page and parse the HTML
response = requests.get(wikiurl)
# Check the HTTP response status code
if response.status_code != 200:
    print("Error: Could not retrieve the page.")
else:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the table on the page
    hdi_table = soup.find('table', {'class': table_class})

    if hdi_table:
        # Extract the data from the table and store it in a Pandas DataFrame
        tables = pd.read_html(str(hdi_table))
# Extract the columns with the HDI score and country name
hdi_df = tables[0][['Nation', 'HDI']]
# Print the resulting DataFrame
my_dataframe = pd.DataFrame(hdi_df)
my_df = my_dataframe.drop(my_dataframe.columns[2], axis=1)
my_df.rename(columns={'Nation': 'Country'}, inplace=True)
my_df.rename(columns={'HDI': 'HDI_score'}, inplace=True)
my_final_df = pd.DataFrame()
my_final_df = my_final_df.assign(Country=my_df["Country"])
my_final_df = my_final_df.assign(HDI_score=my_df["HDI_score"])
otabek = my_final_df.sort_values(by='Country')

# TASK 2. Country Data via API

response1 = requests.get("https://restcountries.com/v3.1/all")
# Check the HTTP response status code
if response1.status_code != 200:
    print("Error: Could not retrieve the data.")
else:
    # Parse the JSON response
    data = response1.json()
    country_data = pd.DataFrame(columns=["Name", "Population", "Area", "Gini", "Neighbors"])
    for country in data:
        name = country["name"]
        population = country['population']
        area = country['area']

        country_data = country_data.append({"Name": name, 'Population': population, 'Area': area}, ignore_index=True)

names = country_data["Name"]


def get_value(row, column, key):
    return row[column].get(key)


country_data["Names1"] = country_data.apply(get_value, args=("Name", "common"), axis=1)
DATA = country_data.drop("Name", axis=1)
perfect_data = DATA.reindex(columns=["Names1", "Population", "Area", "Gini", "Neighbors"])
perfect_data.rename(columns={'Names1': 'Country'}, inplace=True)
merged_otabek_perfectdata = pd.merge(otabek, perfect_data, on="Country")
response_gini = requests.get('https://restcountries.com/v2/all?fields=name,gini')
data_gini = response_gini.json()
df_gini = pd.DataFrame(data_gini)
GINI = pd.DataFrame(df_gini)
GINI_df = GINI.drop("independent", axis=1)
GINI_df.rename(columns={"name": "Country"}, inplace=True)
GINI_df.rename(columns={"gini": "Gini"}, inplace=True)
df10 = merged_otabek_perfectdata.drop("Gini", axis=1)
df11 = df10.drop("Neighbors", axis=1)
merged_gini_rest = pd.merge(df11, GINI_df, on="Country")
response_neighbors = requests.get('https://restcountries.com/v2/all?fields=name,borders')
# Parse the response as JSON
data_borders = response_neighbors.json()
# Convert the data into a Pandas DataFrame
borders_df = pd.DataFrame(data_borders)
new_border = pd.DataFrame(borders_df[['name', 'borders']])


def count_borders(row):
    borders = row['borders']
    if not borders or not isinstance(borders, list):
        return 0
    return len(borders)


new_border['Neighbors'] = new_border.apply(count_borders, axis=1)
df_neighbor = new_border.drop("borders", axis=1)
df_neighbor.rename(columns={"name": "Country"}, inplace=True)
df = pd.merge(merged_gini_rest, df_neighbor, on="Country")

# TASK 3. Analysis  (We need to make the population column into float to use pd.corr() function


col = df["Population"]
col = col.astype(float)
df["Population"] = col
correlation = df.corr()['HDI_score']
my_corr = pd.DataFrame(correlation)
my_corr_ready = my_corr.drop("HDI_score", axis=0)

# TASK 4. Reporting and closing the program

today = date.today()
my_corr_ready.to_csv(str(today) + ".txt", index=True)
my_corr_ready.rename(columns={"HDI_score": "Correlation Report - HDI_score"}, inplace=True)
my_corr_ready.to_csv(str(today) + ".txt", index=True)

sys.exit(0)
