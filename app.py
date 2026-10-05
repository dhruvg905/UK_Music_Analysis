import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing import load_and_standardize
from metrics import get_artist_diversity_metrics, get_collaboration_metrics, get_content_and_release_metrics

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="UK Top 50 Market Analysis", layout="wide", page_icon="🇬🇧")
st.title("🇬🇧 UK Top 50 Playlist Market Structure & Artist Diversity")
st.markdown("Interactive dashboard for Atlantic Recording Corporation UK Market Strategies.")

# --- 2. DATA LOADING ---
# Caching the data load so the app doesn't slow down on every filter change
@st.cache_data
def load_data():
    df, df_artists = load_and_standardize()
    return df, df_artists

df_main, df_artists = load_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Market Filters")

# Date Filter
min_date = df_main['date'].min()
max_date = df_main['date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Album Type Filter
album_types = st.sidebar.multiselect("Album Type", options=df_main['album_type'].unique(), default=df_main['album_type'].unique())

# Collaboration Filter
collab_filter = st.sidebar.radio("Track Type", options=["All", "Solo Tracks Only", "Collaborations Only"])

# --- 4. APPLY FILTERS ---
mask_main = (df_main['date'].dt.date >= date_range[0]) & (df_main['date'].dt.date <= date_range[1])
mask_main &= df_main['album_type'].isin(album_types)

if collab_filter == "Solo Tracks Only":
    mask_main &= (df_main['collaborator_count'] == 1)
elif collab_filter == "Collaborations Only":
    mask_main &= (df_main['collaborator_count'] > 1)

df_filtered = df_main[mask_main]

# Need to re-explode the filtered data for accurate artist metrics
df_filtered_artists = df_filtered.explode('artist_list').rename(columns={'artist_list': 'individual_artist'})

# --- 5. CALCULATE KPIs ---
st.markdown("### Market Structure Metrics")
if not df_filtered.empty:
    artist_kpis = get_artist_diversity_metrics(df_filtered_artists)
    collab_kpis = get_collaboration_metrics(df_filtered)
    content_kpis = get_content_and_release_metrics(df_filtered)

    # Layout for KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Diversity Score", artist_kpis['diversity_score'])
    col2.metric("Concentration Ratio (Top 5)", artist_kpis['concentration_ratio'])
    col3.metric("Collaboration Ratio", collab_kpis['collab_ratio'])
    col4.metric("Explicit Share", content_kpis['explicit_share'])
    
    st.divider()

    # --- 6. VISUALIZATIONS ---
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("#### Artist Dominance Leaderboard")
        top_artists = df_filtered_artists['individual_artist'].value_counts().head(10).reset_index()
        top_artists.columns = ['Artist', 'Chart Appearances']
        fig_artists = px.bar(top_artists, x='Chart Appearances', y='Artist', orientation='h', title="Top 10 Artists by Appearance")
        fig_artists.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_artists, use_container_width=True)

        st.markdown("#### Content Explicitness Analysis")
        explicit_counts = df_filtered['is_explicit'].value_counts().reset_index()
        explicit_counts.columns = ['Is Explicit', 'Count']
        fig_explicit = px.pie(explicit_counts, values='Count', names='Is Explicit', title="Explicit vs Clean Content")
        st.plotly_chart(fig_explicit, use_container_width=True)

    with colB:
        st.markdown("#### Release Format Dominance")
        album_counts = df_filtered['album_type'].value_counts().reset_index()
        album_counts.columns = ['Album Type', 'Count']
        fig_album = px.bar(album_counts, x='Album Type', y='Count', title="Single vs Album Distribution", color='Album Type')
        st.plotly_chart(fig_album, use_container_width=True)
        
        st.markdown("#### Track Duration Insights")
        fig_duration = px.histogram(df_filtered, x='duration_ms', nbins=30, title="Song Duration Distribution (ms)")
        st.plotly_chart(fig_duration, use_container_width=True)

else:
    st.warning("No data matches the selected filters. Please adjust the sidebar options.")