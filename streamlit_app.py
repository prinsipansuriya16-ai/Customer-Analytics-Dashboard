import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path



st.set_page_config(page_title="Customer Analytics Dashboard", layout="wide")

st.title("📊 Customer Analytics Dashboard")
st.header("Customer Insights & Sales Performance Analysis")
st.write(" Customer Analytics Dashboard built using a self-generated dataset of 50000 customer records. An interactive dashboard tracking sales performance, monthly trends, and top product categories,city destribution.")

st.markdown("---")

try:
    BASE_DIR = Path(__file__).parent

    DATA = BASE_DIR/"data"/"sample_customer_data.csv"

    df_final_datail= pd.read_csv(DATA,parse_dates=['Date'])
    
    df_final_datail = df_final_datail.dropna()

    total_bill = df_final_datail["Total bill"].sum()
    # total order
    total_order = len(df_final_datail)
    
    # AOV - Average order value 
    aov = total_bill / total_order
   
    # monthly sales trend
    df_final_datail['Year'] = df_final_datail['Date'].dt.year
    df_final_datail['Month'] = df_final_datail['Date'].dt.month

    monthly_sales = df_final_datail.groupby(by=['Year' , 'Month'])['Total bill'].sum().reset_index()
    monthly_sales['Month'] = monthly_sales['Month'].astype(str)
    monthly_sales['Year'] = monthly_sales['Year'].astype(str)

    month_year=[]
    for x,y in zip(monthly_sales['Month'],monthly_sales['Year']):
        month_year.append(f"{x}-{y}")
    
    month_year = pd.DataFrame(month_year,columns=['month-year'])
    monthly_sales = pd.concat((month_year,monthly_sales),axis=1)


    # highest sales category & top revenue generating category
    category_sales = (df_final_datail.groupby("Category")["Quantity"].sum().sort_values(ascending=False))
    top_revenue = (df_final_datail.groupby('Category')['Total bill'].sum().sort_values(ascending=False))

    # city destribution
    city = pd.DataFrame(df_final_datail['City'].value_counts().reset_index())

except FileNotFoundError:
    st.error("❌ file not found.")
    st.stop()

# 3. SECTION 1: Key Performance Indicators (KPIs)
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Revenue", value=f"${total_bill}")
with col2:
    st.metric(label="Total Orders", value=f"{total_order}")
with col3:
    st.metric(label="Average Order Value (AOV)", value=f"${aov:.2f}")

st.markdown("----")

# ==========================================
# 2. SIDEBAR WIDGET
# ==========================================
st.sidebar.header("🛠️ Dashboard Settings")
indicator_choice = st.sidebar.selectbox(
    "what graph you want to show?",
    ["Monthly Revenue" , "Category Performance Analysis" , "Customer Distribution By City"]
)


# 1- monthly sales


if indicator_choice == "Monthly Revenue":
    st.subheader("📈Monthly Revenue")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_sales['month-year'],
        y=monthly_sales['Total bill'],
        mode='lines',
        name="Monthly sales",
        line=dict(color='green', width=2)
    ))
    fig.update_layout(
        title='MONTHLY SALES',
        xaxis_title='MONTH-YEAR',
        yaxis_title='$',
        template='plotly_white'
    )  
    st.plotly_chart(fig,  use_container_width=True)

elif indicator_choice == "Category Performance Analysis":

    colours = ["#4edc4e", "#9268ba", "#c3c353", "#62a1a8"]

    st.subheader("🏆 Category Performance Analysis")

    col_left, col_right = st.columns(2)

    with col_left:
        st.write("### Top Categories by Revenue")
        st.markdown(f"""
        > **Top Category:** `{top_revenue.idxmax()}`  
        > **Revenue:** `${top_revenue.max()}`
        """)
        
        fig_bar1 = go.Figure()
        fig_bar1.add_trace(go.Bar( x = top_revenue.index, y= top_revenue.values, marker_color=colours,text=[f"revenue:\n${val/1e9:.1f}B" for val in top_revenue],textposition='inside',insidetextanchor='middle'))
        fig_bar1.update_layout(
            xaxis_title="Category",
            yaxis_title="Revenue ($)",
            height=350
        )
        st.plotly_chart(fig_bar1, use_container_width=True)

    with col_right:
        st.write("### Top Categories by Orders (Volume)")
        st.markdown(f"""
        > **Top Category:** `{category_sales.idxmax()}`  
        > **Orders:** `${category_sales.max()}`
        """)

        fig_bar2 = go.Figure()
        fig_bar2.add_trace(go.Bar(x=category_sales.index, y=category_sales.values, marker_color=colours,text=[f"order:\n{val}" for val in category_sales],textposition='inside',insidetextanchor='middle'))
        fig_bar2.update_layout(
            xaxis_title="Category",
            yaxis_title="Number of Orders",
            height=350
        )
        st.plotly_chart(fig_bar2, use_container_width=True)

elif indicator_choice == "Customer Distribution By City":
    st.subheader("📈Customer Distribution By City")
    fig_city = go.Figure()
    fig_city.add_trace(go.Scatter(
        x = city['City'],
        y = city['count'],
        name='Customer per city',
        mode='lines',
        line=dict(color='red', width=2, dash='dashdot')
    ))
    fig_city.update_layout(
        title='Customer per city',
        xaxis_title='city',
        yaxis_title='Number of customer',
        hovermode='x unified',
        template='plotly_white'
    )  
    st.plotly_chart(fig_city,  use_container_width=True)
