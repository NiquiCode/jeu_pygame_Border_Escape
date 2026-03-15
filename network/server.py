import socket
import threading

from network.protocol import encode_message, decode_message


class GameServer:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False

        # Associe chaque socket client à ses infos joueur
        self.players = {}
        self.lock = threading.Lock()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        self.running = True

        thread = threading.Thread(target=self.accept_clients, daemon=True)
        thread.start()

        print(f"[SERVER] Serveur lancé sur {self.host}:{self.port}")

    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print("[SERVER] Client connecté :", addr)

                with self.lock:
                    self.clients.append(client_socket)

                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                thread.start()

            except OSError:
                break

    def handle_client(self, client_socket):
        buffer = ""

        while self.running:
            try:
                data = client_socket.recv(4096)

                if not data:
                    break

                buffer += data.decode()

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)

                    if not line.strip():
                        continue

                    message = decode_message(line)
                    self.handle_message(client_socket, message)

            except Exception as e:
                print("[SERVER] Erreur client :", e)
                break

        self.remove_client(client_socket)

    def handle_message(self, client_socket, message):
        msg_type = message.get("type")

        if msg_type == "JOIN":
            player_data = {
                "id": message["id"],
                "nom": message["nom"],
                "couleur": message.get("couleur", [180, 180, 180])
            }

            with self.lock:
                self.players[client_socket] = player_data

            self.send_player_list()

        elif msg_type == "START_GAME":
            self.broadcast({"type": "START_GAME"})

        elif msg_type == "PLAYER_STATE":
            self.broadcast(message, exclude=client_socket)

        elif msg_type == "CHAT":
            self.broadcast(message)

    def send_player_list(self):
        with self.lock:
            player_list = list(self.players.values())

        self.broadcast({
            "type": "PLAYER_LIST",
            "players": player_list
        })

    def broadcast(self, message, exclude=None):
        dead_clients = []

        with self.lock:
            clients_copy = self.clients[:]

        for client in clients_copy:
            if client == exclude:
                continue

            try:
                client.sendall(encode_message(message))
            except Exception:
                dead_clients.append(client)

        for dead in dead_clients:
            self.remove_client(dead)

    def remove_client(self, client_socket):
        with self.lock:
            if client_socket in self.clients:
                self.clients.remove(client_socket)

            if client_socket in self.players:
                del self.players[client_socket]

        try:
            client_socket.close()
        except Exception:
            pass

        self.send_player_list()

    def stop(self):
        self.running = False

        with self.lock:
            clients_copy = self.clients[:]
            self.clients.clear()
            self.players.clear()

        for client in clients_copy:
            try:
                client.close()
            except Exception:
                pass

        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass