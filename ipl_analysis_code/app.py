# import streamlit as st

# # ✅ MUST be first Streamlit command and ONLY ONCE
# st.set_page_config(
#     page_title="IPL Analytics Pro",
#     layout="wide"
# )

# # Define your pages
# predictor_page = st.Page(
#     "pages/predictor.py",
#     title="IPL Win Predictor",
#     icon="🏏"
# )

# analysis_page = st.Page(
#     "pages/analysis.py",
#     title="Match Analysis Dashboard",
#     icon="📊"
# )

# dashboard_page = st.Page(
#     "pages/dashboard.py",
#     title="Home",
#     icon="🏠"
# )

# # Create navigation
# pg = st.navigation([dashboard_page, predictor_page, analysis_page])

# # Run selected page
# pg.run()



import streamlit as st

# ✅ MUST be first Streamlit command and ONLY ONCE
st.set_page_config(
    page_title="IPL Analytics Pro",
    layout="wide"
)

# Pages
dashboard_page = st.Page(
    "pages/dashboard.py",
    title="Home",
    icon="🏠"
)

predictor_page = st.Page(
    "pages/predictor.py",
    title="IPL Win Predictor",
    icon="🏏"
)

score_predictor_page = st.Page(
    "pages/score_predictor.py",
    title="IPL Score Predictor",
    icon="🎯"
)

analysis_page = st.Page(
    "pages/analysis.py",
    title="Match Analysis Dashboard",
    icon="📊"
)

# Navigation
pg = st.navigation([
    dashboard_page,
    predictor_page,
    score_predictor_page,
    analysis_page
])

pg.run()


