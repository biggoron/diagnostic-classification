# Classification de diagnostics d'imagerie médicale

## Préparer l'environement

### Prérequis

- Avoir Python 3+ installé
- Avoir le gestionaire de packages pip

### Créer, remplir et sourcer l'environement

A la racine du projet
```
python3 -m venv .env
source .env/bin/activate
pip install -r environment.txt
```

## Créer l'arbre de maladies, qui servira de référence pour la classification

```
python src/make_knowledge_graphs.py
```
