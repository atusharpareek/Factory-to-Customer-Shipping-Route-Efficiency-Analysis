# ================================
# STEP 1: Import Libraries
# ================================
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📦 Shipping Route Efficiency Dashboard")

# ================================
# STEP 2: Load & Prepare Data
# ================================
@st.cache_data
def load_data():

    df = pd.read_csv("C:/Users/TUSHAR PAREEK/Downloads/Nassau Candy Distributor.csv")

    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

    df['Shipping Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

    df = df[df['Shipping Lead Time'] >= 0]
    df = df.dropna(subset=['Order Date', 'Ship Date'])

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
    df['Route'] = df['Factory'] + " → " + df['State/Province']

    return df


df = load_data()

# ================================
# FILTERS
# ================================
st.sidebar.header("Filters")

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [df['Order Date'].min(), df['Order Date'].max()],
    key="date"
)

region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(df['Region'].dropna().unique()),
    key="region"
)

state = st.sidebar.selectbox(
    "Select State",
    ["All"] + list(df['State/Province'].dropna().unique()),
    key="state"
)

ship_mode = st.sidebar.selectbox(
    "Select Ship Mode",
    ["All"] + list(df['Ship Mode'].dropna().unique()),
    key="ship"
)

lead_time = st.sidebar.slider(
    "Lead Time Threshold",
    int(df['Shipping Lead Time'].min()),
    int(df['Shipping Lead Time'].max()),
    int(df['Shipping Lead Time'].max()),
    key="lead"
)

# # Clear button
# if st.sidebar.button("🔄 Clear All Filters"):
#     st.session_state.date = [df['Order Date'].min(), df['Order Date'].max()]
#     st.session_state.region = "All"
#     st.session_state.state = "All"
#     st.session_state.ship = "All"
#     st.session_state.lead = int(df['Shipping Lead Time'].max())
#     st.rerun()

# ================================
# APPLY FILTERS
# ================================
filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df['Order Date'] >= pd.to_datetime(start_date)) &
    (filtered_df['Order Date'] <= pd.to_datetime(end_date))
]

if region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == region]

if state != "All":
    filtered_df = filtered_df[filtered_df['State/Province'] == state]

if ship_mode != "All":
    filtered_df = filtered_df[filtered_df['Ship Mode'] == ship_mode]

filtered_df = filtered_df[filtered_df['Shipping Lead Time'] <= lead_time]

# ================================
# KPIs
# ================================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Avg Lead Time", round(filtered_df['Shipping Lead Time'].mean(), 2))
col2.metric("Total Orders", filtered_df['Order ID'].nunique())

delay_rate = (filtered_df['Shipping Lead Time'] > filtered_df['Shipping Lead Time'].quantile(0.75)).mean()
col3.metric("Delay Rate", round(delay_rate, 2))

# ================================
# MODULE 1
# ================================
st.subheader("🚚 Route Efficiency Overview")

route_summary = filtered_df.groupby('Route')['Shipping Lead Time'].mean().reset_index()

st.bar_chart(route_summary.set_index('Route'), color= 'Orange')
st.dataframe(route_summary.sort_values('Shipping Lead Time'))

# Worst routes
st.subheader("⚠️ Worst Performing Routes")
st.dataframe(route_summary.nlargest(5, 'Shipping Lead Time'))

# ================================
# MODULE 2
# ================================
st.subheader("🌍 Geographic Shipping Map")

state_summary = filtered_df.groupby('State/Province').agg({
    'Shipping Lead Time': 'mean',
    'Order ID': 'count'
}).reset_index()

state_summary.columns = ['State', 'Avg Lead Time', 'Volume']

state_abbrev = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR',
    'California':'CA','Colorado':'CO','Connecticut':'CT',
    'Delaware':'DE','Florida':'FL','Georgia':'GA',
    'Hawaii':'HI','Idaho':'ID','Illinois':'IL',
    'Indiana':'IN','Iowa':'IA','Kansas':'KS',
    'Kentucky':'KY','Louisiana':'LA','Maine':'ME',
    'Maryland':'MD','Massachusetts':'MA','Michigan':'MI',
    'Minnesota':'MN','Mississippi':'MS','Missouri':'MO',
    'Montana':'MT','Nebraska':'NE','Nevada':'NV',
    'New Hampshire':'NH','New Jersey':'NJ',
    'New Mexico':'NM','New York':'NY',
    'North Carolina':'NC','North Dakota':'ND',
    'Ohio':'OH','Oklahoma':'OK','Oregon':'OR',
    'Pennsylvania':'PA','Rhode Island':'RI',
    'South Carolina':'SC','South Dakota':'SD',
    'Tennessee':'TN','Texas':'TX','Utah':'UT',
    'Vermont':'VT','Virginia':'VA',
    'Washington':'WA','West Virginia':'WV',
    'Wisconsin':'WI','Wyoming':'WY'
}

state_summary['State Code'] = state_summary['State'].map(state_abbrev)

fig = px.choropleth(
    state_summary,
    locations='State Code',
    locationmode="USA-states",
    color='Avg Lead Time',
    scope="usa",
    title='🗺️ US Heatmap of Shipping Efficiency'
)
st.plotly_chart(fig)

fig2 = px.scatter(
    state_summary,
    x='Volume',
    y='Avg Lead Time',
    hover_name='State',
    title= '📍 Regional Bottleneck Visualization'
)
st.plotly_chart(fig2)

# Bottlenecks
st.subheader("🚨 Critical Bottlenecks")
st.dataframe(state_summary.sort_values('Avg Lead Time', ascending=False).head(5))

# ================================
# MODULE 3
# ================================
st.subheader("🚚 Ship Mode Comparison")

ship_mode_summary = filtered_df.groupby('Ship Mode')['Shipping Lead Time'].mean().reset_index()

fig = px.bar(ship_mode_summary, x='Ship Mode', y='Shipping Lead Time', color='Ship Mode')
st.plotly_chart(fig)

# ================================
# MODULE 4
# ================================
st.subheader("🔍 Route Drill-Down")

selected_state = st.selectbox("Select State", df['State/Province'].dropna().unique())

filtered_state_df = filtered_df[filtered_df['State/Province'] == selected_state]

st.write("State-Level Performance")
st.dataframe(filtered_state_df.groupby('Route')['Shipping Lead Time'].mean().reset_index())

st.write("Order-Level Shipment Timelines")
st.dataframe(filtered_state_df[['Order ID', 'Order Date', 'Ship Date', 'Shipping Lead Time']])

# ================================
# EXTRA
# ================================
st.subheader("🔎 Search Route")

search = st.text_input("Enter Route")

if search:
    st.dataframe(filtered_df[filtered_df['Route'].str.contains(search, case=False)])

st.subheader("⬇️ Download Data")

st.download_button("Download CSV", filtered_df.to_csv(index=False), "data.csv")