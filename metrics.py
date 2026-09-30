import pandas as pd

def get_artist_diversity_metrics(df_artists):
    total_entries = len(df_artists)
    unique_artists = df_artists['individual_artist'].nunique()
    
    # Diversity Score: Unique Artists / Total Entries
    diversity_score = unique_artists / total_entries if total_entries > 0 else 0
    
    # Top 5 Artists Share (Playlist Concentration Ratio)
    top_5_counts = df_artists['individual_artist'].value_counts().head(5).sum()
    concentration_ratio = top_5_counts / total_entries if total_entries > 0 else 0
    
    # Top dominating artists dataframe
    top_artists = df_artists['individual_artist'].value_counts().head(10).reset_index()
    top_artists.columns = ['Artist', 'Chart Appearances']
    
    return {
        'unique_artist_count': unique_artists,
        'diversity_score': round(diversity_score, 4),
        'concentration_ratio': round(concentration_ratio, 4),
        'top_artists': top_artists
    }

def get_collaboration_metrics(df_main):
    # Solo vs Collaborative tracks
    solo_count = len(df_main[df_main['collaborator_count'] == 1])
    collab_count = len(df_main[df_main['collaborator_count'] > 1])
    total = len(df_main)
    
    collab_ratio = collab_count / total if total > 0 else 0
    avg_collaborators = df_main['collaborator_count'].mean()
    
    return {
        'solo_count': solo_count,
        'collab_count': collab_count,
        'collab_ratio': round(collab_ratio, 4),
        'avg_collaborators': round(avg_collaborators, 2)
    }

def get_content_and_release_metrics(df_main):
    total = len(df_main)
    
    # Explicit Content Share
    explicit_count = df_main['is_explicit'].sum()
    explicit_share = explicit_count / total if total > 0 else 0
    
    # Release Strategy: Single vs Album
    single_count = len(df_main[df_main['album_type'] == 'single'])
    album_count = len(df_main[df_main['album_type'] == 'album'])
    
    single_album_ratio = single_count / album_count if album_count > 0 else 0
    
    return {
        'explicit_share': round(explicit_share, 4),
        'single_count': single_count,
        'album_count': album_count,
        'single_album_ratio': round(single_album_ratio, 4)
    }

if __name__ == "__main__":
    # This block tests the functions by importing your data_processing script
    from data_processing import load_and_standardize
    
    print("Running KPI calculations...")
    # Using your existing dataset
    df, df_artists = load_and_standardize("Atlantic_United_Kingdom.csv")
    
    print("\n--- UK Market Structure KPIs ---")
    
    artist_kpis = get_artist_diversity_metrics(df_artists)
    print(f"Unique Artists: {artist_kpis['unique_artist_count']}")
    print(f"Diversity Score: {artist_kpis['diversity_score']}")
    print(f"Artist Concentration Index (Top 5 Share): {artist_kpis['concentration_ratio']}")
    
    collab_kpis = get_collaboration_metrics(df)
    print(f"\nCollaboration Ratio: {collab_kpis['collab_ratio']}")
    print(f"Average Collaborators Per Track: {collab_kpis['avg_collaborators']}")
    
    content_kpis = get_content_and_release_metrics(df)
    print(f"\nExplicit Content Share: {content_kpis['explicit_share']}")
    print(f"Single vs Album Ratio: {content_kpis['single_album_ratio']}")