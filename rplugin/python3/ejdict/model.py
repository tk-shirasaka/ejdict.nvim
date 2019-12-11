from .utils import ejdict_connect


class Model():

    def __init__(self):
        self._con = ejdict_connect()

    def query(self, sql, params=()):
        return self._con.execute(sql, params)

    def search_verb(self, word):
        return [x[0] for x in self.query(
            'SELECT word FROM verbs WHERE verb=? LIMIT 30', (word, ))]

    def search_word(self, word):
        return [x[0] for x in self.query(
            'SELECT mean FROM items WHERE word=? LIMIT 30', (word, ))]
