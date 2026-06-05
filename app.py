import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import fetch_query, engine

st.set_page_config(
    page_title="Traffic Crash Analytics",
    layout="wide"
)

@st.cache_data
def get_summary():
    total = pd.read_sql(
        "SELECT COUNT(*) AS n FROM crashtable",
        engine
    ).iloc[0,0]

    injuries = pd.read_sql(
        "SELECT SUM(INJURIES_TOTAL) AS n FROM crashtable",
        engine
    ).iloc[0,0]

    fatal = pd.read_sql(
        "SELECT SUM(INJURIES_FATAL) AS n FROM crashtable",
        engine
    ).iloc[0,0]

    years = pd.read_sql(
        "SELECT COUNT(DISTINCT YEAR) AS n FROM crashtable",
        engine
    ).iloc[0,0]

    return total, injuries, fatal, years
with st.sidebar:
    st.title("Traffic Crash Analytics")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Crash Analysis",
            "Weather & Lighting",
            "Traffic Safety",
            "Trend Analysis",
            "Geo Analysis",
            "Query Explorer"
        ]
    )

    theme = st.radio(
        "Theme",
        ["Dark", "Light"]
    )

    if theme == " Dark":
        st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

total, injuries, fatal, years = get_summary()

if page == "Overview":
    st.title("Traffic Crash Analytics Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Crashes", f"{total:,}")
    c2.metric("Total Injuries", f"{int(injuries):,}")
    c3.metric("Fatal Injuries", f"{int(fatal):,}")
    c4.metric("Years Covered", years)

    st.subheader("Crash Growth Trend")

    df = fetch_query(14)

    fig = px.line(
        df,
        x="YEAR",
        y="YOY_GROWTH_PCT",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "Crash Analysis":
    st.header("Crash Analysis")

    df = fetch_query(3)

    fig = px.bar(
        df.head(10),
        x="FIRST_CRASH_TYPE",
        y="INJURY_PCT"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df)
elif page == "Weather & Lighting":

    st.header("Weather Analysis")

    df = fetch_query(1)

    fig = px.bar(
        df,
        x="FIRST_CRASH_TYPE",
        y="TOTAL_CRASHES",
        color="WEATHER_CONDITION"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("Lighting Analysis")

    df2 = fetch_query(6)

    fig2 = px.bar(
        df2,
        x="LIGHTING_CONDITION",
        y="AVG_INJURIES",
        color="LIGHTING_CONDITION"
    )

    st.plotly_chart(fig2, use_container_width=True)

elif page == "Traffic Safety":

    st.header("Dangerous Streets")

    df = fetch_query(2)

    fig = px.bar(
        df.head(10),
        x="STREET_NAME",
        y="INJURY_CRASHES"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("Traffic Control Device")

    df2 = fetch_query(7)

    fig2 = px.bar(
        df2.head(10),
        x="TRAFFIC_CONTROL_DEVICE",
        y="AVG_INJURIES_PER_CRASH"
    )

    st.plotly_chart(fig2, use_container_width=True)

elif page == "Trend Analysis":

    st.header("Peak Crash Hour")

    df = fetch_query(4)

    fig = px.line(
        df,
        x="CRASH_MONTH",
        y="CRASH_COUNT",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("High Risk Time Slots")

    df2 = fetch_query(12)

    fig2 = px.bar(
        df2,
        x="TIME_SLOT",
        y="INJURY_CRASHES"
    )

    st.plotly_chart(fig2, use_container_width=True)

elif page == "Geo Analysis":

    st.header("Crash Locations")

    df = fetch_query(8)

    fig = px.scatter(
        df,
        x="LON",
        y="LAT",
        size="CRASH_FREQUENCY"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("Hotspot Zones")

    df2 = fetch_query(15)

    fig2 = px.scatter(
        df2,
        x="ZONE_LON",
        y="ZONE_LAT",
        size="CRASH_COUNT"
    )

    st.plotly_chart(fig2, use_container_width=True)

elif page == "Query Explorer":

    st.header("Query Explorer")

    query_no = st.selectbox(
        "Select Query",
        list(range(1,16))
    )

    df = fetch_query(query_no)

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        f"query_{query_no}.csv",
        "text/csv"
    )

