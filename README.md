# Hybrid-Fragrance-Recommendation-System
A hybrid recommendation system for personalized fragrance gifting using content-based filtering and similarity learning

---

## Technical Overview

This project uses a **hybrid content-based recommendation system** for fragrance recommendation using classical information retrieval and recommendation system techniques.

### Core Machine Learning Pipeline

- **Content-Based Filtering** : recommends fragrances based on textual similarity rather than historical user interactions
- **TF-IDF** — converts the perfume descriptions and fragrance notes into numerical feature vectors by weighting informative scent terms while reducing the influence of common words
- **Cosine Similarity Ranking** : calculates the similarity between fragrance vectors to retrieve the most similar perfumes.
- **Cold-Start Friendly Design**: because recommendations rely on item metadata instead of user interaction history, the system can immediately generate recommendations for new users who provide one or more favorite fragrances.
- **Post-Processing Diversity Constraint**: evaluates recommendation diversity by limiting duplicate brands within recommendation results, demonstrating a simple responsible recommendation strategy.

### Recommendation Systems Concepts Covered

- Content-Based Filtering
- Information Retrieval
- Feature Engineering
- Text Vectorization
- Similarity Search
- Cold Start Recommendation
- Responsible Recommendation Systems

---

## Problem Statement

Purchasing perfume for someone else is challenging because fragrance prefeneces are highly personal and difficult to describe. Many consumers rely on blind purchases, bestseller lists, or generic retailer recommendations that can lead to dissatisfied purchases, wasted products, inefficient returns, and in general just fail to reflect the recipient's actual preferences

So, this project addresses that problem by allowing users to select one or more fragrances the person already enjoys and generating personalized recommendations based on textual fragrance characteristics

---

## Why This Matters

Fragrance is one of the most subjective consumer products available. Unlike books or movies, customers can't easily experience a scent when shopping online, leading to uncertainty and costly blind purchases.

A recommendation system tailored to an individual's existing fragrance preferences can:

- Reduce poor purchasing decisions
- Improve gift personalization
- Increase customer confidence
- Improve product discovery
- Help users explore fragrances beyond best sellers

---

## Project Objectives

- Build a content based recommendation system
- Recommend perfumes using fragrance descriptions and notes
- Demonstrate explainable recommendations
- Evaluate recommendation relevance alongside recommendation diversity
- Deploy an accessible web application

---

## Dataset

Source:

**Kaggle – Perfume Recommendation Dataset**
https://www.kaggle.com/datasets/nandini1999/perfume-recommendation-dataset?resource=download

The dataset contains approximately 2,000 perfumes with:

- Perfume name
- Brand
- Description
- Fragrance notes
- Image URL

The project uses fragrance descriptions and note compositions to colculate the similarity between perfumes

---

## Methodology

### Recommendation Approach

This project implements and utlizes a **content-based recommendation system**

Unlike collaborative filtering, this approach doesn't require historical user interactions and was a natural way to handle cold-start users, future iterations could utilize real time perfume feedback for enhanced data

The workflow consists of
1. User selects perfumes already enjoyed
2. Descriptions and fragrance notes are combined
3. Text is converted into TF-IDF vectors
4. Cosine similarity measures fragrance similarity
5. Highest-ranked perfumes are returned

---

## The Recommendation Pipeline Is:

User Input -> Favorite Perfumes -> Combine Notes + Descriptions - > TF-IDF Vectorization -> Cosine Similarity -> Rank Recommendations -> Streamlit Web Application


---

## Responsible AI Considerations

Many recommendation systems repeatedly surface highly similar or popular products. This deteriorates user trust, making recommendations feel forced and funded rather than genuine.

So, for more responsible recommendation behavior, this project evaluates:
- Recommendation relevance
- Brand diversity within the recommendation list

Rather than evaluating only similarity, the evaluation compares standard similarity based recommendations against a simple diversity aware approach that increases exposure to different fragrance brands while maintaining strong recommendation quality

---

## Evaluation

The evaluation script compares two recommendation strategies

### Standard Similarity

Returns the perfumes with the highest cosine similarity scores.

### Diversity-Aware

Limits duplicate brands in the recommendation list to encourage broader product exposure and a richer exploration

Evaluation metrics include:

- Average recommendation similarity
- Number of unique brands recommended

---

## Web Application

The application allows users to:

- Search existing perfumes
- Select up to three fragrances someone already enjoys
- Generate personalized recommendations
- View fragrance descriptions
- View fragrance notes
- Open shopping links for recommended perfumes

---

## Installation

Clone the repository

```bash
git clone https://github.com/hadil-ghazal/Hybrid-Fragrance-Recommendation-System.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Launch the Streamlit application:

```bash
streamlit run main.py
```

Run the evaluation script:

```bash
python scripts/evaluate.py
```

---

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity

---

## Future Improvements

Potential future enhancements include:

- Hybrid recommendation models
- Sentence-transformer embeddings
- User accounts and fragrance collections
- Wishlist functionality
- Gift registries
- Multi-retailer purchasing links
- Price-aware recommendations
- Explainable recommendation summaries
- Mobile application deployment
- Personalized recommendation history

---

## Commercial Viability

This recommendation engine could be integrated into:

- Fragrance retailers
- Department stores
- Subscription fragrance services
- Beauty marketplaces
- Gift recommendation platforms

Potential monetization opportunities include:

- Affiliate commissions
- Premium recommendation subscriptions
- White-label recommendation APIs
- Retail software licensing
- Sponsored fragrance placements
- Personalized gift registry services

Because the recommendation engine is content-based, it can also be adapted to new fragrance catalogs without requiring large volumes of historical user interaction data.

---

## Ethics

This project recommends products using textual fragrance similarity rather than personal demographic information. An essential piece of the product ethical design  is that it doesn't infer personality traits or psychological characteristics from fragrance preferences. Instead,recs are meant to be viewed as decision support tools, fun and interactive insights, and a way to track personal preference rather than definitive purchasing advice, since at the end of the day, fragrance preference remains highly subjective

---

## Author

**Hadil Ghazal, 2026**

