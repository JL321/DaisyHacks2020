import pandas as pd 
units_df = pd.read_csv("C:/Users/runze/OneDrive/Desktop/DaisyHacks2020/csv_labels/units_dictionary.csv")
print(set(units_df['units'].values.tolist()))