import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Parameters
num_swimmers = 200          # number of individual swimmers
records_per_swimmer = random.randint(20, 35)
genders = ["M", "F"]
competitions = [
    "Nationals", "World Cup", "SEA Games", "Olympic Trials",
    "Local Meet", "Youth Nationals", "Regional Qualifiers"
]

data = []

for swimmer_id in range(1000, 1000 + num_swimmers):
    gender = random.choice(genders)
    age = random.randint(14, 30)

    # Base PB (world-level around 57-59s for men, 64-66s for women)
    if gender == "M":
        personal_best = np.random.normal(59.0, 1.2)  # avg around 59s
    else:
        personal_best = np.random.normal(66.0, 1.5)  # avg around 66s

    # Simulate improvement over years
    start_date = datetime(2010, 1, 1) + timedelta(days=random.randint(0, 1000))
    prev_date = start_date

    for i in range(records_per_swimmer):
        date = prev_date + timedelta(days=random.randint(30, 120))
        days_since_last_comp = (date - prev_date).days

        # Training intensity between 0.6–1.0
        avg_intensity = round(random.uniform(0.6, 1.0), 2)

        # Time performance model:
        # Lower intensity or long gap = slower time
        # Swimmers slightly improve over long periods
        years_since_start = (date - start_date).days / 365.0
        improvement_factor = 1.0 - (years_since_start * random.uniform(0.001, 0.004))
        fatigue_factor = 1.0 + (days_since_last_comp / 8000) + (1.0 - avg_intensity) * 0.05

        recorded_time = personal_best * improvement_factor * fatigue_factor + np.random.normal(0, 0.25)

        competition_name = random.choice(competitions)

        data.append([
            swimmer_id, gender, age, "Breaststroke", 100, date.strftime("%Y-%m-%d"),
            round(personal_best, 2), round(recorded_time, 2),
            avg_intensity, days_since_last_comp, competition_name
        ])

        prev_date = date

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "swimmer_id", "gender", "age", "stroke", "distance", "date",
    "personal_best", "recorded_time", "avg_intensity",
    "days_since_last_comp", "competition_name"
])

# Sort by date for realism
df = df.sort_values(by=["swimmer_id", "date"]).reset_index(drop=True)

# Save CSV
df.to_csv("breaststroke_100m_augmented.csv", index=False)
print("✅ Saved 'breaststroke_100m_augmented.csv' with", len(df), "records.")
