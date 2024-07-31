import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth


# Function to check the login credentials
def check_login(username, password):
    return username == "admin" and password == "admin"

# Function to display the login form
def display_login_form():
    st.session_state['authenticated'] = False
    with st.container():
        st.image('audi_logo.png', use_column_width=True)  # Display the Audi logo
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            st.session_state['authenticated'] = check_login(username, password)
            if not st.session_state['authenticated']:
                st.error("Invalid username or password")

# Main app
def main_app():
    # Your existing Streamlit app code goes here
    st.title('Audi Consumer Data')
    # ... rest of your code ...

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Run the app
if st.session_state['authenticated']:
    main_app()
else:
    display_login_form()


# Assuming 'Audi.csv' is in the same directory as the Streamlit script
# Load the dataset
data = pd.read_csv('Audi.csv')

# Function to filter data
def filter_data(data, model, fuel_type, transmission, year):
    if model != 'All':
        data = data[data['model'] == model]
    if fuel_type != 'All':
        data = data[data['fuelType'] == fuel_type]
    if transmission != 'All':
        data = data[data['transmission'] == transmission]
    if year != 'All':
        data = data[data['year'] == year]
    return data

# Function to calculate statistics
def calculate_stats(data):
    max_price = data['price'].max()
    min_price = data['price'].min()
    avg_price = data['price'].mean()
    # Assuming 'mileage' is the column for MPG and 'tax' is the tax value
    max_mpg = data['mileage'].max()
    min_mpg = data['mileage'].min()
    avg_mpg = data['mileage'].mean()
    max_tax = data['tax'].max()
    return max_price, min_price, avg_price, max_mpg, min_mpg, avg_mpg, max_tax

# Streamlit UI
st.sidebar.header('Filters')
model = st.sidebar.selectbox('Model', options=['All'] + sorted(data['model'].unique().tolist()))
fuel_type = st.sidebar.selectbox('Fuel Type', options=['All'] + sorted(data['fuelType'].unique().tolist()))
transmission = st.sidebar.selectbox('Transmission', options=['All'] + sorted(data['transmission'].unique().tolist()))
year = st.sidebar.selectbox('Year', options=['All'] + sorted(data['year'].unique().tolist(), reverse=True))

# Filter the data based on selections
filtered_data = filter_data(data, model, fuel_type, transmission, year)

# Calculate statistics for the filtered data
max_price, min_price, avg_price, max_mpg, min_mpg, avg_mpg, max_tax = calculate_stats(filtered_data)

# Layout of the dashboard
st.title('Audi Car Insights Dashboard')

# Display statistics - you can layout the page using columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Highest Price", f"${max_price:,.0f}")
    st.metric("Lowest Price", f"${min_price:,.0f}")
    st.metric("Average Price", f"${avg_price:,.0f}")

with col2:
    st.metric("Highest Mileage", f"{max_mpg} Miles")
    st.metric("Lowest Mileage", f"{min_mpg} Miles")
    st.metric("Average Mileage", f"{avg_mpg:.2f} Miles")

with col3:
    st.metric("Highest Tax", f"${max_tax}")

# Engine Size and Average MPG
if model != 'All':  # We show engine size and MPG only for a specific model
    st.header(f"Engine Sizes & Average Miles for {model}")
    engine_sizes = filtered_data.groupby('engineSize')['mileage'].mean().reset_index()
    engine_sizes.rename(columns={'mileage': 'Average MPG'}, inplace=True)
    st.write(engine_sizes)
    # Optionally, you can add a bar chart for visual representation
    fig, ax = plt.subplots()
    ax.bar(engine_sizes['engineSize'], engine_sizes['Average MPG'])
    ax.set_xlabel('Engine Size')
    ax.set_ylabel('Average MPG')
    st.pyplot(fig)

# Remember to run your Streamlit app with `streamlit run your_script.py`
