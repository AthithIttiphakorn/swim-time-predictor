import requests
from bs4 import BeautifulSoup
import csv
import time

START_ATHLETE_ID = 4470524  # starting point
STYLE_ID = 13  # breaststroke
MIN_RESULTS = 7
MAX_ATHLETES = 100

BASE_URL = "https://www.swimrankings.net/index.php?page=athleteDetail"

def fetch_athlete_results(athlete_id):
    url = f"{BASE_URL}&athleteId={athlete_id}&styleId={STYLE_ID}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to get data for athlete {athlete_id} (status {response.status_code})")
            return None
    except Exception as e:
        print(f"Request error for athlete {athlete_id}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table")
    if not tables:
        print(f"No tables found for athlete {athlete_id}")
        return None

    # Heuristic: largest table in page is the results table
    result_table = max(tables, key=lambda t: len(t.find_all("tr")))

    times = []
    dates = []

    for row in result_table.find_all("tr")[1:]:  # skip header
        cols = row.find_all("td")
        if len(cols) < 3:
            continue  # skip invalid rows

        date_text = cols[0].get_text(strip=True)
        time_text = cols[2].get_text(strip=True)

        # Validate date: at least contains digits and plausible format
        if len(date_text) >= 8 and any(c.isdigit() for c in date_text):
            dates.append(date_text)
        else:
            dates.append("")

        # Validate time: must contain ':' or be a digit/dot combo (like 1:05.32)
        if ":" in time_text or time_text.replace(".", "").isdigit():
            times.append(time_text)
        else:
            times.append("")

        if len(times) >= MIN_RESULTS and len(dates) >= MIN_RESULTS:
            break

    if len(times) < MIN_RESULTS or len(dates) < MIN_RESULTS:
        print(f"Athlete {athlete_id} does not have enough results ({len(times)} found). Skipping.")
        return None

    return dates[:MIN_RESULTS], times[:MIN_RESULTS]

def main():
    dates_filename = "dates.csv"
    times_filename = "times.csv"

    with open(dates_filename, "w", newline="", encoding="utf-8") as dates_file, \
         open(times_filename, "w", newline="", encoding="utf-8") as times_file:

        dates_writer = csv.writer(dates_file)
        times_writer = csv.writer(times_file)

        # Write headers
        dates_writer.writerow([f"Date{i+1}" for i in range(MIN_RESULTS)])
        times_writer.writerow([f"Time{i+1}" for i in range(MIN_RESULTS)])

        successful_scrapes = 0
        current_id = START_ATHLETE_ID

        while successful_scrapes < MAX_ATHLETES:
            print(f"Scraping athlete ID: {current_id}")
            results = fetch_athlete_results(current_id)
            if results is not None:
                dates, times = results
                dates_writer.writerow(dates)
                times_writer.writerow(times)
                successful_scrapes += 1
                print(f"Success! Total scraped: {successful_scrapes}")
            else:
                print(f"Skipping athlete {current_id}")

            current_id += 1
            time.sleep(0.5)  # polite delay

if __name__ == "__main__":
    main()

#Right now, it is scraping successfully, but the data is not being added to the CSV files.
