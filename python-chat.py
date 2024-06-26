# rajouter fonction pour exclure un utilisateur
# pouvoir fermer la sesssion par l'hôte

import os
import sys
import time
import socket
import threading
import datetime

embed = r"""
 ___      _   _                ___ _         _   
| _ \_  _| |_| |_  ___ _ _    / __| |_  __ _| |_ 
|  _/ || |  _| ' \/ _ \ ' \  | (__| ' \/ _` |  _|
|_|  \_, |\__|_||_\___/_||_|  \___|_||_\__,_|\__|
     |__/                                        
"""
help_embed = r"""
======[Commandes]======
* /help : voir la liste des commandes disponibles
* /leave : se déconnecter du chat
=======================
"""

def slowPrint(s):
    for c in s :
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)

# effacer la ligne précédente
def erase_line():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

# récupère l'adresse ipv4 de la machien
def get_local_ip() -> str:
    return socket.gethostbyname(socket.gethostname())

def is_ipv4_address(address:str) -> bool:
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

def select_ip() -> str:
    ip = "256.256.256.256"
    while not is_ipv4_address(ip):
        slowPrint("Entrez l'adresse ip du serveur : ")
        ip = input()
    return ip

def select_port() -> int:
    choice_port = False
    while not choice_port:
        slowPrint("Entrez un numéro de port : ")
        try:
            port = int(input())
            choice_port = True
        except ValueError:
            choice_port = False
        if len(str(port)) == 5:
            choice_port = True
        else:
            choice_port = False
    return int(port)

# gestion des commandes
def chat_commands(msg:str, conn, name, host:bool):
    global clients
    if host == True:
        host_command_embed = "Vous ne pouvez pas utiliser de commandes en tant qu'hôte de la discussion..."
        conn.send(host_command_embed.encode())
    else:
        if msg == "/help":
            conn.send(help_embed.encode())
        else:
            command_not_found_embed = "\nLa commande n'existe pas, tapez '/help' pour voir la liste des commandes disponibles\n"
            conn.send(command_not_found_embed.encode())

def host():
    global clients
    host = get_local_ip()
    port = 55555
    clients = {} # utilisateurs connectés

    os.system('cls' if os.name == 'nt' else 'clear')
    print(embed)
    print(f"Adresse IP : {str(host)}\nPort : {str(port)}\n\n=======================================\n")

    def handle_client(conn, addr):
        name = conn.recv(1024).decode()
        welcome_msg = f"\n=======================================\n\nBienvenue {name}! Tapez '/help' pour afficher la liste des commandes disponibles."
        conn.send(welcome_msg.encode())

        wait_msg = True
        while wait_msg:
            msg = conn.recv(1024).decode()
            if msg == "/leave":
                conn.close()
                del clients[conn]
                broadcast(f"{name} a quitté le chat.")
                wait_msg = False
            elif msg[0] == "/":
                print(f"L'utilisateur [{name}] a utilisé la commande '{msg}'")
                chat_commands(msg, conn, name, False)
            else:
                time = datetime.datetime.now().time()
                time_format = f"{time.hour}:{time.minute}:{time.second}"
                broadcast(f"[{time_format}]{name}: {msg}")

    # envoie message à tous les clients
    def broadcast(msg):
        for client in clients:
            client.send(msg.encode())
        print(msg) # affiche les messages pour l'hôte
    
    def host_send(): # thread pour que l'hôte puisse envoyer des messages
        while True:
            msg = input()
            if msg[0] == "/":
                print("Vous ne pouvez pas utiliser de commandes en tant qu'hôte...")
            erase_line()
            time = datetime.datetime.now().time()
            time_format = f"{time.hour}:{time.minute}:{time.second}"
            formatted_msg = f"[{time_format}]Hôte: {msg}"
            broadcast(formatted_msg)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Serveur en écoute sur {host}:{port}")

    host_chat_thread = threading.Thread(target=host_send)
    host_chat_thread.start()

    # accepter des nouvelles connexions    
    while True:
        conn, addr = server.accept()
        print(f"Nouvelle connexion établie avec {addr}")
        
        conn.send("NOM".encode()) # informer le client d'entrer son nom d'utilisateur
        name = conn.recv(1024).decode()
        clients[conn] = name
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def client():
    def receive():
        while True:
            try:
                msg = client_socket.recv(1024).decode()
                if msg == 'NOM':
                    client_socket.send(username.encode())
                else:
                    print(msg)
            except Exception as e:
                print(e)
                break # arreter si erreur

    def send():
        client_socket.send(username.encode())
        while True:
            msg = input()
            erase_line()
            client_socket.send(msg.encode())

    # config client
    os.system('cls' if os.name == 'nt' else 'clear')
    print(embed)

    host = select_ip()
    port = select_port()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    slowPrint("Entrez votre nom d'utilisateur : ")
    username = input()

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()

def setup():
    print(embed)
    choice_made = False
    while not choice_made:
        slowPrint("Voulez vous Héberger un salon ou en Rejoindre un ? (H / R) : ")
        choice = input().upper()
        if choice == "H":
            host()
            choice_made = True
        elif choice == "R":
            client()
            choice_made = True

setup()