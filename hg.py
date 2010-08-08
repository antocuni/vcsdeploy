import py
from mercurial import commands, ui, hg

class MercurialRepo(object):

    def __init__(self, path, create=False):
        self.ui = ui.ui()
        self.repo = hg.repository(self.ui, str(path), create)

    def __getattr__(self, name):
        cmd = getattr(commands, name)
        def fn(*args, **kwds):
            newargs = []
            for arg in args:
                if isinstance(arg, py.path.local):
                    arg = str(arg)
                newargs.append(arg)
            self.ui.pushbuffer()
            cmd(self.ui, self.repo, *newargs, **kwds)
            return self.ui.popbuffer()
        return fn


class MercurialLogic(object):

    def __init__(self, hg, config):
        self.hg = hg
        self.config = config

    def get_current_version(self):
        out = self.hg.identify().strip()
        if ' ' not in out:
            return None
        hash, tag = out.split(' ', 1)
        tag = tag.strip()
        if tag == 'tip':
            return 'Latest version'
        return tag

    def get_list_of_versions(self):
        pass

    def update_to(self, version):
        pass
