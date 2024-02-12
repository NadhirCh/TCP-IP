import socket
import threading
import time
import random

def handle_client(client_socket):
    try:
        # Étape 1: Ouverture de la connexion (SYN, SYN+ACK)
        syn = client_socket.recv(1024).decode()
        print(f"Server: Received SYN - {syn}")
        client_socket.send(b"SYN+ACK")

        # Étape 2: Transfert des données
        # Réception de la demande de nombre de paquets et de rcvwindow
        data = client_socket.recv(1024).decode()
        n_packets, rcvwindow = map(int, data.split(','))
        print(f"Server: Received request for {n_packets} packets with rcvwindow {rcvwindow}")
        for i in range(n_packets):
            # Génération d'une valeur aléatoire entre 0 et 1
            random_value = random.randint(0,1)
            client_socket.send(str(random_value).encode())
            client_socket.send(f"Packet {i + 1}".encode())
            ack = client_socket.recv(1024).decode()
            print(f"Server: Received ACK for Packet {i + 1} - {ack}")

        # Étape 3: Fermeture de la connexion (FIN, ACK)
        fin = client_socket.recv(1024).decode()
        print(f"Server: Received FIN - {fin}")
        closing_message = "en cours de fermeture"
        client_socket.send(closing_message.encode())
        print(f"Server: Sent - {closing_message}")

        # Attente de l'acquittement final du client
        ack = client_socket.recv(1024).decode()
        print(f"Server: Received ACK - {ack}")
        time.sleep(30)  # Temporisateur avant de fermer la connexion
        client_socket.close()
        print("Server: Connection closed")
    except Exception as e:
        print(f"Server Error: {str(e)}")

def server_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server: Started and listening")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Server: Connection established with {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    server_thread()
