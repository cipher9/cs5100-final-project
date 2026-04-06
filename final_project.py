import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Load file
df = pd.read_excel("Data/UWSM_cleaned.xlsx")

col = "Which bills or everyday expenses are the hardest for your household to afford?"

responses = df[col].dropna().astype(str)

items = []
for response in responses:
    parts = [p.strip() for p in response.split(";") if p.strip()]
    items.extend(parts)

grouped_counts = Counter()

for item in items:
    text = item.lower()

    if "housing costs" in text:
        grouped_counts["Housing"] += 1
    elif "groceries/food" in text:
        grouped_counts["Food / Groceries"] += 1
    elif "transportation" in text:
        grouped_counts["Transportation"] += 1
    elif "utilities" in text:
        grouped_counts["Utilities"] += 1
    elif "insurance premiums" in text:
        grouped_counts["Insurance"] += 1
    elif "medical bills" in text or "healthcare" in text:
        grouped_counts["Medical / Healthcare"] += 1
    elif "credit card or loan payments" in text:
        grouped_counts["Debt Payments"] += 1
    elif "phone or internet service" in text:
        grouped_counts["Phone / Internet"] += 1
    else:
        grouped_counts["Other"] += 1

grouped_df = pd.DataFrame(
    grouped_counts.items(),
    columns=["Category", "Total Mentions"]
).sort_values("Total Mentions", ascending=False)

print(grouped_df)

#"What supports would be most helpful for you?"
col = "What supports would be most helpful for you?"

# Clean + split responses
responses = df[col].dropna().astype(str)

items = []
for response in responses:
    parts = [p.strip() for p in response.split(";") if p.strip()]
    items.extend(parts)

# Group categories
grouped_counts = Counter()

for item in items:
    text = item.lower()

    if "food" in text or "grocer" in text:
        grouped_counts["Food Assistance"] += 1
    elif "housing" in text or "rent" in text:
        grouped_counts["Housing Support"] += 1
    elif "health" in text or "medical" in text:
        grouped_counts["Healthcare"] += 1
    elif "transport" in text:
        grouped_counts["Transportation"] += 1
    elif "job" in text or "employment" in text:
        grouped_counts["Job Support"] += 1
    elif "financial" in text or "money" in text:
        grouped_counts["Financial Assistance"] += 1
    elif "childcare" in text:
        grouped_counts["Childcare"] += 1
    elif "education" in text or "training" in text:
        grouped_counts["Education/Training"] += 1
    else:
        grouped_counts["Other"] += 1

# Convert to DataFrame
grouped_df = pd.DataFrame(
    grouped_counts.items(),
    columns=["Category", "Total Mentions"]
).sort_values("Total Mentions", ascending=False)

# 🎨 Colors
colors = [
    "#4CAF50", "#2196F3", "#FF9800", "#9C27B0",
    "#F44336", "#00BCD4", "#FFC107", "#795548"
]

# Optional: use top 6 for cleaner chart
top_df = grouped_df.head(6)

# Plot pie chart
plt.figure(figsize=(8,8))
plt.pie(
    top_df["Total Mentions"],
    labels=top_df["Category"],
    autopct="%1.1f%%",
    startangle=140,
    colors=colors[:len(top_df)]
)

plt.title("Most Helpful Supports Needed", fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()


# "What is your age group?"
'''
col = "What is your age group?"

# Clean text
df[col] = df[col].astype(str).str.strip()

# Remove blanks / invalid
valid_df = df[df[col].notna()]

# Count responses
counts = valid_df[col].value_counts()

# Optional: sort by logical age order (adjust if needed)
order = [
    "Under 18",
    "18 - 24",
    "25 - 44",
    "45 - 64",
    "65 - 75",
    "More than 75"
]

counts = counts.reindex(order).dropna()

# 🎨 Colors
colors = [
    "#4CAF50", "#2196F3", "#FF9800",
    "#9C27B0", "#F44336", "#00BCD4", "#FFC107"
]

# Plot pie chart
plt.figure(figsize=(8,8))
plt.pie(
    counts,
    labels=counts.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=colors[:len(counts)]
)

plt.title("Age Distribution of Respondents", fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()
'''

# Pie chart for community voice question
'''
col = "Are you part of a community whose voice you feel is not being heard?"

# Normalize text
df[col] = df[col].astype(str).str.lower().str.strip()

# Keep only valid responses
valid_df = df[df[col].notna()]

# Count responses
counts = valid_df[col].value_counts()

# Reorder explicitly (so it always shows Yes / No / Maybe nicely)
order = ["yes", "no", "maybe"]
counts = counts.reindex(order).dropna()

# 🎨 Colors
colors = ["#F44336", "#2196F3", "#FF9800"]  
# red = yes (not heard), blue = no, orange = maybe

# Plot pie chart
plt.figure(figsize=(8,8))
plt.pie(
    counts,
    labels=[label.capitalize() for label in counts.index],
    autopct="%1.1f%%",
    startangle=140,
    colors=colors
)

plt.title("Do People Feel Their Community Voice Is Not Being Heard?", 
          fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()
'''
# Pie chart for community voice question



#ALICE Analysis 
'''
col = "If an unexpected expense of $400 came up, would you be able to pay it?"

# Normalize text
df[col] = df[col].astype(str).str.lower().str.strip()

# Total valid responses (exclude blanks)
valid_df = df[df[col].notna()]

# ALICE group = "no" or "maybe"
alice_df = valid_df[
    valid_df[col].str.contains("no", na=False) |
    valid_df[col].str.contains("maybe", na=False)
]

# Calculate percentage
alice_percentage = (len(alice_df) / len(valid_df)) * 100

print(f"ALICE Percentage: {alice_percentage:.2f}%")
print(f"ALICE Count: {len(alice_df)}")
print(f"Total Valid Responses: {len(valid_df)}")

# Count responses
counts = valid_df[col].value_counts()

# 🎨 Define colors
colors = ["#4CAF50", "#F44336", "#FF9800"]  # green, red, orange

# Plot pie chart
plt.figure(figsize=(8,8))
plt.pie(
    counts,
    labels=counts.index.str.capitalize(),
    autopct="%1.1f%%",
    startangle=140,
    colors=colors[:len(counts)]
)

plt.title("Ability to Cover $400 Emergency Expense", fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()


# Plot bar chart
plt.figure()
plt.bar(grouped_df["Category"], grouped_df["Total Mentions"])

plt.xlabel("Category")
plt.ylabel("Total Mentions")
plt.title("Hardest Expenses to Afford")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 🎨 Colors
colors = [
    "#4CAF50", "#2196F3", "#FF9800", "#9C27B0",
    "#F44336", "#00BCD4", "#FFC107", "#795548", "#607D8B"
]

# Plot pie chart
plt.figure(figsize=(8,8))
plt.pie(
    grouped_df["Total Mentions"],
    labels=grouped_df["Category"],
    autopct="%1.1f%%",
    startangle=140
)

plt.title("Distribution of Hardest Expenses to Afford", fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()
'''