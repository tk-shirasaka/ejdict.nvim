import pynvim
from .model import Model


@pynvim.plugin
class Ejdict(object):

    def __init__(self, nvim: pynvim.Nvim):
        self._nvim = nvim
        self._model = Model()
        self._bufnr = self._nvim.call('bufadd', 'ejdict')
        self._nvim.command('augroup ejdict')

    def _get_opts(self):
        window = self._nvim.current.window
        winWidth = window.width
        winHeight = window.height
        row = window.row
        col = window.col

        width = min(winWidth, 100)
        height = min(winHeight, 10)
        row = 1 if winHeight - row > (height / 2) else -1 - height
        col = 1 if winWidth - col > (width / 2) else col - width

        opts = dict(width=width, height=height, row=row, col=col)
        opts['relative'] = 'cursor'

        return opts

    @pynvim.command('EjdictToggle')
    def toggle(self):
        if self._nvim.call('exists', 'b:ejdict_enable'):
            del(self._nvim.current.buffer.vars['ejdict_enable'])
            self._nvim.command('autocmd! ejdict * <buffer>')
            self.clear()
        else:
            self._nvim.current.buffer.vars['ejdict_enable'] = 1
            self._nvim.command('autocmd ejdict CursorMoved,BufEnter <buffer> EjdictSearch')
            self._nvim.command('autocmd ejdict BufLeave <buffer> EjdictClear')
            self.search()

    @pynvim.command('EjdictClear')
    def clear(self):
        try:
            for winid in self._nvim.call('win_findbuf', self._bufnr):
                self._nvim.call('nvim_win_close', winid, False)
        except Exception:
            pass

    @pynvim.command('EjdictSearch')
    def search(self):
        self.clear()
        word = self._nvim.call('expand', '<cword>').lower()

        if not word:
            return

        for word in [word] + self._model.search_verb(word):
            results = self._model.search_word(word)

            if not len(results):
                continue

            buffer = self._nvim.buffers[self._bufnr]
            buffer.options['buftype'] = 'nofile'
            buffer.options['bufhidden'] = 'delete'
            buffer[:] = results
            self._nvim.call('nvim_open_win', self._bufnr, False, self._get_opts())
            self._nvim.options['ruler'] = False

