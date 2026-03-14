import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Social Media Dashboard", layout="wide")

# ----------- BACKGROUND STYLE -----------

st.markdown("""
<style>
.stApp {
    background-color: #F4F6F8;
}
</style>
""", unsafe_allow_html=True)

# ----------- TITLE -----------

st.title("📊 Social Media Engagement Dashboard")
st.write("Analyze likes, comments, shares and engagement performance.")

# ----------- LOAD DATA -----------

df = pd.read_csv("social_media_engagement_5000.csv")

# ----------- SIDEBAR FILTERS -----------

st.sidebar.header("Filter Data")

country = st.sidebar.multiselect(
    "Select Country",
    df["country"].unique(),
    default=df["country"].unique()
)

post_type = st.sidebar.multiselect(
    "Select Post Type",
    df["post_type"].unique(),
    default=df["post_type"].unique()
)

filtered_df = df[
    (df["country"].isin(country)) &
    (df["post_type"].isin(post_type))
]

# ----------- KPI METRICS -----------

st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Posts", len(filtered_df))
col2.metric("Total Likes", int(filtered_df["likes"].sum()))
col3.metric("Total Comments", int(filtered_df["comments"].sum()))
col4.metric("Total Shares", int(filtered_df["shares"].sum()))

# ----------- CHARTS -----------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Posts by Type")
    fig1 = px.bar(
        filtered_df["post_type"].value_counts().reset_index(),
        x="post_type",
        y="count",
        color="post_type",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Posts by Country")
    fig2 = px.bar(
        filtered_df["country"].value_counts().reset_index(),
        x="country",
        y="count",
        color="country",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig2, use_container_width=True)

# ----------- ENGAGEMENT PIE -----------

st.subheader("Engagement Breakdown")

engagement_data = filtered_df[["likes","comments","shares"]].sum()

fig3 = px.pie(
    values=engagement_data.values,
    names=engagement_data.index,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig3)

# ----------- TREND CHART -----------

if "date" in filtered_df.columns:

    filtered_df["date"] = pd.to_datetime(filtered_df["date"])

    trend = filtered_df.groupby("date")[["likes","comments","shares"]].sum().reset_index()

    st.subheader("Engagement Trend Over Time")

    fig4 = px.line(
        trend,
        x="date",
        y=["likes","comments","shares"],
        markers=True
    )

    st.plotly_chart(fig4)

# ----------- TOP POSTS -----------

st.subheader("Top 10 Viral Posts")

top_posts = filtered_df.sort_values("likes", ascending=False).head(10)

st.dataframe(top_posts)

# ----------- DATASET PREVIEW -----------

st.subheader("Dataset Preview")

st.dataframe(filtered_df.head(20))
