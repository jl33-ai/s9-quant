
import pandas as pd
df = pd.read_csv('data.csv')
            
# Check if dataframe is empty or the column 'timetaken' is not present
if df.empty or 'timetaken' not in df.columns:
  pass

df = df.tail(200)

# Calculate the average
exp = str(round(df['timetaken'].mean(), 3))

# Calculate the variance of the data
std = str(round(df['timetaken'].std(ddof=0), 3))
