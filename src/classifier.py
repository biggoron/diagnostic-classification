import os
import re
import codecs
import pickle
import csv
import string
import sys
import numpy as np
from collections import Counter
from functools import reduce
from anytree import Node
from unidecode import unidecode


class Classifier:
    """Tool to classify a text (full text or single word) in disease categories."""
    def __init__(self, data_dir='data/'):
        diseases_tree_path = os.path.join(data_dir, 'diseases_tree.csv')
        if not os.path.isfile(diseases_tree_path):
            print("Please read README.md and generate the diseases graph first.")
        self.disease_nodes = self._read_tree(diseases_tree_path)
        self.root_nodes = [node for node in self.disease_nodes.values() if node.is_root][:19]
        self.common_words_list = self._get_common_words_list(data_dir)
        self.corpus = self._build_corpus()
        # Convert category words to word count dict
        word_count = [Counter(cat_text.split(' ')) for cat_text in self.corpus]
        #build tfidf
        overall_word_count = reduce(lambda x, y: x + y, word_count)
        self.words_in_corpus = list(overall_word_count.keys())
        self.corpus_tfidf = [
            self.div_counter(cat_word_count, overall_word_count)
            for cat_word_count in word_count]

    @staticmethod
    def div_counter(count_a, count_b):
        """Divides in category word count with overall word count. prevents 0 divisions"""
        for word, count in count_a.items():
            if word in count_b.keys():
                count_a[word] /= count_b[word]
            else:
                count_a[word] = 1
        return count_a


    def _add_to_tree_nodes(self, cat_list, nodes):
        cat_list = [unidecode(cat).lower() for cat in cat_list]
        if cat_list[-1] in nodes.keys():
            return nodes
        if len(cat_list) == 1:
            value = cat_list[0]
            nodes.update({value: Node(value)})
            return nodes
        else:
            if cat_list[-2] not in nodes.keys():
                nodes = self._add_to_tree_nodes(cat_list[:-1], nodes)
            value = cat_list[-1]
            nodes.update({value: Node(value, parent=nodes[cat_list[-2]])})
            return nodes


    def _read_tree(self, tree_path):
        """Loads the diseases tree as a tree data structure."""
        nodes = {}
        with open(tree_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            line_count = 0
            for row in csv_reader:
                nodes = self._add_to_tree_nodes(row, nodes)
        return nodes


    @staticmethod
    def _get_common_words_list(data_dir):
        """Loads the common words as a list."""
        diseases_tree_path = os.path.join(data_dir, 'usual_words.pkl')
        if not os.path.isfile(diseases_tree_path ):
            print("Please read README.md and generate the common words file first.")
        with open(diseases_tree_path, 'rb') as f:
            common_words_list = pickle.load(f)
        return common_words_list


    def _tree_to_text(self, node, tree_text=[]):
        if node.is_leaf:
            tree_text += node.name.replace('\'', ' ').translate(str.maketrans(' ', ' ', string.punctuation)).split(' ')
        else:
            for child in node.children:
                tree_text += self._tree_to_text(child, [])
        return tree_text 
        

    def _build_corpus(self):
        # Convert each subtree to a text sequence of all words contained
        # in the subtree. Then removes usual words
        corpus = [
            ' '.join([
                word for word in self._tree_to_text(node, [])
                if word not in self.common_words_list and len(word) > 2])
            for node in self.root_nodes]
        return corpus

    def print_categories(self):
        print("######################")
        print("# List of categories #")
        print("######################")
        for i, node in enumerate(self.root_nodes):
            print(f"{i}: {node.name}")

    def process_file(self, path_to_file):
        with codecs.open(path_to_file, 'r', 'iso-8859-1') as content:
            text = content.read().replace('\r\n', ' ').replace('\'', ' ').lower()
            text = unidecode(text)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r' {2,}', ' ', text)
            text = re.sub(r' {2,}', ' ', text)
            text = ' '.join([
                word for word in text.split(' ')
                if word in self.words_in_corpus and \
                word not in self.common_words_list and \
                len(word) > 2])
        return text

    def classify(self, path_to_file):
        text = self.process_file(path_to_file)
        print("####################################################")
        print("# List of words, with classification probabilities #")
        print("####################################################")
        for word_ in text.split(' '):
            print(f"### {word_} ###")
            print([cat[word_] for cat in self.corpus_tfidf])
        cat_probas = np.array([
            [cat[word] for cat in self.corpus_tfidf]
            for word in text.split(' ')]).sum(axis=0)
        cat_probas = cat_probas / cat_probas.sum()
        cat_probas = {self.root_nodes[i].name: proba for i, proba in enumerate(cat_probas)}

        print("########################################")
        print("# Overall classification probabilities #")
        print("########################################")
        print(cat_probas)

        top_3 = sorted(cat_probas.items(), key=lambda item: item[1])[-3:][::-1]
        print("#########")
        print("# TOP 3 #")
        print("#########")
        print(top_3)
        return cat_probas

if __name__ == '__main__':
    classifier = Classifier()
    classifier.print_categories()
    classifier.classify(sys.argv[1])
