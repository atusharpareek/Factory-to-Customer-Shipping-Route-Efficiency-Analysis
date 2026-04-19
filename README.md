# Factory-to-Customer-Shipping-Route-Efficiency-Analysis

📦 Factory-to-Customer Shipping Route Efficiency Analysis
🚀 Project Overview

This project analyzes logistics data to evaluate the efficiency of factory-to-customer shipping routes. It focuses on identifying delivery delays, inefficient routes, and geographic bottlenecks using data analytics and visualization techniques.

An interactive dashboard built using Streamlit enables real-time exploration of shipping performance across routes, regions, and shipping methods.

🎯 Objectives
Analyze shipping lead time across routes
Identify efficient and inefficient delivery routes
Detect geographic bottlenecks
Compare shipping modes
Enable data-driven logistics optimization

📊 Dataset Description

The dataset contains over 10,000 shipping records from a candy distribution network.

Key Features:
Order Date & Ship Date → used to calculate lead time
Product Name → mapped to factories
State/Province & Region → geographic analysis
Ship Mode → delivery method comparison
Order ID → shipment tracking

⚙️ Methodology
1️⃣ Data Cleaning
Removed invalid records
Handled missing values
Converted date columns
2️⃣ Feature Engineering
Calculated Shipping Lead Time
Mapped products to factories
Created Route (Factory → State)
3️⃣ Data Aggregation
Route-level performance
State-level performance
Computed KPIs:
Average Lead Time
Variability
Volume
4️⃣ Delay Identification
Defined delay using 75th percentile threshold
5️⃣ Visualization & Dashboard
Built interactive dashboard using Streamlit

📈 Key Insights
Identified high-delay routes and inefficient delivery paths
Detected geographic bottlenecks in specific states
Found significant variation in shipping performance across routes
Observed performance differences between shipping modes
Highlighted inconsistencies in delivery times (high variability)

🖥️ Dashboard Features
📊 Modules
Route Efficiency Overview
Geographic Shipping Map
Ship Mode Comparison
Route Drill-Down
🎛️ Filters
Date range
Region / State
Ship mode
Lead time threshold

🧰 Tech Stack
Python (Pandas, NumPy)
Visualization: Plotly, Matplotlib, Seaborn
Dashboard: Streamlit

📂 Project Structure
project/
│
├── main.py          # Data analysis & preprocessing
├── app.py           # Streamlit dashboard
├── dataset.csv      # Input dataset
├── README.md        # Project documentation

▶️ How to Run the Project
1️⃣ Install dependencies
pip install pandas numpy matplotlib seaborn plotly streamlit
2️⃣ Run the dashboard
streamlit run app.py
3️⃣ Open in browser
http://localhost:8501

💼 Business Impact
Enables data-driven logistics decisions
Helps identify and fix delivery inefficiencies
Improves route optimization and performance monitoring

🔮 Future Scope
Real-time data integration
Machine learning for delay prediction
Route optimization algorithms
Cost analysis

👨‍💻 Author
Tushar Pareek
