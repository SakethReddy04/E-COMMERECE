
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FAQBot:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(self.df["Question"])

    def get_answer(self, user_input):
        user_vec = self.vectorizer.transform([user_input])
        sim = cosine_similarity(user_vec, self.vectors)
        idx = sim.argmax()
        return self.df.iloc[idx]["Answer"]
