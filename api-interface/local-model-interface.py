import streamlit as st
import requests
import json
import os
from applicationinsights import TelemetryClient
from dotenv import load_dotenv


# Start the local server with the "streamlit run api-interface/local-model-interface.py"

# Streamlit interface
st.title("API Tweet Sentiment Analysis")

# Initialize the TelemetryClient with the connection string
load_dotenv('.azure_secret')
instrumentation_key = os.getenv('INSTRUMENTATION_KEY')

# Create a placeholder for the text input
tweet_input = st.empty()
tweet = tweet_input.text_input("Enter a tweet")

# Define the predict function
def predict(tweet):
    # Define the API endpoint
    # Local URL
    # url = "http://localhost:8000/predict"

    # Online API
    url = "https://sentiment-tweet-analysis.azurewebsites.net/predict"

    # Define the tweet to be analyzed
    tweet = {"text": tweet}

    # Send a POST request to the API
    response = requests.post(url, json=tweet)

    return json.loads(response.text)

if st.button("Predict"):
    prediction = predict(tweet)
    
    # Check the prediction and assign a label
    if prediction["Negative class"] > 0.5:
        sentiment = 'Negatif'
    else:
        sentiment = 'Positif'
    
    st.write("Prediction : ", sentiment)
    
    # Ask for user validation
    st.write("Is the prediction correct ?")
    if st.button("Yes"):
        st.write("Thanks for your feedback !")
    elif st.button("No"):
        # Send a trace to the Application Insight service
        tc = TelemetryClient(instrumentation_key)
        tc.track_trace('Incorrect prediction for tweet: {}'.format(tweet))
        tc.flush()
     
    # Clear the text input
    tweet_input.text_input("Enter a tweet", value='', key='1')