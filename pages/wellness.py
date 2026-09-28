import streamlit as st

from modules.ayurvedic import (
    AyurvedaKnowledgeEngine
)

from modules.homeopathy import (
    HomeopathyKnowledgeEngine
)

from modules.safety import (
    HealthSafetyEngine
)


st.set_page_config(
    page_title="SmartHealth AI - Wellness",
    page_icon="🌿",
    layout="wide"
)


st.title("🌿 Traditional Wellness Knowledge")

st.write(
    """
    Explore informational material from the application's
    Ayurveda and homeopathy knowledge datasets.
    """
)


st.warning(
    "This section is educational only. Traditional wellness "
    "information should not be treated as a proven treatment "
    "or replacement for professional medical care."
)


tab1, tab2 = st.tabs(
    [
        "🌿 Ayurveda",
        "⚕️ Homeopathy"
    ]
)


# ============================================================
# AYURVEDA
# ============================================================

with tab1:

    st.header(
        "Ayurveda Knowledge"
    )

    try:

        engine = AyurvedaKnowledgeEngine()

        query = st.text_input(
            "Search Ayurveda",
            placeholder="Example: digestion, sleep, diet"
        )

        if st.button(
            "🔎 Search",
            key="ayurveda_button"
        ):

            results = engine.search(
                query,
                top_n=10
            )

            if results.empty:

                st.info(
                    "No matching records found."
                )

            else:

                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

    except Exception as error:

        st.error(
            f"Could not load Ayurveda data: {error}"
        )


# ============================================================
# HOMEOPATHY
# ============================================================

with tab2:

    st.header(
        "Homeopathy Knowledge"
    )

    try:

        engine = HomeopathyKnowledgeEngine()

        query = st.text_input(
            "Search Homeopathy",
            placeholder="Example: traditional information"
        )

        if st.button(
            "🔎 Search",
            key="homeopathy_button"
        ):

            results = engine.search(
                query,
                top_n=10
            )

            if results.empty:

                st.info(
                    "No matching records found."
                )

            else:

                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

    except Exception as error:

        st.error(
            f"Could not load Homeopathy data: {error}"
        )


st.divider()


st.info(
    HealthSafetyEngine.get_traditional_disclaimer()
)