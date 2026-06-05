import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import urllib.parse
from recommender import MusicRecommender

# Set page configuration
st.set_page_config(
    page_title="VibeSync - Music Recommendation System",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling (glassmorphism, dark mode, outfit font)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global font override */
    html, body, [class*="css"], .stMarkdown, .stSelectbox, .stSlider {
        font-family: 'Outfit', 'Inter', sans-serif !important;
    }

    /* Main background gradient */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #15162a 0%, #0e0f17 100%) !important;
        color: #f8fafc !important;
    }

    /* Header styling with gradient */
    .header-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        background: transparent;
    }

    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa 0%, #6366f1 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(99, 102, 241, 0.2);
        letter-spacing: -0.03em;
    }

    .sub-title {
        font-size: 1.2rem;
        color: #94a3b8;
        font-weight: 300;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }

    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4);
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.35);
        box-shadow: 0 15px 50px 0 rgba(99, 102, 241, 0.12);
        transform: translateY(-4px);
    }

    .song-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }

    .song-artist {
        font-size: 1.2rem;
        color: #a78bfa;
        margin-bottom: 1rem;
        font-weight: 500;
    }

    /* Badge tags */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .badge-genre {
        background: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .badge-match {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.4);
        font-size: 0.8rem;
        padding: 0.35rem 0.85rem;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.15);
    }

    /* Music recommendation track list */
    .rec-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
    }

    .rec-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(99, 102, 241, 0.25);
        transform: scale(1.01);
    }

    .rec-info {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }

    .rec-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #ffffff;
    }

    .rec-artist {
        font-size: 0.95rem;
        color: #94a3b8;
    }

    .rec-actions {
        display: flex;
        gap: 0.75rem;
        align-items: center;
    }

    .btn-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 50%;
        text-decoration: none;
        transition: all 0.2s ease;
    }

    .btn-spotify {
        background: rgba(29, 185, 84, 0.1);
        border: 1px solid rgba(29, 185, 84, 0.3);
        color: #1db954;
    }

    .btn-spotify:hover {
        background: #1db954;
        color: #ffffff;
        box-shadow: 0 0 15px rgba(29, 185, 84, 0.4);
    }

    .btn-youtube {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid rgba(255, 0, 0, 0.3);
        color: #ff0000;
    }

    .btn-youtube:hover {
        background: #ff0000;
        color: #ffffff;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.4);
    }

    /* Player simulation */
    .now-playing {
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 1.5rem;
        padding-top: 1.25rem;
    }

    .progress-bar-container {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        margin: 0.75rem 0;
        position: relative;
    }

    .progress-bar-fill {
        width: 42%;
        height: 100%;
        background: linear-gradient(90deg, #6366f1, #a78bfa);
        border-radius: 2px;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
    }

    .player-time {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #64748b;
    }

    /* Customized sidebar */
    [data-testid="stSidebar"] {
        background-color: #0b0c16 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* Selectbox styling */
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
    }

    /* Section subtitles */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.25rem;
        border-left: 4px solid #6366f1;
        padding-left: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize recommendation engine
@st.cache_resource
def get_recommender():
    return MusicRecommender("spotify_tracks.csv")

try:
    recommender = get_recommender()
except Exception as e:
    st.error(f"Error loading system: {e}. Please ensure spotify_tracks.csv is generated.")
    st.stop()

# Title banner
st.markdown("""
<div class="header-container">
    <h1 class="main-title">🎵 VIBESYNC</h1>
    <p class="sub-title">COGNITIVE MUSIC RECOMMENDATION SYSTEM USING COSINE SIMILARITY</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters & inputs
with st.sidebar:
    st.markdown("<h3 style='color: #a78bfa; font-weight: 700; margin-bottom: 1.5rem;'>CONTROL PANEL</h3>", unsafe_allow_html=True)
    
    # Track list dropdown preparation
    available_songs = sorted(recommender.df['title'].tolist())
    
    selected_song_title = st.selectbox(
        "Select a song you like:",
        available_songs,
        index=available_songs.index("Blinding Lights") if "Blinding Lights" in available_songs else 0
    )
    
    # Sidebar options
    num_recommendations = st.slider(
        "Number of recommendations:",
        min_value=3,
        max_value=10,
        value=5,
        step=1
    )
    
    # Genre filter override option
    genre_filter = st.multiselect(
        "Restrict recommendations to genres:",
        options=sorted(recommender.df['genre'].unique().tolist()),
        default=[]
    )
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 0.85rem; color: #64748b; line-height: 1.4;'>
        <strong>How it works:</strong><br>
        Each song is represented as a high-dimensional vector using normalized audio features. 
        When you select a song, the system calculates the <strong>cosine similarity</strong> 
        between its vector and every other song in our library, returning the closest matches.
    </div>
    """, unsafe_allow_html=True)

# Get recommendations
try:
    query_song, recommendations = recommender.get_recommendations(selected_song_title, top_n=10)
    
    # Apply genre filter if selected
    if genre_filter:
        recommendations = [r for r in recommendations if r['genre'] in genre_filter]
        
    # Slice to the requested number of recommendations
    recommendations = recommendations[:num_recommendations]
except Exception as e:
    st.error(f"Error getting recommendations: {e}")
    st.stop()

# Layout splits: Main song dashboard & radar visualization
col1, col2 = st.columns([1, 1.1], gap="large")

with col1:
    st.markdown('<div class="section-title">Selected Track</div>', unsafe_allow_html=True)
    
    # Query song glass card
    st.markdown(f"""<div class="glass-card"><div class="badge badge-genre">{query_song['genre']}</div><div class="song-header">{query_song['title']}</div><div class="song-artist">by {query_song['artist']}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;margin-top:1rem;font-size:0.9rem;color:#94a3b8;"><div>Tempo: <strong>{query_song['tempo']:.0f} BPM</strong></div><div>Loudness: <strong>{query_song['loudness']:.1f} dB</strong></div><div>Energy: <strong>{query_song['energy'] * 100:.0f}%</strong></div><div>Danceability: <strong>{query_song['danceability'] * 100:.0f}%</strong></div></div><div class="now-playing"><div style="display:flex;align-items:center;gap:0.75rem;"><span style="font-size:1.5rem;color:#a78bfa;cursor:pointer;">▶️</span><span style="font-size:0.85rem;font-weight:500;color:#cbd5e1;">Simulated Player Preview</span></div><div class="progress-bar-container"><div class="progress-bar-fill"></div></div><div class="player-time"><span>0:42</span><span>3:15</span></div></div></div>""", unsafe_allow_html=True)

    # Search links for Selected Song
    spotify_query = urllib.parse.quote(f"{query_song['title']} {query_song['artist']}")
    st.markdown(f"""<div style="display:flex;gap:1rem;margin-bottom:2rem;padding-left:0.5rem;"><a class="btn-icon btn-spotify" href="https://open.spotify.com/search/{spotify_query}" target="_blank" title="Search on Spotify">🟢</a><span style="color:#94a3b8;font-size:0.9rem;align-self:center;">Find original track on Spotify</span><a class="btn-icon btn-youtube" href="https://www.youtube.com/results?search_query={spotify_query}" target="_blank" title="Search on YouTube">🔴</a><span style="color:#94a3b8;font-size:0.9rem;align-self:center;">Watch video on YouTube</span></div>""", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-title">Audio Feature Signature</div>', unsafe_allow_html=True)
    
    # Radar chart comparing query song features
    # Standardize features of the query song (we need to min-max normalize just for plotting,
    # but since recommender loads and pre-processes, we can pull the normalized values directly)
    query_idx = recommender.df[recommender.df['track_id'] == query_song['track_id']].index[0]
    query_norm_vals = recommender.scaled_features.iloc[query_idx].to_dict()
    
    # We plot key representative audio attributes
    radar_features = ["danceability", "energy", "speechiness", "acousticness", "liveness", "valence"]
    radar_values = [query_norm_vals[f] for f in radar_features]
    
    # Radar chart figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=radar_values,
        theta=[f.capitalize() for f in radar_features],
        fill='toself',
        name=query_song['title'],
        fillcolor='rgba(99, 102, 241, 0.25)',
        line=dict(color='rgba(99, 102, 241, 0.85)', width=2.5)
    ))
    
    # Add top recommendation to radar if available to show comparison
    if recommendations:
        top_rec = recommendations[0]
        top_rec_idx = recommender.df[recommender.df['track_id'] == int(top_rec['track_id'])].index[0]
        top_rec_norm = recommender.scaled_features.iloc[top_rec_idx].to_dict()
        top_rec_values = [top_rec_norm[f] for f in radar_features]
        
        fig.add_trace(go.Scatterpolar(
            r=top_rec_values,
            theta=[f.capitalize() for f in radar_features],
            fill='toself',
            name=f"Top Match: {top_rec['title']}",
            fillcolor='rgba(52, 211, 153, 0.15)',
            line=dict(color='rgba(52, 211, 153, 0.75)', width=2, dash='dash')
        ))
        
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showticklabels=False,
                ticks="",
                gridcolor='rgba(255, 255, 255, 0.08)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.08)',
                linecolor='rgba(255, 255, 255, 0.08)'
            ),
            bgcolor='rgba(0, 0, 0, 0)'
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='#cbd5e1'),
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=40, l=45, r=45),
        height=320
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown("<br>", unsafe_allow_html=True)

# Recommendations display
st.markdown('<div class="section-title">Recommended Tracks</div>', unsafe_allow_html=True)

if not recommendations:
    st.warning("No recommendations matching the selected filters. Try broadening your criteria.")
else:
    # Render recommended tracks
    for idx, rec in enumerate(recommendations, 1):
        match_percentage = rec['similarity'] * 100
        spotify_search = urllib.parse.quote(f"{rec['title']} {rec['artist']}")
        
        # Build raw feature preview details
        details_html = f"Tempo: {rec['features']['tempo']:.0f} BPM | Energy: {rec['features']['energy']*100:.0f}% | Danceability: {rec['features']['danceability']*100:.0f}%"
        
        st.markdown(f"""<div class="rec-card"><div class="rec-info"><div style="display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap;"><span class="rec-title">{idx}. {rec['title']}</span><span class="badge badge-genre" style="margin-bottom:0;">{rec['genre']}</span><span class="badge badge-match" style="margin-bottom:0;">{match_percentage:.1f}% Match</span></div><div class="rec-artist" style="margin-top:0.25rem;">by {rec['artist']}</div><div style="font-size:0.8rem;color:#64748b;margin-top:0.35rem;">{details_html}</div></div><div class="rec-actions"><a class="btn-icon btn-spotify" href="https://open.spotify.com/search/{spotify_search}" target="_blank" title="Search on Spotify">🟢</a><a class="btn-icon btn-youtube" href="https://www.youtube.com/results?search_query={spotify_search}" target="_blank" title="Search on YouTube">🔴</a></div></div>""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 2D Scatterplot visualization
st.markdown('<div class="section-title">Dataset Space Visualization</div>', unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.95rem; color: #94a3b8; margin-top: -0.75rem; margin-bottom: 1.5rem;'>Explore the overall library space plotted on Energy vs Danceability. See where your current song and recommended tracks sit in the general distribution.</p>", unsafe_allow_html=True)

# Prepare dataset plot
df_plot = recommender.df.copy()
df_plot['type'] = 'Library Track'

# Tag query and recommendations
df_plot.loc[df_plot['track_id'] == query_song['track_id'], 'type'] = 'Selected Track'

rec_ids = [int(r['track_id']) for r in recommendations]
df_plot.loc[df_plot['track_id'].isin(rec_ids), 'type'] = 'Recommended Track'

# Color map
color_map = {
    'Library Track': 'rgba(148, 163, 184, 0.25)',  # semi-transparent slate
    'Selected Track': '#6366f1',                   # Indigo glow
    'Recommended Track': '#10b981'                 # Emerald green
}

# Hover details
df_plot['hover_text'] = df_plot.apply(
    lambda r: f"<b>{r['title']}</b><br>Artist: {r['artist']}<br>Genre: {r['genre']}<br>Danceability: {r['danceability']:.2f}<br>Energy: {r['energy']:.2f}", 
    axis=1
)

# Plotly scatter figure
fig_scatter = px.scatter(
    df_plot,
    x="danceability",
    y="energy",
    color="type",
    color_discrete_map=color_map,
    category_orders={"type": ["Library Track", "Recommended Track", "Selected Track"]},
    custom_data=["hover_text"]
)

# Customize markers
fig_scatter.update_traces(
    hovertemplate="%{customdata[0]}<extra></extra>",
    marker=dict(size=10, line=dict(width=0.5, color='rgba(255,255,255,0.2)'))
)

# Scale up Selected Track and Recommended Tracks
selected_mask = fig_scatter.data[2] if len(fig_scatter.data) > 2 else None
# Find traces by name and update marker properties
for trace in fig_scatter.data:
    if trace.name == 'Selected Track':
        trace.marker.size = 18
        trace.marker.symbol = 'star'
        trace.marker.line = dict(width=1.5, color='#ffffff')
    elif trace.name == 'Recommended Track':
        trace.marker.size = 14
        trace.marker.symbol = 'circle'
        trace.marker.line = dict(width=1, color='#ffffff')

fig_scatter.update_layout(
    xaxis=dict(
        title=dict(text="Danceability", font=dict(color='#cbd5e1')),
        gridcolor='rgba(255,255,255,0.05)',
        zerolinecolor='rgba(255,255,255,0.05)',
        tickfont=dict(color='#64748b')
    ),
    yaxis=dict(
        title=dict(text="Energy", font=dict(color='#cbd5e1')),
        gridcolor='rgba(255,255,255,0.05)',
        zerolinecolor='rgba(255,255,255,0.05)',
        tickfont=dict(color='#64748b')
    ),
    legend=dict(
        font=dict(color='#cbd5e1'),
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(255,255,255,0.05)',
        borderwidth=1,
        yanchor="top",
        y=0.98,
        xanchor="left",
        x=0.02
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.01)',
    margin=dict(t=10, b=10, l=10, r=10),
    height=400
)

st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})

# Footer
st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin-top: 3rem;'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.85rem; padding-bottom: 2rem;'>
    VibeSync Music Recommendation Dashboard | Built with Python, Streamlit & Cosine Similarity
</div>
""", unsafe_allow_html=True)
