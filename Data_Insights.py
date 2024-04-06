# -*- coding: utf-8 -*-
"""Untitled35.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e4G6LjCCngnzPT-ce6UG3szdzh4vRW9J
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np

df1 = pd.read_csv('/content/wtf.csv')

# Define a function to calculate 'COMP_PRICE' based on the conditions
def calculate_comp_price(group):
    # Check if any row in rank 1 contains "LASER RE" using partial match
    if (group['RANK'] == 1).any() and group.loc[group['RANK'] == 1, 'SUPPLIER'].str.contains('LASER RE').any():
        # Set COMP_PRICE to the price of rank 1
        group['COMP_PRICE'] = group.loc[group['RANK'] == 1, 'PRICE']
    else:
        # Set COMP_PRICE to the price of rank 1 minus 0.02
        group['COMP_PRICE'] = group.loc[group['RANK'] == 1, 'PRICE'] - 0.02
    return group


def create_comp_df(df1):

  # Calculate the date 12 months ago from today
  start_date = datetime.now() - timedelta(days=365)

  # Filter the DataFrame for dates greater than or equal to the start_date
  df1 = df1[df1['Date'] >= start_date]

  # Now last_12_months_df contains only the rows from the last 12 months


  df1 = df1[df1['SOS'] == '(null)']

  # Step 1: Filter df1 for rows where the supplier is "LASER RE-NU INTERNATIONAL"
  laser_re_nu_df1 = df1[df1['SUPPLIER'].str.contains('LASER RE-NU INTERNATIONAL', case=False, na=False)]

  # Step 2: Extract the unique part numbers sold by LASER RE-NU INTERNATIONAL
  laser_re_nu_part_numbers = laser_re_nu_df1['MFPARTNUMBER'].unique()

  # Step 3: Filter df1 to include only the part numbers sold by LASER RE-NU INTERNATIONAL
  comp_df = df1[df1['MFPARTNUMBER'].isin(laser_re_nu_part_numbers)].copy()

  # Step 4: Count the number of unique competitors for each part number
  #part_number_competitor_counts = comp_df.groupby('MFPARTNUMBER')['SUPPLIER'].nunique()

  # Step 5: Filter the DataFrame to include only part numbers with more than one competitor
  #comp_df = comp_df[comp_df['MFPARTNUMBER'].isin(part_number_competitor_counts[part_number_competitor_counts > 1].index)]

  # Step 6: Create a new column called "rank" where the part numbers are ranked by price within each group of part numbers
  # Group by 'MFPARTNUMBER' and 'SUPPLIER', calculate the sum of 'EXTNEDEDPRICE'
  df_grouped = df1.groupby(['MFPARTNUMBER', 'SUPPLIER'])['EXTNEDEDPRICE'].sum().reset_index()

  # Group by 'MFPARTNUMBER' and rank based on the sum of 'EXTNEDEDPRICE'
  df_grouped['RANK'] = df_grouped.groupby('MFPARTNUMBER')['EXTNEDEDPRICE'].rank(method='dense', ascending=False)

  # Merge the ranked data back to the original DataFrame
  comp_df = pd.merge(comp_df, df_grouped[['MFPARTNUMBER', 'SUPPLIER', 'RANK']], on=['MFPARTNUMBER', 'SUPPLIER'], how='left')









  # Load the CSV file into a DataFrame
  cost_df = pd.read_csv('43_items.csv')
  cost_df.rename(columns={'Part Number': 'MFPARTNUMBER'}, inplace=True)

  # Merge comp_df with cost_df based on the common 'Part Number' column
  comp_df = pd.merge(comp_df, cost_df, on='MFPARTNUMBER', how='left')















  # Group by 'MFPARTNUMBER' and get the 'NAME' associated with 'RANK' 1
  comp_df['RANK1_NAME'] = comp_df.groupby('MFPARTNUMBER')['NAME'].transform(lambda x: x.iloc[0] if x.index[0] == x.index.min() else None)

  # Assuming comp_df is your DataFrame containing the columns 'MFPARTNUMBER', 'RANK', and 'PRICE'
  comp_df['RANK1_PRICE'] = comp_df.groupby('MFPARTNUMBER')['PRICE'].transform(lambda x: x.iloc[0] if x.index[0] == x.index.min() else None)

  # Price for 'LASER RE'
  comp_df['LASER_RE_PRICE'] = comp_df.loc[comp_df['SUPPLIER'].str.contains('LASER RE'), 'PRICE']

  # Supplier of Rank 1
  comp_df['RANK1_SUPPLIER'] = comp_df.groupby('MFPARTNUMBER')['SUPPLIER'].transform(lambda x: x.iloc[0] if x.index[0] == x.index.min() else np.nan)

  # MFNAME
  comp_df['RANK1_MFNAME'] = comp_df.groupby('MFPARTNUMBER')['MFNAME'].transform('first')








  return comp_df



# Function to extract the first two words from a supplier name
def get_first_two_words(supplier_name):
    words = supplier_name.split()[:2]  # Extract the first two words
    return ' '.join(words)  # Join the words back into a single string

# Define a custom function to calculate the COMP_PRICE column
#def calculate_comp_price(group):
    # Identify rows where the rank is 1 and the supplier is "LASER RE-NU INTERNATIONAL"
    #rank_1_laser_re_nu = (group['RANK'] == 1) & group['SUPPLIER'].str.contains('LASER RE-NU INTERNATIONAL')

    # Identify rows where the rank is 2
    #rank_2 = (group['RANK'] == 2)

    # Calculate comp_price based on conditions
    #comp_price = group['PRICE'] - 0.02  # Subtract 0.02 from all prices initially
    #comp_price.loc[rank_1_laser_re_nu] = group.loc[rank_2, 'PRICE'] - 0.02  # If rank 1 is "LASER RE-NU INTERNATIONAL", set comp_price to rank 2 price - 0.02
    #return comp_price


def calculate_comp_price(group):

    # Identify rows where the supplier contains "LASER RE" and the rank is 1
    laser_re_rank_1 = group['SUPPLIER'].str.contains('LASER RE') & (group['RANK'] == 1)

    # Identify rows where the rank is 2
    rank_2 = (group['RANK'] == 2)

    if laser_re_rank_1.any():
      rank_1_laser_re_nu = (group['RANK'] == 1) & group['SUPPLIER'].str.contains('LASER RE-NU INTERNATIONAL')
      comp_price = group['PRICE'] - 0.02  # Subtract 0.02 from all prices initially
      comp_price.loc[rank_1_laser_re_nu] = group.loc[rank_2, 'PRICE'] - 0.02
      return comp_price

    else:
      # Calculate comp_price based on conditions for each row in the group
      comp_price = group['PRICE'] - 0.02  # Subtract 0.02 from all prices initially
      comp_price_valid = comp_price > group['Cost']
      comp_price[~comp_price_valid] = None  # Set to None where condition is not met
      return comp_price





# Define a custom function to calculate the difference with rank 1 or 2
def calculate_difference(x):
    # Check if rank 1 item has the specified supplier
    if x.loc[x['RANK'] == 1, 'SUPPLIER'].str.contains('LASER RE-NU INTERNATIONAL').any():
        # Get price of rank 2 if rank 1 has the specified supplier
        rank_2_price = x.loc[x['RANK'] == 2, 'PRICE'].iloc[0]
        return x['PRICE'] - rank_2_price
    else:
        # Get price of rank 1 if rank 1 doesn't have the specified supplier
        rank_1_price = x.loc[x['RANK'] == 1, 'PRICE'].iloc[0]
        return x['PRICE'] - rank_1_price

# Competitor List
comp_list = ['ELLISON SYSTEMS INC. D/B/A SHOPLET.',
              'UNITED OFFICE SOLUTIONS, INC',
              'BERGAMO GROUP BUSINESS SOLUTIONS',
              'REPLENISH INK INC',
              'THE OFFICE GROUP, INC.',
              'ALPHAVETS LLC',
              'SUPPLIES NOW',
              'B & D SUPPLIES, INC.',
              'AAA LASER SERVICE & SUPPLIES, INC.',
              'STAPLES INC',
              'AXISCORE, LLC D/B/A COREBUY',
              'HASKELL NEW YORK INC.',
              'INNOVATIVE OFFICE SOLUTIONS LLC',
              'STERLING BUSINESS MACHINES, INC',
              'TONERQUEST',
              'THE OFFICE GROUP INC',
              'CAPRICE ELECTRONICS, INC.',
              'RITAS TAPE MEDIA / COMPUPRO GLOBAL',
              'JLWS ENTERPRISES INC.',
              'STEC-STEADFAST TECHNICS',
              'RED HILL SUPPLY',
              'GOOGOZ.COM, INC.',
              'ENTERPRISE TECHNOLOGY SOLUTIONS,INC',
              'PREMIER & COMPANIES, INC.',
              'ZEE TECHNOLOGIES',
              'GORILLA STATIONERS LLC',
              'SOLVIX SOLUTIONS LLC',
              'PELICAN SALES, INC.',
              'DREAM RANCH LLC / DREAM RANCH OFFIC',
              'ADVANTAGE OFFICE PRODUCTS, LLC',
              'OFFICE TEC SUPPLIES',
              'COMPLETE PACKAGING & SHIPPING SUPPL',
              'BUSINESS PRODUCTS GROUP INC',
              'LUCILLE MAUD CORPORATION',
              'M&A GLOBAL CARTRIDGES LLC',
              'DE NOVO GROUP LLC',
              'MENSCH MILL & LUMBER CORP.',
              'JFK SUPPLIES INC',
              'TSRC INC. DBA FRANK PARSONS',
              'WECSYS LLC',
              'PREMIER BUSINESS PRODUCTS, INC.',
              'BAHFED CORP',
              'GREAT FALLS PAPER COMPANY',
              'EVERY TOOL, INC.',
              'KLEIN, WALTER',
              'ALLIED INK CORPORATION',
              'BZ DEFENSE LLC',
              'WINSTON-SALEM INDUSTRIES FOR THE BL',
              'OFFICE DEPOT, INC.',
              'ACORN OFFICE PRODUCTS',
              'SUPPLY CHIMP',
              'AFFORDABLE CUSTODIAL SUPPLY',
              'NEW CENTURY TECHNOLOGIES INC',
              'CRIMSON IMAGING SUPPLIES, LLC',
              'MORCHEM INDUSTRIES INC.',
              'INDEPENDENT HARDWARE, INC.',
              'MSC INDUSTRIAL DIRECT CO., INC.',
              'WRIGGLESWORTH ENTERPRISES, INC.',
              'DOCUMENT IMAGING DIMENSIONS, INC.',
              'GOVERNMENT OFFICE TECHNOLOGIES LLC',
              'LIBERTY DATA PRODUCTS, INC.',
              'HORIZON OFFICE SUPPLY LLC',
              'NOREX GROUP, LLC',
              'COMPONENT SOURCING GROUP',
              'WESTCARB ENTERPRISES, INC.',
              'MSC INDUSTRIAL SUPPLY CO, INC',
              'M.A.N.S. DISTRIBUTORS, INC.',
              'SEVA TECHNICAL SERVICES',
              'AMERICAN SANITARY PRODUCTS, INC.',
              'CNC FEDERAL SUPPLIES',
              'NOBLE SUPPLY & LOGISTICS',
              'HUNTON OFFICE SUPPLY',
              'EME SOLUTIONS',
              'MDM OFFICE SYSTEMS',
              'INTERIOR FACILITIES DESIGN, LLC',
              'MORNING STAR INDUSTRIES, INC.',
              'NATIONAL INDUSTRIES FOR THE BLIND',
              'PERFECT OUTPUT, DBA LASEREQUIPMENT',
              'L C INDUSTRIES INC.',
              'CAPP, INC.',
              'GLOBAL SUPPLY CENTER',
              'ZIOS CORPORATION',
              'MENSCH MILL & LUMBER',
              'AUTOMATION AIDS INC',
              'NORTHEAST OFFICE SUPPLY CO. LLC.',
              'BLUEBAY OFFICE INC.',
              'STERILE SERVICES CO.',
              'HOFFMAN TECHNOLOGIES, INC.',
              'KPAUL PROPERTIES LLC',
              'HARDWARE, INC.',
              'AMERICAN TONER AND SUPPLY',
              'KAPLAN EARLY LEARNING COMPANY',
              'THE OFFICE PAL NJ LLC',
              'XY SYSTEMS INC.',
              'AITA CONSULTING SERVICES INC',
              'BURHANI ENTERPRISES, INC.',
              'FCI TECH INC.',
              'INTERNATIONAL COMMERCE & MARKETING',
              'THE TOOLS MAN INC',
              'SOURCE ONE MRO',
              'SPS INDUSTRIAL INC.',
              'DIVINE IMAGING INC.',
              'BOTACH INC.',
              'CARTRIDGE SAVERS INC.',
              'SUPPLY-SAVER CORPORATION',
              'WORLDWIDE MEDICAL PRODUCTS',
              'SHELBY DISTRIBUTIONS',
              'SHORE SOLUTIONS, INC.',
              'WISECOM TECHNOLOGIES INC',
              'PROCUREMENT & GOVERNMENT SALES INC',
              'COMMUNICATIONS PROFESSIONALS, INC.',
              'MIDWEST OFFICE SUPPLY',
              'ROYAL MEDIA NETWORK, INC.',
              'RELYCO SALES, INC.',
              'GRAYBAR ELECTRIC COMPANY, INC',
              'TRI-STATE CAMERA EXCH. INC.',
              'ARTISTRY LLC',
              'TERA CONSULTING INC',
              'FEDERAL SUPPLY LLC',
              'MJL ENTERPRISES LLC',
              'HD SUPPLY FACILITIES MAINTENANCE',
              'SITA BUSINESS SYSTEMS, INC.',
              'XY-SYSTEMS, INC.',
              'ZOLL MEDICAL CORPORATION',
              'AMERICAN TONER & INK',
              'LAZER CARTRIDGES PLUS, LLC.',
              'MANER BUILDERS SUPPLY COMPANY, LLC',
              'NEW CENTURY IMAGING',
              'HALL & ASSOCIATES COMPUTING INC',
              'SAITECH INC.',
              'PROSOURCE PACKAGING, INC.',
              'JACOBS GARDNER SUPPLY CO., INC.',
              'ARYA CORPORATION',
              'THE SUPPLIES GUYS',
              'WATS INTERNATIONAL INC',
              'MISTER PAPER INC',
              'NEW CENTURY IMAGING, INC',
              'BLUE FISH WORX, L.P',
              'GUY BROWN, LLC',
              'PACIFIC INK, INC.',
              'ATHANA INTERNATIONAL, INC.',
              'PERFORMIX BUSINESS SERVICES LLC',
              'ACCESS PRODUCTS INC.',
              'BETTER DIRECT',
              'MAPLE AMHERST ASSOCIATES, INC.',
              'DBISP, LLC',
              'APPLIED INDUSTRIAL TECHNOLOGIES',
              'BUSINESS EXPRESS, INC.',
              'ITECH DEVICES INC',
              'SILICON NETWORKS, LLC',
              'DILTEX INC',
              'NEW CENTURY TECHNOLOGIES INC.',
              'GMI COMPANIES INC.',
              'SOUTHEASTERN PAPER GROUP',
              'DD OFFICE PRODUCTS DBA LIBERTY PAPE',
              'INKDOG, LLC',
              'VIP OFFICE FURNITURE AND SUPPLY',
              'SOMA COMPUTER',
              'GEM LASER EXPRESS',
              'L & B GROUP, LLC',
              'LASER PLUS IMAGING',
              'AMERITECH SOLUTIONS',
              'AROCEP FEDERAL, LLC',
              'RIBBONS EXPRESS',
              'LAKOTA ENTERPRISES',
              'PC SPECIALISTS, INC.',
              '10GFEDSUPPLY, LLC',
              'ADVANTAGE WEST',
              'FEDGOV SUPPLY, LLP',
              'ICEBERG ENTEPRISES, LCC',
              'UNBEATABLE SALE. COM INC',
              'HEUTINK USA, INC',
              'ARGONAUT',
              'OSC SOLUTIONS, INC.',
              'SANDS BUSINESS EQUIPMENT & SUPPLIES',
              'OFFICE SUPPLY COMPANY,THE',
              'A&E SUPPLY',
              'OFFICE INK PROS, INC.']




# Initialize Filtering


# Convert 'date', 'day', 'month', and 'year' columns to datetime format
df1['Date'] = pd.to_datetime(df1['Date'])
df1['DAY'] = pd.to_datetime(df1['DAY'], format='%d').dt.day
df1['MONTH'] = pd.to_datetime(df1['MONTH'], format='%m').dt.month
df1['YEAR'] = pd.to_datetime(df1['YEAR'], format='%Y').dt.year

# Standardize the format of part numbers by removing hyphens and spaces
df1['MFPARTNUMBER'] = df1['MFPARTNUMBER'].str.replace(r'[-\s]', '')

# Copy values from 'PARTNUMBER' to 'MFPARTNUMBER' where 'MFPARTNUMBER' is NaN
df1.loc[df1['MFPARTNUMBER'].isna(), 'MFPARTNUMBER'] = df1.loc[df1['MFPARTNUMBER'].isna(), 'PARTNUMBER']

# Make a copy of the 'MFNAME' column
mf_name_copy = df1['MFNAME'].copy()

# Drop NaN columns from the DataFrame
df1 = df1.dropna(axis=1, how='any')

# Add the copied 'MFNAME' column back to the DataFrame
df1['MFNAME'] = mf_name_copy

# Convert all supplier names to uppercase
df1.loc[:, 'SUPPLIER'] = df1['SUPPLIER'].str.upper()

# Remove trailing punctuation marks (except commas) and whitespace using regex
df1.loc[:,'SUPPLIER'] = df1['SUPPLIER'].str.replace(r'[^\w\s,]+$', '', regex=True)

# Remove commas from supplier names
df1.loc[:,'SUPPLIER'] = df1['SUPPLIER'].str.replace(',', '')

# Map each supplier name to its first two words
df1['FIRST_TWO_WORDS'] = df1['SUPPLIER'].apply(get_first_two_words)

# Group by 'FIRST_TWO_WORDS' and select the supplier name with the fewest total words
df1['WORD_COUNT'] = df1['SUPPLIER'].str.split().apply(len)
preferred_supplier = df1.groupby('FIRST_TWO_WORDS')['SUPPLIER'].min()

# Update the 'SUPPLIER' column with the preferred supplier names
df1.loc[:,'SUPPLIER'] = df1['FIRST_TWO_WORDS'].map(preferred_supplier)

# Drop the 'FIRST_TWO_WORDS' and 'WORD_COUNT' columns
df1 = df1.drop(columns=['FIRST_TWO_WORDS', 'WORD_COUNT'])







# Create comp_df
comp_df = create_comp_df(df1)

print(comp_df.columns)



# Apply the function to each group of MFPARTNUMBER
result = comp_df.groupby('MFPARTNUMBER').apply(calculate_comp_price)




# Merge the result of groupby operation with comp_df based on MFPARTNUMBER
comp_df = pd.merge(result, comp_df, on='MFPARTNUMBER', how='left')



# Print the merged DataFrame
print(comp_df)




comp_df = comp_df.reset_index(drop=True)











# Step 1: Create a list of part numbers sold by competitors
part_numbers_by_competitors = df1[df1['SUPPLIER'].str.contains('|'.join(comp_list), case=False, na=False)]['MFPARTNUMBER'].unique()

# Step 2: Filter the original DataFrame based on the list of part numbers
filtered_df = df1[df1['MFPARTNUMBER'].isin(part_numbers_by_competitors)]

# Step 3: Create a filtered DataFrame containing only rows with part numbers sold by competitors
rest_of_data_df = df1[~df1['MFPARTNUMBER'].isin(part_numbers_by_competitors)]





# Step 1: Create a list of part numbers sold by "LASER RE" as a supplier
laser_re_part_numbers = df1[df1['SUPPLIER'].str.contains('LASER RE', case=False, na=False)]['MFPARTNUMBER'].unique()

# Step 2: Filter the DataFrame based on the list of part numbers excluding those sold by "LASER RE"
filtered_df = filtered_df[~filtered_df['MFPARTNUMBER'].isin(laser_re_part_numbers)]










# Reset Index of both Dataframes
df1 = filtered_df.reset_index(drop=True)
rest_of_data_df = rest_of_data_df.reset_index(drop=True)



# Copy the 'NAME' from the first row to every other row within each group
df1['COPY_NAME'] = df1.groupby('MFPARTNUMBER')['NAME'].transform('first')








# Save filtered_df to a CSV file
df1.to_csv('filtered_data.csv', index=False)

# Save rest_of_data_df to a CSV file
rest_of_data_df.to_csv('rest_of_data.csv', index=False)

# Save comp_df to a CSV file
comp_df.to_csv('comp_data.csv', index=False)

