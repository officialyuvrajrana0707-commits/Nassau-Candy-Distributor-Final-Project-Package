import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Nassau Candy Route Efficiency",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Nassau_Candy_Final_Analysis.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(
        DATA_FILE,
        sheet_name="Cleaned Data",
        engine="openpyxl"
    )

df = load_data()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("Nassau Candy Distributor — Shipping Route Efficiency")
st.caption("Dashboard built from the supplied dataset and project specification.")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

with st.sidebar:
    st.header("Filters")

    regions = st.multiselect(
        "Region",
        sorted(df["Region"].dropna().unique()),
        default=sorted(df["Region"].dropna().unique())
    )

    states = st.multiselect(
        "State / Province",
        sorted(df["State/Province"].dropna().unique())
    )

    modes = st.multiselect(
        "Ship Mode",
        sorted(df["Ship Mode"].dropna().unique()),
        default=sorted(df["Ship Mode"].dropna().unique())
    )

    min_lead = int(df["Shipping Lead Time"].min())
    max_lead_data = int(df["Shipping Lead Time"].max())

    max_lead = st.slider(
        "Maximum lead-time filter (days)",
        min_value=min_lead,
        max_value=max_lead_data,
        value=max_lead_data
    )

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

f = df[
    df["Region"].isin(regions)
    & df["Ship Mode"].isin(modes)
    & (df["Shipping Lead Time"] <= max_lead)
].copy()

if states:
    f = f[f["State/Province"].isin(states)]

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Records",
    f"{len(f):,}"
)

c2.metric(
    "Unique Orders",
    f"{f['Order ID'].nunique():,}"
)

avg_lead = f["Shipping Lead Time"].mean()

c3.metric(
    "Avg Lead Time",
    f"{avg_lead:,.1f} days" if not pd.isna(avg_lead) else "N/A"
)

c4.metric(
    "Sales",
    f"${f['Sales'].sum():,.2f}"
)

# --------------------------------------------------
# DATA QUALITY WARNING
# --------------------------------------------------

st.warning(
    "Data-quality note: the supplied Order Dates are 2024–2025 "
    "while Ship Dates are 2026–2030, producing 904–1,642 day "
    "lead times. Validate source dates before operational use."
)

# --------------------------------------------------
# ROUTE ANALYSIS
# --------------------------------------------------

route = (
    f.groupby("Route")
    .agg(
        Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Median_Lead_Time=("Shipping Lead Time", "median"),
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
    .sort_values("Avg_Lead_Time")
)

left, right = st.columns(2)

with left:
    st.subheader("Fastest Routes")

    st.dataframe(
        route.head(10),
        use_container_width=True,
        hide_index=True
    )

with right:
    st.subheader("Slowest Routes")

    st.dataframe(
        route.tail(10)
        .sort_values("Avg_Lead_Time", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# SHIP MODE ANALYSIS
# --------------------------------------------------

st.subheader("Average Lead Time by Ship Mode")

mode = (
    f.groupby("Ship Mode")
    .agg(
        Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
    .sort_values("Avg_Lead_Time")
)

st.bar_chart(
    mode.set_index("Ship Mode")["Avg_Lead_Time"]
)

st.dataframe(
    mode,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# REGION ANALYSIS
# --------------------------------------------------

st.subheader("Average Lead Time by Region")

reg = (
    f.groupby("Region")
    .agg(
        Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
    .sort_values("Avg_Lead_Time")
)

st.dataframe(
    reg,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# STATE ANALYSIS
# --------------------------------------------------

st.subheader("State-level Performance")

state = (
    f.groupby(["State/Province", "Region"])
    .agg(
        Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Sales=("Sales", "sum")
    )
    .reset_index()
    .sort_values("Avg_Lead_Time", ascending=False)
)

st.dataframe(
    state,
    use_container_width=True,
    hide_index=True
)
