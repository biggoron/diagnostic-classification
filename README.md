# Classification de diagnostics d'imagerie médicale

## Préparer l'environement

### Prérequis

- Avoir Python 3+ installé
- Avoir le gestionaire de packages pip

### Créer, remplir et sourcer l'environement

A la racine du projet, à la première execution
```
python3 -m venv .env
source .env/bin/activate
pip install -r environment.txt
```
Suite à ces opérations, un dossier .env est créé. Par la suite il suffira d'executer: 
```
source .env/bin/activate
```

## Créer l'arbre de maladies, qui servira de référence pour la classification

```
python src/make_knowledge_graphs.py
```

## Créer la liste de mots courants (basée sur les misérables). Elle servira à nettoyer les textes.

```
python src/build_usual_words.py
```

## Classifier un texte

```
python src/classifier.py path/to/the/file_to_classify.txt
```
