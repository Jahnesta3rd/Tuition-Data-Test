import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load and clean the data
def load_data():
    df = pd.read_csv("tuition data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Tuition'] = df['Tuition'].replace('[\$,]', '', regex=True).astype(float)
    df = df.sort_values('Date')
    df['Daily Change'] = df['Tuition']
    return df

# Simulation function
def simulate_tuition_growth(df, start_date, num_days, target_tuition, num_simulations=10000):
    historical_changes = df[df['Date'] >= start_date]['Daily Change'].values

    if len(historical_changes) < 2:
        raise ValueError("Not enough data after the given start date.")

    mean_change = np.mean(historical_changes)
    std_change = np.std(historical_changes)

    results = []
    for _ in range(num_simulations):
        simulated_changes = np.random.normal(mean_change, std_change, num_days)
        cumulative_total = np.sum(simulated_changes)
        results.append(cumulative_total)

    results = np.array(results)
    probability = np.mean(results >= target_tuition)

    return results, probability

# Streamlit UI
st.title("Tuition Goal Probability Simulator")

# Inputs
start_date = st.date_input("Start Date", datetime(2023, 7, 3))
num_days = st.number_input("Number of Days", min_value=1, value=60)
target_tuition = st.number_input("Target Tuition (?)", min_value=0.0, value=10000000.0, step=100000.0)

# Run simulation on button click
if st.button("Run Simulation"):
    try:
        df = load_data()
        results, probability = simulate_tuition_growth(df, pd.to_datetime(start_date), num_days, target_tuition)

        # Show probability
        st.success(f"Estimated Probability: {probability * 100:.2f}%")

        # Plot histogram
        fig, ax = plt.subplots()
        ax.hist(results, bins=50, alpha=0.7)
        ax.axvline(target_tuition, color='red', linestyle='dashed', linewidth=2)
        ax.set_title("Simulated Tuition Outcomes")
        ax.set_xlabel("Total Tuition After {} Days".format(num_days))
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error: {e}")

