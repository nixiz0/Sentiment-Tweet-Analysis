import pytest
from fastapi.testclient import TestClient
from fastapi_model import app, Tweet


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Welcome To":"Sentiment Analysis"}

def test_predict_sentiment():
    response = client.post("/predict", json={"text": "I love this!"})
    assert response.status_code == 200
    assert "Negative class" in response.json()
    assert "Positive class" in response.json()

def test_model_version():
    response = client.get("/model/version")
    assert response.status_code == 200
    assert "model_version" in response.json()

def test_set_model_version():
    response = client.put("/model/version/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Model version set to 1"}