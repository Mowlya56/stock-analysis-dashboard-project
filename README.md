📈 Stock Analysis Dashboard

An interactive Streamlit web app for analyzing stock trends, computing key indicators (SMA, EMA, RSI), and visualizing performance using real-time data from Yahoo Finance.

🚀 Features

📊 Fetch Live Stock Data using Yahoo Finance (yfinance)

🧮 Compute Indicators: SMA (Simple Moving Average), EMA (Exponential Moving Average), RSI (Relative Strength Index)

🌐 Interactive Charts built with Plotly (zoom, pan, hover)

📅 Custom Date Range selection for historical data

📥 Download CSV option for further analysis

⚙️ User-friendly Streamlit Interface

🛠️ Tools & Technologies
Category	Tools
Language	Python 3.x
Web Framework	Streamlit
Data Source	Yahoo Finance API (yfinance)
Visualization	Plotly
Data Handling	pandas, numpy

📂 Project Structure

📁 stock-analysis-dashboard
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── Stock_Analysis_Dashboard_Report.pdf   # 2-page internship report

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/yourusername/stock-analysis-dashboard.git
cd stock-analysis-dashboard

2️⃣ Create a virtual environment (recommended)

On Windows:
python -m venv venv
.\venv\Scripts\activate

On macOS / Linux:
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Streamlit app
streamlit run app.py


Your browser will open automatically to:

👉 http://localhost:8501

🧮 How It Works

Enter a stock ticker (e.g., AAPL, GOOG, MSFT) in the sidebar.

Select a date range and indicator windows (SMA, EMA, RSI).

Click Fetch & Analyze.

The dashboard displays:

Interactive price chart (Close + SMA + EMA)

RSI chart with overbought/oversold zones

Latest data table and indicator summary

Optionally, download the CSV of historical data.
