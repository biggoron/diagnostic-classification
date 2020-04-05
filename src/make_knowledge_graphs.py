"""
This module provides functions to create knowledge trees summarizing
informations found on the WHO diseases classification and the VIDAL drugs classification.
"""

import re
from urllib.request import urlopen
import html
import json
import time
from random import random
import pickle


# Root link to WHO diseases classification
DISEASES_ROOT_LINK = "https://icd.who.int/browse10/2008/fr/JsonGetRootConcepts?useHtml=true"

def _set_disease_category_url(id_field):
    """Returns the link to a disease category, provided its name."""
    return f"https://icd.who.int/browse10/2008/fr/JsonGetChildrenConcepts?ConceptId={id_field}&useHtml=true&showAdoptedChildren=true"

def _insert_children_disease_categories_in_tree(url, level, category_list, results):
    """
    Recursively fetch disease subcategories online, and stores
    knowledge in nested lists
    """
    # Important to introduce delay, to avoid making the website crash with
    # too many requests
    time.sleep((random() + 1) / 10.)
    # Fetch url corresponding to a node in the knowledge tree
    page_response = urlopen(url)
    # Process the html escape sequences
    str_page = html.unescape(page_response.read().decode('utf8'))
    # Escape problematic " caracters
    str_page = re.sub(r'Doigt "à ressort"', 'Doigt \\"à ressort\\"', str_page)
    str_page = re.sub(r'Oreille "en chou-fleur"', 'Oreille \\"en chou-fleur\\"', str_page)
    str_page = re.sub(r'Syndrome de la "bile épaisse"', 'Syndrome de la \\"bile épaisse\\"', str_page)
    str_page = re.sub(r'Hanche "à ressort"', 'Hanche \\"à ressort\\"', str_page)
    # Load page as json
    json_page = json.loads(str_page)
    # Regex targeting the category names we are looking for
    cat_regex = r'\<\/span>\r\n(?P<cat_name>[^\r\n]+)'
    # [ID, sub_category, is the node a leaf boolean]
    children_categories = [
        (
            line['ID'],
            re.search(cat_regex, line['html']).group('cat_name'),
            line['isLeaf']
        )
    for line in json_page]
    for id_field, cat_name, leaf in children_categories:
        print(f'{id_field} - {cat_name} - {leaf}')
        # extend the branch of the tree with a new node.
        children_category_list = category_list + [cat_name.lstrip().rstrip()]
        if leaf:
            # We the appended node is a leaf, return the result
            results += [children_category_list]
        else:
            # Else repeat recursively the operation on the children
            children_url = set_disease_category_url(id_field)
            children_level = level + 1
            results = insert_children_disease_categories_in_tree(
                children_url, children_level, children_category_list, results)
    return results

def download_and_save_diseases_tree(output='data/diseases_tree.csv'):
    """Stores in a csv a disease tree created recursively from OMS diseases classification"""
    tree = insert_children_disease_categories_in_tree(DISEASES_ROOT_LINK, 0, [], [])
    # Format the tree to csv style
    tree_str = '\n'.join(['|'.join(line) for line in results])
    with open(output, 'w') as f:
        f.write(tree_str)
    
