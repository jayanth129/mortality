!pip install joblib

import streamlit as st
import pandas as pd
import joblib

# Load the trained decision tree model
model = joblib.load('decision_tree_model.pkl')

# Define the maximum and minimum values for GDP and Population
max_population = int(329064917.0)
min_population = int(8910.0)
max_gdp = int(21381000000000.0)
min_gdp = int(8824746.238)

# Define the age brackets
age_brackets = {
    '7-27 days': 'Deaths - All causes - Sex: Both - Age: 7-27 days (Number)',
    '1-4 years': 'Deaths - All causes - Sex: Both - Age: 1-4 years (Number)',
    '0-6 days': 'Deaths - All causes - Sex: Both - Age: 0-6 days (Number)',
    '28-364 days': 'Deaths - All causes - Sex: Both - Age: 28-364 days (Number)'
}

# Define the Streamlit app
def main():
    st.title('Mortality Prediction App')

    # Create input fields for user to input data
    year = st.sidebar.slider('Year', min_value=1990, max_value=2024, step=1)
    population = st.sidebar.slider('Population (historical estimates)', min_value=min_population, max_value=max_population, step=1, value=min_population)
    gdp = st.sidebar.slider('GDP', min_value=min_gdp, max_value=max_gdp, step=1, value=min_gdp)

    # Create radio buttons for the most common age bracket
    selected_age_bracket = st.sidebar.radio('Most deaths fall within what age bracket:', list(age_brackets.keys()))

    # Create radio buttons for selecting the leading cause of death
    selected_cause = st.sidebar.radio('What was the leading cause of death:', 
                                      ['Nutritional deficiencies', 'Infectious Diseases', 'Chronic Diseases', 
                                       'Neonatal Conditions', 'Injuries and Trauma', 'Other Conditions'])

    # Map selected cause to binary values
    binary_mapping = {'Nutritional deficiencies': 0, 'Infectious Diseases': 1, 'Chronic Diseases': 2, 
                      'Neonatal Conditions': 3, 'Injuries and Trauma': 4, 'Other Conditions': 5}
    selected_cause_code = binary_mapping[selected_cause]

    # Create a DataFrame with user inputs
    user_input = pd.DataFrame({
        'Year': [year],
        'Nutritional deficiencies': [1 if selected_cause_code == 0 else 0],
        'Population (historical estimates)': [population],
        'Deaths - All causes - Sex: Both - Age: 7-27 days (Number)': [1 if age_brackets[selected_age_bracket] == 'Deaths - All causes - Sex: Both - Age: 7-27 days (Number)' else 0],
        'Deaths - All causes - Sex: Both - Age: 1-4 years (Number)': [1 if age_brackets[selected_age_bracket] == 'Deaths - All causes - Sex: Both - Age: 1-4 years (Number)' else 0],
        'Deaths - All causes - Sex: Both - Age: 0-6 days (Number)': [1 if age_brackets[selected_age_bracket] == 'Deaths - All causes - Sex: Both - Age: 0-6 days (Number)' else 0],
        'Deaths - All causes - Sex: Both - Age: 28-364 days (Number)': [1 if age_brackets[selected_age_bracket] == 'Deaths - All causes - Sex: Both - Age: 28-364 days (Number)' else 0],
        'GDP': [gdp],
        'Infectious Diseases': [1 if selected_cause_code == 1 else 0],
        'Chronic Diseases': [1 if selected_cause_code == 2 else 0],
        'Neonatal Conditions': [1 if selected_cause_code == 3 else 0],
        'Injuries and Trauma': [1 if selected_cause_code == 4 else 0],
        'Other Conditions': [1 if selected_cause_code == 5 else 0]
    })

    # Make predictions
    prediction = model.predict(user_input)

    # Convert prediction to human-readable format
    risk_level = 'High' if prediction[0] == 1 else 'Low'

    # Display the prediction
    st.subheader('Predicted Risk Level:')
    st.write(risk_level)

# Run the Streamlit app
if __name__ == '__main__':
    main()
