# No AI was used to generate this code
# all code authored by HG on 5/17/26
# 
# 
#Using Data sourced from Kaggle: https://www.kaggle.com/datasets/nandini1999/perfume-recommendation-dataset?resource=download

# This script implements a content based fragrance recommendation system using TF-IDF
# vectorization and cosine similarity. The model analyzes perfume descriptions
# and fragrance notes to recommend perfumes that are most similar to those
# already liked by the user



from pathlib import Path
from urllib.parse import quote_plus


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "perfumes.csv"


class FragranceRecommender:
    #Content-based perfume recommendation system

    def __init__(self):
        #Latin1 required for this dataset
        self.perfumes = pd.read_csv(DATA_PATH, encoding="latin1")

        # Removing rows missing name and brand
        self.perfumes = self.perfumes.dropna(subset=["Name", "Brand"])

        #Combining description and notes into one text feature
        self.perfumes["combined_features"] = (
            self.perfumes["Description"].fillna("")
            + " "
            + self.perfumes["Notes"].fillna("")
        )

        #Converting perfume text into TF-IDF feature vectors
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
        )

        self.feature_matrix = self.vectorizer.fit_transform(
            self.perfumes["combined_features"]
        )

    def get_perfume_names(self) -> list:
        """Returning the perfume names for the app dropdown"""

        return sorted(self.perfumes["Name"].unique().tolist())

    def recommend(
        self,
        liked_perfumes: list,
        number_of_results: int = 5,
    ) -> pd.DataFrame:
        """Recommending perfumes similar to the selected fragrances"""

        liked_indices = self.perfumes[
            self.perfumes["Name"].isin(liked_perfumes)
        ].index.tolist()

        if not liked_indices:
            return pd.DataFrame()

        # Creating one profile by averaging the selected perfume vectors
        #scent_profile = self.feature_matrix[liked_indices].mean(axis=0)

        scent_profile = np.asarray(
            self.feature_matrix[liked_indices].mean(axis=0)
        )


        # Step to compare the profile with every perfume in the dataset
        similarity_scores = cosine_similarity(
            scent_profile,
            self.feature_matrix,
        ).flatten()

        results = self.perfumes.copy()
        results["match_score"] = similarity_scores

        # Excluding any perfumes the user already likes
        results = results[
            ~results["Name"].isin(liked_perfumes)
        ]

        # Returning the highest scoring recommendations
        results = results.sort_values(
            by="match_score",
            ascending=False,
        ).head(number_of_results)

        results["match_percent"] = (
            results["match_score"] * 100
        ).round(1)

        results["shop_link"] = results.apply(
            lambda row: self.create_shop_link(
                row["Brand"],
                row["Name"],
            ),
            axis=1,
        )

        return results[
            [
                "Name",
                "Brand",
                "Description",
                "Notes",
                "Image URL",
                "match_percent",
                "shop_link",
            ]
        ]

    @staticmethod
    def create_shop_link(brand: str, perfume_name: str) -> str:
        """Create a Google Shopping link."""

        search_query = quote_plus(
            f"{brand} {perfume_name} perfume"
        )

        return (
            "https://www.google.com/search"
            f"?tbm=shop&q={search_query}"
        )

if __name__ == "__main__":
    recommender = FragranceRecommender()

    first_perfume = recommender.get_perfume_names()[0]

    print("Testing with:", first_perfume)

    sample_results = recommender.recommend(
        liked_perfumes=[first_perfume],
    )

    print(sample_results)