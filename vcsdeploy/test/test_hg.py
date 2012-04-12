import py
from vcsdeploy.logic import DefaultConfig, UnknownRevisionError
from vcsdeploy.hg import MercurialLogic, MercurialRepo

def create_repo(tmpdir):
    hg = MercurialRepo(tmpdir, create=True)
    myfile = tmpdir.join('myfile.py')

    myfile.write('version = 1.0')
    hg.add(myfile)
    hg.commit(message='initial checkin')
    hg.tag('Version 1.0')

    myfile.write("ops, that's a bug")
    hg.commit(message='introduce a bug')
    hg.tag('intermediate tag')

    myfile.write('version = 1.1')
    hg.commit(message='fix the bug')
    hg.tag('Version 1.1')
    return hg

def pytest_funcarg__logic(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    hg = create_repo(tmpdir)
    config = DefaultConfig()
    config.path = hg.path
    return MercurialLogic(config)
    

def test_get_current_version(logic):
    hg = logic.hg
    assert logic.get_current_version() == 'Latest version'
    hg.update('Version 1.1')
    assert logic.get_current_version() == 'Version 1.1'
    hg.update(rev='Version 1.0')
    assert logic.get_current_version() == 'Version 1.0'
    hg.update()
    assert logic.get_current_version() == 'Latest version'
    hg.update(rev=1)
    assert logic.get_current_version() is None


def test_get_list_of_versions(logic):
    assert logic.get_list_of_versions() == ['Version 1.1', 'Version 1.0']


def test_update_to(logic):
    myfile = logic.config.path.join('myfile.py')
    logic.update_to('Version 1.0')
    assert myfile.read() == 'version = 1.0'
    logic.update_to('Version 1.1')
    assert myfile.read() == 'version = 1.1'

def test_unknown_revision(logic):
    py.test.raises(UnknownRevisionError, "logic.update_to('foobar')")
    py.test.raises(UnknownRevisionError, "logic.update_to('xxx 1.2.3')")


def test_pull(tmpdir):
    # setup a "remote" repo where the "development" will go on, and a "local"
    # one where the program is installed. The idea is that the local will pull
    # from the remote
    remotedir = tmpdir.join('remote')
    localdir = tmpdir.join('local')
    hg_remote = create_repo(remotedir)
    hg_remote.clone(localdir)

    # simulate some development
    myfile_remote = remotedir.join('myfile.py')
    myfile_remote.write('version = 1.2')
    hg_remote.commit(message='new fancy features')
    hg_remote.tag('Version 1.2')
    
    # use Version 1.1 in production
    config = DefaultConfig()
    config.path = localdir
    logic = MercurialLogic(config)
    logic.update_to('Version 1.1')
    assert logic.get_current_version() == 'Version 1.1'

    # now, let's look for updates
    logic.pull()
    assert logic.get_current_version() == 'Version 1.1'
    assert logic.get_list_of_versions() == ['Version 1.2', 'Version 1.1', 'Version 1.0']
    logic.update_to('Version 1.2')
    assert logic.get_current_version() == 'Version 1.2'
    
