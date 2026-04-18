# David Cho
# 4/9/2026
import pandas as pd
from collections import Counter
import re

df = pd.read_excel("Data/UWSM_cleaned.xlsx")

county_col = "Do you currently live or work in Southern Maine? (Can select more than one)"
challenge_col = "What are the biggest challenges facing households in your community today?"

# Helpers
def clean(x):
    if pd.isna(x):
        return ""
    return str(x).lower().strip()

def split_vals(x):
    return [p.strip() for p in str(x).split(";") if p.strip()]

def remove_parentheses(text):
    return re.sub(r"\(.*?\)", "", text).strip()

# -----------------------------
# Expand dataset by county
# -----------------------------
rows = []

for _, row in df.iterrows():
    counties = split_vals(clean(row[county_col]))
    challenges = split_vals(row[challenge_col])

    for c in counties:
        if "cumberland" in c:
            rows.append(("Cumberland", challenges))
        elif "york" in c:
            rows.append(("York", challenges))

expanded_df = pd.DataFrame(rows, columns=["County", "Challenges"])

# -----------------------------
# Total respondents per county
# -----------------------------
# NOTE: counts people, not mentions
total_respondents = expanded_df.groupby("County").size()

print("Total Respondents Per County:")
print(total_respondents)

# -----------------------------
# % of respondents mentioning each challenge
# -----------------------------
results = []

for county, group in expanded_df.groupby("County"):
    total_people = len(group)

    counter = Counter()

    for challenges in group["Challenges"]:
        cleaned = [remove_parentheses(c).title() for c in challenges]
        unique_challenges = set(cleaned)  # avoid double counting per person
        
        for c in unique_challenges:
            counter[c] += 1

    for challenge, count in counter.items():
        percent = (count / total_people) * 100
        results.append({
            "County": county,
            "Challenge": challenge,
            "Respondents": count,
            "Percent (%)": round(percent, 1)
        })

result_df = pd.DataFrame(results)

# Sort nicely
result_df = result_df.sort_values(["County", "Percent (%)"], ascending=[True, False])

print("\nChallenge Percentages by County:")
print(result_df)