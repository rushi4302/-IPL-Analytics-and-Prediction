import streamlit as st

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0e1117;
    }

    /* Seamless Background */
    .main {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
    }

    [data-testid="stSidebarNav"], section[data-testid="stSidebar"], 
    #MainMenu, footer, header {visibility: hidden; display: none;}

    /* Hero Section with Glassmorphism */
    .hero-section {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 80px 20px;
        border-radius: 40px;
        text-align: center;
        margin-bottom: 60px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    .hero-title {
        font-size: 5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0 !important;
        letter-spacing: -2px;
    }

    .hero-subtitle {
        color: #38bdf8 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 10px !important;
    }

    /* Premium Feature Cards */
    .feature-card {
        background: #ffffff !important;
        border-radius: 32px;
        padding: 50px 40px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
    }

    .feature-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 30px 60px rgba(56, 189, 248, 0.2);
        border-color: #38bdf8;
    }

    .card-icon { 
        background: #f1f5f9;
        width: 80px;
        height: 80px;
        line-height: 80px;
        border-radius: 20px;
        font-size: 3rem; 
        margin: 0 auto 25px; 
        display: block; 
    }

    .card-title { 
        font-size: 2.5rem !important; 
        color: #0f172a !important; 
        font-weight: 800 !important;
    }

    .card-description { 
        color: #475569 !important; 
        font-size: 1.2rem !important;
        line-height: 1.6;
        margin-bottom: 30px !important;
    }

    /* Modern List Styling */
    .features-list {
        text-align: left;
        margin: 20px 0 30px 0;
        display: inline-block;
    }

    .features-list li {
        color: #1e293b !important;
        font-weight: 500;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        font-size: 1.1rem;
    }

    .features-list li::before {
        content: '✦';
        color: #38bdf8;
        margin-right: 12px;
        font-weight: bold;
    }

    /* Action Buttons */
    div.stButton > button {
        background: #0f172a;
        color: white !important;
        border-radius: 18px;
        padding: 18px 0;
        font-weight: 700;
        font-size: 1.2rem;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div.stButton > button:hover {
        background: #38bdf8;
        color: #0f172a !important;
        box-shadow: 0 10px 20px rgba(56, 189, 248, 0.4);
    }

    /* Bottom Stats Section */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-top: 60px;
    }

    .stat-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 24px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stat-val {
        display: block;
        font-size: 3rem;
        font-weight: 900;
        color: #ffffff;
    }

    .stat-lab {
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Main UI
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">IPL ANALYTICS PRO</h1>
    <p class="hero-subtitle">The Future of Cricket Intelligence</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="card-icon">🎯</span>
        <h2 class="card-title">Win Predictor</h2>
        <p class="card-description">Precision-engineered ML models calculating real-time probabilities with every ball.</p>
        <ul class="features-list">
            <li>Live Chase Probability</li>
            <li>Wicket Impact Analysis</li>
            <li>Venue Pressure Scoring</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Enter Predictor", key="pred_btn", use_container_width=True):
        st.switch_page("pages/predictor.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="card-icon">📊</span>
        <h2 class="card-title">Match Insight</h2>
        <p class="card-description">Uncover hidden patterns using historical data from over 1,000 IPL matches.</p>
        <ul class="features-list">
            <li>Head-to-Head Dominance</li>
            <li>Player vs Team Stats</li>
            <li>Dynamic Trend Dashboards</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📈 Explore Analytics", key="anal_btn", use_container_width=True):
        st.switch_page("pages/analysis.py")

# Stats Grid
st.markdown("""
<div class="stats-container">
    <div class="stat-box">
        <span class="stat-val">95%</span>
        <span class="stat-lab">Model Accuracy</span>
    </div>
    <div class="stat-box">
        <span class="stat-val">10+</span>
        <span class="stat-lab">Seasons Data</span>
    </div>
    <div class="stat-box">
        <span class="stat-val">RealTime</span>
        <span class="stat-lab">Processing</span>
    </div>
</div>
""", unsafe_allow_html=True)
