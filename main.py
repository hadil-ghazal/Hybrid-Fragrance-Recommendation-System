
# No AI was used to generate this code
# all code authored by HG on 5/17/26
#
# THis seciton of code has the Streamlit web application for personalized fragrance searching and gifting
# The usre can select perfumes their friend or family already owns and likes and then the application
# generates similar fragrance recommendations using the recommendation model
# ============================================================================

#Imports
import streamlit as st
from scripts.model import FragranceRecommender


st.set_page_config(
    page_title="Scent Match",
    page_icon="🌸",
    layout="wide",
)


@st.cache_resource
def load_recommender() -> FragranceRecommender:
#Loading and caching the fragrance rec model

    return FragranceRecommender()


def display_perfume_card(perfume) -> None:
 #showing one fragrance recommendation, perfume: One row from the rec results

    left_column, right_column = st.columns([1, 3])

    with left_column:
        image_url = perfume["Image URL"]

        if isinstance(image_url, str) and image_url.strip():
            st.image(
                image_url,
                use_container_width=True,
            )

    with right_column:
        st.subheader(perfume["Name"])
        st.write(f"**Brand:** {perfume['Brand']}")
        st.write(f"**Match score:** {perfume['match_percent']}%")

        notes = perfume["Notes"]

        if isinstance(notes, str) and notes.strip():
            st.write(f"**Notes:** {notes}")

        description = perfume["Description"]

        if isinstance(description, str) and description.strip():
            st.write(description)

        st.link_button(
            "Shop this fragrance",
            perfume["shop_link"],
        )


def main() -> None:
    #Run the Streamlit fragrance recommendation application here

    recommender = load_recommender()

    st.title("Scent Match")

    st.write(
        "Find a thoughtful perfume gift using fragrances "
    )

    liked_perfumes = st.multiselect(
        "Select up to three perfumes they already love:",
        options=recommender.get_perfume_names(),
        max_selections=3,
    )

    number_of_results = st.slider(
        "Number of recommendations:",
        min_value=3,
        max_value=10,
        value=5,
    )

    if st.button(
        "Find Their Scent Match",
        type="primary",
    ):
        if not liked_perfumes:
            st.warning(
                "Select at least one perfume before generating recommendations"
            )
            return

        recommendations = recommender.recommend(
            liked_perfumes=liked_perfumes,
            number_of_results=number_of_results,
        )

        if recommendations.empty:
            st.warning(
                "No recommendations were found for the selected perfumes"
            )
            return

        st.header("Recommended Gifts")

        st.caption(
            "Recommendations are ranked using similarity between perfume "
            "descriptions and fragrance notes"
        )

        for _, perfume in recommendations.iterrows():
            with st.container(border=True):
                display_perfume_card(perfume)


if __name__ == "__main__":
    main()