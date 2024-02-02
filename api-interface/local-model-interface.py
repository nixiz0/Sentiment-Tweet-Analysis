import streamlit as st
import requests
import json


# Start the local server with the "streamlit run api-interface/local-model-interface.py"

# Streamlit interface
st.title("API Tweet Sentiment Analysis")

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

    # Return the response from the API
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
        pass
     
    # Clear the text input
    tweet_input.text_input("Enter a tweet", value='', key='1')