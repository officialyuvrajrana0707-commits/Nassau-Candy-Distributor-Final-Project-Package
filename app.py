import streamlit as st
import pandas as pd

st.set_page_config(page_title='Nassau Candy Route Efficiency', layout='wide')
@st.cache_data
def load_data():
    return pd.read_excel('Nassau_Candy_Final_Analysis.xlsx', sheet_name='Cleaned Data')

df=load_data()
st.title('Nassau Candy Distributor — Shipping Route Efficiency')
st.caption('Dashboard built from the supplied dataset and project specification.')

with st.sidebar:
    st.header('Filters')
    regions=st.multiselect('Region', sorted(df.Region.dropna().unique()), default=sorted(df.Region.dropna().unique()))
    states=st.multiselect('State / Province', sorted(df['State/Province'].dropna().unique()))
    modes=st.multiselect('Ship Mode', sorted(df['Ship Mode'].dropna().unique()), default=sorted(df['Ship Mode'].dropna().unique()))
    max_lead=st.slider('Maximum lead-time filter (days)', int(df['Shipping Lead Time'].min()), int(df['Shipping Lead Time'].max()), int(df['Shipping Lead Time'].max()))

f=df[df.Region.isin(regions)&df['Ship Mode'].isin(modes)&(df['Shipping Lead Time']<=max_lead)].copy()
if states: f=f[f['State/Province'].isin(states)]

c1,c2,c3,c4=st.columns(4)
c1.metric('Records',f'{len(f):,}')
c2.metric('Unique Orders',f"{f['Order ID'].nunique():,}")
c3.metric('Avg Lead Time',f"{f['Shipping Lead Time'].mean():,.1f} days")
c4.metric('Sales',f"${f['Sales'].sum():,.2f}")

st.warning('Data-quality note: the supplied Order Dates are 2024–2025 while Ship Dates are 2026–2030, producing 904–1,642 day lead times. Validate source dates before operational use.')

route=f.groupby('Route').agg(Shipments=('Order ID','count'),Avg_Lead_Time=('Shipping Lead Time','mean'),Median_Lead_Time=('Shipping Lead Time','median'),Sales=('Sales','sum'),Gross_Profit=('Gross Profit','sum')).reset_index().sort_values('Avg_Lead_Time')
left,right=st.columns(2)
with left:
    st.subheader('Fastest Routes')
    st.dataframe(route.head(10), use_container_width=True, hide_index=True)
with right:
    st.subheader('Slowest Routes')
    st.dataframe(route.tail(10).sort_values('Avg_Lead_Time',ascending=False), use_container_width=True, hide_index=True)

st.subheader('Average Lead Time by Ship Mode')
mode=f.groupby('Ship Mode').agg(Shipments=('Order ID','count'),Avg_Lead_Time=('Shipping Lead Time','mean')).reset_index().sort_values('Avg_Lead_Time')
st.bar_chart(mode.set_index('Ship Mode')['Avg_Lead_Time'])

st.subheader('Average Lead Time by Region')
reg=f.groupby('Region').agg(Shipments=('Order ID','count'),Avg_Lead_Time=('Shipping Lead Time','mean')).reset_index().sort_values('Avg_Lead_Time')
st.dataframe(reg, use_container_width=True, hide_index=True)

st.subheader('State-level Performance')
state=f.groupby(['State/Province','Region']).agg(Shipments=('Order ID','count'),Avg_Lead_Time=('Shipping Lead Time','mean'),Sales=('Sales','sum')).reset_index().sort_values('Avg_Lead_Time',ascending=False)
st.dataframe(state, use_container_width=True, hide_index=True)
