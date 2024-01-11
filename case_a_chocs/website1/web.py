from flask import Flask, render_template, Response, stream_with_context
from pulsar import Client, ConsumerType
import requests
import json
import time
import sqlite3

app = Flask(__name__)

# Initialisation de la base de données SQLite
def init_db():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_count (
            event_name TEXT PRIMARY KEY,
            ticket_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Mise à jour du compteur de tickets pour un événement
def update_ticket_count(event_name):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()

    # Vérifiez si l'événement existe déjà
    cursor.execute('SELECT ticket_count FROM event_count WHERE event_name = ?', (event_name,))
    row = cursor.fetchone()

    if row:
        # Mettez à jour le compteur existant
        new_count = row[0] + 1
        cursor.execute('UPDATE event_count SET ticket_count = ? WHERE event_name = ?', (new_count, event_name))
    else:
        # Créez un nouveau compteur pour le nouvel événement
        cursor.execute('INSERT INTO event_count (event_name, ticket_count) VALUES (?, 1)', (event_name,))

    conn.commit()
    conn.close()

print("Configuration du client Pulsar...")
client = Client('pulsar://localhost:6650')
topic_name = "persistent://public/default/my_topic1"
subscription_name = 'dashboard_subscription'

def get_event_data():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event_count')
    data = cursor.fetchall()
    conn.close()
    return data


def get_ticket_details(ticket_id):
    # Votre code existant pour obtenir les détails du ticket
    url = f"http://127.0.0.1:8000/api/ticket/{ticket_id}/"
    headers = {"Authorization": "Token 82682c7fbca9598e7c286bd274f73a9060d6130f"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Détails du ticket récupérés : {response.json()}")
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des détails du ticket: {e}")
        return None

def message_listener(consumer, message):
    print("Message reçu de Pulsar...")
    try:
        data = json.loads(message.data().decode())
        print(f"Données du message : {data}")
        if data.get("event") == "ticket_created":
            ticket_details = get_ticket_details(data.get("id"))
            if ticket_details:
                event_name = ticket_details.get("event")
                if event_name:
                    # Mettez à jour le compteur pour cet événement
                    update_ticket_count(event_name)
                    print(f"Compteur mis à jour pour l'événement '{event_name}'")
                consumer.acknowledge(message)
    except Exception as e:
        print(f"Erreur lors du traitement du message: {e}")
        consumer.negative_acknowledge(message)

print("Abonnement au topic Pulsar...")
consumer = client.subscribe(topic_name, subscription_name, consumer_type=ConsumerType.Shared, message_listener=message_listener)

@app.teardown_appcontext
def cleanup(error):
    print("Nettoyage en cours...")
    try:
        consumer.close()
        print("Consommateur Pulsar fermé.")
    except Exception:
        print("Erreur lors de la fermeture du consommateur Pulsar.")
    try:
        client.close()
        print("Client Pulsar fermé.")
    except Exception:
        print("Erreur lors de la fermeture du client Pulsar.")

def event_stream():
    while True:
        try:
            event_data = get_event_data()
            yield f"data: {json.dumps(event_data)}\n\n"
            time.sleep(1)  # Envoyer les données toutes les secondes
        except Exception as e:
            print(f"Exception dans le flux SSE: {e}")
            continue

@app.route('/stream')
def stream_route():
    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

@app.route('/')
def index():
    print("Page d'accueil demandée...")
    event_data = get_event_data()
    return render_template('index.html', event_data=event_data)

if __name__ == '__main__':
    print("Initialisation de la base de données...")
    init_db()
    print("Démarrage de l'application Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000)
