# Projet scolaire
# Optimisation non-linéaire en nombre entier

Ce dossier contient le travail d'un projet d'optimisation non-linéaire en nombre entier réalisé dans le cadre du Mastère Optimisation des systèmes énergétiques des Mines de Paris.

## Description des fichiers

### Dossier data_results

Ce dossier contient les Excel issue des optimisation GAMS (fichier GDX). Ces Excel sont à la source de l'application de visualisation des résultats.<br>
Note : il est nécessaire de rajouter un onglet 'comments' à chaque nouvel Excel.

### Dossier Documentation

Ce dossier contient l'énoncé du problème et un pdf d'explication de la méthode et des résultats.

### Dossier GAMS

Ce dossier contient les fichiers GAMS modélisant le problème.

### Autres

Notebook Results_processing : notebook de travail sans intérêts particuliers<br>
<br>
Fichier python visualisation : fichier python pour visualiser les résultats<br>
<br>
requirements.txt : requirements pour l'application streamlit externe<br>
<br>
requirements_py_venv.txt

## Installation et fonctionnement

Le projet utilise GAMS pour modéliser le problème mais les résultats sont traiter sous python. Pour faire fonctionner le traitement sous python :

### Optionnel : créer un environnement python

Etape 1 : créer l'environnement (il est conseiller de l'appeler ONLNE)<br>
`python create venv ONLNE`
<br>
Etape 2 : installer les packages python requis<br>
`pip install -r requirements_py_venv.txt`
<br>

### Faire fonctionner l'application streamlit
`streamlit run visualisation.py`