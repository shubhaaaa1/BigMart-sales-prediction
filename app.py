import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the trained model
try:
    model = pickle.load(open('big_mart_model.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'big_mart_model.pkl' is in the same directory.")
    st.stop()

# App Title
st.set_page_config(page_title="Big Mart Sales Prediction", page_icon="🛒", layout="centered")
st.title("🛒 Big Mart Sales Prediction App")

# Sidebar for user input
st.sidebar.header("Enter the Item Details")

def user_input_features():
    Item_Identifier = st.sidebar.text_input('Item Identifier (optional)', 'FDA15')

    Item_Weight = st.sidebar.number_input('Item Weight', min_value=0.0, max_value=25.0, step=0.1)

    Item_Fat_Content = st.sidebar.selectbox('Item Fat Content', ('Low Fat', 'Regular'))
    fat_content_dict = {'Low Fat': 0, 'Regular': 1}
    Fat_Content = fat_content_dict[Item_Fat_Content]

    Item_Visibility = st.sidebar.slider('Item Visibility', 0.0, 0.3, 0.05)

    Item_Type = st.sidebar.selectbox('Item Type', [
        'Baking Goods', 'Breads', 'Breakfast', 'Canned', 'Dairy', 'Frozen Foods',
        'Fruits and Vegetables', 'Health and Hygiene', 'Hard Drinks', 'Household',
        'Meat', 'Others', 'Seafood', 'Snack Foods', 'Soft Drinks', 'Starchy Foods'
    ])
    item_type_dict = {
        'Baking Goods': 0, 'Breads': 1, 'Breakfast': 2, 'Canned': 3, 'Dairy': 4,
        'Frozen Foods': 5, 'Fruits and Vegetables': 6, 'Health and Hygiene': 7,
        'Hard Drinks': 8, 'Household': 9, 'Meat': 10, 'Others': 11,
        'Seafood': 12, 'Snack Foods': 13, 'Soft Drinks': 14, 'Starchy Foods': 15
    }
    Item_Type_Encoded = item_type_dict[Item_Type]

    Item_MRP = st.sidebar.number_input('Item MRP', min_value=0.0, max_value=300.0, step=1.0)

    Outlet_Identifier = st.sidebar.text_input('Outlet Identifier (optional)', 'OUT049')

    Outlet_Establishment_Year = st.sidebar.number_input('Outlet Establishment Year', min_value=1985, max_value=2025, step=1)

    Outlet_Size = st.sidebar.selectbox('Outlet Size', ('High', 'Medium', 'Small'))
    outlet_size_dict = {'High': 0, 'Medium': 1, 'Small': 2}
    Outlet_Size_Encoded = outlet_size_dict[Outlet_Size]

    Outlet_Location_Type = st.sidebar.selectbox('Outlet Location Type', ('Tier 1', 'Tier 2', 'Tier 3'))
    outlet_location_dict = {'Tier 1': 0, 'Tier 2': 1, 'Tier 3': 2}
    Outlet_Location_Encoded = outlet_location_dict[Outlet_Location_Type]

    Outlet_Type = st.sidebar.selectbox('Outlet Type', (
        'Grocery Store', 'Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3'))
    outlet_type_dict = {'Grocery Store': 0, 'Supermarket Type1': 1, 'Supermarket Type2': 2, 'Supermarket Type3': 3}
    Outlet_Type_Encoded = outlet_type_dict[Outlet_Type]

    data = {
        'Item_Weight': Item_Weight,
        'Item_Fat_Content': Fat_Content,
        'Item_Visibility': Item_Visibility,
        'Item_Type': Item_Type_Encoded,
        'Item_MRP': Item_MRP,
        'Outlet_Establishment_Year': Outlet_Establishment_Year,
        'Outlet_Size': Outlet_Size_Encoded,
        'Outlet_Location_Type': Outlet_Location_Encoded,
        'Outlet_Type': Outlet_Type_Encoded
    }

    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Display user input
st.subheader('Entered Item Details')
st.write(input_df)

# Optional: Dataset preview
if st.checkbox("Show Sample Data"):
    try:
        data = pd.read_csv('big_mart_data.csv')
        st.write(data.sample(5))
    except FileNotFoundError:
        st.warning("Dataset file not found. Upload 'big_mart_data.csv' if you want to use this feature.")

# Predict Button
if st.button('Predict Sales'):
    with st.spinner('Predicting...'):
        try:
            prediction = model.predict(input_df)
            st.success(f'Predicted Sales: ₹ {prediction[0]:.2f}')
        except Exception as e:
            st.error(f"Error in prediction: {e}")



