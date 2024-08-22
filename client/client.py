import socket
import threading
import json

from utils.constants import *


class Client:
    def __init__(self, controller, port=55555, ):
        self._controller = controller
        self.nickname = None

        self.host  = socket.gethostbyname(socket.gethostname())
        self.server_host = self.host # Change this to the server's IP address
        self.port = port

        self._socket = None

        self.closed = True
        self.started = False
        self.target_words = ["word1", "word2", "word3", "word4", "word5"]
        self._word_idx = 0
        self.points = 0

        self._thread = None

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.server_host, self.port))
        self._start()

    def _start(self):
        self.closed = False
        self.started = True

        self._thread = threading.Thread(target=self.__receive)
        self._thread.start()

    def register(self,):
        self.__send(C_NICKNAME, self.nickname)

    def combine_words(self, word1, word2):
        self.__send(C_COMBINE, {"word1": word1, "word2": word2})

    def make_guess(self, guess):
        self.__send(C_GUESS, {"guess": guess, "idx": self._word_idx})

    def next_word(self):
        self._word_idx += 1

    def stop1(self):
        self.__send(C_STOP, None)

    def __send(self, request, payload):
        msg = {"type": request, "payload": payload}
        print(f"Sending: {msg}")
        self._socket.send(json.dumps(msg).encode(ENCODING))

    def __receive(self):
        while not self.closed:
            try:
                data = self._socket.recv(1024).decode(ENCODING)
                message = json.loads(data)
                self.__process_message(message)
            except:
                break
        self.close()

    def __process_message(self, msg):
        print(f"Received: {msg}")
        msg_type = msg.get("type")
        payload = msg.get("payload")

        if msg_type == S_REGISTER:
            self.register()

        elif msg_type == S_START_GAME:
            self._word_idx = 0
            self.target_words = payload
            self._controller.on_game_start()

        elif msg_type == S_COMB_RESULT:
            self._controller.set_result(payload)

        elif msg_type == S_GUESS_RESULT:
            self._controller.set_points(payload)

        elif msg_type == S_LOBBY_CLOSED:
            self._word_idx = 0
            self._controller.on_lobby_closed()

        elif msg_type == S_FINAL_SCORE:
            self._controller.set_scoreboard(payload)

    def close(self):
        if not self.closed and self._socket and self.started:
            try:
                self.__send(C_LEAVE, None)
                self._socket.close()
            except:
                pass
            self.nickname = None
            self.closed = True
            self.started = False
            self._socket = None
