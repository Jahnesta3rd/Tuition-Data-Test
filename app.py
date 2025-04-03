import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# Monte Carlo multi-year projection app
st.title("Multi-Year Monte Carlo Financial Projection")

# User Inputs
initial_revenue = st.number_input("Initial Monthly Revenue (?)", value=1_000_000.0, step=100_000.0)
initial_expenses = st.number_input("Initial Monthly Expenses (?)", value=600_000.0, step=100_000.0)
n_years = st.slider("Projection Period (Years)", 1, 10, 5)
n_simulations = st.slider("Number of Simulations", 1000, 10000, 5000, step=1000)

# Growth assumptions
mean_rev_growth = st.number_input("Avg Monthly Revenue Growth (%)", value=2.0) / 100
std_rev_growth = st.number_input("Std Dev of Revenue Growth (%)", value=1.0) / 100

mean_exp_growth = st.number_input("Avg Monthly Expense Growth (%)", value=1.5) / 100
std_exp_growth = st.number_input("Std Dev of Expense Growth (%)", value=0.7) / 100

# Run simulation
months = n_years * 12
simulated_results = []

for i in range(n_simulations):
    revenue = initial_revenue
    expenses = initial_expenses
    net_income_stream = []

    for _ in range(months):
        rev_growth = np.random.normal(mean_rev_growth, std_rev_growth)
        exp_growth = np.random.normal(mean_exp_growth, std_exp_growth)

        revenue *= (1 + rev_growth)
        expenses *= (1 + exp_growth)

        net_income = revenue - expenses
        net_income_stream.append(net_income)

    simulated_results.append(net_income_stream)

# Convert to array and compute cumulative income
simulated_results = np.array(simulated_results)
cumulative_income = np.cumsum(simulated_results, axis=1)

# Visualization: Sample paths
st.subheader("Sample Cumulative Net Income Paths")
fig, ax = plt.subplots()
for i in range(min(100, n_simulations)):
    ax.plot(cumulative_income[i], alpha=0.1)
ax.set_title("Monte Carlo Net Income Forecast")
ax.set_xlabel("Month")
ax.set_ylabel("Cumulative Net Income")
st.pyplot(fig)

# Summary Stats
st.subheader("Summary Statistics")
final_values = cumulative_income[:, -1]
percentiles = np.percentile(final_values, [5, 50, 95])
st.write(f"5th Percentile: ?{percentiles[0]:,.0f}")
st.write(f"Median (50th): ?{percentiles[1]:,.0f}")
st.write(f"95th Percentile: ?{percentiles[2]:,.0f}")

# Histogram
st.subheader("Distribution of Final Net Income")
fig2, ax2 = plt.subplots()
ax2.hist(final_values, bins=50, alpha=0.7)
ax2.axvline(percentiles[1], color='red', linestyle='dashed', label='Median')
ax2.set_title("Distribution of Net Income After {} Years".format(n_years))
ax2.set_xlabel("Net Income")
ax2.set_ylabel("Frequency")
ax2.legend()
st.pyplot(fig2)

# Download Button for Raw Results
st.subheader("Download Simulation Results")
df_download = pd.DataFrame(cumulative_income)
buffer = io.BytesIO()
df_download.to_csv(buffer, index=False)
buffer.seek(0)
st.download_button(
    label="Download Cumulative Income CSV",
    data=buffer,
    file_name="monte_carlo_projection.csv",
    mime="text/csv"
)

st.info("To deploy this app, upload it along with a requirements.txt to Streamlit Cloud.")
