import re

class DefaultConfig(object):
    version_regex = '^Version'
    path = None


class AbstractLogic(object):
    def pull(self):
        raise NotImplementedError
    
    def get_current_version(self):
        raise NotImplementedError
    
    def get_list_of_versions(self):
        raise NotImplementedError

    def update_to(self, version):
        raise NotImplementedError
