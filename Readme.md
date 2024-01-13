# Urbanisation de la case à choc
## Introduction

Bienvenue dans le dépôt du projet Composite développé pour la Case à Chocs. Ce projet met en avant une sélection stratégique de technologies et de langages de programmation visant à garantir performance, sécurité, et intégration harmonieuse avec les systèmes existants. Cette documentation met en lumière les technologies clés choisies pour ce projet, expliquant leurs rôles fondamentaux dans la réalisation du Proof of Concept (PoC).



## Installation

### Cloner le projet depuis le référentiel Git
```bash
git clone https://github.com/AmadeusEnki/UrbaChoc.git
```
```bash
cd case_a_chocs
```
```bash
docker pull apachepulsar/pulsar:latest
```
```bash
docker run -p 6650:6650 -p 8080:8080 apachepulsar/pulsar
```
```python
pip install -r requirements.txt
```
## Pour lancer le projet
### Pour lancer Django
```python
python manage.py makemigrations
```
```python
python manage.py migrate
```
```python
python manage.py runserver
```
### Pour lancer le website aller dans le dossier website1
```python
cd website1
```
```python
python website1\web.py
```
Pour simuler le petzi depuis la racine du dossier
```python
python petzi_simulator.py http://127.0.0.1:8000/api/webhook/
```
