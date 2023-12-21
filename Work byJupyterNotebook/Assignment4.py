#!/usr/bin/env python
# coding: utf-8

# # Assignment 4: Addressing Complexity
# ### Xinyi Li 23337042

# In[38]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# In[39]:


df=pd.read_csv('Global_Education.csv',encoding='ISO-8859-1')
df.head()


# In[40]:


print(df.dtypes)


# In[41]:


df.isnull().sum()


# In[42]:


df.describe()


# ### Global Education Analysis

# In[43]:


# Task 2.1: Gender inequality in education data
fig_preprimarygender_inequality = px.bar(df, x='Countries and areas',
                               y=['OOSR_Pre0Primary_Age_Male', 'OOSR_Pre0Primary_Age_Female'],
                               title='Out-of-School Rates by Gender (Pre-Primary Age)',
                               labels={'value': 'Rate', 'variable': 'Gender'})
fig_preprimarygender_inequality.update_traces(hoverinfo='all', hovertemplate="Country: %{x}<br>Rate: %{y}")

fig_primarygender_inequality = px.bar(df, x='Countries and areas',
                               y=['OOSR_Primary_Age_Male', 'OOSR_Primary_Age_Female'],
                               title='Out-of-School Rates by Gender (Primary Age)',
                               labels={'value': 'Rate', 'variable': 'Gender'})
fig_primarygender_inequality.update_traces(hoverinfo='all', hovertemplate="Country: %{x}<br>Rate: %{y}")

fig_lowersecgender_inequality = px.bar(df, x='Countries and areas',
                               y=['OOSR_Lower_Secondary_Age_Male', 'OOSR_Lower_Secondary_Age_Female'],
                               title='Out-of-School Rates by Gender (Lower_Secondary Age)',
                               labels={'value': 'Rate', 'variable': 'Gender'})
fig_lowersecgender_inequality.update_traces(hoverinfo='all', hovertemplate="Country: %{x}<br>Rate: %{y}")

fig_uppersecgender_inequality = px.bar(df, x='Countries and areas',
                               y=['OOSR_Upper_Secondary_Age_Male', 'OOSR_Upper_Secondary_Age_Female'],
                               title='Out-of-School Rates by Gender (Upper_Secondary Age)',
                               labels={'value': 'Rate', 'variable': 'Gender'})
fig_uppersecgender_inequality.update_traces(hoverinfo='all', hovertemplate="Country: %{x}<br>Rate: %{y}")

# Task 2.2: Relationship between primary education gross enrollment rate and birth rate
fig_birthrate_education = px.scatter(df, x='Countries and areas', y='Birth_Rate',
                                     size='Birth_Rate', color='Gross_Primary_Education_Enrollment',
                                     title='Relationship Between Birth Rate and Primary Education Enrollment',
                                     hover_name='Countries and areas')
fig_birthrate_education.update_layout(hovermode='closest')

fig_preprimarygender_inequality.show()
fig_primarygender_inequality.show()
fig_lowersecgender_inequality.show()
fig_uppersecgender_inequality.show()
fig_birthrate_education.show()


# In[44]:


#Task 2.3: Global or regional differences in education indicators
app = dash.Dash(__name__)

# layout
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='education-level-dropdown',
            options=[
                {'label': 'Primary Education Enrollment', 'value': 'Gross_Primary_Education_Enrollment'},
                {'label': 'Tertiary Education Enrollment', 'value': 'Gross_Tertiary_Education_Enrollment'}
            ],
            value='Gross_Primary_Education_Enrollment',
            placeholder="Select an education level",
            className='dropdown'
        ),
        dcc.Input(id='country-input', type='text', placeholder='Enter a country name', className='input'),
        html.Button('Submit', id='submit-button', n_clicks=0, className='button')
    ], className='control-panel'),
    dcc.Graph(id='education-global-graph'),
    html.Div(id='country-data-output', className='output')
], className='container')


@app.callback(
    [Output('education-global-graph', 'figure'),
     Output('country-data-output', 'children')],
    [Input('submit-button', 'n_clicks'),
     Input('education-level-dropdown', 'value')],
    [State('country-input', 'value')]
)
def update_graph_and_data(n_clicks, selected_education_level, country_value):
    # color channel
    color_range = [df[selected_education_level].min(), df[selected_education_level].max()]

    # show specific country
    filtered_df = df[df['Countries and areas'] == country_value] if country_value in df['Countries and areas'].values else df
    country_data_output = f"Data for {country_value}: \n{filtered_df.to_string(index=False)}" if country_value in df['Countries and areas'].values else "No data available or incorrect country name."

    # create map
    fig = px.choropleth(filtered_df, locations='Countries and areas', locationmode='country names',
                        color=selected_education_level, range_color=color_range,
                        title=f'Global {selected_education_level.replace("_", " ")} Rates')
    fig.update_geos(projection_type="natural earth", showcoastlines=True, coastlinecolor="RebeccaPurple")

    return fig, country_data_output

if __name__ == '__main__':
    app.run_server(debug=True)


# In[45]:


# Task 4: Analysis of the relationship between education indicators and economic development：The relationship between primary education gross enrollment rate and unemployment rate
fig_education_economy = px.scatter(df, x='Gross_Primary_Education_Enrollment', y='Unemployment_Rate',
                                   color='Countries and areas',
                                   hover_data=['Countries and areas', 'Gross_Primary_Education_Enrollment', 'Unemployment_Rate'],
                                   title='Relation between Primary Education Enrollment and Unemployment Rate')
fig_education_economy.show()


# In[47]:


# Task extra
# Create dashboards with scatter plots and bar charts
fig_dashboard = make_subplots(rows=1, cols=2, subplot_titles=('Literacy Rate vs Birth Rate', 'Primary Education Enrollment by Gender'))

# Scatter Plot: Literacy Rate vs. Birth Rate
fig_dashboard.add_trace(go.Scatter(x=df['Birth_Rate'], y=df['Youth_15_24_Literacy_Rate_Male'], mode='markers', name='Male Literacy Rate'),
                        row=1, col=1)
fig_dashboard.add_trace(go.Scatter(x=df['Birth_Rate'], y=df['Youth_15_24_Literacy_Rate_Female'], mode='markers', name='Female Literacy Rate'),
                        row=1, col=1)

# Bar chart: Primary education enrollment rates by country
fig_dashboard.add_trace(go.Bar(x=df['Countries and areas'], y=df['Gross_Primary_Education_Enrollment'], name='Primary Education Enrollment'),
                        row=1, col=2)

fig_dashboard.update_layout(title_text='Education and Population Indicators Dashboard')
fig_dashboard.show()


# In[ ]:




