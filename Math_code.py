import pandas as pd
import math

# Create a pandas DataFrame to hold the values
data = pd.DataFrame({
    'a': [3],  # First number
    'b': [4],  # Second number
    'c': [5]   # Number to add
})

# Calculate the mathematical expression (3 * 4) + 5
data['result'] = data.apply(lambda row: math.prod([row['a'], row['b']]) + row['c'], axis=1)

# Print the DataFrame with the result
print(data)

