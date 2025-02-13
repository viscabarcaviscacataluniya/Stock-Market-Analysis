#!/usr/bin/env python
# coding: utf-8

# import pandas as pd
# 
# data = pd.read_csv("nifty50_closing_prices.csv")
# 
# print(data.head())

# In[2]:


data['Date'] = pd.to_datetime(data['Date'])


# # Feature Engineering

# In[4]:


print(data.isnull().sum())


# In[5]:


data.fillna(method='ffill', inplace=True)


# # Data Visualization

# In[6]:


import plotly.graph_objs as go
import plotly.express as px

fig = go.Figure()

for company in data.columns[1:]:
    fig.add_trace(go.Scatter(x=data['Date'], y=data[company],
                             mode='lines',
                             name=company,
                             opacity=0.5))

fig.update_layout(
    title='Stock Price Trends of All Indian Companies',
    xaxis_title='Date',
    yaxis_title='Closing Price (INR)',
    xaxis=dict(tickangle=45), 
    legend=dict(
        x=1.05,
        y=1,
        traceorder="normal",
        font=dict(size=10),
        orientation="v"
    ),
    margin=dict(l=0, r=0, t=30, b=0),  
    hovermode='x',
    template='plotly_white'
)

fig.show()


# In[7]:


all_companies = data.columns[1:]

volatility_all_companies = data[all_companies].std()

volatility_all_companies.sort_values(ascending=False).head(10)


# In[8]:


growth_all_companies = data[all_companies].pct_change() * 100

average_growth_all_companies = growth_all_companies.mean()

average_growth_all_companies.sort_values(ascending=False).head(10)


# In[9]:


initial_prices_all = data[all_companies].iloc[0]
final_prices_all = data[all_companies].iloc[-1]

roi_all_companies = ((final_prices_all - initial_prices_all) / initial_prices_all) * 100

roi_all_companies.sort_values(ascending=False).head(10)


# # Creating a Mutual Fund Plan Based on High ROI and Low Risk

# In[11]:


roi_threshold = roi_all_companies.median()
volatility_threshold = volatility_all_companies.median()

selected_companies = roi_all_companies[(roi_all_companies > roi_threshold) & (volatility_all_companies < volatility_threshold)]

selected_companies.sort_values(ascending=False)


# In[12]:


selected_volatility = volatility_all_companies[selected_companies.index]
inverse_volatility = 1 / selected_volatility

investment_ratios = inverse_volatility / inverse_volatility.sum()

investment_ratios.sort_values(ascending=False)


# # Analyzing Our Mutual Fund Plan

# In[13]:


top_growth_companies = average_growth_all_companies.sort_values(ascending=False).head(10)
risk_growth_rate_companies = volatility_all_companies[top_growth_companies.index]
risk_mutual_fund_companies = volatility_all_companies[selected_companies.index]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=risk_mutual_fund_companies.index,
    x=risk_mutual_fund_companies,
    orientation='h',  # Horizontal bar
    name='Mutual Fund Companies',
    marker=dict(color='blue')
))

fig.add_trace(go.Bar(
    y=risk_growth_rate_companies.index,
    x=risk_growth_rate_companies,
    orientation='h',  
    name='Growth Rate Companies',
    marker=dict(color='green'),
    opacity=0.7
))

fig.update_layout(
    title='Risk Comparison: Mutual Fund vs Growth Rate Companies',
    xaxis_title='Volatility (Standard Deviation)',
    yaxis_title='Companies',
    barmode='overlay',  
    legend=dict(title='Company Type'),
    template='plotly_white'
)

fig.show()


# In[14]:


expected_roi_mutual_fund = roi_all_companies[selected_companies.index]

expected_roi_growth_companies = roi_all_companies[top_growth_companies.index]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=expected_roi_mutual_fund.index,
    x=expected_roi_mutual_fund,
    orientation='h',  
    name='Mutual Fund Companies',
    marker=dict(color='blue')
))

fig.add_trace(go.Bar(
    y=expected_roi_growth_companies.index,
    x=expected_roi_growth_companies,
    orientation='h',  
    name='Growth Rate Companies',
    marker=dict(color='green'),
    opacity=0.7
))

fig.update_layout(
    title='Expected ROI Comparison: Mutual Fund vs Growth Rate Companies',
    xaxis_title='Expected ROI (%)',
    yaxis_title='Companies',
    barmode='overlay',  
    legend=dict(title='Company Type'),
    template='plotly_white'
)

fig.show()


# # Calculating Expected Returns

# In[15]:


import numpy as np

monthly_investment = 5000  # Monthly investment in INR
years = [1, 3, 5, 10]  # Investment periods (in years)
n = 12  # Number of times interest is compounded per year (monthly)

avg_roi = expected_roi_mutual_fund.mean() / 100  # Convert to decimal

def future_value(P, r, n, t):
    return P * (((1 + r/n)**(n*t) - 1) / (r/n)) * (1 + r/n)

future_values = [future_value(monthly_investment, avg_roi, n, t) for t in years]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[str(year) + " year" for year in years],
    y=future_values,
    mode='lines+markers',
    line=dict(color='blue'),
    marker=dict(size=8),
    name='Future Value'
))

fig.update_layout(
    title="Expected Value of Investments of ₹ 5000 Per Month (Mutual Funds)",
    xaxis_title="Investment Period",
    yaxis_title="Future Value (INR)",
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey'),
    template="plotly_white",
    hovermode='x'
)

fig.show()


# In[ ]:




