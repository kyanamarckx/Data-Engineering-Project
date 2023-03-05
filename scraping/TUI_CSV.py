import pandas as  pd

df = pd.read_json('jsonData/tuiScrapeJsonData.json')

df.to_csv('csvData/data.csv', index=None)