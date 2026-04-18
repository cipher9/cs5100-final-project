# David Cho
# 4/9/2026
# Analyze challenges by race groups
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

df = pd.read_excel("Data/UWSM_cleaned.xlsx")

race_col = "How do you describe your race or ethnicity? (Can select more than one)"
voice_col = "Are you part of a community whose voice you feel is not being heard?"

# Data cleaning helpers
def clean(x):
    if pd.isna(x):
        return ""
    return str(x).lower().strip()

def remove_parentheses(text):
    return re.sub(r"\(.*?\)", "", text).strip()

def split_vals(x):
    return [p.strip() for p in str(x).split(";") if p.strip()]

df[race_col] = df[race_col].apply(clean)
df[voice_col] = df[voice_col].apply(clean)

# Split
df["Race_Array"] = df[race_col].apply(lambda x: [r.strip() for r in x.split(";") if r.strip()])

# one row per race
df_exploded = df.explode("Race_Array")

# Not enough information/data for analysis
final = ["other", "prefer not to answer", "native hawaiian or pacific islander"]

df_exploded = df_exploded[
    ~df_exploded["Race_Array"].isin(final)
]

# Remove blanks just in case
df_exploded = df_exploded[df_exploded["Race_Array"] != ""]

# Create unheard flag
df_exploded["Unheard"] = df_exploded[voice_col].str.contains("yes", na=False)

# Group
grouped = df_exploded.groupby("Race_Array").agg(
    total=("Unheard", "count"),
    unheard=("Unheard", "sum")
)

grouped["percent_unheard"] = (grouped["unheard"] / grouped["total"]) * 100

# Sort
result = grouped.sort_values("percent_unheard", ascending=False)

print(result)

# Plot
top = result.head(6)

plt.figure(figsize=(10,6))
plt.bar(top.index.str.title(), top["percent_unheard"])

plt.ylabel("% Feeling Unheard")
plt.title("Which Groups Feel Most Unheard?")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()

# Get data comparison for race vs challenges
race_col = "How do you describe your race or ethnicity? (Can select more than one)"
challenge_col = "What are the biggest challenges facing households in your community today?"

# Prepare data
df[race_col] = df[race_col].apply(clean)
df["Race_List"] = df[race_col].apply(split_vals)

# one row per race
df = df.explode("Race_List")

# Filter categories that didn't have enough data or were too vague
# Unfortunately there was only 1 response for Hawaiian/Pacific Islander, and "other" and "prefer not to answer" are too vague to analyze
df = df[
    ~df["Race_List"].str.contains("other|prefer not|hawaiian", na=False)
]
df = df[df["Race_List"] != ""]

# Count + normalize
race_totals = df["Race_List"].value_counts()

race_challenge_counts = {}

for race, group in df.groupby("Race_List"):
    items = []
    
    for val in group[challenge_col].dropna():
        parts = split_vals(val)
        parts = [remove_parentheses(p).title() for p in parts]
        items.extend(parts)
    
    counts = Counter(items)
    
    # normalize to %
    total_people = race_totals[race]
    normalized = {k: (v / total_people) * 100 for k, v in counts.items()}
    
    race_challenge_counts[race.title()] = normalized

# Get top challenges 
all_counts = Counter()
for c in race_challenge_counts.values():
    all_counts.update(c)

top_challenges = [k for k, _ in all_counts.most_common(6)]

# Build dataframe
races = list(race_challenge_counts.keys())

data = []
for race in races:
    row = [race_challenge_counts[race].get(c, 0) for c in top_challenges]
    data.append(row)

plot_df = pd.DataFrame(data, index=races, columns=top_challenges)

# Plot
ax = plot_df.plot(kind="bar", figsize=(12,6), legend=False)

plt.title("Top Community Challenges by Race (Normalized %)")
plt.ylabel("Percent of Group (%)")
plt.xlabel("Race/Ethnicity")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()

# Separate legend so that it doesn't hide the bar graph
fig_legend = plt.figure(figsize=(8,2))
ax_legend = fig_legend.add_subplot(111)

# Hide axes
ax_legend.axis("off")

# Create legend
handles, labels = ax.get_legend_handles_labels()

legend = ax_legend.legend(
    handles,
    labels,
    loc="center",
    ncol=3, 
    frameon=False
)

plt.show()