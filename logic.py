import re

class DefaultConfig(object):
    version_regex = '^Version'


class AbstractLogic(object):
    def get_current_version(self):
        raise NotImplementedError
    
    def get_list_of_versions(self):
        raise NotImplementedError

    def update_to(self, version):
        raise NotImplementedError

