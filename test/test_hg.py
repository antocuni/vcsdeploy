from vcsdeploy.logic import DefaultConfig
from vcsdeploy.hg import MercurialLogic, MercurialRepo

def pytest_funcarg__hg(request):
    tmpdir = request.getfuncargvalue('tmpdir')
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


def test_get_current_version(hg):
    logic = MercurialLogic(hg, config=None)
    assert logic.get_current_version() == 'Latest version'
    hg.update('Version 1.1')
    assert logic.get_current_version() == 'Version 1.1'
    hg.update(rev='Version 1.0')
    assert logic.get_current_version() == 'Version 1.0'
    hg.update()
    assert logic.get_current_version() == 'Latest version'


def test_get_list_of_versions(hg):
    logic = MercurialLogic(hg, config=DefaultConfig())
    assert logic.get_list_of_versions() == ['Version 1.1', 'Version 1.0']


def test_update_to(hg):
    logic = MercurialLogic(hg, config=DefaultConfig())
    myfile = hg.path.join('myfile.py')
    logic.update_to('Version 1.0')
    assert myfile.read() == 'version = 1.0'
    logic.update_to('Version 1.1')
    assert myfile.read() == 'version = 1.1'
