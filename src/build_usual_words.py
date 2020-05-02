from collections import Counter
import pickle
import string

from unidecode import unidecode

if __name__ == '__main__':
    # Open and normalize text to extract usual vocabulary
    with open('data/les_miserables.txt', 'r') as text:
        fantine = text.read().replace('\n', ' ')
    fantine = unidecode(fantine).lower()
    fantine = (
        fantine
        .replace('\'', ' ')
        .translate(str.maketrans(' ', ' ', string.punctuation))
    )
    fantine = fantine.split(' ')
    # Other words we want to discard, but not present in les miserables
    other_usual_words = ['precision', 'maladie', 'maladies', 'absence']
    usual_words = [
        couple[0]
        for couple in Counter(fantine).most_common(1000) + other_usual_words]
    print(usual_words)
    with open('data/usual_words.pkl', 'wb') as f:
        pickle.dump(usual_words, f)
