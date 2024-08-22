import replicate
import os
from sklearn.metrics.pairwise import cosine_similarity

TOKEN = os.environ["REPLICATE_API_TOKEN"]

import database as db
import numpy as np
from utils.constants import *


class Game:
    def __init__(self):
        self.players = []
        self.__db = db.Database('database.db')
        self.__db.create_table()
        self.target_words = []
        self.points = {}
        self.active = False

        self.max_players = 2
        self.min_players = 2

        self.api = replicate.Client(api_token= TOKEN)

    def get_target_words(self, num=5):
        self.target_words = self.__db.get_random_words(num)
        return self.target_words

    def start_game(self):
        self.active = True
        return self.target_words

    def add_player(self, player):
        if len(self.players) >= self.max_players or self.active:
            return False

        self.players.append(player)
        self.points[player] = 0
        return True

    def remove_player(self, player):
        self.players.remove(player)

    def get_player_points(self, player):
        return round(self.points[player], 2)

    def make_guess(self, player, guess, target):
        correct = guess == target
        if correct:
            self.points[player] += 1
        else:
            similarity = self.__compare_words(guess, target)
            self.points[player] += round(similarity, 2)
        return self.points[player]

    def combine_words(self, word1, word2):
        result = self.__db.check_combination(word1, word2)
        result = self.__generate_word(
            word1, word2) if result is None else result

        return "None" if result is None else result

    def __compare_words(self, word1, word2):
        emb1 = self.api.run(
            "replicate/all-mpnet-base-v2:b6b7585c9640cd7a9572c6e129c9549d79c9c31f0d3fdce7baac7c67ca38f305",
            input={"text": word1}
        )[0]["embedding"]
        emb1 = np.array(emb1).reshape(1, -1)

        emb2 = self.api.run(
            "replicate/all-mpnet-base-v2:b6b7585c9640cd7a9572c6e129c9549d79c9c31f0d3fdce7baac7c67ca38f305",
            input={"text": word2}
        )[0]["embedding"]
        emb2 = np.array(emb2).reshape(1, -1)

        similarity = cosine_similarity(emb1, emb2)[0][0]
        return similarity

    def __generate_word(self, word1, word2):
        result = ""
        rep_input = {
            "top_k": 0,
            "top_p": 0.9,
            "prompt": f"{word1}, {word2}",
            "max_tokens": 6,
            "min_tokens": 0,
            "temperature": 1.1,
            "system_prompt": "You are a helpful assistant",
            "length_penalty": 0.85,
            "stop_sequences": "<|end_of_text|>,<|eot_id|>",
            "prompt_template": PROMPT_TEMPLATE,
            "presence_penalty": 1.15,
            "log_performance_metrics": False
        }
        prediction = self.api.run(
            "meta/meta-llama-3-70b-instruct",
            input=rep_input
        )

        for event in prediction:
            result += str(event)

        if result == "" or result == "None":
            return None
        else:
            result = result.replace("\"", "")
            return result
