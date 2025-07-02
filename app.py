import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_predictions():
    df_pred = pd.read_excel('outputs/Data_w_Predictions.xlsx')
    df_pred['period'] = pd.to_datetime(df_pred['period'], dayfirst=True)
    return df_pred

@st.cache_data
def load_best_models():
    df_models = pd.read_excel('outputs/BestModels_MAPE.xlsx')
    return df_models

df_pred = load_predictions()
df_models = load_best_models()

st.title('Macro Demand for Fuels & Eco-fuels in Spain')

st.header("Consumption Predictions")

regions_pred = sorted(df_pred['CCAA'].unique())
products_all = sorted(df_pred['Product'].unique())

selected_region_pred = st.selectbox('Select Autonomous Community for Prediction', regions_pred, key='region_pred')

if selected_region_pred == "España":
    products_pred = products_all
else:
    products_pred = [p for p in products_all if p != "HVO"]

selected_product_pred = st.selectbox('Select Product for Prediction', products_pred, key='prod_pred')

st.subheader(f"Best Model and MAPE for {selected_product_pred} in {selected_region_pred}")
df_models_filtered = df_models[
    (df_models['CCAA'].str.contains(selected_region_pred, case=False, na=False)) &
    (df_models['Product'].str.contains(selected_product_pred, case=False, na=False))
]
st.dataframe(df_models_filtered[['Product', 'MAPE', 'Model']].reset_index(drop=True))

df_pred_filtered = df_pred[(df_pred['CCAA'] == selected_region_pred) & (df_pred['Product'] == selected_product_pred)].copy()
df_pred_filtered = df_pred_filtered.sort_values('period')
df_pred_filtered.set_index('period', inplace=True)

st.write(f"Historical Data and Predictions for {selected_product_pred} in {selected_region_pred}")
st.dataframe(df_pred_filtered[['Tonnes', 'LOWER', 'UPPER', 'Average']])

fig_pred = go.Figure()

df_pred_filtered.reset_index(inplace=True)

if selected_product_pred == "HVO" and selected_region_pred == "España":

    fig_pred.add_trace(go.Scatter(
        x=df_pred_filtered['period'].loc[df_pred_filtered['Average'] == 0],
        y=df_pred_filtered['Tonnes'].loc[df_pred_filtered['Average'] == 0],
        mode='lines+markers',
        name='Tonnes',
        line=dict(color='blue')
    ))

    fig_pred.add_trace(go.Scatter(
        x=df_pred_filtered['period'].loc[df_pred_filtered['Average'] != 0],
        y=df_pred_filtered['Tonnes'].loc[df_pred_filtered['Average'] != 0],
        mode='lines+markers',
        name='Predicted Tonnes',
        line=dict(color='green')
    ))

    fig_pred.add_trace(go.Scatter(
        x=df_pred_filtered['period'].loc[df_pred_filtered['Average'] != 0],
        y=df_pred_filtered['Average'].loc[df_pred_filtered['Average'] != 0],
        mode='lines+markers',
        name='Average',
        line=dict(color='orange')
    ))

else:
    fig_pred.add_trace(go.Scatter(
        x=df_pred_filtered['period'].loc[df_pred_filtered['Average'] == 0],
        y=df_pred_filtered['Tonnes'].loc[df_pred_filtered['Average'] == 0],
        mode='lines+markers',
        name='Actual Tonnes',
        line=dict(color='blue')
    ))

    fig_pred.add_trace(go.Scatter(
        x=df_pred_filtered['period'].loc[df_pred_filtered['Average'] != 0],
        y=df_pred_filtered['Tonnes'].loc[df_pred_filtered['Average'] != 0],
        mode='lines+markers',
        name='Predicted Tonnes',
        line=dict(color='green')
    ))

    fig_pred.add_trace(go.Scatter(
        x=df_pred_filtered['period'].loc[df_pred_filtered['Average'] != 0],
        y=df_pred_filtered['Average'].loc[df_pred_filtered['Average'] != 0],
        mode='lines+markers',
        name='Average',
        line=dict(color='orange')
    ))

    fig_pred.add_trace(go.Scatter(
        x=pd.Series(list(df_pred_filtered['period'].loc[df_pred_filtered['Average'] != 0].to_list()) + list(df_pred_filtered['period'].loc[df_pred_filtered['Average'] != 0].to_list()[::-1])),
        y=pd.concat([df_pred_filtered['UPPER'].loc[df_pred_filtered['Average'] != 0], df_pred_filtered['LOWER'].loc[df_pred_filtered['Average'] != 0][::-1]]),
        fill='toself',
        fillcolor='rgba(255,165,0,0.2)',
        line=dict(color='rgba(255,165,0,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Confidence Interval'
    ))

min_tonnes = df_pred_filtered['Tonnes'][df_pred_filtered['Tonnes'] > 0].min()
min_average = df_pred_filtered['Average'][df_pred_filtered['Average'] > 0].min() if any(df_pred_filtered['Average'] > 0) else min_tonnes
y_min = min(min_tonnes, min_average) * 0.95

fig_pred.update_layout(
    title='Actual Consumption and Prediction with Intervals',
    xaxis_title='Date',
    yaxis_title='Tonnes',
    yaxis=dict(range=[y_min, df_pred_filtered[['Tonnes', 'UPPER']].max().max() * 1.05]),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

st.plotly_chart(fig_pred, use_container_width=True)