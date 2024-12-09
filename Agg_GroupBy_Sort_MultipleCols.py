# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:39:29 2024

@author: shiva
"""

import pandas as pd
import os

# Read Excel file
xl_file1 = "/Users/shiva/Shiva Arthi/Learning/Data Science/Python/FoodSales1-1.xlsx"
df1 = pd.read_excel(xl_file1)

op_file1 = "/Users/shiva/Shiva Arthi/Learning/Data Science/Python/op_file1.xlsx"
if os.path.exists(op_file1):
    os.remove(op_file1)

else:

# Group by multiple columns and sum a specific column
    grouped = df1.groupby(['Region','Category', 'Product']).agg({'TotalPrice': 'sum'}).reset_index()

# Sort by multiple columns descending
    sorted_df1 = grouped.sort_values(by=['Region','Category', 'Product'], ascending=False)


# Save to Excel
sorted_df1.to_excel('op_file1.xlsx', index=False)
op1 = 'op_file1.xlsx'

print(f"file 'op1' created successfully")


# =============================================================================
# Repeat the above steps for 2nd file
# =============================================================================

xl_file2 = "/Users/shiva/Shiva Arthi/Learning/Data Science/Python/FoodSales2-1.xlsx"
df2 = pd.read_excel(xl_file2)

op_file2 = "/Users/shiva/Shiva Arthi/Learning/Data Science/Python/op_file2.xlsx"
if os.path.exists(op_file2):
    os.remove(op_file2)

else:

# Group by multiple columns and sum a specific column
    grouped = df2.groupby(['Region','Category', 'Product']).agg({'TotalPrice': 'sum'}).reset_index()

# Sort by multiple columns descending
    sorted_df2 = grouped.sort_values(by=['Region','Category', 'Product'], ascending=False)


# Save to Excel
sorted_df2.to_excel('op_file2.xlsx', index=False)
op2 = 'op_file2.xlsx'

print(f"file 'op2' created successfully")