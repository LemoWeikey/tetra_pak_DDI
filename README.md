# Tetra Pak Analytics Dashboard

Interactive analytics dashboard for Tetra Pak supply chain data with dual-section analysis.

## Features

### Section 1: Overtime Trend Analysis
- **Multi-select quantity units** with fancy dropdown
- **Dual-axis line chart** showing Amount (USD) and Volume over time
- Interactive date-based visualization

### Section 2: Detailed Analytics
- **Single unit selection** with radio buttons
- **Top 4 Suppliers Chart** - Dual y-axis showing Amount and Volume
- **Category Distribution Pie Chart** - Toggle between Amount/Volume view
- **Top 5 Products Chart** - Dual x-axis horizontal bars with interactive filtering
- **Top 4 Companies Trend** - Time series with Amount/Volume toggle

## Quick Start

### Streamlit App

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### HTML Dashboard

Simply open `dashboard.html` in your browser, or use a local server:

```bash
python3 -m http.server 8000
# Then visit http://localhost:8000/dashboard.html
```

## Data Preparation

The dashboard uses `tetra_pak_final_data_finish.xlsx`. To regenerate the JSON data:

```bash
python prepare_data.py
```

## File Structure

```
├── app.py                              # Streamlit application
├── dashboard.html                      # HTML/JS dashboard
├── prepare_data.py                     # Data processing script
├── tetra_pak_final_data_finish.xlsx   # Source data
├── tetra_pak_data.json                # Processed JSON data
├── requirements.txt                    # Python dependencies
└── README.md                          # This file
```

## Technologies

- **Streamlit** - Interactive Python web app
- **Plotly** - Interactive charts
- **Pandas** - Data processing
- **Chart.js** - HTML dashboard charts
- **HTML/CSS/JavaScript** - Web dashboard

## Interactive Features

- Multi-select dropdown for unit filtering (Section 1)
- Radio button single selection (Section 2)
- Click pie chart to filter products by category
- Toggle between Amount and Volume views
- Dual-axis charts for comprehensive analysis
- Responsive design for all screen sizes

---

Built with ❤️ for Tetra Pak analytics
