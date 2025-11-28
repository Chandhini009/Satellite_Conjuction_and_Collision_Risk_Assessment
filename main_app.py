# app.py
import os
import streamlit as st
from skyfield.api import load
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from numpy.linalg import norm

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="🛰️ Satellite Conjunction & Collision Risk Analysis",
    layout="wide",
)

# ----------------------------
# Custom Styling
# ----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
    color: white;
}
h1, h2, h3 {
    color: #FFD700;
    text-align: center;
    font-family: 'Trebuchet MS', sans-serif;
}
.dataframe {
    background-color: rgba(255, 255, 255, 0.05);
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
.card {
    background-color: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(255,215,0,0.2);
    margin-bottom: 20px;
}
hr {
    border: 1px solid #FFD700;
}
.stTabs [role="tablist"] {
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🛰️ Satellite Conjunction & Collision Risk Analysis 🌌")
st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------
# Load TLE File
# ----------------------------
tle_file = "data/satellites_active.tle"
if not os.path.exists(tle_file):
    st.error(f"❌ TLE file not found: {tle_file}")
    st.stop()

stations = load.tle_file(tle_file)
st.success(f"✅ Loaded {len(stations)} satellites from TLE data")

# ----------------------------
# Utility Functions
# ----------------------------
def eda_summary(stations):
    data = [{
        "Name": sat.name,
        "Inclination": sat.model.inclo,
        "RAAN": sat.model.nodeo,
        "Eccentricity": sat.model.ecco,
        "Mean Motion": sat.model.no_kozai
    } for sat in stations]
    df = pd.DataFrame(data)
    return df, df.describe()

def propagate_satellite(sat, hours=24, step_min=10):
    ts = load.timescale()
    times = ts.utc(2025, 9, 27, 0, 0, range(0, hours * 60 + 1, step_min))
    geocentric = sat.at(times)
    lat, lon = geocentric.subpoint().latitude.degrees, geocentric.subpoint().longitude.degrees
    return pd.DataFrame({"Time": times.utc_datetime(), "Latitude": lat, "Longitude": lon})

# ----------------------------
# Improved Conjunction Detection
# ----------------------------
def detect_conjunctions_for_sat(selected_sat, stations, hours=24, step_min=10, threshold=500):
    df_list = []
    ts = load.timescale()
    times = ts.utc(2025, 9, 27, 0, 0, range(0, hours * 60 + 1, step_min))
    pos_sel = selected_sat.at(times).position.km.T
    vel_sel = selected_sat.at(times).velocity.km_per_s.T

    for sat in stations:
        if sat.name == selected_sat.name:
            continue

        pos_oth = sat.at(times).position.km.T
        vel_oth = sat.at(times).velocity.km_per_s.T

        rel_pos = pos_sel - pos_oth
        rel_vel = vel_sel - vel_oth
        dist = norm(rel_pos, axis=1)
        v_rel = norm(rel_vel, axis=1)

        close_idx = np.where(dist < threshold)[0]
        for idx in close_idx:
            df_list.append({
                "Time": times[idx].utc_datetime(),
                "Satellite1": selected_sat.name,
                "Satellite2": sat.name,
                "Distance_km": round(dist[idx], 3),
                "Rel_Velocity_km/s": round(v_rel[idx], 3)
            })

    return pd.DataFrame(df_list)

# ----------------------------
# Improved Collision Risk Calculation (for conjunction sats)
# ----------------------------
def compute_risk_for_sat(selected_sat, stations, hours=24, step_min=10):
    ts = load.timescale()
    times = ts.utc(2025, 9, 27, 0, 0, range(0, hours * 60 + 1, step_min))
    pos_sel = selected_sat.at(times).position.km.T
    vel_sel = selected_sat.at(times).velocity.km_per_s.T
    df_list = []

    for sat in stations:
        if sat.name == selected_sat.name:
            continue

        pos_oth = sat.at(times).position.km.T
        vel_oth = sat.at(times).velocity.km_per_s.T
        rel_pos = pos_sel - pos_oth
        rel_vel = vel_sel - vel_oth

        dist = norm(rel_pos, axis=1)
        v_rel = norm(rel_vel, axis=1)

        dmin_idx = np.argmin(dist)
        dmin = dist[dmin_idx]
        vmin = v_rel[dmin_idx]

        # Improved risk: considers both distance and velocity
        risk = min(1, (1000 / dmin) * np.exp(-vmin / 8))
        df_list.append({
            "Satellite1": selected_sat.name,
            "Satellite2": sat.name,
            "Min_Distance_km": round(dmin, 2),
            "Rel_Velocity_km/s": round(vmin, 2),
            "Risk_Score": round(risk, 3),
            "Risk_Level": "🟥 High" if risk > 0.7 else ("🟧 Moderate" if risk > 0.4 else "🟩 Low")
        })

    return pd.DataFrame(df_list)

# ----------------------------
# Main Interface
# ----------------------------
sat_name = st.selectbox("Select Satellite", [s.name for s in stations])
satellite = next(s for s in stations if s.name == sat_name)

tab1, tab2, tab3 = st.tabs(["📊 EDA Summary", "🌍 Orbit & Conjunctions", "💥 Collision Risk"])

# ----------------------------
# TAB 1: EDA
# ----------------------------
with tab1:
    df_meta, summary = eda_summary(stations)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Exploratory Data Analysis (EDA)")
    st.dataframe(df_meta, use_container_width=True)
    st.write(summary)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# TAB 2: Orbit & Conjunctions
# ----------------------------
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"Ground Track of {sat_name}")
    df_orbit = propagate_satellite(satellite)
    st.dataframe(df_orbit, use_container_width=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_orbit["Longitude"], df_orbit["Latitude"], marker="o", color="#FFD700")
    ax.set_xlabel("Longitude", color="white")
    ax.set_ylabel("Latitude", color="white")
    ax.set_title(f"Ground Track: {sat_name}", color="#FFD700")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_facecolor("#203a43")
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"Conjunction Detection (<500 km) for {sat_name}")
    df_conj = detect_conjunctions_for_sat(satellite, stations)

    if df_conj.empty:
        st.info("No conjunctions detected.")
    else:
        st.dataframe(df_conj, use_container_width=True)

        plt.figure(figsize=(10, 4))
        pairs = df_conj[["Satellite1", "Satellite2"]].apply(lambda x: f"{x[0]}-{x[1]}", axis=1)
        unique_pairs = pairs.unique()
        palette = sns.color_palette("husl", len(unique_pairs))
        color_map = dict(zip(unique_pairs, palette))

        for pair in unique_pairs:
            pair_data = df_conj[pairs == pair]
            plt.scatter(pair_data["Time"], pair_data["Distance_km"],
                        color=color_map[pair], s=50, label=pair)
        plt.axhline(y=500, color="red", linestyle="--", label="Threshold=500 km")
        plt.xlabel("Time (UTC)", color="white")
        plt.ylabel("Distance (km)", color="white")
        plt.title("Conjunction Timeline", color="#FFD700")
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize="small")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.gca().set_facecolor("#203a43")
        st.pyplot(plt.gcf())
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# TAB 3: Collision Risk
# ----------------------------
with tab3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"Collision Risk Assessment for {sat_name}")

    df_conj = detect_conjunctions_for_sat(satellite, stations)
    if df_conj.empty:
        st.info("No conjunctions detected — no collision risk computed.")
    else:
        sats_in_conj = df_conj["Satellite2"].unique()
        sats_conj_objs = [s for s in stations if s.name in sats_in_conj]

        df_risk = compute_risk_for_sat(satellite, sats_conj_objs)

        total_conj = len(df_conj)
        high_risk = (df_risk["Risk_Level"] == "🟥 High").sum()
        max_risk = df_risk["Risk_Score"].max()

        col1, col2, col3 = st.columns(3)
        col1.metric("🚀 Total Conjunctions", total_conj)
        col2.metric("⚠️ High-Risk Encounters", high_risk)
        col3.metric("🔥 Highest Risk Score", round(max_risk, 3))

        st.dataframe(df_risk, use_container_width=True)

                # --- Enhanced Readable Collision Risk Graph ---
        num_sats = len(df_risk)
        fig_height = max(6, num_sats * 0.6)
        fig, ax = plt.subplots(figsize=(14, fig_height))

        colors = df_risk["Risk_Level"].map({
            "🟥 High": "#ff4d4d",
            "🟧 Moderate": "#ffb347",
            "🟩 Low": "#90ee90"
        })

        bars = ax.barh(df_risk["Satellite2"], df_risk["Risk_Score"], color=colors)

        # Add text labels (risk values) next to bars
        for bar, risk in zip(bars, df_risk["Risk_Score"]):
            ax.text(
                bar.get_width() + 0.02,
                bar.get_y() + bar.get_height() / 2,
                f"{risk:.3f}",
                va="center",
                ha="left",
                fontsize=11,
                color="white",
                weight="bold"
            )

        # --- Style and layout for full clarity ---
        ax.set_xlabel("Risk Score (0–1)", fontsize=13, color="white", labelpad=10)
        ax.set_title(f"🛰️ Collision Risk Levels — {sat_name}", fontsize=15, color="#FFD700", pad=20)
        ax.set_xlim(0, 1.1)
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        ax.set_facecolor("#203a43")
        ax.tick_params(colors="white", labelsize=11)
        
        # ✅ Force all satellite names to show clearly
        ax.set_yticks(np.arange(num_sats))
        ax.set_yticklabels(df_risk["Satellite2"], fontsize=12, color="black", ha="right")
        plt.subplots_adjust(left=0.35, right=0.95, top=0.95, bottom=0.05)  # add margin for names
        
        # Legend
        legend_labels = ["🟥 High (>0.7)", "🟧 Moderate (0.4–0.7)", "🟩 Low (<0.4)"]
        legend_colors = ["#ff4d4d", "#ffb347", "#90ee90"]
        handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in legend_colors]
        ax.legend(
            handles,
            legend_labels,
            loc="lower right",
            facecolor="#203a43",
            edgecolor="none",
            fontsize=10,
            labelcolor="white"
        )

        st.pyplot(fig)
