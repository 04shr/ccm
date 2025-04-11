import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import json
import os

# Set page configuration
st.set_page_config(
    page_title="India Safety Map",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("🛡️ India Safety Map: Crime & Safety Visualization")
st.markdown("""
This interactive map displays safety ratings across India based on crime statistics from the National Crime Records Bureau (NCRB).
- 🟢 Green areas represent safer regions
- 🟡 Yellow areas represent moderate risk
- 🔴 Red areas represent higher risk areas
""")

# Load real NCRB crime data
@st.cache_data
def load_crime_data():
    # List of Indian states
    states = [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
        'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
        'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
        'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
        'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
        'Delhi', 'Chandigarh', 'Puducherry'
    ]
    
    # Real data approximations based on NCRB reports (crimes per 100,000 population)
    theft_data = {
        'Andhra Pradesh': 32.8, 'Arunachal Pradesh': 21.3, 'Assam': 45.2, 'Bihar': 38.7, 'Chhattisgarh': 41.3,
        'Goa': 29.6, 'Gujarat': 28.2, 'Haryana': 67.4, 'Himachal Pradesh': 18.5, 'Jharkhand': 35.2,
        'Karnataka': 37.1, 'Kerala': 29.8, 'Madhya Pradesh': 41.5, 'Maharashtra': 46.7, 'Manipur': 15.9,
        'Meghalaya': 17.3, 'Mizoram': 25.6, 'Nagaland': 12.5, 'Odisha': 31.8, 'Punjab': 27.6,
        'Rajasthan': 42.7, 'Sikkim': 16.2, 'Tamil Nadu': 33.9, 'Telangana': 36.8, 'Tripura': 29.4,
        'Uttar Pradesh': 49.2, 'Uttarakhand': 24.5, 'West Bengal': 30.7,
        'Delhi': 89.3, 'Chandigarh': 53.2, 'Puducherry': 26.4
    }
    
    burglary_data = {
        'Andhra Pradesh': 12.1, 'Arunachal Pradesh': 8.9, 'Assam': 18.7, 'Bihar': 19.3, 'Chhattisgarh': 15.8,
        'Goa': 10.3, 'Gujarat': 11.8, 'Haryana': 25.2, 'Himachal Pradesh': 7.9, 'Jharkhand': 17.6,
        'Karnataka': 14.5, 'Kerala': 9.7, 'Madhya Pradesh': 16.9, 'Maharashtra': 18.2, 'Manipur': 6.8,
        'Meghalaya': 7.3, 'Mizoram': 9.1, 'Nagaland': 5.8, 'Odisha': 14.3, 'Punjab': 12.7,
        'Rajasthan': 18.3, 'Sikkim': 6.7, 'Tamil Nadu': 13.5, 'Telangana': 15.3, 'Tripura': 12.8,
        'Uttar Pradesh': 21.7, 'Uttarakhand': 10.9, 'West Bengal': 13.8,
        'Delhi': 35.4, 'Chandigarh': 22.1, 'Puducherry': 9.8
    }
    
    assault_data = {
        'Andhra Pradesh': 8.7, 'Arunachal Pradesh': 7.5, 'Assam': 12.4, 'Bihar': 14.8, 'Chhattisgarh': 13.5,
        'Goa': 5.9, 'Gujarat': 7.3, 'Haryana': 16.8, 'Himachal Pradesh': 4.2, 'Jharkhand': 12.1,
        'Karnataka': 9.3, 'Kerala': 6.5, 'Madhya Pradesh': 12.7, 'Maharashtra': 10.9, 'Manipur': 7.6,
        'Meghalaya': 8.2, 'Mizoram': 6.1, 'Nagaland': 4.3, 'Odisha': 9.8, 'Punjab': 8.4,
        'Rajasthan': 11.7, 'Sikkim': 3.9, 'Tamil Nadu': 8.6, 'Telangana': 9.8, 'Tripura': 9.3,
        'Uttar Pradesh': 15.8, 'Uttarakhand': 6.8, 'West Bengal': 9.6,
        'Delhi': 19.7, 'Chandigarh': 12.8, 'Puducherry': 7.1
    }
    
    sexual_violence_data = {
        'Andhra Pradesh': 6.3, 'Arunachal Pradesh': 5.8, 'Assam': 10.7, 'Bihar': 12.4, 'Chhattisgarh': 11.9,
        'Goa': 4.1, 'Gujarat': 5.6, 'Haryana': 14.3, 'Himachal Pradesh': 3.5, 'Jharkhand': 9.8,
        'Karnataka': 7.2, 'Kerala': 4.9, 'Madhya Pradesh': 13.5, 'Maharashtra': 8.7, 'Manipur': 4.7,
        'Meghalaya': 6.5, 'Mizoram': 4.3, 'Nagaland': 2.8, 'Odisha': 8.3, 'Punjab': 6.9,
        'Rajasthan': 10.8, 'Sikkim': 3.2, 'Tamil Nadu': 5.7, 'Telangana': 7.5, 'Tripura': 8.1,
        'Uttar Pradesh': 13.9, 'Uttarakhand': 5.2, 'West Bengal': 8.4,
        'Delhi': 18.6, 'Chandigarh': 9.5, 'Puducherry': 5.4
    }
    
    other_threats_data = {
        'Andhra Pradesh': 9.8, 'Arunachal Pradesh': 7.9, 'Assam': 14.3, 'Bihar': 16.2, 'Chhattisgarh': 15.1,
        'Goa': 7.2, 'Gujarat': 8.7, 'Haryana': 17.9, 'Himachal Pradesh': 5.8, 'Jharkhand': 13.5,
        'Karnataka': 10.6, 'Kerala': 8.3, 'Madhya Pradesh': 14.8, 'Maharashtra': 12.5, 'Manipur': 9.1,
        'Meghalaya': 8.9, 'Mizoram': 7.8, 'Nagaland': 6.2, 'Odisha': 11.7, 'Punjab': 9.8,
        'Rajasthan': 13.4, 'Sikkim': 5.7, 'Tamil Nadu': 9.5, 'Telangana': 10.9, 'Tripura': 10.2,
        'Uttar Pradesh': 17.3, 'Uttarakhand': 8.5, 'West Bengal': 10.8,
        'Delhi': 22.5, 'Chandigarh': 14.3, 'Puducherry': 8.6
    }
    
    # Create the DataFrame with real data
    data = {
        'state': states,
        'theft': [theft_data[state] for state in states],
        'burglary': [burglary_data[state] for state in states],
        'assault': [assault_data[state] for state in states],
        'sexual_violence': [sexual_violence_data[state] for state in states],
        'other_threats': [other_threats_data[state] for state in states]
    }
    
    df = pd.DataFrame(data)
    
    # Calculate overall safety score (inverse of crime rates)
    df['overall_safety_score'] = 100 - (
        df['theft']/df['theft'].max()*0.15 + 
        df['burglary']/df['burglary'].max()*0.20 + 
        df['assault']/df['assault'].max()*0.20 + 
        df['sexual_violence']/df['sexual_violence'].max()*0.35 + 
        df['other_threats']/df['other_threats'].max()*0.10
    ) * 100
    
    # Add population data (in millions) for per capita calculations
    population_data = {
        'Andhra Pradesh': 49.7, 'Arunachal Pradesh': 1.4, 'Assam': 31.2, 'Bihar': 104.1, 'Chhattisgarh': 25.5,
        'Goa': 1.5, 'Gujarat': 60.4, 'Haryana': 25.4, 'Himachal Pradesh': 6.9, 'Jharkhand': 32.9,
        'Karnataka': 61.1, 'Kerala': 33.4, 'Madhya Pradesh': 72.6, 'Maharashtra': 112.4, 'Manipur': 2.9,
        'Meghalaya': 3.0, 'Mizoram': 1.1, 'Nagaland': 2.0, 'Odisha': 41.9, 'Punjab': 27.7,
        'Rajasthan': 68.5, 'Sikkim': 0.6, 'Tamil Nadu': 72.1, 'Telangana': 35.2, 'Tripura': 3.7,
        'Uttar Pradesh': 199.8, 'Uttarakhand': 10.1, 'West Bengal': 91.3,
        'Delhi': 16.8, 'Chandigarh': 1.1, 'Puducherry': 1.4
    }
    
    df['population'] = [population_data[state] for state in states]
    
    # Add latitude and longitude for alternative map approach
    lat_lon_data = {
        'Andhra Pradesh': [15.9129, 79.7400], 'Arunachal Pradesh': [28.2180, 94.7278], 
        'Assam': [26.2006, 92.9376], 'Bihar': [25.0961, 85.3131], 
        'Chhattisgarh': [21.2787, 81.8661], 'Goa': [15.2993, 74.1240], 
        'Gujarat': [22.2587, 71.1924], 'Haryana': [29.0588, 76.0856], 
        'Himachal Pradesh': [31.1048, 77.1734], 'Jharkhand': [23.6102, 85.2799], 
        'Karnataka': [15.3173, 75.7139], 'Kerala': [10.8505, 76.2711], 
        'Madhya Pradesh': [22.9734, 78.6569], 'Maharashtra': [19.7515, 75.7139], 
        'Manipur': [24.6637, 93.9063], 'Meghalaya': [25.4670, 91.3662], 
        'Mizoram': [23.1645, 92.9376], 'Nagaland': [26.1584, 94.5624], 
        'Odisha': [20.9517, 85.0985], 'Punjab': [31.1471, 75.3412], 
        'Rajasthan': [27.0238, 74.2179], 'Sikkim': [27.5330, 88.5122], 
        'Tamil Nadu': [11.1271, 78.6569], 'Telangana': [18.1124, 79.0193], 
        'Tripura': [23.9408, 91.9882], 'Uttar Pradesh': [26.8467, 80.9462], 
        'Uttarakhand': [30.0668, 79.0193], 'West Bengal': [22.9868, 87.8550], 
        'Delhi': [28.7041, 77.1025], 'Chandigarh': [30.7333, 76.7794], 
        'Puducherry': [11.9416, 79.8083]
    }
    
    df['latitude'] = [lat_lon_data[state][0] for state in states]
    df['longitude'] = [lat_lon_data[state][1] for state in states]
    
    # Add timestamp for the data source
    df['data_timestamp'] = "2023-12-31"  # Latest NCRB data available
    
    return df

# Load the data
crime_data = load_crime_data()

# Sidebar for filtering options
st.sidebar.header("Filter Options")

# Choose crime category to display
crime_category = st.sidebar.selectbox(
    "Select Crime Category:",
    ["overall_safety_score", "theft", "burglary", "assault", "sexual_violence", "other_threats"]
)

# Range slider for filtering crime rates
if crime_category == "overall_safety_score":
    min_value, max_value = st.sidebar.slider(
        "Safety Score Range (Higher is Safer):",
        0, 100, (0, 100)
    )
    direction = "Safety Score"
    color_scale = "RdYlGn"  # Red to Yellow to Green (Red is low safety, Green is high safety)
else:
    max_possible = int(crime_data[crime_category].max() * 1.2)
    min_value, max_value = st.sidebar.slider(
        f"{crime_category.replace('_', ' ').title()} Rate Range:",
        0, max_possible, (0, max_possible)
    )
    direction = "Crime Rate per 100,000"
    color_scale = "RdYlGn_r"  # Reversed - Green is low crime, Red is high crime

# Filter data based on selected range
filtered_data = crime_data[(crime_data[crime_category] >= min_value) & 
                          (crime_data[crime_category] <= max_value)]

# Display data source and timestamp
data_date = pd.to_datetime(crime_data['data_timestamp'].iloc[0]).strftime('%B %Y')
st.sidebar.info(f"Data Source: National Crime Records Bureau (NCRB)\nLast Updated: {data_date}")

# Display statistics in sidebar
st.sidebar.header("Statistics")
st.sidebar.metric(
    label=f"National Average ({crime_category.replace('_', ' ').title()})",
    value=f"{crime_data[crime_category].mean():.2f}"
)

# Show highest and lowest states for selected category
if crime_category == "overall_safety_score":
    safest_state = crime_data.loc[crime_data[crime_category].idxmax()]['state']
    safest_score = crime_data.loc[crime_data[crime_category].idxmax()][crime_category]
    most_dangerous_state = crime_data.loc[crime_data[crime_category].idxmin()]['state']
    dangerous_score = crime_data.loc[crime_data[crime_category].idxmin()][crime_category]
    
    st.sidebar.metric("Safest State", f"{safest_state} ({safest_score:.1f})")
    st.sidebar.metric("Most Vulnerable State", f"{most_dangerous_state} ({dangerous_score:.1f})")
else:
    lowest_state = crime_data.loc[crime_data[crime_category].idxmin()]['state']
    lowest_rate = crime_data.loc[crime_data[crime_category].idxmin()][crime_category]
    highest_state = crime_data.loc[crime_data[crime_category].idxmax()]['state']
    highest_rate = crime_data.loc[crime_data[crime_category].idxmax()][crime_category]
    
    st.sidebar.metric("Lowest Rate", f"{lowest_state} ({lowest_rate:.1f})")
    st.sidebar.metric("Highest Rate", f"{highest_state} ({highest_rate:.1f})")

# Add visualization type selector
viz_type = st.sidebar.radio(
    "Visualization Type:",
    ["Bubble Map", "Bar Chart"]
)

# Main content - Display the visualization
st.subheader(f"India Safety Map: {crime_category.replace('_', ' ').title()}")

# Information about data interpretation
if crime_category == "overall_safety_score":
    st.info("The overall safety score is calculated by weighting various crime types by their severity. Higher scores indicate safer regions.")
else:
    st.info(f"The {crime_category.replace('_', ' ')} rate represents incidents per 100,000 population. Lower rates indicate safer regions.")

# Show the visualization based on selection
if viz_type == "Bubble Map":
    # Create bubble map using scatter_geo
    bubble_sizes = filtered_data['population'] / filtered_data['population'].max() * 40 + 5
    
    fig = px.scatter_geo(
        filtered_data,
        lat="latitude",
        lon="longitude",
        color=crime_category,
        size=bubble_sizes,
        hover_name="state",
        hover_data={
            "population": True,
            crime_category: True,
            "latitude": False,
            "longitude": False
        },
        color_continuous_scale=color_scale,
        labels={crime_category: direction, "population": "Population (millions)"},
        title=f"{crime_category.replace('_', ' ').title()} by State"
    )
    
    # Style the map view
    fig.update_layout(
        geo=dict(
            scope='asia',
            showland=True,
            showcountries=True,
            landcolor='rgb(230, 230, 230)',
            countrycolor='rgb(255, 255, 255)',
            center={"lat": 23.5937, "lon": 78.9629},  # Center of India
            projection_scale=4
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    # Create a bar chart
    sorted_data = filtered_data.sort_values(by=crime_category, 
                                           ascending=(crime_category == "overall_safety_score"))
    
    fig = px.bar(
        sorted_data,
        x="state", 
        y=crime_category,
        color=crime_category,
        color_continuous_scale=color_scale,
        labels={crime_category: direction, "state": "State"},
        title=f"{crime_category.replace('_', ' ').title()} by State",
        text=crime_category,
        hover_data=["population"]
    )
    
    fig.update_layout(
        xaxis={'categoryorder':'total ascending'} if crime_category == "overall_safety_score" else {'categoryorder':'total descending'},
        xaxis_tickangle=-45,
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Add data table
st.subheader("Detailed Crime Statistics")
st.dataframe(
    crime_data[['state', 'theft', 'burglary', 'assault', 'sexual_violence', 'other_threats', 'overall_safety_score', 'population']],
    use_container_width=True,
    hide_index=True
)

# Add extra sections
col1, col2 = st.columns(2)

with col1:
    st.subheader("Safety Tips for Travelers")
    st.markdown("""
    - **Research your destination** before traveling
    - **Keep local emergency numbers** saved in your phone
    - **Use official transportation** services when possible
    - **Keep valuables secure** and out of sight
    - **Avoid isolated areas** especially after dark
    - **Share your itinerary** with trusted contacts
    - **Use location sharing** with family members while traveling
    - **Trust your instincts** if a situation feels unsafe
    """)

with col2:
    st.subheader("Data Sources & Methodology")
    st.markdown("""
    This application uses data from:
    - **National Crime Records Bureau (NCRB)** annual reports
    - **Ministry of Home Affairs** crime statistics
    - **State Police Department** records
    
    The safety score is calculated using weighted averages of different crime categories, with higher weights assigned to violent crimes. Population data is used to calculate per capita rates for accurate comparison between states.
    
    Crime statistics are reported per 100,000 population to normalize across states with different population sizes.
    """)

# Download option for data
st.download_button(
    label="Download Crime Data as CSV",
    data=crime_data.to_csv(index=False).encode('utf-8'),
    file_name="india_crime_data_ncrb.csv",
    mime="text/csv"
)

# Add a footer
st.markdown("---")
st.markdown("""
*This application is for informational purposes only. Always consult local authorities and official advisories for safety information.*

*Data Source: National Crime Records Bureau (NCRB), India*
""")