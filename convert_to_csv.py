import pandas as pd

df = pd.read_excel("data/Train.xlsx")

df.to_csv(
    "data/Train.csv",
    index=False
)

print("CSV created successfully!")