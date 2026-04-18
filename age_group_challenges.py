# David Cho
# 4/9/2026
# Analyze challenges by age group
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

df = pd.read_excel("Data/UWSM_cleaned.xlsx")

age_col = "What is your age group?"
challenge_col = "What are the biggest challenges facing households in your community today?"

# clean data from excel sheet
def clean(x):
    if pd.isna(x):
        return ""
    return str(x).strip()

def remove_parentheses(text):
    return re.sub(r"\(.*?\)", "", str(text)).strip()

def split_vals(x):
    if pd.isna(x):
        return []
    return [p.strip() for p in str(x).split(";") if p.strip()]

# Clean age column
df[age_col] = df[age_col].apply(clean)

# Keep only rows with age
df = df[df[age_col] != ""]

# Count + normalize
age_totals = df[age_col].value_counts()
age_challenge_counts = {}

for age, group in df.groupby(age_col):
    items = []

    for val in group[challenge_col].dropna():
        parts = split_vals(val)
        parts = [remove_parentheses(p).title() for p in parts]
        items.extend(parts)

    counts = Counter(items)
    total_people = age_totals[age]

    normalized = {k: (v / total_people) * 100 for k, v in counts.items()}
    age_challenge_counts[age] = normalized

# Build dataframe
plot_df = pd.DataFrame.from_dict(age_challenge_counts, orient="index").fillna(0)

# Order the age groups for plot
age_order = [
    "Under 18",
    "18 - 24",
    "25 - 44",
    "45 - 64",
    "65 - 75",
    "More than 75"
]

# Reorder rows using labels 
plot_df = plot_df.reindex([a for a in age_order if a in plot_df.index])

# Find top 6 challenges
top_challenges = plot_df.sum(axis=0).sort_values(ascending=False).head(6).index
plot_df = plot_df[top_challenges]

plot_df.plot(kind="bar", figsize=(12, 6))

plt.title("Top Community Challenges by Age Group (Normalized %)")
plt.ylabel("Percent of Group (%)")
plt.xlabel("Age Group")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# Count each age group
age_counts = df[age_col].value_counts()

print(age_counts)