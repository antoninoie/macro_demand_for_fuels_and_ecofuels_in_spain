# ⛽ Macro Demand Forecast for Fuels and Eco-fuels in Spain

This Streamlit dashboard presents interactive *fuel consumption forecasts* across Spain's Autonomous Communities. Users can explore historical and forecasted demand, view the best-performing model per region/product, and analyze confidence intervals—all based on precomputed results.

🔗 *Live app*:  
[Click here to open the dashboard](https://macrodemandforfuelsandecofuelsinspain-dtmcxdfbb8dcjcdgqco4ab.streamlit.app/)

---

## 📊 Dashboard Features

- *Select region and fuel product* (e.g., Diesel A, Gasoline 95, HVO)
- Display of *best model and MAPE* for each combination
- *Time-series plot* of actual vs. predicted values with confidence bands
- *Historical and forecast data table* in tonnes

> Note: *HVO data is available only at the national level (España)*

---

## 📁 Repository Structure

├── app.py # Streamlit app logic
├── outputs/
│ ├── Data_w_Predictions.xlsx # Historical + forecast data
│ └── BestModels_MAPE.xlsx # Best model + MAPE per combination
├── requirements.txt # Python dependencies
└── README.md # This file
