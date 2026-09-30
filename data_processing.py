import pandas as pd

def load_and_standardize(file_path):
    print("Loading dataset...")
    df = pd.read_csv(file_path)
    
    # 1. Date Validation
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    
    # 2. String Normalization (trimming extra spaces)
    df['artist'] = df['artist'].str.strip()
    df['song'] = df['song'].str.strip()
    
    # 3. Handle Collaborations
    # Create a list of artists by splitting on '&' and ','
    df['artist_list'] = df['artist'].str.replace(',', '&').str.split('&')
    
    # Strip whitespace from individual artist names in the list
    df['artist_list'] = df['artist_list'].apply(lambda x: [artist.strip() for artist in x])
    
    # Count the number of collaborating artists on the track
    df['collaborator_count'] = df['artist_list'].apply(len)
    
    # Create an exploded dataframe where each row represents ONE artist per song
    # This is critical for our Artist Dominance & Diversity KPIs
    df_exploded = df.explode('artist_list').rename(columns={'artist_list': 'individual_artist'})
    
    print("\n--- Standardization Complete ---")
    print(f"Original records: {len(df)}")
    print(f"Exploded records (accounting for collaborations): {len(df_exploded)}")
    
    return df, df_exploded

if __name__ == "__main__":
    # Ensure 'Atlantic_United_Kingdom.csv' is in the same folder as this script
    file_path = "Atlantic_United_Kingdom.csv"
    
    df_main, df_artists = load_and_standardize(file_path)
    
    # Preview the exploded data to verify collaborations split correctly
    print("\nPreview of Exploded Artist Data:")
    print(df_artists[['song', 'artist', 'individual_artist', 'collaborator_count']].head(10))