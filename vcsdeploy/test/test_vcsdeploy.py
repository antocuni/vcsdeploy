import py
from vcsdeploy.logic import DefaultConfig, load_config

def test_load_config(tmpdir):
    configfile = tmpdir.join('config.py')
    configfile.write(py.code.Source("""
        class Config(object):
             x = 42
             version_regex = 'foo'
        """))
    Config = load_config(str(configfile))
    assert Config.x == 42
    assert Config.path is None # from DefaultConfig
    assert Config.version_regex == 'foo' # from Config
    #
    mro = Config.__mro__
    assert len(mro) == 4
    assert mro[0] is Config
    assert mro[1].__name__ == 'Config' # the original Config class in the file
    assert mro[2] is DefaultConfig
    assert mro[3] is object

    
