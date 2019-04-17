import pandas as pd
import requests
import time
import sys
from bs4 import BeautifulSoup


outfile = sys.argv[1]
if not outfile:
    raise ValueError("No outfile specified.")


URL = "https://www.timeanddate.com/weather/usa/chicago/historic?month={}&year={}"


data = []
for year in range(2010, 2019):
    for month in range(1, 13):
        url = URL.format(month, year)
        response = requests.get(url)
        # const avgTemp = document.querySelectorAll(".sep-t")[0].children[1].textContent;
        soup = BeautifulSoup(response.text, "html.parser")
        temp_str = soup.select(".sep-t")[0].find_all("td")[0].getText()
        avg_temp = int(temp_str.split()[0])
        record = {"month": month, "year": year, "temperature": avg_temp}
        data.append(record)
        time.sleep(1)
df = pd.DataFrame(data)
df.to_csv(outfile, index=False)
print("Saved {} records of historical weather data.".format(len(df)))
