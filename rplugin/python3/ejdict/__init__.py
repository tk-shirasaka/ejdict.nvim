import pynvim
import sqlite3

SOURCE = 'rplugin/python3/ejdict/__init__.py'
TARGET = 'ejdic-hand-sqlite/ejdict.sqlite3'
EJDICT_PATH = __file__.replace(SOURCE, TARGET)


@pynvim.plugin
class Ejdict(object):

    def __init__(self, nvim: pynvim.Nvim):
        self._nvim = nvim
        self._con = sqlite3.connect(EJDICT_PATH)
        self._bufnr = self._nvim.call('bufadd', 'ejdict')

        if not self._nvim.call('exists', 'ejdict#auto_start'):
            self._nvim.vars['ejdict#auto_start'] = ['text']

    def _search_verb(self, word):
        sql = 'SELECT word FROM verbs WHERE verb=? LIMIT 30'
        search = (word, )
        return [x[0] for x in self._con.execute(sql, search)]

    def _search_word(self, word):
        sql = 'SELECT mean FROM items WHERE word=? LIMIT 30'
        search = (word, )
        return [x[0] for x in self._con.execute(sql, search)]

    def _get_opts(self):
        window = self._nvim.current.window
        winWidth = window.width
        winHeight = window.height
        row, col = window.cursor

        width = min(winWidth, 100)
        height = min(winHeight, 10)
        row = 1 if winHeight - row > (height / 2) else -1 - height
        col = 1 if winWidth - col > (width / 2) else col - width

        opts = dict(width=width, height=height, row=row, col=col)
        opts['relative'] = 'cursor'

        return opts

    @pynvim.command('Ejdict', nargs=1)
    def search(self, args):
        results = []
        word = args[0].lower()

        for word in [word] + self._search_verb(word):
            results = self._search_word(word)

            if not len(results):
                continue

            buffer = self._nvim.buffers[self._bufnr]
            buffer.options['buftype'] = 'nofile'
            buffer.options['bufhidden'] = 'delete'
            buffer[:] = results
            self._nvim.call('nvim_open_win', self._bufnr, False, self._get_opts())
            self._nvim.options['ruler'] = False

    @pynvim.command('EjdictCword')
    def search_cword(self):
        word = self._nvim.call('expand', '<cword>')
        if word:
            self.search([word])

    @pynvim.autocmd('CursorMoved')
    def cursor_moved(self):
        try:
            for winid in self._nvim.call('win_findbuf', self._bufnr):
                self._nvim.call('nvim_win_close', winid, False)
        except Exception:
            pass

        filetype = self._nvim.current.buffer.options['filetype']
        if filetype in self._nvim.vars['ejdict#auto_start']:
            self.search_cword()
