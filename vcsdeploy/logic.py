
def load_config(configfile):
    """
    Load a class named Config from ``configfile``.
    
    If the class Config does not inherit from DefaultConfig, a new class
    inheriting from Config and DefaultConfig is automatically created. This
    way, we are sure that DefaultConfig is always in the __mro__
    """
    dic = {}
    execfile(configfile, dic)
    Config = dic['Config']
    if DefaultConfig not in Config.__bases__:
        newbases = (Config, DefaultConfig)
        Config = type('Config', newbases, {})
    return Config


class DefaultConfig(object):
    version_regex = '^Version'
    path = None
    editable_revision = False
    show_revision = True
    logfile = None

class VcsError(Exception):
    pass

class UnknownRevisionError(VcsError):
    pass

class AbstractLogic(object):
    def pull(self):
        raise NotImplementedError
    
    def get_current_version(self):
        raise NotImplementedError

    def get_current_revision(self):
        raise NotImplementedError

    def get_list_of_versions(self):
        raise NotImplementedError

    def update_to(self, version):
        raise NotImplementedError

