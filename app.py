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
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    }
    h1 {
        background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        text-align: center;
        font-weight: 700;
    }
    .section-header {
        color: white;
        font-size: 1.8em;
        font-weight: 600;
        text-align: center;
        padding: 20px 0;
        border-top: 2px solid rgba(139, 92, 246, 0.3);
        border-bottom: 2px solid rgba(139, 92, 246, 0.3);
        margin: 40px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
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

try:
    df = load_data()

    # Header
    st.markdown("<h1>Tetra Pak Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1em;'>Real-time insights and performance metrics</p>", unsafe_allow_html=True)

    # Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Amount", f"${df['Amount'].sum():,.0f}")
    with col2:
        st.metric("📦 Total Volume", f"{df['quantity'].sum():,.0f}")
    with col3:
        st.metric("📊 Transactions", f"{len(df):,}")
    with col4:
        st.metric("🏢 Active Suppliers", f"{df['Supplier'].nunique()}")

    # SECTION 1: Overtime Trend Analysis
    st.markdown("<div class='section-header'>📈 Section 1: Overtime Trend Analysis</div>", unsafe_allow_html=True)

    st.markdown("#### 🔍 Select Quantity Units (Multiple Selection)")
    units_available = sorted(df['Quantity unit'].unique())
    selected_units_s1 = st.multiselect(
        "Choose units for overtime analysis:",
        options=units_available,
        default=units_available,
        key="section1_units"
    )

    if selected_units_s1:
        # Filter data for section 1
        df_s1 = df[df['Quantity unit'].isin(selected_units_s1)]

        # Aggregate by date
        daily_data = df_s1.groupby('Transaction Date').agg({
            'Amount': 'sum',
            'quantity': 'sum'
        }).reset_index().sort_values('Transaction Date')

        # Create overtime trend chart
        fig_overtime = make_subplots(specs=[[{"secondary_y": True}]])

        fig_overtime.add_trace(
            go.Scatter(
                x=daily_data['Transaction Date'],
                y=daily_data['Amount'],
                name="Total Amount (USD)",
                mode='lines',
                line=dict(color='#1f77b4', width=3),
                fill='tozeroy',
                fillcolor='rgba(31, 119, 180, 0.1)'
            ),
            secondary_y=False
        )

        units_text = f"{len(selected_units_s1)} units" if len(selected_units_s1) > 1 else selected_units_s1[0]

        fig_overtime.add_trace(
            go.Scatter(
                x=daily_data['Transaction Date'],
                y=daily_data['quantity'],
                name=f"Quantity ({units_text})",
                mode='lines',
                line=dict(color='#ff7f0e', width=3, dash='dot'),
                fill='tozeroy',
                fillcolor='rgba(255, 127, 14, 0.1)'
            ),
            secondary_y=True
        )

        fig_overtime.update_layout(
            title=f"Financial vs Volume Analysis Over Time - {units_text}",
            hovermode='x unified',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig_overtime.update_xaxes(title_text="Transaction Date", gridcolor='rgba(148, 163, 184, 0.1)')
        fig_overtime.update_yaxes(title_text="<b>Total Amount (USD)</b>", title_font=dict(color="#1f77b4", size=14), secondary_y=False, gridcolor='rgba(148, 163, 184, 0.1)')
        fig_overtime.update_yaxes(title_text=f"<b>Quantity ({units_text})</b>", title_font=dict(color="#ff7f0e", size=14), secondary_y=True)

        st.plotly_chart(fig_overtime, use_container_width=True)
    else:
        st.warning("Please select at least one quantity unit.")

    # SECTION 2: Detailed Analytics
    st.markdown("<div class='section-header'>📊 Section 2: Detailed Analytics by Quantity Unit</div>", unsafe_allow_html=True)

    st.markdown("#### 🔍 Select Quantity Unit (Choose One Only)")
    selected_unit_s2 = st.radio(
        "Choose one unit for detailed analysis:",
        options=units_available,
        horizontal=True,
        key="section2_unit"
    )

    # Filter data for section 2
    df_s2 = df[df['Quantity unit'] == selected_unit_s2]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 4 Suppliers")

        # Aggregate by supplier
        supplier_data = df_s2.groupby('Supplier').agg({
            'Amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        supplier_data = supplier_data.nlargest(4, 'Amount')

        # Create bar chart with dual y-axes (exactly like HTML)
        fig_suppliers = make_subplots(specs=[[{"secondary_y": True}]])

        fig_suppliers.add_trace(
            go.Bar(
                x=supplier_data['Supplier'],
                y=supplier_data['Amount'],
                name='Amount (USD)',
                marker_color='rgba(139, 92, 246, 0.8)',
                marker_line_color='rgba(139, 92, 246, 1)',
                marker_line_width=2,
                yaxis='y'
            ),
            secondary_y=False
        )

        fig_suppliers.add_trace(
            go.Bar(
                x=supplier_data['Supplier'],
                y=supplier_data['quantity'],
                name='Volume',
                marker_color='rgba(59, 130, 246, 0.8)',
                marker_line_color='rgba(59, 130, 246, 1)',
                marker_line_width=2,
                yaxis='y2'
            ),
            secondary_y=True
        )

        fig_suppliers.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig_suppliers.update_xaxes(gridcolor='rgba(148, 163, 184, 0.1)')
        fig_suppliers.update_yaxes(
            title_text="<b>Amount (USD)</b>",
            title_font=dict(color="#8b5cf6", size=14),
            secondary_y=False,
            gridcolor='rgba(148, 163, 184, 0.1)'
        )
        fig_suppliers.update_yaxes(
            title_text="<b>Volume (Quantity)</b>",
            title_font=dict(color="#3b82f6", size=14),
            secondary_y=True
        )

        st.plotly_chart(fig_suppliers, use_container_width=True)

    with col2:
        st.markdown("#### Category Distribution")

        # Toggle for pie chart
        pie_mode = st.radio("View by:", ["Amount", "Volume"], horizontal=True, key="pie_toggle")

        # Aggregate by category
        category_data = df_s2.groupby('category_group').agg({
            'Amount': 'sum',
            'quantity': 'sum'
        }).reset_index()

        values = category_data['Amount'] if pie_mode == "Amount" else category_data['quantity']
        total = values.sum()
        percentages = (values / total * 100).round(1)

        # Create labels with percentages like HTML
        labels_with_pct = [f"{cat} ({pct}%)" for cat, pct in zip(category_data['category_group'], percentages)]

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels_with_pct,
            values=values,
            marker=dict(
                colors=['#8b5cf6', '#3b82f6', '#06b6d4', '#10b981', '#f59e0b',
                       '#ef4444', '#ec4899', '#6366f1', '#14b8a6', '#f97316'],
                line=dict(color='#1e293b', width=3)
            ),
            textposition='auto'
        )])

        fig_pie.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Top 5 Products")

        # Category filter (since Streamlit can't click pie chart)
        st.info("💡 Click a category below to filter products (replaces pie chart click)")

        categories = ['All'] + sorted(df_s2['category_group'].unique().tolist())
        selected_category = st.selectbox(
            "Filter by category:",
            options=categories,
            key="category_filter"
        )

        # Filter products
        if selected_category and selected_category != 'All':
            df_products = df_s2[df_s2['category_group'] == selected_category]
            st.markdown(f"**Showing: Top 5 in {selected_category}**")
        else:
            df_products = df_s2
            st.markdown("**Showing: Top 5 Products (All Categories)**")

        # Aggregate by product
        product_data = df_products.groupby('standardized_name').agg({
            'Amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        product_data = product_data.nlargest(5, 'Amount')
        product_data['name_short'] = product_data['standardized_name'].apply(
            lambda x: x[:30] + '...' if len(x) > 30 else x
        )

        # FIXED: Create horizontal bar chart with BOTH bars per product (like HTML)
        fig_products = go.Figure()

        # Add Amount bars
        fig_products.add_trace(
            go.Bar(
                y=product_data['name_short'],
                x=product_data['Amount'],
                name='Amount (USD)',
                orientation='h',
                marker_color='rgba(16, 185, 129, 0.8)',
                marker_line_color='rgba(16, 185, 129, 1)',
                marker_line_width=2,
                offsetgroup=0
            )
        )

        # Add Volume bars
        fig_products.add_trace(
            go.Bar(
                y=product_data['name_short'],
                x=product_data['quantity'],
                name='Volume',
                orientation='h',
                marker_color='rgba(245, 158, 11, 0.8)',
                marker_line_color='rgba(245, 158, 11, 1)',
                marker_line_width=2,
                offsetgroup=1,
                xaxis='x2'
            )
        )

        fig_products.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            barmode='group',  # FIXED: group mode shows 2 bars per product
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(
                title="<b>Amount (USD)</b>",
                titlefont=dict(color="#10b981", size=14),
                gridcolor='rgba(148, 163, 184, 0.1)',
                side='bottom'
            ),
            xaxis2=dict(
                title="<b>Volume (Quantity)</b>",
                titlefont=dict(color="#f59e0b", size=14),
                overlaying='x',
                side='top'
            ),
            yaxis=dict(gridcolor='rgba(0,0,0,0)')
        )

        st.plotly_chart(fig_products, use_container_width=True)

    with col4:
        st.markdown("#### Top 4 Companies Trend Over Time")

        # Toggle for trend chart (exactly like HTML)
        trend_mode = st.radio("View trend by:", ["Amount", "Volume"], horizontal=True, key="trend_toggle")

        # Get top 4 suppliers by Amount
        supplier_totals = df_s2.groupby('Supplier')['Amount'].sum().nlargest(4)
        top4_suppliers = supplier_totals.index.tolist()

        # Filter and aggregate by date and supplier
        df_trend = df_s2[df_s2['Supplier'].isin(top4_suppliers)]
        trend_data = df_trend.groupby(['Transaction Date', 'Supplier']).agg({
            'Amount': 'sum',
            'quantity': 'sum'
        }).reset_index().sort_values('Transaction Date')

        fig_trend = go.Figure()

        colors = ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b']

        # Only show 4 lines (one per company) based on toggle
        for idx, supplier in enumerate(top4_suppliers):
            supplier_trend = trend_data[trend_data['Supplier'] == supplier]
            y_values = supplier_trend['Amount'] if trend_mode == "Amount" else supplier_trend['quantity']

            fig_trend.add_trace(
                go.Scatter(
                    x=supplier_trend['Transaction Date'],
                    y=y_values,
                    name=supplier,
                    mode='lines',
                    line=dict(color=colors[idx], width=3)
                )
            )

        y_title = "<b>Amount (USD)</b>" if trend_mode == "Amount" else "<b>Volume (Quantity)</b>"

        fig_trend.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(
                title=y_title,
                title_font=dict(color="#8b5cf6", size=14),
                gridcolor='rgba(148, 163, 184, 0.1)'
            ),
            xaxis=dict(
                title="<b>Transaction Date</b>",
                gridcolor='rgba(148, 163, 184, 0.1)'
            )
        )

        st.plotly_chart(fig_trend, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ Data file not found. Please ensure 'tetra_pak_final_data_finish.xlsx' is in the same directory as this app.")
except Exception as e:
    st.error(f"⚠️ Error loading data: {str(e)}")
    st.exception(e)
