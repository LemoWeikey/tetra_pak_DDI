# Tetra Pak Analytics Dashboard

## Features

This interactive web dashboard provides comprehensive analytics for Tetra Pak data with the following visualizations:

1. **Quantity Unit Filter** - Checkboxes to filter data by different quantity units (Pieces, Kilograms, Square Meters, etc.)

2. **Top 4 Suppliers Chart** - Bar graph showing the top 4 suppliers by Amount (USD) and Volume (Quantity)

3. **Category Distribution Pie Chart** - Interactive pie chart showing the distribution of category groups by:
   - Amount (USD) - toggleable
   - Volume (Quantity) - toggleable
   - Click on any pie slice to filter the products chart

4. **Top 5 Products Chart** - Horizontal bar chart showing:
   - Top 5 products overall (by default)
   - Top 5 products in selected category (when pie chart is clicked)
   - Both Amount and Volume displayed side-by-side

5. **Top 4 Companies Trend Chart** - Line graph showing:
   - 4 companies (top by amount)
   - 2 lines per company (Amount in solid line, Volume in dashed line)
   - Timeline on x-axis (Transaction Date)

## How to Run

### Step 1: Ensure you have the data file ready
The data has already been exported to `tetra_pak_data.json`

### Step 2: Open the dashboard
Simply open `dashboard.html` in your web browser:

#### Option A - Double click
- Double-click on `dashboard.html` file

#### Option B - Use Python HTTP server (recommended for Chrome users)
```bash
cd "/Users/jamesgatsby/Desktop/tetra pak"
python3 -m http.server 8000
```
Then open your browser and go to: `http://localhost:8000/dashboard.html`

#### Option C - Use VS Code Live Server
- Right-click on `dashboard.html` in VS Code
- Select "Open with Live Server"

## How to Use

1. **Filter by Unit**: Check/uncheck the quantity units to filter the data across all charts

2. **View Top Suppliers**: See the top 4 suppliers by amount and volume in the first chart

3. **Analyze Categories**:
   - Click "Amount" or "Volume" buttons to toggle the pie chart view
   - Click on any pie slice to see the top 5 products in that category

4. **Track Trends**: View how the top 4 companies perform over time with both amount and volume metrics

## Interactive Features

- All charts update dynamically when you change the unit filters
- Pie chart slices are clickable to drill down into specific categories
- Toggle between Amount and Volume views for category distribution
- Hover over any chart element to see detailed values
- Responsive design works on desktop and mobile devices

## Technologies Used

- HTML5
- CSS3 (with modern flexbox and grid layouts)
- JavaScript (ES6+)
- Chart.js 4.4.0 (for all visualizations)

## Data Structure

The dashboard expects data with the following fields:
- `Transaction Date` - Date of transaction
- `Amount` - Total amount in USD
- `quantity` - Volume/quantity of items
- `Quantity unit` - Unit of measurement
- `Supplier` - Supplier name
- `category_group` - Category classification
- `standardized_name` - Product name

---

**Note**: All charts are fully interactive and responsive. The dashboard automatically handles data aggregation, sorting, and percentage calculations.
