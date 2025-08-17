import http.client
from bs4 import BeautifulSoup
import time

athleteID = 4470524

def conv_timeToSeconds(time_str: str) -> str:
    """Convert time string to seconds."""
    try:
        mins, seconds = time_str.split(':')
        return str(int(mins) * 60 + float(seconds))
    except:
        return str(time_str)

for i in range(30):
    conn = http.client.HTTPSConnection("www.swimrankings.net")
    conn.request("GET", f"/index.php?page=athleteDetail&athleteId={athleteID}&styleId=13")
    response = conn.getresponse()
    
    print(f"Status code: {response.status}")
    print(f"Reason: {response.reason}")

    body1 = response.read().decode()
    soup = BeautifulSoup(body1, 'html.parser')
    #print(type(body1))

    timesList = []
    datesList = []
    try:
        # Get the first athleteRanking table (Long Course)
        two_columns = soup.find("table", class_="twoColumns")
        course_sections = two_columns.find_all("table", class_="athleteRanking")
        #print(course_sections)
        if course_sections:
            lc_section = course_sections[0]  # Long Course always comes first
            #print(lc_section)

            times = lc_section.find_all("a", class_="time")
            dates = lc_section.find_all("td", class_="date")

            for currentTime in times:
                timesList.append(conv_timeToSeconds(currentTime.get_text()))

            for day in dates:
                datesList.append(day.get_text())

        # Write results if we actually found LC data
        if timesList:
            with open('times.csv', 'a') as f:
                f.write(f"{athleteID}," + ','.join(timesList) + '\n')

        if datesList:
            with open('dates.csv', 'a') as f:
                f.write(f"{athleteID}," + ','.join(datesList) + '\n')

    except:
        time.sleep(1)

    athleteID += 1
    time.sleep(2.3)
