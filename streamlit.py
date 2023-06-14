import streamlit as st

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp

df=pd.read_csv('df.csv')
df1=pd.read_csv('global-hunger-index.csv')
df2=pd.read_csv('cause_of_deaths.csv')
color_palette = ['#FBE9EB', '#F9C9D1', '#F79AB5', '#F56B99', '#F33D7E']
# Assuming your DataFrame is named 'df'
df['Average'] = df.Overweight + df.Underweight + df.Wasting + df.Stunting / 4

name3 = df.groupby("Country")["Average"].mean().sort_values(ascending=False).index[:10]
yax3 = df.groupby("Country")["Average"].mean().sort_values(ascending=False).round()[:10]

    
# Main section to show the effect on children
def show_effect_on_children():
    st.header("Effects")

    # Dropdown selectbox with different topics
    topic = st.selectbox("Select a topic", [
        "Underweight Percentage vs Country",
        "Stunting Percentage by Country",
        "Overweight Percentage vs Country",
        "Obesity Percentage by Country",
        "Trends of Stunting, Wasting, and Overweight"
    ])

    # Conditional statements to select the appropriate plot based on the topic
    if topic == "Underweight Percentage vs Country":
        plot_underweight_percentage()
    elif topic == "Stunting Percentage by Country":
        plot_stunting_percentage()
    elif topic == "Overweight Percentage vs Country":
        plot_overweight_percentage()
    elif topic == "Obesity Percentage by Country":
        plot_obesity_percentage()
    elif topic == "Trends of Stunting, Wasting, and Overweight":
        plot_trends()    

# Function to plot underweight percentage vs country
def plot_underweight_percentage():
    # Convert the "Underweight" column to numeric
    df['Underweight'] = pd.to_numeric(df['Underweight'], errors='coerce')

    # Define a custom sunset color palette
    custom_colors = ['#FFDDC1', '#FFB59F', '#FF8F7D', '#FF6A5B', '#FF4439']

    # Creating a scatter plot with improved readability and custom color palette
    fig = px.scatter(df, x='Country', y='Underweight',
                     size='Underweight', color='Underweight',
                     color_continuous_scale=custom_colors,
                     hover_data=['Country', 'Underweight'],
                     title="Underweight Percentage vs. Country")

    # Configuring the layout
    fig.update_layout(plot_bgcolor='white')

    # Displaying the plot
    st.plotly_chart(fig)
    
# Function to plot stunting percentage by country
def plot_stunting_percentage():
    # Convert 'Year' column to numeric type
    df['Year'] = pd.to_numeric(df['Year'])

    # Calculate the average stunting percentage by country
    stunting_avg = df.groupby("Country")["Stunting"].mean().reset_index()

    # Define a custom sunset color palette
    custom_colors = ['#FFDDC1', '#FFB59F', '#FF8F7D', '#FF6A5B', '#FF4439']

    # Create the choropleth map using plotly express
    fig = px.choropleth(stunting_avg, 
                        locations='Country',
                        locationmode='country names',
                        color='Stunting',
                        color_continuous_scale=custom_colors,
                        hover_name='Country',
                        title='Stunting Percentage by Country',
                        labels={'Stunting': 'Stunting %'},
                        projection='natural earth'
                        )

    # Configuring the layout
    fig.update_layout(geo=dict(showframe=False, showcoastlines=False))

    # Add interactivity
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Stunting: %{z}%")

    # Add a slider for filtering years
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    selected_year = st.slider('Select Year', min_value=min_year, max_value=max_year, value=min_year, step=1)

    # Filter the data based on the selected year
    filtered_df = df[df['Year'] == selected_year]

    # Update the choropleth map data
    fig.data[0].locations = filtered_df['Country']
    fig.data[0].z = filtered_df['Stunting']

    # Displaying the plot
    st.plotly_chart(fig)



# Function to plot overweight percentage vs country
def plot_overweight_percentage():
    # Define a custom sunset color palette
    custom_colors = ['#FFDDC1', '#FFB59F', '#FF8F7D', '#FF6A5B', '#FF4439']

    # Creating a scatter plot for Overweight vs. Country
    fig = px.scatter(df, x='Country', y='Overweight', hover_data=['Income Classification', 'Overweight'],
                     color='Overweight', color_continuous_scale=custom_colors,
                     labels={'Overweight': 'Overweight (%)'})

    # Configuring the layout
    fig.update_layout(
        title="Overweight Percentage vs. Country",
        xaxis_title="Country",
        yaxis_title="Overweight Percentage",
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white'
    )

    # Update marker properties
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='black')))

    # Displaying the plot
    st.plotly_chart(fig)

# Function to plot obesity percentage by country
def plot_obesity_percentage():
    # Calculate the average overweight percentage by country
    overweight_avg = df.groupby("Country")["Overweight"].mean().reset_index()

    # Define a custom sunset color palette
    custom_colors = ['#FFDDC1', '#FFB59F', '#FF8F7D', '#FF6A5B', '#FF4439']

    # Create the choropleth map using plotly.express
    fig = px.choropleth(
        overweight_avg,
        locations='Country',
        locationmode='country names',
        color='Overweight',
        color_continuous_scale=custom_colors,
        range_color=(0, 100),
        labels={'Overweight': 'Overweight Percentage'},
        title='Overweight Percentage by Country'
    )

    # Add a slider for filtering years
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    selected_years = st.slider('Select Years Range', min_value=min_year, max_value=max_year, value=(min_year, max_year), step=1)

    # Filter the data based on the selected years range
    filtered_df = df[df['Year'].between(selected_years[0], selected_years[1])]

    # Update the choropleth map data
    fig.data[0].locations = filtered_df['Country']
    fig.data[0].z = filtered_df['Overweight']

    # Displaying the plot
    st.plotly_chart(fig)

    # Configuring the layout
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='natural earth'
        )
    )

    # Displaying the plot
    st.plotly_chart(fig)
    
def plot_trends():
    # Compute average values across years
    avg_stunting = df.groupby('Year')['Stunting'].mean().reset_index()
    avg_wasting = df.groupby('Year')['Wasting'].mean().reset_index()
    avg_overweight = df.groupby('Year')['Overweight'].mean().reset_index()

    # Create subplots
    fig = sp.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    # Line graph for Stunting
    fig.add_trace(go.Scatter(x=avg_stunting['Year'], y=avg_stunting['Stunting'], name='Stunting',
                             line=dict(color='#FF4439')), row=1, col=1)

    # Line graph for Wasting
    fig.add_trace(go.Scatter(x=avg_wasting['Year'], y=avg_wasting['Wasting'], name='Wasting',
                             line=dict(color='#FF6A5B')), row=2, col=1)

    # Line graph for Overweight
    fig.add_trace(go.Scatter(x=avg_overweight['Year'], y=avg_overweight['Overweight'], name='Overweight',
                             line=dict(color='#FF8F7D')), row=3, col=1)

    # Update layout
    fig.update_layout(title='Average Trends of Stunting, Wasting, and Overweight',
                      xaxis=dict(title='Year'),
                      yaxis=dict(title='Percentage'),
                      height=800)

    # Displaying the plot
    st.plotly_chart(fig)    







#Overview Tab
# Define a custom color palette
def show_overview():
    # Header
        st.title('Malnutrition: A Global Problem')

        # Introduction
        st.markdown(
            """
            <div class="introduction">
            Malnutrition is a critical health issue affecting millions of people worldwide.
            It leads to stunting, underweight children, and even mortality. Addressing
            malnutrition is crucial to achieve the Sustainable Development Goal (SDG) of
            reducing hunger. This interactive application provides an overview of global
            malnutrition and its consequences.
            </div>
            """, unsafe_allow_html=True)

        # Image and additional image
        col1, col2 = st.columns(2)

        with col1:
            st.image('https://www.insightsonindia.com/wp-content/uploads/2023/01/malnu.png', caption='Malnutrition Types', width=600, output_format='PNG', use_column_width=False)

        with col2:
            st.image('https://prod-media-eng.dhakatribune.com/uploads/2020/12/webp-net-compress-image-1608023573686.jpg', caption='Child with Malnutrition', width=600, output_format='PNG', use_column_width=False)

        # Radio button to select the plot
        plot_option = st.radio("Select Plot", ("Countries with Highest Average Malnutrition", "Income vs. Weight"))
    
        if plot_option == "Countries with Highest Average Malnutrition":
            plot_highest_avg_malnutrition()
    
        elif plot_option == "Income vs. Weight":
            plot_income_vs_weight()
            

def plot_highest_avg_malnutrition():
    df['Average'] = df.Overweight + df.Underweight + df.Wasting + df.Stunting / 4

    # Assuming your DataFrame is named 'df'
    name3 = df.groupby("Country")["Average"].mean().sort_values(ascending=False).index[:10]
    yax3 = df.groupby("Country")["Average"].mean().sort_values(ascending=False).round()[:10]

    # Define a custom color palette
    custom_colors = ['#FFDDC1', '#FFB59F', '#FF8F7D', '#FF6A5B', '#FF4439']

    fig = px.bar(df, y=yax3, x=name3, color=name3, color_discrete_sequence=custom_colors)
    fig.update_layout(
        title="Top 10 Countries",
        xaxis_title="Country name",
        yaxis_title="Count"
    )
    fig.update_xaxes(tickangle=-45)

    # Displaying the plot
    st.plotly_chart(fig)
    
def plot_income_vs_weight():
    # Scatter plot for income vs. underweight with red color
    fig1 = px.scatter(df, x='Income Classification', y='Underweight', trendline='ols',
                      color_discrete_sequence=['red'])
    fig1.update_layout(
        title='Income vs. Underweight',
        xaxis_title='Income Classification',
        yaxis_title='Underweight'
    )

    # Scatter plot for income vs. overweight with red color
    fig2 = px.scatter(df, x='Income Classification', y='Overweight', trendline='ols',
                      color_discrete_sequence=['red'])
    fig2.update_layout(
        title='Income vs. Overweight',
        xaxis_title='Income Classification',
        yaxis_title='Overweight'
    )

    # Display the plots
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)    

            
            
# Define the show_hunger function
def show_hunger():
    # Add a dropdown menu for plot selection
    plot_selection = st.selectbox('Choose a plot', 
                                  ['GHI over Time', 'CHI by Country', 'Global Hunger Index (GHI) for Top 10 Countries'])
    
    # Call the respective plot function based on the selection
    if plot_selection == 'GHI over Time':
        plot_ghi_by_country()
    elif plot_selection == 'CHI by Country':
        plot_chi_over_time()
    elif plot_selection == 'Global Hunger Index (GHI) for Top 10 Countries':
        plot_ghi_top_10_countries()

# Plot 1: GHI by country
def plot_ghi_by_country():
    # Create a choropleth map for Global Hunger Index (GHI) by country
    # Calculate the average Global Hunger Index (GHI) by country
    avg_ghi = df1.groupby('Entity')['Global Hunger Index (2021)'].mean().reset_index()

    # Select the top 10 countries based on average GHI
    top_10_countries = avg_ghi.nlargest(10, 'Global Hunger Index (2021)')['Entity']

    # Add a multiple select box menu to choose countries
    selected_countries = st.multiselect('Select Countries', top_10_countries)

    # Filter the GHI data for the selected countries
    df_selected = df1[df1['Entity'].isin(selected_countries)]

    # Visualize Global Hunger Index (GHI) for the selected countries
    fig = px.line(df_selected, x='Year', y='Global Hunger Index (2021)', color='Entity')
    fig.update_layout(
        title='Global Hunger Index (GHI) Over Time',
        xaxis_title='Year',
        yaxis_title='GHI',
        legend_title='Country',
        height=1000,  # Adjust the height of the plot
        width=1000  # Adjust the width of the plot
    )

    # Display the plot
    st.plotly_chart(fig)


# Plot 2: CHI over time
def plot_chi_over_time():
    # Convert 'Year' column to numeric type
    df1['Year'] = pd.to_numeric(df1['Year'])

    # Add a slider for filtering years
    min_year = int(df1['Year'].min())
    max_year = 2006
    selected_year = st.slider('Select Year', min_value=min_year, max_value=max_year, value=min_year, step=1)

    # Filter the data based on the selected year
    filtered_df = df1[df1['Year'] == selected_year]

    # Create a choropleth map for Global Hunger Index (GHI) by country
    fig = px.choropleth(filtered_df, 
                         locations='Code',
                         color='Global Hunger Index (2021)',
                         color_continuous_scale=color_palette,
                         hover_name='Entity',
                         title='Global Hunger Index (GHI) by Country')
    fig.update_layout(height=1000, width=1000)  # Adjust the height and width of the plot

    # Display the map
    st.plotly_chart(fig)



# Plot 3: Global Hunger Index (GHI) for Top 10 Countries
def plot_ghi_top_10_countries():
    # Calculate the average Global Hunger Index (GHI) by country
    avg_ghi = df1.groupby('Entity')['Global Hunger Index (2021)'].mean().reset_index()

    # Select the top 10 countries based on average GHI
    top_10_countries = avg_ghi.nlargest(10, 'Global Hunger Index (2021)')['Entity']

    # Filter the GHI data for the top 10 countries
    df_top_10 = df1[df1['Entity'].isin(top_10_countries)]

    # Create the interactive bar chart with a slider
    fig3 = px.bar(df_top_10, x='Entity', y='Global Hunger Index (2021)', color='Entity',
                  color_discrete_sequence=color_palette,
                  title='Global Hunger Index (GHI) for Top 10 Countries',
                  labels={'Entity': 'Country', 'Global Hunger Index (2021)': 'GHI'},
                  animation_frame='Year', range_y=[0, df1['Global Hunger Index (2021)'].max()],
                  height=1000,  # Adjust the height of the plot
                  width=1000  # Adjust the width of the plot
    )
    fig3.update_layout(
        xaxis={'categoryorder': 'total descending'},
        yaxis={'title': 'GHI'},
        legend={'title': 'Country'},
        showlegend=False
    )

    # Display the bar chart
    st.plotly_chart(fig3)

# Call the hunger_section function
#show_hunger()


# Assuming your DataFrame is named 'df'
df['Average'] = df.Overweight + df.Underweight + df.Wasting + df.Stunting / 4

# Define a custom color palette
custom_colors = ['#FFDDC1', '#FFB59F', '#FF8F7D', '#FF6A5B', '#FF4439']


def create_choropleth_map(df, colorscale):
    fig = px.choropleth(df, 
                        locations='Country',
                        locationmode='country names',
                        color='Average',
                        color_continuous_scale=colorscale,
                        title='Global Average Overweight, Underweight, Wasting, and Stunting',
                        labels={'Average': 'Count'},
                        range_color=[df['Average'].min(), df['Average'].max()]
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        height=500,  # Adjust the height of the plot
        width=800  # Adjust the width of the plot
    )

    st.plotly_chart(fig)


def show_mortality():
    st.header("Mortality")
    # Radio box menu for plot selection
    plot_option = st.radio("Select a plot", ("Deaths Related to Malnutrition Features", "Malnutrition Total Number of Deaths"))

    if plot_option == "Deaths Related to Malnutrition Features":
        plot_deaths_related_to_malnutrition()
    elif plot_option == "Malnutrition Total Number of Deaths":
        plot_total_number_of_deaths()
        
        
def plot_deaths_related_to_malnutrition():
    # Select the relevant columns related to malnutrition
    malnutrition_features = df2[['Country/Territory', 'Year', 'Protein-Energy Malnutrition', 'Nutritional Deficiencies']]

    # Group the data by year and calculate the total deaths for each year
    total_deaths_by_year = malnutrition_features.groupby('Year').sum()

    # Create a stacked bar chart to visualize deaths related to malnutrition features
    fig = go.Figure()
    fig.add_trace(go.Bar(x=total_deaths_by_year.index, y=total_deaths_by_year['Protein-Energy Malnutrition'], name='Protein-Energy Malnutrition'))
    fig.add_trace(go.Bar(x=total_deaths_by_year.index, y=total_deaths_by_year['Nutritional Deficiencies'], name='Nutritional Deficiencies'))

    fig.update_layout(title='Deaths Related to Malnutrition Features',
                      xaxis_title='Year',
                      yaxis_title='Total Number of Deaths',
                      barmode='stack')

    # Display the plot
    st.plotly_chart(fig)
    
def plot_total_number_of_deaths():
    # Select the relevant columns related to malnutrition
    malnutrition_features = df2[['Country/Territory', 'Code', 'Protein-Energy Malnutrition', 'Nutritional Deficiencies']]

    # Calculate the total deaths for each country
    total_deaths_by_country = malnutrition_features.groupby(['Country/Territory', 'Code']).sum().reset_index()

    # Create a choropleth map to visualize malnutrition-related deaths
    fig = px.choropleth(total_deaths_by_country, 
                        locations='Code',
                        color='Protein-Energy Malnutrition',
                        hover_name='Country/Territory',
                        locationmode='ISO-3',
                        color_continuous_scale='purples',
                        title='Malnutrition-Related Deaths by Country')

    fig.update_layout(geo=dict(showframe=False, 
                               showcoastlines=False,
                               projection_type='equirectangular'),
                      coloraxis_colorbar=dict(title='Total Number of Deaths'))

    # Display the plot
    st.plotly_chart(fig)

             
        
        


def main():
    # Set page title and favicon
    st.set_page_config(page_title='Malnutrition App', page_icon=':apple:', layout='wide')

    # Set background color
    st.markdown("""
        <style>
        body {
            background-color: #F5F5F5;
            color: #333333;
            font-family: Arial, sans-serif;
        }

        .header {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        .section {
            margin-bottom: 40px;
            font-size: 18px;
        }

        .introduction {
            font-size: 24px;
            margin-bottom: 20px;
        }

        .custom-image {
            margin-bottom: 40px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Navigation bar
    section = st.sidebar.selectbox('Navigation', ('Overview', 'Effects', 'Hunger', 'Mortality'))

    if section == 'Overview':
        show_overview()
    elif section == 'Effects':
        show_effect_on_children()
    elif section == 'Hunger':
        show_hunger()
    elif section == 'Mortality':
        show_mortality()
 


if __name__ == '__main__':
    main()
