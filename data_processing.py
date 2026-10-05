import pandas as pd
import os

def load_and_standardize(file_path="Atlantic_United_Kingdom.csv"):
    print("Loading dataset...")
    
    # Build absolute path to ensure Streamlit Cloud finds the file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_path)
    
    # Read the dataset
    df = pd.read_csv(full_path)
    
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
    df_exploded = df.explode('artist_list').rename(columns={'artist_list': 'individual_artist'})
    
    print("\n--- Standardization Complete ---")
    print(f"Original records: {len(df)}")
    print(f"Exploded records: {len(df_exploded)}")
    
    return df, df_exploded

if __name__ == "__main__":
    # Test the function locally
    df_main, df_artists = load_and_standardize()
    print("\nPreview of Exploded Artist Data:")
    print(df_artists[['song', 'artist', 'individual_artist', 'collaborator_count']].head(10))