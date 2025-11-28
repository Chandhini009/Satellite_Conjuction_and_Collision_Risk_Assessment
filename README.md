# 🛰️ Satellite Conjunction & Collision Risk Assessment

An application built for Orbit Analysis using TLE Data

## 📌 Overview

This project is an interactive Streamlit-based web application that analyzes Earth-orbiting satellites using TLE (Two-Line Element) data.
It provides:

📊 Exploratory Data Analysis (EDA) of orbital parameters

🌍 Ground track visualization

🛰️ Conjunction detection (<500 km proximity)

💥 Collision risk scoring, based on distance + relative velocity

Built using Skyfield, NumPy, Pandas, and Matplotlib, the app is designed for real-time orbital safety analysis and space situational awareness (SSA).

## 🚀 Features
### 1. Satellite Metadata & EDA

Loads all active satellites from TLE file

Displays inclination, RAAN, eccentricity, mean motion

Summary statistics for quick insights

### 2. Orbit Propagation & Ground Track

Propagates orbits for 24 hours

Computes latitude–longitude ground trace

Visualizes trajectory on a global 2D plot

### 3. Conjunction Detection (<500 km)

Computes satellite–satellite distances

Identifies all close approaches

Provides timeline visualization using scatter plots

### 4. Collision Risk Estimation

#### Risk score considers:

Minimum distance

Relative velocity

Exponential decay model for realistic risk weighting

#### Displays:

High-risk encounters

Detailed risk table

Horizontal bar graph with color-coded risk levels

## 📂 Project Structure
📁 project/
│── app.py
│── requirements.txt
│── data/
│     └── satellites_active.tle
│── README.md  (this file)

## 🛠️ Technologies Used

Python 3.10+

Streamlit – UI framework

Skyfield – Orbit propagation + TLE handling

Pandas – Data processing

NumPy – Vector math

Matplotlib / Seaborn – Visualizations

## 📦 Installation
### 1️⃣ Clone the repository
git clone https://github.com/your-username/satellite-conjunction-analysis.git
cd satellite-conjunction-analysis

### 2️⃣ Install dependencies
pip install -r requirements.txt

### 3️⃣ Place TLE file

Add your TLE file here:

data/satellites_active.tle

### 4️⃣ Run the App
streamlit run app.py

## 📊 How Collision Risk is Calculated

#### For each satellite pair:

Orbit is propagated for 24 hours

Closest approach distance is found

Relative velocity at that point is computed

#### Risk score is assigned:

𝑅
𝑖
𝑠
𝑘
=

Risk=min(1,(1000/dmin)×e−(vrel/8))

### Risk levels:

🟥 High → >0.7

🟧 Moderate → 0.4–0.7

🟩 Low → <0.4

## 🎨 UI & Styling

Dark gradient space-themed background

Gold-colored headings

Card-style containers

Styled tables and plots

## 📈 Example Screenshots


## 📌 Future Enhancements

3D orbit visualization (Plotly)

Real-time TLE fetching from Celestrak

Monte-Carlo probability estimation

Satellite clustering & anomaly detection
