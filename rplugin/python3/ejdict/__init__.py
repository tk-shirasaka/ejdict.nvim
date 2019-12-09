import pynvim
import sqlite3

EJDICT_PATH = 'ejdic-hand-sqlite/ejdict.sqlite3'


@pynvim.plugin
class Ejdict(object):

    def __init__(self, nvim: pynvim.Nvim):
        self._nvim = nvim
        self._con = sqlite3.connect(EJDICT_PATH)

    def _search_verb(self, word):
        sql = 'SELECT word FROM verbs WHERE verb=? LIMIT 30'
        search = (word, )
        return [x[0] for x in self._con.execute(sql, search)]

    def _search_word(self, word):
        sql = 'SELECT mean FROM items WHERE word=? LIMIT 30'
        search = (word, )
        return [x[0] for x in self._con.execute(sql, search)]

    @pynvim.command('Ejdict', nargs=1)
    def search(self, word):
        word = 'abases'
        results = []

        for word in [word] + self._search_verb(word):
            results = self._search_word(word)

            if len(results):
                break

        self._nvim.current.buffer = results
