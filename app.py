import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(
    page_title="Tetra Pak Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LIGHT THEME CSS ---
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b; /* Dark text */
    }

    /* Main Background */
    .stApp {
        background: #f8fafc; /* Light gray background */
    }

    /* Headers */
    h1 {
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%); /* Indigo to Cyan */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        font-size: 3rem !important;
        text-align: center;
        padding-bottom: 0.5rem;
    }
    
    .header-subtitle {
        text-align: center;
        color: #64748b; /* Slate 500 */
        font-size: 1.1em;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Stats Cards */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #6366f1;
    }

    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-size: 0.85em !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0f172a !important; /* Dark Slate 900 */
        font-weight: 700 !important;
        font-size: 2em !important;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.8em;
        font-weight: 600;
        color: #1e293b;
        text-align: center;
        margin: 40px 0 20px 0;
        padding: 15px 0;
        border-top: 2px solid #e2e8f0;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Charts Container */
    .chart-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s;
    }
    
    .chart-box:hover {
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #6366f1;
    }
    
    /* Remove streamlit menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- LOADING DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('tetra_pak_final_data_finish.xlsx')
        df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
        df = df.dropna(subset=['Transaction Date'])
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
        df['Quantity unit'] = df['Quantity unit'].astype(str).str.strip().fillna('Unknown')
        df['category_group'] = df['category_group'].astype(str).fillna('Unknown')
        df['standardized_name'] = df['standardized_name'].astype(str).fillna('Unknown')
        df['Supplier'] = df['Supplier'].astype(str).fillna('Unknown')
        return df
    except Exception as e:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Error loading 'tetra_pak_final_data_finish.xlsx'. Please check if the file exists.")
    st.stop()

# --- HEADER ---
st.markdown("<h1>Tetra Pak Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='header-subtitle'>Real-time insights and performance metrics (Light Mode)</p>", unsafe_allow_html=True)


# --- SECTION 1 & GLOBAL STATS FILTER ---
# Logic: Controls Stats Cards + Section 1 Chart
st.markdown("<div class='section-header'>📈 Global Overview (Section 1)</div>", unsafe_allow_html=True)

col_f1, col_f2 = st.columns([1, 3])
with col_f1:
    # "Select All" toggle
    select_all_units = st.checkbox("Select All Units", value=True)

with col_f2:
    units_available = sorted(df['Quantity unit'].unique())
    if select_all_units:
        st.info("All units selected (Global Stats & Section 1)")
        selected_units_s1 = units_available
        current_units_label = "All Units"
    else:
        selected_units_s1 = st.multiselect(
            "Select specific units:",
            options=units_available,
            default=[],
            placeholder="Choose units..."
        )
        current_units_label = f"{len(selected_units_s1)} Selected" if selected_units_s1 else "None"

# Apply Filter for Section 1 / Stats
if not selected_units_s1:
    df_s1 = df.iloc[0:0] # Empty
    st.warning("Please select at least one unit to view stats.")
else:
    df_s1 = df[df['Quantity unit'].isin(selected_units_s1)]

# --- STATS CARDS ---
col1, col2, col3, col4 = st.columns(4)

total_amount = df_s1['Amount'].sum()
total_volume = df_s1['quantity'].sum()
total_tx = len(df_s1)
active_suppliers = df_s1['Supplier'].nunique()

with col1:
    st.metric("Total Amount", f"${total_amount:,.0f}")
with col2:
    st.metric("Total Volume", f"{total_volume:,.0f}")
with col3:
    st.metric("Transactions", f"{total_tx:,}")
with col4:
    st.metric("Active Suppliers", f"{active_suppliers}")


# --- OVERTIME ANALYSIS CHART (Section 1) ---
if not df_s1.empty:
    daily_data = df_s1.groupby('Transaction Date').agg({
        'Amount': 'sum',
        'quantity': 'sum'
    }).reset_index().sort_values('Transaction Date')

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Amount Line
    fig_trend.add_trace(
        go.Scatter(
            x=daily_data['Transaction Date'],
            y=daily_data['Amount'],
            name="Total Amount (USD)",
            line=dict(color='#4f46e5', width=3), # Indigo
            fill='tozeroy',
            fillcolor='rgba(79, 70, 229, 0.1)'
        ), secondary_y=False
    )
    
    # Volume Line
    fig_trend.add_trace(
        go.Scatter(
            x=daily_data['Transaction Date'],
            y=daily_data['quantity'],
            name=f"Quantity ({current_units_label})",
            line=dict(color='#06b6d4', width=3, dash='dot'), # Cyan
            fill='tozeroy',
            fillcolor='rgba(6, 182, 212, 0.1)'
        ), secondary_y=True
    )

    fig_trend.update_layout(
        title=dict(text=f"Financial vs Volume Analysis", font=dict(color="#1e293b", size=16)),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white', 
        font=dict(color='#1e293b'),
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig_trend.update_xaxes(showgrid=True, gridcolor='#e2e8f0')
    fig_trend.update_yaxes(title_text="Total Amount (USD)", title_font=dict(color="#4f46e5"), secondary_y=False, showgrid=True, gridcolor='#e2e8f0')
    fig_trend.update_yaxes(title_text="Quantity", title_font=dict(color="#06b6d4"), secondary_y=True, showgrid=False)

    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# --- SECTION 2: DETAILED ANALYTICS ---
st.markdown("<div class='section-header'>📊 Detailed Analytics (Section 2 - Independent)</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Select any unit below to inspect specific details. This selection is independent of the global filter.</p>", unsafe_allow_html=True)

# Independent Selector - showing ALL units
# "Scroll down to select" implemented via Streamlit Radio or Selectbox. 
# Radio is good for single choice, but can take space if many items. 
# User asked for "scroll down to select not give the list then they tick", implying SelectBox or Radio.
# Let's use a Radio since user mentioned "radio button single selection" in original request, but maybe a Selectbox is cleaner for "scroll"?
# "should be scroll down to select... it a scroll down to choose" -> Probably Selectbox is what they mean by "scroll down". 
# But existing code used Radio. Let's switch to SelectBox for cleaner UI if list is long.
# Actually, the user prompt said "shhould be scoll down to select not give the list then they tick...".
# I'll stick to `selectbox` for Section 2 to satisfy "scroll down".

selected_unit_s2 = st.selectbox(
    "Select Quantity Unit for Detail View:",
    options=units_available,
    index=0
)

df_s2 = df[df['Quantity unit'] == selected_unit_s2]

# --- Row 1 of Charts ---
col_charts_1, col_charts_2 = st.columns(2)

# 1. Top 4 Suppliers
with col_charts_1:
    supplier_data = df_s2.groupby('Supplier').agg({'Amount': 'sum', 'quantity': 'sum'}).reset_index()
    supplier_data = supplier_data.nlargest(4, 'Amount')
    
    fig_sup = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Amount Bar
    fig_sup.add_trace(go.Bar(
        x=supplier_data['Supplier'], y=supplier_data['Amount'], name='Amount',
        marker_color='rgba(79, 70, 229, 0.9)', # Indigo
        offsetgroup=1
    ), secondary_y=False)
    
    # Volume Bar
    fig_sup.add_trace(go.Bar(
        x=supplier_data['Supplier'], y=supplier_data['quantity'], name='Volume',
        marker_color='rgba(6, 182, 212, 0.9)', # Cyan
        offsetgroup=2
    ), secondary_y=True)
    
    fig_sup.update_layout(
        title=dict(text="Top 4 Suppliers", font=dict(color="#1e293b", size=16)),
        plot_bgcolor='white',
        paper_bgcolor='white', 
        font=dict(color='#1e293b'),
        height=450,
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_sup.update_xaxes(showgrid=False)
    fig_sup.update_yaxes(title_text="Amount", secondary_y=False, showgrid=True, gridcolor='#e2e8f0')
    fig_sup.update_yaxes(title_text="Volume", secondary_y=True, showgrid=False)
    
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    st.plotly_chart(fig_sup, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 2. Category Distribution (Pie)
with col_charts_2:
    
    # Initialize Session State
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = "All"

    st.markdown("#### Filter Products by Category")
    
    cat_data = df_s2.groupby('category_group').agg({'Amount': 'sum', 'quantity': 'sum'}).reset_index()
    cats_for_filter = ["All"] + sorted(cat_data['category_group'].unique().tolist())
    
    # --- Quick Filter Buttons (Reliable One-Click Filtering) ---
    st.write("**Filter Products by Category:**")
    manual_cat_select = st.radio(
        "Select Category:", 
        options=cats_for_filter, 
        key="selected_category", 
        horizontal=True, 
        label_visibility="collapsed"
    )

    pie_mode = st.radio("View Pie by:", ["Amount", "Volume"], horizontal=True, key="pie_mode")
    values = cat_data['Amount'] if pie_mode == 'Amount' else cat_data['quantity']
    
    # Standard Pie Chart (Visual Only)
    # Colors: Professional Palette
    pie_colors = ['#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    
    # 1. Sort Data Explicitly (Deterministic Order)
    cat_data['sort_val'] = values
    cat_data = cat_data.sort_values('sort_val', ascending=False).reset_index(drop=True)
    
    # Update values to look at the sorted column
    sorted_values = cat_data['sort_val']
    sorted_labels = cat_data['category_group']
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=sorted_labels,
        values=sorted_values,
        hole=0.4,
        marker=dict(colors=pie_colors),
        textinfo='percent',
        textposition='inside',
        insidetextorientation='horizontal',
        sort=False 
    )])
    
    fig_pie.update_layout(
        title=dict(text="Category Distribution", font=dict(color="#1e293b", size=16)),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1e293b'),
        height=400,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1),
        margin=dict(t=30, b=10, l=10, r=10),
    )
    
    # Simplified interaction - Visual Only
    st.plotly_chart(
        fig_pie, 
        use_container_width=True, 
        key="pie_visual_final",
        config={"displayModeBar": False} 
    )
    
    st.markdown("</div>", unsafe_allow_html=True)


# --- Row 2 of Charts ---
col_charts_3, col_charts_4 = st.columns(2)

# 3. Top 5 Products
with col_charts_3:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    
    # Use State (Source of Truth set by Radio)
    cat_filter_val = st.session_state["selected_category"]

    # UI for Filter Status
    if cat_filter_val != "All":
        st.markdown(f"**Filtered by Category:** <span style='color:#4f46e5; font-size:1.1em; font-weight:bold;'>{cat_filter_val}</span>", unsafe_allow_html=True)
    else:
        st.markdown("**Top 5 Products (All Categories)**")
    
    # Logic to filter DataFrame
    if cat_filter_val != 'All':
         prod_df = df_s2[df_s2['category_group'] == cat_filter_val]
    else:
         prod_df = df_s2
    
    prod_agg = prod_df.groupby('standardized_name').agg({'Amount': 'sum', 'quantity': 'sum'}).reset_index()
    prod_agg = prod_agg.nlargest(5, 'Amount')
    prod_agg = prod_agg.sort_values('Amount', ascending=True) 
    
    prod_agg['short_name'] = prod_agg['standardized_name'].apply(lambda x: x[:25] + '...' if len(x)>25 else x)

    
    # Dual Axis Horizontal Bar
    fig_prod = go.Figure()

    # Amount (Axis 1 - Bottom)
    fig_prod.add_trace(go.Bar(
        y=prod_agg['short_name'], 
        x=prod_agg['Amount'], 
        name='Amount (USD)', 
        orientation='h',
        marker_color='rgba(16, 185, 129, 0.9)', # Emerald
        offsetgroup=1
    ))
    
    # Volume (Axis 2 - Top)
    fig_prod.add_trace(go.Bar(
        y=prod_agg['short_name'], 
        x=prod_agg['quantity'], 
        name='Volume', 
        orientation='h',
        marker_color='rgba(245, 158, 11, 0.9)', # Amber
        offsetgroup=2,
        xaxis='x2'
    ))
    
    fig_prod.update_layout(
        title=dict(text=f"Top 5 Products", font=dict(color="#1e293b", size=16)),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1e293b'),
        height=450,
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        xaxis=dict(
            title="Amount (USD)",
            title_font=dict(color="#10b981"),
            tickfont=dict(color="#10b981"),
            showgrid=True,
            gridcolor='#e2e8f0',
        ),
        xaxis2=dict(
            title="Volume",
            title_font=dict(color="#f59e0b"),
            tickfont=dict(color="#f59e0b"),
            showgrid=False,
            overlaying='x',
            side='top'
        ),
        yaxis=dict(showgrid=False)
    )
    
    st.plotly_chart(fig_prod, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# 4. Top 4 Suppliers Trend (Continuous)
with col_charts_4:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    
    trend_mode = st.radio("View Trend by:", ["Amount", "Volume"], horizontal=True, key="trend_mode_s2")
    
    top_sups = df_s2.groupby('Supplier')['Amount'].sum().nlargest(4).index.tolist()
    
    full_date_range = pd.date_range(start=df_s2['Transaction Date'].min(), end=df_s2['Transaction Date'].max(), freq='D')
    
    fig_comp = go.Figure()
    # Light theme colors
    colors = ['#4f46e5', '#06b6d4', '#10b981', '#f59e0b']
    
    for i, sup in enumerate(top_sups):
        sup_df = df_s2[df_s2['Supplier'] == sup]
        sup_daily = sup_df.groupby('Transaction Date').agg({'Amount': 'sum', 'quantity': 'sum'}).reindex(full_date_range).fillna(0).reset_index()
        sup_daily.rename(columns={'index': 'Transaction Date'}, inplace=True)

        y_val = sup_daily['Amount'] if trend_mode == 'Amount' else sup_daily['quantity']
        
        fig_comp.add_trace(go.Scatter(
            x=sup_daily['Transaction Date'], y=y_val, name=sup,
            line=dict(color=colors[i%len(colors)], width=3)
        ))
        
    fig_comp.update_layout(
        title=dict(text="Top 4 Suppliers Trend (Continuous)", font=dict(color="#1e293b", size=16)),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1e293b'),
        height=450,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_comp.update_xaxes(showgrid=True, gridcolor='#e2e8f0')
    fig_comp.update_yaxes(showgrid=True, gridcolor='#e2e8f0')
    
    st.plotly_chart(fig_comp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
