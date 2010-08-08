from vcsdeploy.logic import DefaultConfig
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


def test_get_list_of_versions(logic):
    assert logic.get_list_of_versions() == ['Version 1.1', 'Version 1.0']


def test_update_to(logic):
    myfile = logic.config.path.join('myfile.py')
    logic.update_to('Version 1.0')
    assert myfile.read() == 'version = 1.0'
    logic.update_to('Version 1.1')
    assert myfile.read() == 'version = 1.1'
