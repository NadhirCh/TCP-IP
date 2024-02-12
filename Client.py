import tkinter as tk
from threading import Thread
import socket
import time
import random

def update_text_area(message):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, message + "\n")
    text_area.config(state=tk.DISABLED)
    text_area.see(tk.END)

def open_connection():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        syn_message = "SYN"
        client_socket.send(syn_message.encode())
        update_text_area(f"Client: Sent - {syn_message}")
        syn_ack = client_socket.recv(1024).decode()
        update_text_area(f"Server Response: {syn_ack}")
    except Exception as e:
        update_text_area(f"Client Error: {str(e)}")

def request_packets():
    try:
        n_packets = int(entry_packets.get())
        rcvwindow = int(entry_rcvwindow.get())
        data_request = f"{n_packets},{rcvwindow}"
        client_socket.send(data_request.encode())
        update_text_area(f"Client: Requested {n_packets} packets with rcvwindow size {rcvwindow}")
        i=0
        while(i<n_packets):
            rand = random.randint(0, 1)
            if rand==0:
                packet = client_socket.recv(1024).decode()
                client_socket.send(b"ACK")
                update_text_area(f"Server Response: {packet} (Size: {rcvwindow} bytes)")
                update_text_area(f"Client: Sent ACK for Packet {i+1}")
                i += 1


            else:
                update_text_area(f"Client : Error : NACK packet  {i+1}")
                update_text_area(f"Serveur: Renvoie du packet {i+1}")


    except Exception as e:
        update_text_area(f"Client Error: {str(e)}")

def close_connection():
    try:
        # Le client envoie un paquet FIN
        fin_message = "FIN"
        client_socket.send(fin_message.encode())
        update_text_area(f"Client: Sent - {fin_message}")

        # Réception de la réponse du serveur (en cours de fermeture)
        server_response = client_socket.recv(1024).decode()
        update_text_area(f"Server Response: {server_response}")

        # Le client envoie un acquittement pour la réponse du serveur
        ack_message = "ACK"
        client_socket.send(ack_message.encode())
        update_text_area(f"Client: Sent - {ack_message}")

        # Délai de fermeture (temporisateur de 30 secondes)
        time.sleep(30)
        client_socket.close()
        update_text_area("Client: Connection closed")
    except Exception as e:
        update_text_area(f"Client Error: {str(e)}")

root = tk.Tk()
root.title("TCP Client")

entry_label_packets = tk.Label(root, text="Enter Number of Packets:")
entry_label_packets.pack()

entry_packets = tk.Entry(root, width=10)
entry_packets.pack()

entry_label_rcvwindow = tk.Label(root, text="Enter rcvwindow Size:")
entry_label_rcvwindow.pack()

entry_rcvwindow = tk.Entry(root, width=10)
entry_rcvwindow.pack()

open_button = tk.Button(root, text="Open Connection", command=lambda: Thread(target=open_connection).start())
open_button.pack()

request_button = tk.Button(root, text="Request Packets", command=lambda: Thread(target=request_packets).start())
request_button.pack()

close_button = tk.Button(root, text="Close Connection", command=lambda: Thread(target=close_connection).start())
close_button.pack()

text_area = tk.Text(root, height=15, width=60)
text_area.pack()
text_area.config(state=tk.DISABLED)

root.mainloop()