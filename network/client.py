import socket
import threading

from network.protocol import decode_message, encode_message


class GameClient:
    def __init__(self):
        self.socket = None
        self.running = False
        self.received_messages = []
        self.lock = threading.Lock()

    def connect(self, host, port=5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.running = True

        thread = threading.Thread(target=self.receive_loop, daemon=True)
        thread.start()

        print(f"[CLIENT] Connecté à {host}:{port}")

    def receive_loop(self):
        buffer = ""

        try:
            while self.running:
                data = self.socket.recv(4096)
                if not data:
                    break

                buffer += data.decode("utf-8")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not line.strip():
                        continue

                    message = decode_message(line)

                    with self.lock:
                        self.received_messages.append(message)

        except Exception as e:
            print(f"[CLIENT] Erreur réception : {e}")

        finally:
            self.running = False
            if self.socket:
                try:
                    self.socket.close()
                except Exception:
                    pass

    def send(self, message):
        if not self.socket or not self.running:
            return

        try:
            self.socket.sendall(encode_message(message))
        except Exception as e:
            print(f"[CLIENT] Erreur envoi : {e}")

    def get_messages(self):
        with self.lock:
            messages = self.received_messages[:]
            self.received_messages.clear()
        return messages

    def disconnect(self):
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass