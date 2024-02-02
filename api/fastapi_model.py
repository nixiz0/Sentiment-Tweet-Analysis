import os
import string
import re
import pickle
from fastapi import FastAPI
from uvicorn import run
from pydantic import BaseModel
from keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow import keras


# To launch locally, go on 'api' folder and do the command :
# <= uvicorn fastapi_model:app --reload =>

app = FastAPI()
class Tweet(BaseModel):
    text: str

# Initialize current_model_version
current_model_version = 2

@app.get('/')
def menu():
    return {"Welcome To":"Sentiment Analysis"}

@app.on_event("startup")
def load_model(version: int=current_model_version):
    global model
    model_filename = f'./api/model/small_glove_v{version}.h5'

    # Load the pre-trained model
    model = keras.models.load_model(model_filename)

@app.put("/model/version/{version}")
def set_model_version(version: int):
    global current_model_version
    current_model_version = version
    load_model(version)
    return {"message": f"Model version set to {version}"}

@app.get("/model/version")
def get_model_version():
    return {"model_version": current_model_version}

def preprocess(tweet):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # Convert text to lowercase
    tweet = tweet.lower()

    # Remove '@' followed by names
    tweet = re.sub(r'@\w+', '', tweet)

    # Remove all punctuation
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))

    # Remove non-ASCII characters
    tweet = tweet.encode('ascii', 'ignore').decode()

    # Remove HTTP and HTTPS links
    tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet)

    # Remove stopwords and lemmatize the text
    tweet = ' '.join(lemmatizer.lemmatize(word) for word in tweet.split() if word not in stop_words)

    return tweet
    
def load_tokenizer(version: int=current_model_version):
    # Load the tokenizer based on the specified version
    tokenizer_filename = f'./api/tokenizer/small_tokenizer_v{version}.pickle'
    with open(tokenizer_filename, 'rb') as handle:
        return pickle.load(handle)

def tokenize(tweet, tokenizer_version: int=current_model_version):
    # Preprocess the tweet
    processed_tweet = preprocess(tweet)

    # Load the tokenizer with the specified version
    tokenizer = load_tokenizer(version=tokenizer_version)

    # Tokenize the tweet
    tokenized_tweet = tokenizer.texts_to_sequences([processed_tweet])

    # Padding sequences
    max_length = 120
    padded_tweet = pad_sequences(tokenized_tweet, maxlen=max_length, padding='post')

    return padded_tweet

@app.post('/predict')
def predict_sentiment(tweet: Tweet, model_version: int=current_model_version, tokenizer_version: int=current_model_version):
    # Set the current model version
    load_model(version=model_version)

    # Preprocess and tokenize the tweet
    tokenize_tweet = tokenize(tweet.text, tokenizer_version=tokenizer_version)

    # Predict sentiment
    prediction = model.predict(tokenize_tweet)

    # Return prediction
    return {"Negative class": float(prediction[0][0]), "Positive class": float(prediction[0][1])}
    
if __name__ == "__main__":
    port = int(os.environ.get("WEBSITES_PORT", 8000))
    run("__main__:app", host="0.0.0.0", port=port, log_level="info")