import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Manufacturing Demand Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_csv("sales_cleaned.csv")

    df['Inv.Date'] = pd.to_datetime(df['Inv.Date'])

    df['Year_Month'] = (
        df['Inv.Date']
        .dt.to_period('M')
        .astype(str)
    )

    return df


df = load_data()

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "Executive Overview",
        "Territory Intelligence",
        "Customer Intelligence",
        "Product Intelligence",
        "Forecasting",
        "Executive Insights"
    ]
)

# =====================================================
# EXECUTIVE OVERVIEW
# =====================================================

if page == "Executive Overview":

    st.title("Manufacturing Demand Intelligence Platform")

    st.markdown(
        "### Business Intelligence & Demand Forecasting Dashboard"
    )

    st.markdown("---")

    # =================================================
    # KPI CALCULATIONS
    # =================================================

    total_volume = round(
        df['Billed Qty (CBM)'].sum(),
        2
    )

    total_customers = df['Customer Name'].nunique()

    total_territories = df['Territory'].nunique()

    total_materials = df['Material'].nunique()

    # Top Territory

    territory_volume = (
        df.groupby('Territory')['Billed Qty (CBM)']
        .sum()
        .sort_values(ascending=False)
    )

    top_territory = territory_volume.index[0]

    top_territory_pct = round(
        (
            territory_volume.iloc[0]
            /
            territory_volume.sum()
        ) * 100,
        2
    )

    # Top 10 Customer Share

    customer_volume = (
        df.groupby('Customer Name')['Billed Qty (CBM)']
        .sum()
        .sort_values(ascending=False)
    )

    top10_share = round(
        (
            customer_volume.head(10).sum()
            /
            customer_volume.sum()
        ) * 100,
        2
    )

    # =================================================
    # KPI CARDS
    # =================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Volume (CBM)",
            f"{total_volume:,.0f}"
        )

    with col2:
        st.metric(
            "Customers",
            total_customers
        )

    with col3:
        st.metric(
            "Territories",
            total_territories
        )

    st.write("")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Materials",
            total_materials
        )

    with col5:
        st.metric(
            "Top Territory Share",
            f"{top_territory_pct}%"
        )

    with col6:
        st.metric(
            "Top 10 Customer Share",
            f"{top10_share}%"
        )

    st.markdown("---")

    # =================================================
    # MONTHLY DEMAND TREND
    # =================================================

    st.subheader("Monthly Demand Trend")

    monthly_volume = (
        df.groupby('Year_Month')['Billed Qty (CBM)']
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        monthly_volume,
        x='Year_Month',
        y='Billed Qty (CBM)',
        markers=True,
        title="Monthly Demand Trend"
    )

    fig1.update_layout(
        xaxis_title="Month",
        yaxis_title="Volume (CBM)"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # =================================================
    # DIVISION CONTRIBUTION
    # =================================================

    col7, col8 = st.columns(2)

    with col7:

        st.subheader("Division Contribution")

        division_volume = (
            df.groupby('Division Text')
            ['Billed Qty (CBM)']
            .sum()
            .reset_index()
        )

        fig2 = px.pie(
            division_volume,
            names='Division Text',
            values='Billed Qty (CBM)',
            hole=0.4
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    with col8:

        st.subheader("Top 10 Territories")

        top_territories = (
            df.groupby('Territory')['Billed Qty (CBM)']
            .sum()
            .reset_index()
            .sort_values(
                by='Billed Qty (CBM)',
                ascending=False
            )
            .head(10)
        )

        fig3 = px.bar(
            top_territories,
            x='Billed Qty (CBM)',
            y='Territory',
            orientation='h'
        )

        fig3.update_layout(
            yaxis={'categoryorder': 'total ascending'}
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

# =====================================================
# PLACEHOLDER PAGES
# =====================================================

elif page == "Territory Intelligence":

    st.title("Territory Intelligence")

    st.markdown(
        "### Territory-wise Demand Analysis"
    )

    # ==========================================
    # TERRITORY DATA
    # ==========================================

    territory_data = (
        df.groupby('Territory')['Billed Qty (CBM)']
        .sum()
        .reset_index()
        .sort_values(
            by='Billed Qty (CBM)',
            ascending=False
        )
    )

    territory_data['Contribution %'] = (
        territory_data['Billed Qty (CBM)']
        /
        territory_data['Billed Qty (CBM)'].sum()
    ) * 100

    # ==========================================
    # TOP TERRITORY KPIs
    # ==========================================

    top_territory = territory_data.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Top Territory",
            top_territory['Territory']
        )

    with col2:
        st.metric(
            "Volume (CBM)",
            f"{top_territory['Billed Qty (CBM)']:,.0f}"
        )

    with col3:
        st.metric(
            "Contribution %",
            f"{top_territory['Contribution %']:.2f}%"
        )

    st.markdown("---")

    # ==========================================
    # TOP 10 TERRITORIES
    # ==========================================

    st.subheader("Top 10 Territories")

    top10 = territory_data.head(10)

    fig = px.bar(
        top10,
        x='Billed Qty (CBM)',
        y='Territory',
        orientation='h',
        text='Billed Qty (CBM)'
    )

    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================================
    # TERRITORY CONTRIBUTION
    # ==========================================

    st.subheader("Territory Contribution")

    fig2 = px.pie(
        top10,
        names='Territory',
        values='Billed Qty (CBM)',
        hole=0.4
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ==========================================
    # TERRITORY TABLE
    # ==========================================

    st.subheader("Territory Ranking")

    st.dataframe(
        territory_data,
        use_container_width=True
    )

elif page == "Customer Intelligence":

    st.title("Customer Intelligence")

    st.markdown(
        "### Customer Demand & Concentration Analysis"
    )

    # ==========================================
    # CUSTOMER DATA
    # ==========================================

    customer_data = (
        df.groupby('Customer Name')['Billed Qty (CBM)']
        .sum()
        .reset_index()
        .sort_values(
            by='Billed Qty (CBM)',
            ascending=False
        )
    )

    customer_data['Contribution %'] = (
        customer_data['Billed Qty (CBM)']
        /
        customer_data['Billed Qty (CBM)'].sum()
    ) * 100

    # ==========================================
    # KPI CALCULATIONS
    # ==========================================

    top_customer = customer_data.iloc[0]

    top10_share = round(
        customer_data.head(10)['Contribution %'].sum(),
        2
    )

    top20_share = round(
        customer_data.head(20)['Contribution %'].sum(),
        2
    )

    # ==========================================
    # KPI CARDS
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Top Customer",
            top_customer['Customer Name']
        )

    with col2:
        st.metric(
            "Top 10 Share",
            f"{top10_share}%"
        )

    with col3:
        st.metric(
            "Top 20 Share",
            f"{top20_share}%"
        )

    st.markdown("---")

    # ==========================================
    # TOP CUSTOMERS
    # ==========================================

    st.subheader("Top 20 Customers")

    top20 = customer_data.head(20)

    fig = px.bar(
        top20,
        x='Billed Qty (CBM)',
        y='Customer Name',
        orientation='h'
    )

    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================================
    # CONTRIBUTION CHART
    # ==========================================

    st.subheader("Customer Contribution")

    fig2 = px.pie(
        top20,
        names='Customer Name',
        values='Billed Qty (CBM)',
        hole=0.4
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ==========================================
    # CUSTOMER TABLE
    # ==========================================

    st.subheader("Customer Ranking")

    st.dataframe(
        customer_data,
        use_container_width=True
    )

elif page == "Product Intelligence":

    st.title("Product Intelligence")

    st.markdown(
        "### Product, Material & Thickness Analysis"
    )

    # ==========================================
    # DIVISION ANALYSIS
    # ==========================================

    division_data = (
        df.groupby('Division Text')['Billed Qty (CBM)']
        .sum()
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Division Contribution")

        fig1 = px.pie(
            division_data,
            names='Division Text',
            values='Billed Qty (CBM)',
            hole=0.4
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        st.subheader("Division Summary")

        st.dataframe(
            division_data,
            use_container_width=True
        )

    st.markdown("---")

    # ==========================================
    # THICKNESS ANALYSIS
    # ==========================================

    st.subheader("Top Thickness Categories")

    thickness_data = (
        df.groupby('Thickness')['Billed Qty (CBM)']
        .sum()
        .reset_index()
        .sort_values(
            by='Billed Qty (CBM)',
            ascending=False
        )
        .head(10)
    )

    fig2 = px.bar(
        thickness_data,
        x='Thickness',
        y='Billed Qty (CBM)',
        text='Billed Qty (CBM)'
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # TOP MATERIALS
    # ==========================================

    st.subheader("Top 20 Materials")

    material_data = (
        df.groupby('Material Desc.')['Billed Qty (CBM)']
        .sum()
        .reset_index()
        .sort_values(
            by='Billed Qty (CBM)',
            ascending=False
        )
        .head(20)
    )

    fig3 = px.bar(
        material_data,
        x='Billed Qty (CBM)',
        y='Material Desc.',
        orientation='h'
    )

    fig3.update_layout(
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # MATERIAL TABLE
    # ==========================================

    st.subheader("Material Ranking")

    st.dataframe(
        material_data,
        use_container_width=True
    )

elif page == "Forecasting":

    st.title("Demand Forecasting")

    st.markdown(
        "### Forecasting Model Performance"
    )

    # ==========================================
    # KPI CARDS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Model",
            "Moving Average"
        )

    with col2:
        st.metric(
            "MAE",
            "120.02"
        )

    with col3:
        st.metric(
            "RMSE",
            "149.06"
        )

    with col4:
        st.metric(
            "Forecast Horizon",
            "72 Days"
        )

    st.markdown("---")

    # ==========================================
    # DAILY DEMAND TREND
    # ==========================================

    daily_demand = (
        df.groupby('Inv.Date')['Billed Qty (CBM)']
        .sum()
        .reset_index()
    )

    daily_demand.columns = ['Date', 'Demand']

    st.subheader("Historical Demand Trend")

    fig = px.line(
        daily_demand,
        x='Date',
        y='Demand',
        title='Daily Demand Volume'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # FORECASTING SUMMARY
    # ==========================================

    st.subheader("Forecasting Summary")

    st.success(
        """
        • Forecasting performed using Daily Demand Data (359 observations)

        • Moving Average model outperformed Exponential Smoothing

        • MAE = 120.02 CBM

        • RMSE = 149.06 CBM

        • Demand shows recovery after May 2021

        • Strong upward trend observed from August onwards
        """
    )

elif page == "Executive Insights":

    st.title("Executive Insights")

    st.markdown(
        "### Key Business Findings"
    )

    st.success(
        """
        📈 Demand recovered strongly after May 2021.

        📈 October recorded the highest monthly demand volume.

        📈 Top 4 territories contribute over 52% of total business volume.

        📈 Prelam - Ghaziabad contributes nearly 20% of total demand.

        📈 MDF Plain accounts for approximately 80% of total demand.

        📈 Top 5 thickness categories contribute nearly 50% of demand.

        📈 Customer base is well diversified with Top 20 customers contributing only 34.26%.
        """
    )

    st.markdown("---")

    st.subheader("Strategic Recommendations")

    st.info(
        """
        1. Strengthen inventory planning for 18mm and 16.75mm thickness categories.

        2. Closely monitor high-dependency territories such as Ghaziabad and Delhi.

        3. Expand sales efforts in lower-performing territories.

        4. Continue focus on MDF Plain products due to dominant demand.

        5. Use demand forecasting outputs for production planning and inventory optimization.
        """
    )

    st.markdown("---")

    st.subheader("Project Impact")

    st.write(
        """
        This platform enables:
        
        • Demand Monitoring
        
        • Territory Performance Analysis
        
        • Customer Intelligence
        
        • Product Intelligence
        
        • Manufacturing Demand Forecasting
        
        • Executive Decision Support
        """
    )