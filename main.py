# ================================
# STEP 1: Import Libraries & Setup
# ================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ================================
# STEP 2: Data Loading
# ================================
df = pd.read_csv("C:/Users/TUSHAR PAREEK/Downloads/Nassau Candy Distributor.csv")

# print(df.head())

# ================================
# STEP 3: Initial Data Exploration (EDA)
# ================================
# print(df.info())
# print(df.describe())
# print(df.isnull().sum())

# ================================
# STEP 4: Data Cleaning & Preprocessing
# ================================
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

# Create Shipping Lead Time
df['Shipping Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# Remove invalid rows
df = df[df['Shipping Lead Time'] >= 0]

# Drop missing values
df = df.dropna(subset=['Order Date', 'Ship Date'])

# print(df['Shipping Lead Time'].describe())

# ================================
# STEP 5: Feature Engineering
# ================================
product_factory_map = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

df['Factory'] = df['Product Name'].map(product_factory_map)

# Create Route
df['Route'] = df['Factory'] + " → " + df['State/Province']
# print(df['Route'])

# ================================
# STEP 6: Define Delay Threshold
# ================================
threshold = df['Shipping Lead Time'].quantile(0.75)
df['Delayed'] = df['Shipping Lead Time'] > threshold

# ================================
# STEP 7: Route-Level Aggregation
# ================================
route_summary = df.groupby('Route').agg({
    'Shipping Lead Time': ['mean', 'std', 'count']
}).reset_index()

route_summary.columns = ['Route', 'Avg Lead Time', 'Variability', 'Volume']

# Add Efficiency Score (NEW KPI)
route_summary['Efficiency Score'] = 1 / route_summary['Avg Lead Time']
# print(route_summary.head())

# ================================
# STEP 8: Route Efficiency Benchmarking
# ================================
top_routes = route_summary.nsmallest(10, 'Avg Lead Time')
worst_routes = route_summary.nlargest(10, 'Avg Lead Time')

# print('Top Routes:\n',top_routes)
# print()
# print('Worst Routes:\n',worst_routes)

# ================================
# STEP 9A: Delay Analysis
# ================================
delay_rate = df.groupby('Route')['Delayed'].mean().reset_index()
# print(delay_rate.head())

# ================================
# STEP 9B: Delay Analysis
# ================================

top_delayed = delay_rate.sort_values('Delayed', ascending=False).head(10)
# print(top_delayed.head())

# ================================
# STEP 10: Ship Mode Performance Analysis
# ================================
ship_mode_summary = df.groupby('Ship Mode')['Shipping Lead Time'].mean().reset_index()
# print(ship_mode_summary.head())

# ================================
# STEP 11: Geographic (State-Level) Analysis
# ================================
state_summary = df.groupby('State/Province').agg({
    'Shipping Lead Time': 'mean',
    'Order ID': 'count'
}).reset_index()

state_summary.columns = ['State', 'Avg Lead Time', 'Volume']
# print(state_summary.head(10))

# ================================
# STEP 12: Bottleneck Detection
# ================================
lead_time_threshold = state_summary['Avg Lead Time'].quantile(0.75)
volume_threshold = state_summary['Volume'].quantile(0.75)

bottlenecks = state_summary[
    (state_summary['Avg Lead Time'] > lead_time_threshold) &
    (state_summary['Volume'] > volume_threshold)
]
# print(bottlenecks.head())

# ================================
# STEP 13: Variability Analysis
# ================================
high_variability = route_summary.sort_values('Variability', ascending=False)
# print(high_variability.head())

# ================================
# STEP 14: Region-Level Analysis
# ================================
region_summary = df.groupby('Region')['Shipping Lead Time'].mean().reset_index()

#print(region_summary.head())

# ================================
# STEP 15: Factory-Level Analysis (NEW)
# ================================
factory_summary = df.groupby('Factory')['Shipping Lead Time'].mean().reset_index()

# print(factory_summary.head())

# ================================
# STEP 16: Cost-Time Tradeoff Analysis (NEW)
# ================================
cost_analysis = df.groupby('Ship Mode').agg({
    'Shipping Lead Time': 'mean',
    'Cost': 'mean'
}).reset_index()
# Format Cost column
cost_analysis['Cost'] = cost_analysis['Cost'].apply(lambda x: f"${x:.2f}")

# print(cost_analysis.head())

# ================================
# STEP 17: Combined Route Metrics
# ================================
final_summary = route_summary.merge(delay_rate, on='Route')

# Filter meaningful routes (Volume threshold)
merged = route_summary.merge(delay_rate, on='Route')
important_routes = merged[merged['Volume'] >= 5]

# print(final_summary.head())

# ================================
# STEP 18A: Visualization
# ================================

# Top Routes
plt.figure()
top_routes.sort_values('Avg Lead Time').plot(
    x='Route', y='Avg Lead Time', kind='barh', color='purple'
)
plt.title("Top 10 Fastest Routes")
# plt.show()

# Worst Routes
plt.figure()
worst_routes.sort_values('Avg Lead Time').plot(
    x='Route', y='Avg Lead Time', kind='barh', color='orange'
)
plt.title("Worst 10 Routes")
# plt.show()

# Ship Mode Comparison
plt.figure()
sns.barplot(data=ship_mode_summary, x='Ship Mode', y='Shipping Lead Time', color='blue')
plt.title("Lead Time by Ship Mode")
# plt.show()

# Bottleneck Scatter
plt.figure()
plt.scatter(state_summary['Volume'], state_summary['Avg Lead Time'], color='green')
plt.xlabel("Volume")
plt.ylabel("Avg Lead Time")
plt.title("Bottleneck Detection")
# plt.show()

# Region Analysis
plt.figure()
sns.barplot(data=region_summary, x='Region', y='Shipping Lead Time', color='red')
plt.title("Region-wise Lead Time")
# plt.show()

# ================================
# STEP 19: Key Outputs
# ================================
# print("Top Routes:\n", top_routes)
# print("\nWorst Routes:\n", worst_routes)
# print("\nTop Delayed Routes:\n", top_delayed)
# print("\nHigh Variability Routes:\n", high_variability)
# print("\nBottleneck States:\n", bottlenecks)
# print("\nFactory Performance:\n", factory_summary)
# print("\nCost-Time Tradeoff:\n", cost_analysis)
# print("\nImportant Routes:\n", important_routes.head(10))

