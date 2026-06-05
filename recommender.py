import pandas as pd
import numpy as np

class MusicRecommender:
    def __init__(self, csv_path="spotify_tracks.csv"):
        self.csv_path = csv_path
        self.df = None
        self.features = [
            "danceability", "energy", "key", "loudness", 
            "mode", "speechiness", "acousticness", 
            "instrumentalness", "liveness", "valence", "tempo"
        ]
        self.scaled_features = None
        self.load_and_preprocess()

    def load_and_preprocess(self):
        # Load dataset
        try:
            self.df = pd.read_csv(self.csv_path)
        except Exception as e:
            raise FileNotFoundError(f"Could not load dataset from {self.csv_path}: {e}")

        # Ensure all columns exist
        missing_cols = [col for col in self.features if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns in dataset: {missing_cols}")

        # Normalize features using Min-Max scaling
        # (val - min) / (max - min) to scale every feature to [0, 1]
        df_features = self.df[self.features].copy()
        min_vals = df_features.min()
        max_vals = df_features.max()
        
        # Avoid division by zero if min == max
        range_vals = max_vals - min_vals
        range_vals[range_vals == 0] = 1.0
        
        self.scaled_features = (df_features - min_vals) / range_vals

    def get_recommendations(self, title, top_n=5):
        if self.df is None or self.scaled_features is None:
            self.load_and_preprocess()

        # Find the query song (case-insensitive search)
        matches = self.df[self.df['title'].str.lower() == title.lower()]
        
        if matches.empty:
            # Try a fuzzy substring search if exact match fails
            matches = self.df[self.df['title'].str.lower().str.contains(title.lower())]
            if matches.empty:
                raise ValueError(f"Song '{title}' not found in the dataset.")
            
        # Take the first match
        query_idx = matches.index[0]
        query_vector = self.scaled_features.iloc[query_idx].values

        # Compute cosine similarity
        matrix = self.scaled_features.values
        
        # Cosine similarity formula: dot(A, B) / (norm(A) * norm(B))
        dot_products = np.dot(matrix, query_vector)
        query_norm = np.linalg.norm(query_vector)
        matrix_norms = np.linalg.norm(matrix, axis=1)
        
        # Add a small epsilon to avoid division by zero
        similarities = dot_products / (matrix_norms * query_norm + 1e-9)

        # Create a copy of the dataframe to store similarities
        df_result = self.df.copy()
        df_result['similarity'] = similarities

        # Exclude the query song from recommendations
        df_result = df_result.drop(query_idx)

        # Sort by similarity descending
        recommendations = df_result.sort_values(by='similarity', ascending=False).head(top_n)

        # Format output as a list of dictionaries
        output = []
        for idx, row in recommendations.iterrows():
            output.append({
                "track_id": str(row["track_id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "similarity": float(row["similarity"]),
                # Also include raw features for visualization
                "features": {col: float(row[col]) for col in self.features}
            })
            
        return matches.iloc[0].to_dict(), output

# Self-test when run directly
if __name__ == "__main__":
    print("Running self-test...")
    import os
    if not os.path.exists("spotify_tracks.csv"):
        print("Error: spotify_tracks.csv not found. Please run generate_dataset.py first.")
    else:
        recommender = MusicRecommender("spotify_tracks.csv")
        song_title = "Blinding Lights"
        try:
            query, recs = recommender.get_recommendations(song_title, 5)
            print(f"\nQuery Song: '{query['title']}' by {query['artist']} [{query['genre']}]")
            print("\nTop 5 Recommendations:")
            for i, rec in enumerate(recs, 1):
                print(f"{i}. '{rec['title']}' by {rec['artist']} (Genre: {rec['genre']}, Similarity: {rec['similarity']:.4f})")
        except Exception as e:
            print(f"Self-test failed: {e}")
