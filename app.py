import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the trained model
model = pickle.load(open('big_mart_model.pkl', 'rb'))  # Make sure you have this file in your directory

# App Title
st.set_page_config(page_title="Big Mart Sales Prediction", page_icon="🛒", layout="centered")
st.title("🛒 Big Mart Sales Prediction App")

# Sidebar for user input
st.sidebar.header("Enter the Item Details")

def user_input_features():
    Item_Weight = st.sidebar.number_input('Item Weight', min_value=0.0, max_value=25.0, step=0.1)

    Item_Fat_Content = st.sidebar.selectbox('Item Fat Content', ('Low Fat', 'Regular'))
    if Item_Fat_Content == 'Low Fat':
        Fat_Content = 0
    else:
        Fat_Content = 1

    Item_Visibility = st.sidebar.slider('Item Visibility', 0.0, 0.3, 0.05)

    Item_Type = st.sidebar.selectbox('Item Type', [
        'Fruits and Vegetables', 'Dairy', 'Baking Goods', 'Snack Foods', 'Frozen Foods',
        'Breakfast', 'Health and Hygiene', 'Soft Drinks', 'Meat', 'Household',
        'Canned', 'Breads', 'Starchy Foods', 'Others', 'Hard Drinks', 'Seafood'
    ])

    # Encoding Item_Type manually
    item_type_dict = {
        'Fruits and Vegetables': 0, 'Dairy': 1, 'Baking Goods': 2, 'Snack Foods': 3,
        'Frozen Foods': 4, 'Breakfast': 5, 'Health and Hygiene': 6, 'Soft Drinks': 7,
        'Meat': 8, 'Household': 9, 'Canned': 10, 'Breads': 11, 'Starchy Foods': 12,
        'Others': 13, 'Hard Drinks': 14, 'Seafood': 15
    }
    Item_Type_Encoded = item_type_dict[Item_Type]

    Item_MRP = st.sidebar.number_input('Item MRP', min_value=0.0, max_value=300.0, step=1.0)

    Outlet_Size = st.sidebar.selectbox('Outlet Size', ('Small', 'Medium', 'High'))
    outlet_size_dict = {'Small': 0, 'Medium': 1, 'High': 2}
    Outlet_Size_Encoded = outlet_size_dict[Outlet_Size]

    Outlet_Location_Type = st.sidebar.selectbox('Outlet Location Type', ('Tier 1', 'Tier 2', 'Tier 3'))
    outlet_location_dict = {'Tier 1': 0, 'Tier 2': 1, 'Tier 3': 2}
    Outlet_Location_Encoded = outlet_location_dict[Outlet_Location_Type]

    Outlet_Type = st.sidebar.selectbox('Outlet Type', (
        'Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3', 'Grocery Store'))
    outlet_type_dict = {'Supermarket Type1': 0, 'Supermarket Type2': 1, 'Supermarket Type3': 2, 'Grocery Store': 3}
    Outlet_Type_Encoded = outlet_type_dict[Outlet_Type]

    data = {
        'Item_Weight': Item_Weight,
        'Item_Fat_Content': Fat_Content,
        'Item_Visibility': Item_Visibility,
        'Item_Type': Item_Type_Encoded,
        'Item_MRP': Item_MRP,
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

# Predict Button
if st.button('Predict Sales'):
    prediction = model.predict(input_df)
    st.subheader(f'Predicted Sales: ₹ {prediction[0]:.2f}')




