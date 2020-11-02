import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('https://raw.githubusercontent.com/parulnith/Website-articles-datasets/master/India%20GDP%20Growth%20Rate%20.csv', parse_dates=['Year'])
df['Year'] = df['Year'].apply(lambda x: pd.Timestamp(x).strftime('%Y'))
#calling xkcd() method 
plt.xkcd(scale=5, length=400)
df.plot(x='Year',y='GDP Growth (%)',kind='bar')
plt.ylabel('GDP Growth (%)')
plt.xticks(rotation=-20)
plt.figure(figsize=(10,8))
plt.show()