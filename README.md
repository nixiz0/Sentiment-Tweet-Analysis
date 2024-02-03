
# Tweet Sentiment Analaysis

Tweet Sentiment Analysis Project.

The goal here is to prototype an AI product that can predict the sentiment associated with a tweet.

## Notebooks

In the notebooks folder are the notebooks for experiments, processing and building models allowing sentiment analysis using different models ranging from the simple machine learning model to the deep learning model using neural networks and transfer learning pre trained model.

There is also an MLflow file allowing tacking and monitoring of the performance of the models during their training.

Small precision : there's no artifacts folder containing the .pkl model for reasons of storage limitations, the files are in fact too large to be stored online on Github.

To execute locally the MLflow UI dashboard you have to run this command in your shell : ```cd notebooks``` 

And after you can execute the command : 
```mlflow ui```

Now you can access to MLflow UI on your local address : **http://localhost:5000**

=> To run the notebooks part you will find in the folder a file *requirements_notebooks.txt* which contains all the libraries necessary to run the notebooks.

=> You also have in main the "history_models" folder which shows the learning curves of the different models.


## API

For the API you have the "API" folder which contains the fastapi script to launch the API locally or online on the cloud and you have test_api which allows the execution of unit tests for the API.

You will also find a "model" and "tokenizer" folder which each contain their models and tokenizer with their respective versions.

**To run locally the API**

- You must download the *requirements.txt* into your virtual environment which will give you all the libraries necessary to use the API.

- Then you run this command on your shell ```uvicorn api.fastapi_model:app --reload```

Now you will have your local API on your local address : **http://127.0.0.1:8000**  

**To run locally the interface API**

- Now that you have started your API locally with uvicorn you must go to the "api-interface" folder and you will see the script allowing you to run an interface with streamlit to interact with your API.

- To run the streamlit interface you have to do this command on your shell ```streamlit run api-interface/local-model-interface.py```

- Pay close attention to the url you want to use, there are 2 urls, you comment on the ones you want to use, here to run and use the API locally you must use the url **http://localhost: 8000/predict**

**To run online the interface API**
- If you have deploy on the cloud the API above, you have to put on the url the address of your online API to use it, like ```https://sentiment-tweet-analysis.azurewebsites.net/predict``` 