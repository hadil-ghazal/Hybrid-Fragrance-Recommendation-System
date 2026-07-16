# ============================================================================
# AI ASSISTANCE DISCLOSURE
# UI/visual design pass generated with Claude (Claude Sonnet 5, Anthropic) on 7/15/26.
# Original app logic and structure authored by HG on 5/17/26 (see prior version).
#
# What changed in this pass (main.py only — model.py/evaluate.py untouched):
#   - Added a custom CSS "design system" (inject_styles) with a dark ink/brass
#     palette, Cormorant Garamond + Jost fonts, replacing default Streamlit styling
#   - Rebuilt the hero section (title/eyebrow/subtitle) via render_hero()
#   - Rewrote perfume result cards as single custom HTML blocks (build_card_html)
#     with an image or monogram placeholder, brand, name, a "match %" badge,
#     truncated description, notes, and a styled shop link — replacing the old
#     display_perfume_card() built from st.columns/st.write/st.link_button
#   - Added a 3-column responsive results grid (render_results_grid)
#   - Added styled empty/notice states (render_notice) replacing st.warning
#   - Added HTML-escaping (via the `html` module) for all CSV-sourced text
#     since it is now rendered as raw HTML, to avoid broken markup/injection
#   - Hid default Streamlit chrome (menu, footer, header) for a cleaner look
# ============================================================================
#
# This section of code has the Streamlit web application for personalized fragrance searching and gifting
# The user can select perfumes their friend or family already owns and likes and then the application
# generates similar fragrance recommendations using the recommendation model
# ============================================================================

# Imports
import html

import streamlit as st
from scripts.model import FragranceRecommender


st.set_page_config(
    page_title="Scent Match",
    page_icon="🌸",
    layout="wide",
)


# ----------------------------------------------------------------------------
# Design tokens
# Palette is built around glass perfume bottles and brass hardware rather than
# a generic light/dark theme: deep amber-black ground, brass-gold accent,
# a wine-red note for tags, warm ivory type.
# ----------------------------------------------------------------------------
INK = "#16130F"
INK_2 = "#1D1811"
GOLD = "#B8935B"
GOLD_SOFT = "#DCC297"
WINE = "#6B2A35"
IVORY = "#F1E9DC"
STONE = "#9C9284"
LINE = "rgba(184, 147, 91, 0.22)"


def inject_styles() -> None:
    """Injecting the custom 'atelier' visual identity for the app"""

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Jost', sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 15% -10%, {INK_2} 0%, {INK} 45%, #100D0A 100%);
            color: {IVORY};
        }}

        #MainMenu, footer, header {{ visibility: hidden; }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1120px;
        }}

        /* ---------- Hero ---------- */
        .sm-hero {{
            text-align: center;
            padding: 0.5rem 0 2rem 0;
            border-bottom: 1px solid {LINE};
            margin-bottom: 2.25rem;
        }}
        .sm-eyebrow {{
            font-family: 'Jost', sans-serif;
            letter-spacing: 0.38em;
            text-transform: uppercase;
            font-size: 0.7rem;
            font-weight: 500;
            color: {GOLD};
        }}
        .sm-title {{
            font-family: 'Cormorant Garamond', serif;
            font-weight: 500;
            font-size: 3.6rem;
            color: {IVORY};
            margin: 0.35rem 0 0.7rem 0;
        }}
        .sm-sub {{
            font-family: 'Jost', sans-serif;
            font-weight: 300;
            font-size: 1.02rem;
            color: {STONE};
            max-width: 540px;
            margin: 0 auto;
            line-height: 1.6;
        }}

        /* ---------- Section / panel labels ---------- */
        .sm-panel-label {{
            font-family: 'Jost', sans-serif;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            font-size: 0.7rem;
            font-weight: 500;
            color: {GOLD};
            margin-bottom: 0.5rem;
            display: block;
        }}
        .sm-section-heading {{
            font-family: 'Cormorant Garamond', serif;
            font-style: italic;
            font-size: 2rem;
            color: {IVORY};
            margin: 0 0 0.2rem 0;
        }}
        .sm-caption {{
            font-family: 'Jost', sans-serif;
            font-weight: 300;
            font-size: 0.85rem;
            color: {STONE};
            margin-bottom: 1.6rem;
        }}

        hr.sm-divider {{
            border: none;
            border-top: 1px solid {LINE};
            margin: 2.6rem 0 2rem 0;
        }}

        /* ---------- Result card ---------- */
        .sm-card {{
            background: linear-gradient(180deg, {INK_2} 0%, #17130D 100%);
            border: 1px solid {LINE};
            border-radius: 3px;
            padding: 1.4rem 1.5rem 1.6rem 1.5rem;
            margin-bottom: 1.4rem;
            height: 100%;
            transition: border-color 0.2s ease, transform 0.2s ease;
        }}
        .sm-card:hover {{
            border-color: rgba(184, 147, 91, 0.55);
            transform: translateY(-3px);
        }}
        .sm-card-img {{
            width: 100%;
            height: 190px;
            object-fit: cover;
            border-radius: 2px;
            margin-bottom: 1.1rem;
            filter: sepia(0.12) saturate(1.05);
        }}
        .sm-card-img-placeholder {{
            width: 100%;
            height: 190px;
            border-radius: 2px;
            margin-bottom: 1.1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(160deg, #241D14 0%, #171209 100%);
            border: 1px solid {LINE};
        }}
        .sm-card-img-placeholder span {{
            font-family: 'Cormorant Garamond', serif;
            font-style: italic;
            font-size: 2.6rem;
            color: {GOLD};
        }}
        .sm-card-brand {{
            font-family: 'Jost', sans-serif;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            font-size: 0.68rem;
            font-weight: 500;
            color: {STONE};
        }}
        .sm-card-name {{
            font-family: 'Cormorant Garamond', serif;
            font-style: italic;
            font-weight: 500;
            font-size: 1.65rem;
            color: {IVORY};
            line-height: 1.2;
            margin: 0.15rem 0 0.65rem 0;
        }}
        .sm-badge {{
            display: inline-block;
            border: 1px solid {GOLD};
            color: {GOLD_SOFT};
            font-family: 'Jost', sans-serif;
            font-size: 0.7rem;
            font-weight: 500;
            letter-spacing: 0.06em;
            padding: 0.18rem 0.6rem;
            border-radius: 20px;
            margin-bottom: 0.8rem;
        }}
        .sm-notes-label {{
            font-family: 'Jost', sans-serif;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            font-size: 0.62rem;
            font-weight: 500;
            color: {GOLD};
            display: block;
            margin-top: 0.7rem;
        }}
        .sm-notes-text {{
            font-family: 'Jost', sans-serif;
            font-weight: 300;
            font-size: 0.85rem;
            color: #C9C0B2;
            line-height: 1.5;
        }}
        .sm-desc {{
            font-family: 'Jost', sans-serif;
            font-weight: 300;
            font-size: 0.85rem;
            color: {STONE};
            line-height: 1.55;
            margin-top: 0.55rem;
        }}
        .sm-shop-btn {{
            display: inline-block;
            margin-top: 1.1rem;
            border: 1px solid {GOLD};
            color: {GOLD_SOFT} !important;
            text-decoration: none !important;
            font-family: 'Jost', sans-serif;
            font-size: 0.7rem;
            font-weight: 500;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 0.5rem 1.05rem;
            border-radius: 20px;
            transition: background 0.2s ease, color 0.2s ease;
        }}
        .sm-shop-btn:hover {{
            background: {GOLD};
            color: {INK} !important;
        }}

        /* ---------- Notice / empty states ---------- */
        .sm-notice {{
            border: 1px dashed {LINE};
            border-radius: 3px;
            padding: 2rem;
            text-align: center;
            margin-top: 1rem;
        }}
        .sm-notice-title {{
            font-family: 'Cormorant Garamond', serif;
            font-style: italic;
            font-size: 1.4rem;
            color: {IVORY};
            margin-bottom: 0.4rem;
        }}
        .sm-notice-text {{
            font-family: 'Jost', sans-serif;
            font-weight: 300;
            font-size: 0.88rem;
            color: {STONE};
        }}

        /* ---------- Streamlit widget overrides ---------- */
        .stButton > button {{
            background: {GOLD} !important;
            color: {INK} !important;
            border: none !important;
            border-radius: 2px !important;
            font-family: 'Jost', sans-serif !important;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            padding: 0.65rem 1.6rem !important;
        }}
        .stButton > button:hover {{
            background: {GOLD_SOFT} !important;
        }}
        [data-baseweb="tag"] {{
            background-color: {WINE} !important;
        }}
        .stSlider [data-baseweb="slider"] div[role="slider"] {{
            background-color: {GOLD} !important;
            border-color: {GOLD} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def load_recommender() -> FragranceRecommender:
    """Loading and caching the fragrance rec model"""

    return FragranceRecommender()


def render_hero() -> None:
    """Rendering the top-of-page brand moment"""

    st.markdown(
        """
        <div class="sm-hero">
            <span class="sm-eyebrow">A Personal Fragrance Atelier</span>
            <div class="sm-title">Scent Match</div>
            <div class="sm-sub">
                Select the fragrances someone already loves, and we'll trace
                the notes to their next signature scent.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_notice(title: str, text: str) -> None:
    """Rendering a styled notice for empty or missing-input states"""

    st.markdown(
        f"""
        <div class="sm-notice">
            <div class="sm-notice-title">{html.escape(title)}</div>
            <div class="sm-notice-text">{html.escape(text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def truncate(text: str, max_length: int = 150) -> str:
    """Trimming long descriptions so cards stay visually even"""

    text = text.strip()

    if len(text) <= max_length:
        return text

    return text[:max_length].rsplit(" ", 1)[0] + "…"


def build_card_html(perfume) -> str:
    """Building one fragrance recommendation as a single styled card"""

    name = html.escape(str(perfume["Name"]))
    brand = html.escape(str(perfume["Brand"]))
    match_percent = perfume["match_percent"]
    shop_link = html.escape(str(perfume["shop_link"]), quote=True)

    image_url = perfume["Image URL"]

    if isinstance(image_url, str) and image_url.strip():
        image_html = (
            f'<img class="sm-card-img" src="{html.escape(image_url, quote=True)}" '
            f'alt="{name}" />'
        )
    else:
        initial = html.escape(str(perfume["Name"])[:1].upper())
        image_html = (
            f'<div class="sm-card-img-placeholder"><span>{initial}</span></div>'
        )

    notes_html = ""
    notes = perfume["Notes"]

    if isinstance(notes, str) and notes.strip():
        notes_html = (
            '<span class="sm-notes-label">Fragrance Notes</span>'
            f'<div class="sm-notes-text">{html.escape(notes)}</div>'
        )

    desc_html = ""
    description = perfume["Description"]

    if isinstance(description, str) and description.strip():
        desc_html = f'<div class="sm-desc">{html.escape(truncate(description))}</div>'

    return f"""
    <div class="sm-card">
        {image_html}
        <div class="sm-card-brand">{brand}</div>
        <div class="sm-card-name">{name}</div>
        <div class="sm-badge">{match_percent}% match</div>
        {desc_html}
        {notes_html}
        <div>
            <a class="sm-shop-btn" href="{shop_link}" target="_blank">
                Shop this fragrance
            </a>
        </div>
    </div>
    """


def render_results_grid(recommendations) -> None:
    """Laying recommendations out as an even, responsive card grid"""

    rows = [
        recommendations.iloc[i : i + 3]
        for i in range(0, len(recommendations), 3)
    ]

    for row in rows:
        columns = st.columns(3)

        for column, (_, perfume) in zip(columns, row.iterrows()):
            with column:
                st.markdown(build_card_html(perfume), unsafe_allow_html=True)


def main() -> None:
    """Run the Streamlit fragrance recommendation application here"""

    inject_styles()

    recommender = load_recommender()

    render_hero()

    st.markdown(
        '<span class="sm-panel-label">Step One — Their Current Favorites</span>',
        unsafe_allow_html=True,
    )

    liked_perfumes = st.multiselect(
        "Select up to three perfumes they already love:",
        options=recommender.get_perfume_names(),
        max_selections=3,
        label_visibility="collapsed",
        placeholder="Search and select up to three fragrances…",
    )

    left, right = st.columns([3, 1])

    with left:
        st.markdown(
            '<span class="sm-panel-label">Step Two — How Many Matches</span>',
            unsafe_allow_html=True,
        )
        number_of_results = st.slider(
            "Number of recommendations:",
            min_value=3,
            max_value=10,
            value=5,
            label_visibility="collapsed",
        )

    with right:
        st.write("")
        find_clicked = st.button("Find Their Scent Match", type="primary")

    if find_clicked:
        if not liked_perfumes:
            render_notice(
                "Nothing selected yet",
                "Choose at least one perfume above before generating recommendations.",
            )
            return

        recommendations = recommender.recommend(
            liked_perfumes=liked_perfumes,
            number_of_results=number_of_results,
        )

        if recommendations.empty:
            render_notice(
                "No matches found",
                "Try selecting a different fragrance to generate recommendations.",
            )
            return

        st.markdown('<hr class="sm-divider" />', unsafe_allow_html=True)

        st.markdown(
            '<div class="sm-section-heading">Recommended Gifts</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sm-caption">Ranked by similarity between fragrance '
            "descriptions and notes.</div>",
            unsafe_allow_html=True,
        )

        render_results_grid(recommendations)


if __name__ == "__main__":
    main()