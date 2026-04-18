# David Cho
# 4/9/2026
# Analyze by ALICE vs Non-ALICE and Cumberland vs York
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
# Load cleaned file
df = pd.read_excel("Data/UWSM_cleaned.xlsx")

# Column names
county_col = "Do you currently live or work in Southern Maine? (Can select more than one)"
alice_col = "If an unexpected expense of $400 came up, would you be able to pay it?"

supports_col = "What supports would be most helpful for you?"
expenses_col = "Which bills or everyday expenses are the hardest for your household to afford?"
challenges_col = "What are the biggest challenges facing households in your community today?"

# Clean data helper
def clean_text(x):
    if pd.isna(x):
        return ""
    return str(x).strip().lower()

# Create county group
def get_county_group(x):
    x = clean_text(x)
    if "cumberland" in x:
        return "Cumberland"
    elif "york" in x:
        return "York"
    else:
        return None
    
# Split response helper
def split_vals(x):
    return [p.strip() for p in str(x).split(";") if p.strip()]

# Create ALICE group
# ALICE = No or Maybe Non-ALICE = Yes
def get_alice_group(x):
    x = clean_text(x)
    if "no" in x or "maybe" in x:
        return "ALICE"
    elif "yes" in x:
        return "Non-ALICE"
    else:
        return None

df["County_Group"] = df[county_col].apply(get_county_group)
df["ALICE_Group"] = df[alice_col].apply(get_alice_group)

# Keep only valid groups
county_df = df[df["County_Group"].notna()].copy()
alice_df = df[df["ALICE_Group"].notna()].copy()

# Split responses in cells by ";" and count mentions helper
def split_multi_response(series):
    items = []
    for value in series.dropna():
        text = str(value).strip()
        if text:
            parts = [p.strip() for p in text.split(";") if p.strip()]
            items.extend(parts)
    return items

# Summarize top findings by group helper
def top_findings_by_group(data, group_col, response_col, top_n=10):
    rows = []

    for group_name, group_df in data.groupby(group_col):
        all_items = split_multi_response(group_df[response_col])
        counts = Counter(all_items)
        total_mentions = sum(counts.values())

        for item, count in counts.most_common(top_n):
            pct = (count / total_mentions * 100) if total_mentions > 0 else 0
            rows.append({
                "Group": group_name,
                "Response": item,
                "Count": count,
                "Percent_of_Group_Mentions": round(pct, 2)
            })

    return pd.DataFrame(rows)

# Run analysis
county_supports = top_findings_by_group(county_df, "County_Group", supports_col, top_n=10)
county_expenses = top_findings_by_group(county_df, "County_Group", expenses_col, top_n=10)
county_challenges = top_findings_by_group(county_df, "County_Group", challenges_col, top_n=10)

alice_supports = top_findings_by_group(alice_df, "ALICE_Group", supports_col, top_n=10)
alice_expenses = top_findings_by_group(alice_df, "ALICE_Group", expenses_col, top_n=10)
alice_challenges = top_findings_by_group(alice_df, "ALICE_Group", challenges_col, top_n=10)

# Print results
print("\nCumberland vs York: Supports")
print(county_supports)

print("\nCumberland vs York: Expenses")
print(county_expenses)

print("\nCumberland vs York: Challenges")
print(county_challenges)

print("\nALICE vs Non-ALICE: Supports")
print(alice_supports)

print("\nALICE vs Non-ALICE: Expenses")
print(alice_expenses)

print("\nALICE vs Non-ALICE: Challenges")
print(alice_challenges)

df["ALICE_Group"] = df[alice_col].apply(get_alice_group)
df = df[df["ALICE_Group"].notna()]

# Split and count
def get_counts(data):
    items = []
    for val in data.dropna():
        parts = [p.strip() for p in str(val).split(";") if p.strip()]
        items.extend(parts)
    return Counter(items)

alice_counts = get_counts(df[df["ALICE_Group"] == "ALICE"][supports_col])
non_alice_counts = get_counts(df[df["ALICE_Group"] == "Non-ALICE"][supports_col])

# Top categories
all_keys = list((alice_counts + non_alice_counts).keys())
top_keys = sorted(all_keys, key=lambda x: (alice_counts[x] + non_alice_counts[x]), reverse=True)[:6]

alice_vals = [alice_counts[k] for k in top_keys]
non_alice_vals = [non_alice_counts[k] for k in top_keys]

# Plot
x = range(len(top_keys))
width = 0.35

plt.figure(figsize=(10,6))
plt.bar(x, alice_vals, width, label="ALICE")
plt.bar([i + width for i in x], non_alice_vals, width, label="Non-ALICE")

plt.xticks([i + width/2 for i in x], top_keys, rotation=45, ha="right")

# Make labels smaller and more readable
labels = [
    "Food or Grocery",
    "Healthcare or Mental Health",
    "Rental Assistance",
    "Transportation",
    "Debt or Improving Credit",
    "Job Training or Education"
]

plt.xticks([i + width/2 for i in x], labels, rotation=45, ha="right")

plt.ylabel("Mentions")
plt.title("ALICE vs Non-ALICE: Support Needs")
plt.legend()

plt.tight_layout()
plt.show()


####### Cumberland vs York #######
# Build county dataset
cumberland_items = []
york_items = []

for _, row in df.iterrows():
    counties = split_vals(clean_text(row[county_col]))
    challenges = split_vals(row[challenges_col])

    for c in counties:
        if "cumberland" in c:
            cumberland_items.extend(challenges)
        elif "york" in c:
            york_items.extend(challenges)

# Count
cumberland_counts = Counter(cumberland_items)
york_counts = Counter(york_items)

# Get top shared challenges
all_keys = set(cumberland_counts) | set(york_counts)

top_keys = sorted(
    all_keys,
    key=lambda x: cumberland_counts[x] + york_counts[x],
    reverse=True
)[:6]

cumberland_vals = [cumberland_counts[k] for k in top_keys]
york_vals = [york_counts[k] for k in top_keys]

# Plot
x = range(len(top_keys))
width = 0.35

plt.figure(figsize=(10,6))
plt.bar(x, cumberland_vals, width, label="Cumberland", color="#2196F3")
plt.bar([i + width for i in x], york_vals, width, label="York", color="#FF9800")

# Make labels smaller and more readable
labels = [
    "Housing",
    "Basic Expenses",
    "Affordable Healthcare",
    "Mental Health",
    "Affordable and Available Childcare",
    "Jobs with Low Wages or No Benefits"
]

plt.xticks([i + width/2 for i in x], labels, rotation=45, ha="right")
plt.ylabel("Mentions")
plt.title("Cumberland vs York: Community Challenges")
plt.legend()

plt.tight_layout()
plt.show()