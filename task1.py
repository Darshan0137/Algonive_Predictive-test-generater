import random
import re
from collections import defaultdict

class PredictiveTextGenerator:
    def __init__(self, filename=None, n=2):
        self.n = n
        self.model = defaultdict(list)
        self.filename = filename
        training_text = self.load_training_text(filename)
        self.train(training_text)

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        return text.split()

    def load_training_text(self, filename):
        default_text = (
            "Python is a powerful programming language. "
            "Python can be used for data science, web development, and automation. "
            "I love learning Python because it is simple and versatile. "
            "Data analysis using Python is very efficient. "
            "Machine learning with Python is fun and interesting."
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    print(f"Loaded training data from '{filename}'")
                    return file.read()
            except FileNotFoundError:
                print(f"File '{filename}' not found. Using default text.")
        return default_text

    def train(self, text):
        words = self.preprocess_text(text)
        if len(words) < self.n:
            return
        for i in range(len(words) - self.n + 1):
            key = tuple(words[i:i + self.n - 1])
            next_word = words[i + self.n - 1]
            self.model[key].append(next_word)

    def save_new_data(self, new_text):
        if not self.filename:
            return
        try:
            with open(self.filename, 'a', encoding='utf-8') as file:
                file.write("\n" + new_text)
        except Exception as e:
            print(f"Could not save data: {e}")

    def predict_next_word(self, text):
        words = self.preprocess_text(text)
        if len(words) < self.n - 1:
            return "Please type more words for prediction."
        key = tuple(words[-(self.n - 1):])
        if key in self.model:
            return random.choice(self.model[key])
        return "No prediction available."

    def chat(self):
        print("=== Predictive Text Generator (Dynamic Learning) ===")
        print("Type a few words and get a next-word suggestion.")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == 'exit':
                print("Goodbye")
                break
            if not user_input:
                print("Please type something.")
                continue

            suggestion = self.predict_next_word(user_input)
            print(f"Suggested next word: {suggestion}")

            # Learn dynamically from user input
            self.train(user_input)
            self.save_new_data(user_input)

if __name__ == "__main__":
    generator = PredictiveTextGenerator(filename="data.txt", n=2)
    generator.chat()

user_input = input("You: ").strip()