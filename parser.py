from bs4 import BeautifulSoup
from scrape import html

html_doc, _, athleteID = html()



soup = BeautifulSoup(html_doc, 'html.parser')
times = soup.find_all("a", class_="time")
dates = soup.find_all("td", class_="date")

#print(type(times))  -- Its a class
datesList = []
for day in dates:
    datesList.append(day.get_text())
    print(day.get_text(), end=" | ")

print()
timesList = []
for time in times:
    timesList.append(time.get_text())
    print(time.get_text(), end=" | ")

with open('times.csv', 'a') as f:
    f.write(f"{athleteID}," + ','.join(timesList) + '\n')


with open('dates.csv', 'a') as f:
    f.write(f"{athleteID}," + ','.join(datesList) + '\n')
