# No AI was used to generate this code
# all code authored by HG on 5/17/26
# This script is to evaluate the fragrance rec system
# by comparing the standard top 5 similarity recs
# with a simple diversified version.

#Specific approach here is to measure hte average match score and the number of unique brands


#Imports
import pandas as pd
from model import FragranceRecommender


def create_diverse_recommendations(
    recommendations: pd.DataFrame,
    number_of_results: int = 5,
) -> pd.DataFrame:
    # Keeping the highest-ranked perfume from each unique brand
    #...Args: recommendations: Ranked perfume recommendations,. number_of_results: Number of recommendations to return
   # Returns:a DataFrame that has brand diversified recommendations
    

    return (
        recommendations
        .drop_duplicates(subset="Brand")
        .head(number_of_results)
        .copy()
    )


def calculate_metrics(
    recommendations: pd.DataFrame,
) -> dict:
    #Calculating simple relevance and diversity metrics. Args
    #...recommendations: the recommended results to evaluate 
    # Returns: A dictionary w/ average match and unique brand counts

    return {
        "average_match": round(
            recommendations["match_percent"].mean(),
            1,
        ),
        "unique_brands": recommendations["Brand"].nunique(),
    }


def main() -> None:
    """Run the recommendation evaluation."""

    recommender = FragranceRecommender()

    # Using existing perfume from the dataset for testing
    test_perfume = recommender.get_perfume_names()[0]

    # Generatign  more option so that variations can be applied
    candidate_results = recommender.recommend(
        liked_perfumes=[test_perfume],
        number_of_results=20,
    )

    ####################################################################
    # Standard approach: use the five most similar perfumes.
    standard_results = candidate_results.head(5).copy()

    ####################################################################
    # Responsible approach: prefer different brands.
    diverse_results = create_diverse_recommendations(
        recommendations=candidate_results,
        number_of_results=5,
    )

    standard_metrics = calculate_metrics(standard_results)
    diverse_metrics = calculate_metrics(diverse_results)

    evaluation_results = pd.DataFrame(
        [
            {
                "Approach": "Standard similarity",
                "Average Match": standard_metrics["average_match"],
                "Unique Brands": standard_metrics["unique_brands"],
            },
            {
                "Approach": "Diversity-aware",
                "Average Match": diverse_metrics["average_match"],
                "Unique Brands": diverse_metrics["unique_brands"],
            },
        ]
    )

    print(f"Test perfume: {test_perfume}\n")

    print("Standard recommendations:")
    print(
        standard_results[
            ["Name", "Brand", "match_percent"]
        ]
    )

    print("\nDiversity-aware recommendations:")
    print(
        diverse_results[
            ["Name", "Brand", "match_percent"]
        ]
    )

    print("\nEvaluation comparison:")
    print(evaluation_results)


if __name__ == "__main__":
    main()