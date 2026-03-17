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

        self.players = {}
        self.lock = threading.Lock()
        self.host_socket = None
        self.game_started = False

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
            with self.lock:
                if self.host_socket is None:
                    self.host_socket = client_socket

                is_host = client_socket == self.host_socket

                player_data = {
                    "id": message["id"],
                    "nom": message["nom"],
                    "couleur": message.get("couleur", [180, 180, 180]),
                    "x": message.get("x", 220),
                    "y": message.get("y", 360),
                    "score": message.get("score", 0),
                    "vies": message.get("vies", 10),
                    "is_host": is_host
                }

                self.players[client_socket] = player_data

            self.send_player_list()

            if self.game_started:
                try:
                    client_socket.sendall(encode_message({"type": "START_GAME"}))
                except Exception:
                    self.remove_client(client_socket)

        elif msg_type == "START_GAME":
            with self.lock:
                if client_socket != self.host_socket:
                    return
                self.game_started = True

            self.broadcast({"type": "START_GAME"})

        elif msg_type == "PLAYER_STATE":
            with self.lock:
                if client_socket in self.players:
                    self.players[client_socket]["x"] = message.get("x", self.players[client_socket]["x"])
                    self.players[client_socket]["y"] = message.get("y", self.players[client_socket]["y"])
                    self.players[client_socket]["score"] = message.get("score", self.players[client_socket]["score"])
                    self.players[client_socket]["vies"] = message.get("vies", self.players[client_socket]["vies"])
                    self.players[client_socket]["couleur"] = message.get("couleur", self.players[client_socket]["couleur"])
                    self.players[client_socket]["nom"] = message.get("nom", self.players[client_socket]["nom"])
                    self.players[client_socket]["facing_right"] = message.get("facing_right", True)

            self.broadcast(message, exclude=client_socket)

        elif msg_type == "CHAT":
            self.broadcast(message)

    def send_player_list(self):
        with self.lock:
            if self.host_socket is not None and self.host_socket not in self.players and len(self.players) > 0:
                self.host_socket = next(iter(self.players.keys()))

            for sock, pdata in self.players.items():
                pdata["is_host"] = sock == self.host_socket

            player_list = list(self.players.values())

        self.broadcast({
            "type": "PLAYER_LIST",
            "players": player_list,
            "game_started": self.game_started
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

            if client_socket == self.host_socket:
                self.host_socket = next(iter(self.players.keys()), None)

            if len(self.players) == 0:
                self.game_started = False

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
            self.host_socket = None
            self.game_started = False

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