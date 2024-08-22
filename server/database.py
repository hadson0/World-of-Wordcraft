import sqlite3


class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self):
        db = sqlite3.connect(self.db_file)
        cursor = db.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS combinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word1 TEXT NOT NULL,
            word2 TEXT NOT NULL,
            result TEXT NOT NULL
        )
        ''')
        db.close()

    def add_combination(self, word1, word2, result):
        exists = self.check_combination(word1, word2) is not None

        if exists:
            return False

        db = sqlite3.connect(self.db_file)
        cursor = db.cursor()

        cursor.execute('''
        INSERT INTO combinations (word1, word2, result)
        VALUES (?, ?, ?)
        ''', (word1, word2, result))
        db.commit()

        db.close()

    def check_combination(self, word1, word2):
        db = sqlite3.connect(self.db_file)
        cursor = db.cursor()

        cursor.execute('''
        SELECT result FROM combinations
        WHERE word1 = ? AND word2 = ?
        ''', (word1, word2))
        result = cursor.fetchone()
        result = None if result is None else result[0]

        db.close()

        return result

    def get_random_words(self, num_words):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        #return ["Lava", "Magma", "Mountain", "Ash", "Sun"]

        cursor.execute('''
        SELECT result FROM combinations
        WHERE id >= 50 AND id <= 200
        ORDER BY RANDOM() LIMIT ?
        ''', (num_words,))

        random_words = [row[0] for row in cursor.fetchall()]
        conn.close()

        if len(random_words) < num_words:
            return ["Wine", "Oasis", "Rain", "Perfume", "Sun"]

        return random_words
