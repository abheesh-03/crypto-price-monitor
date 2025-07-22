import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px

# Snowflake connection
conn = snowflake.connector.connect(
    user="Abheesh",
    password="Abheeshdp28m416,
    account="GHDSQFZ-FS70206",
    warehouse="COMPUTE_WH",
    database="SNOWFLAKE_LEARNING_DB",
    schema="ABHEESH_LOAD_DATA_FROM_AMAZON_AWS"
)

# Function to load data
def load_data():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM crypto_prices ORDER BY TIMESTAMP DESC')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'TIMESTAMP', 'COIN', 'PRICE'])
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
    return df

st.title("📈 Crypto Prices Dashboard")

# Refresh button
if st.button('🔄 Refresh Data'):
    st.rerun()

df = load_data()

st.subheader('Raw Data')
st.dataframe(df)

# Filter by coin
st.subheader('Filter by Coin')
coins = df['COIN'].unique().tolist()
selected_coins = st.multiselect('Select Coins', coins, default=coins)

df_filtered = df[df['COIN'].isin(selected_coins)]

st.subheader('Filtered Data')
st.dataframe(df_filtered)

# Plot
st.subheader('Price Trend by Coin')
fig = px.line(df_filtered, x='TIMESTAMP', y='PRICE', color='COIN', markers=True)
st.plotly_chart(fig)

conn.close()
