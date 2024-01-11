#Urbanisation de la case à choc

Description courte et concise du projet.

## Installation

Cloner le projet depuis le référentiel Git :
```bash
git clone https://github.com/AmadeusEnki/UrbaChoc.git

cd case_a_chocs
   
docker pull apachepulsar/pulsar:latest

docker run -p 6650:6650 -p 8080:8080 apachepulsar/pulsar
```
Depuis la racine du dossier
```python
pip install -r requirements.txt
```
##Pour lancer le projet
```python
python manage.py runserver

python website1\web.py

python petzi_simulator.py http://127.0.0.1:8000/api/webhook/
```
