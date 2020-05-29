import re
import datetime
import py
import git
from vcsdeploy.logic import AbstractLogic, UnknownRevisionError


class GitLogic(AbstractLogic):

    def __init__(self, config):
        self.config = config
        self.repo = git.Repo(config.path)

    def _get_current_tag(self):
        for tag in self.repo.tags:
            if tag.commit == self.repo.head.commit:
                return tag
        return None

    def get_current_version(self):
        tag =self._get_current_tag()
        if tag is not None:
            return tag.name
        if self.repo.head.commit == self.repo.branches.master.commit:
            return 'Latest version'
        return None
