from ray import serve
import requests
import joblib
from sklearn.feature_extraction.text import CountVectorizer

class RandomForestModel:
    def __init__(self):
        self.model = joblib.load('models/RandomForestClassifier.pkl')
        self.vectorizer = joblib.load('tmp/vectorizer.pkl')
        with open("/tmp/comments_labels.json") as f:
            self.label_list = json.load(f)

    def __call__(self, flask_request):
        payload = flask_request.json
        print("Worker: received flask request with data", payload)

        new_input = payload['comment']
        new_input_vec = self.vectorizer.transform(new_input)
        prediction = self.model.predict([new_input])[0]
        sentiment = self.label_list['prediction']
        return {"result":sentiment}

client = serve.start()
client.create_backend("lr:v1", RandomForestModel)
client.create_endpoint("comments_classifier", backend="lr:v1", route="/classifier")

sample_request_input = {
    "comment": "fuck this is shit"
}
response = requests.get(
    "http://localhost:8000/classifier", json=sample_request_input)
print(response.text)


