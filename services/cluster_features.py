import joblib;
from sklearn.feature_extraction.text import TfidfVectorizer

def predictCluster(feature:str):
    vectorizer=joblib.load('vectorizer.pkl')
    model=joblib.load('model.pkl')
    # print(model.cluster_centers_)
    Y = vectorizer.transform([feature])
    prediction = model.predict(Y)[0];
    print("cluster: ",prediction);
    return prediction

