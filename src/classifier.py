import os
import csv
from anytree import Node
from unidecode import unidecode
from src.make_knowledge_graphs import download_and_save_diseases_tree

class Classifier:
    """Tool to classify a text (full text or single word) in disease categories."""
    def __init__(self, data_dir='data/'):
        csv_name = ''
        if CLASSIFIER_DATA_PATH in os.environ.keys():
            data_dir = os.environ['CLASSIFIER_DATA_PATH']
        diseases_tree_path = os.path.join(data_dir, 'diseases_tree.csv')
        if not os.path.isfile(output):
            download_and_save_diseases_tree(data_dir)
        self.disease_nodes = self._read_tree(diseases_tree_path)
        self.common_words_list = self._get_common_words_list(data_dir)
        self.category_map
        self.category_reverse_map

    @staticmethod
    def _add_to_tree_nodes(cat_list, nodes):
        cat_list = [unidecode(cat).lower() for cat in cat_list]
        if cat_list[-1] in nodes.keys():
            return nodes
        if len(cat_list) == 1:
            value = cat_list[0]
            nodes.update({value: Node(value)})
            return nodes
        else:
            if cat_list[-2] not in nodes.keys():
                nodes = add_to_nodes(cat_list[:-1], nodes)
            value = cat_list[-1]
            nodes.update({value: Node(value, parent=nodes[cat_list[-2]])})
            return nodes

    @staticmethod
    def _read_tree(tree_path):
        nodes = {}
        with open(tree_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            line_count = 0
            for row in csv_reader:
                nodes = add_to_nodes(row, nodes)
        return nodes

    @staticmethod
    def _get_common_words_list(data_dir):

    def _build_tfidf_tree():
        pass

    def _build_tfidf_doc():
        pass

    def _clean_text():
        pass

    def _clean_tree():
        pass

    def classify_disease(txt, n_best=-1):
        pass

    def _get_disease_scores(txt):
        pass
