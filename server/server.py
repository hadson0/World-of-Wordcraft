import socket
import threading
import json
import sys

from game import Game
from utils.constants import *


class Server:

    def __init__(self, port=55555):
        self.host  = socket.gethostbyname(socket.gethostname())
        print(self.host)
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((self.host, self.port))
        self.socket.listen()

        self.client_names = {}
        self.lobbies = {}
        self.lobby_queue = []
        self.opponents = {}
        self.waiting_for_pair = None

        self.threads = []

    def run(self):
        print(f"Server is running on {self.host}:{self.port}")
        while True:
            client, address = self.socket.accept()
            print(f"Connection from {address}")
            thread = threading.Thread(
                target=self.handle_client, args=(client,))
            self.threads.append(thread)
            thread.start()

    def register_client(self, client):
        self.send_message(S_REGISTER, None, client)

        try:
            response_msg = json.loads(client.recv(1024).decode(ENCODING))
            msg_type = response_msg.get("type")
            payload = response_msg.get("payload")
            print(f"Received: {msg_type} {payload}")
        except:
            return

        if msg_type == C_NICKNAME:
            print(f"Client {payload} connected")
            self.client_names[client] = payload
            self.matchmaking(client)

        elif msg_type == C_LEAVE:
            self.disconnect(client)

    def matchmaking(self, client):
        if not self.lobby_queue:
            self.lobby_queue.append(client)

            while client in self.lobby_queue:
                continue
        else:
            while True:
                for other in self.lobby_queue:
                    if other != client:
                        if other in self.lobby_queue:
                            self.lobby_queue.remove(other)
                        if client in self.lobby_queue:
                            self.lobby_queue.remove(client)
                        self.start_game(client, other)
                        return

    def start_game(self, client1, client2):
        self.opponents[client1] = client2
        self.opponents[client2] = client1

        game = Game()
        self.lobbies[client1] = game
        self.lobbies[client2] = game

        game.add_player(client1)
        game.add_player(client2)

        game.start_game()
        target_words = game.get_target_words()

        print(
            f"Starting game between {self.client_names.get(client1)} and {self.client_names.get(client2)}")

        self.send_message(S_START_GAME, target_words, client1)
        self.send_message(S_START_GAME, target_words, client2)

    def get_scoreboard(self, client):
        opponent = self.opponents.get(client)
        if not opponent:
            return

        game = self.lobbies[client]
        player1 = self.client_names.get(client)
        player2 = self.client_names.get(opponent)
        score1 = game.get_player_points(client)
        score2 = game.get_player_points(opponent)

        if score1 > score2:
            winner = {"name": player1, "points": score1}
            loser = {"name": player2, "points": score2}
        else:
            winner = {"name": player2, "points": score2}
            loser = {"name": player1, "points": score1}

        return {"winner": winner, "loser": loser}

    def handle_client(self, client):
        self.register_client(client)

        while True:
            try:
                data = client.recv(1024).decode(ENCODING)
                if not data:
                    continue
                message = json.loads(data)
                print(f"Received: {message}")
                self.process_message(message, client)
            except:
                break

        self.send_to_opponent(S_LOBBY_CLOSED, None, client)
        self.disconnect(client)

    def disconnect(self, client):
        opponent = self.opponents.get(client)

        if not client or not opponent or not self.client_names.get(client):
            return

        print(f"Disconnecting {self.client_names.get(client)} and {self.client_names.get(opponent)}")

        if opponent in self.opponents:
            del self.opponents[opponent]

        if client in self.opponents:
            del self.opponents[client]

        if client in self.client_names:
            del self.client_names[client]

        if opponent in self.client_names:
            del self.client_names[opponent]

        if client in self.lobbies:
            del self.lobbies[client]

        if opponent in self.lobbies:
            del self.lobbies[opponent]

        client.close()

    def send_message(self, msg_type, payload, client):
        msg = {"type": msg_type, "payload": payload}
        msg = json.dumps(msg).encode(ENCODING)
        print(f"Sending: {msg} to {self.client_names.get(client)}")
        client.send(msg)

    def send_to_opponent(self, msg_type, payload, client):
        opponent = self.opponents.get(client)
        if not opponent or opponent not in self.client_names:
            return
        self.send_message(msg_type, payload, opponent)

    def process_message(self, msg, client):
        msg_type = msg.get("type")
        payload = msg.get("payload")
        lobby = self.lobbies[client]

        if msg_type == C_COMBINE:
            word1 = payload.get("word1")
            word2 = payload.get("word2")
            result = lobby.combine_words(word1, word2)
            self.send_message(S_COMB_RESULT, result, client)

        elif msg_type == C_GUESS:
            guess = payload.get("guess")
            target_idx = payload.get("idx")
            target = lobby.target_words[target_idx]
            lobby.make_guess(client, guess, target)
            points = lobby.get_player_points(client)
            self.send_message(S_GUESS_RESULT, points, client)

        elif msg_type == C_STOP:
            scores = self.get_scoreboard(client)
            self.send_message(S_FINAL_SCORE, scores, client)
            self.send_to_opponent(S_FINAL_SCORE, scores, client)

        elif msg_type == C_LEAVE:
            self.disconnect(client)
            self.disconnect(self.opponents[client])

    def __del__(self):
        self.socket.close()
