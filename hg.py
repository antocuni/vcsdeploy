import re
import py
from mercurial import commands, ui, hg

from vcsdeploy.logic import AbstractLogic

class MercurialRepo(object):

    def __init__(self, path, create=False):
        self.path = path
        self.repo = hg.repository(ui.ui(), str(path), create)
        self.ui = self.repo.ui

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


class MercurialLogic(AbstractLogic):

    def __init__(self, config):
        self.config = config
        self.hg = MercurialRepo(config.path, create=False)

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
        out = self.hg.tags()
        versions = []
        for line in out.splitlines():
            tag, rev = line.rsplit(' ', 1)
            tag = tag.strip()
            if re.match(self.config.version_regex, tag):
                versions.append(tag)
        return versions

    def update_to(self, version):
        self.hg.update(version)
