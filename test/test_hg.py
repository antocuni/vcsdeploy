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
    hg.update('Version 1.1')
    assert logic.get_current_version() == 'Version 1.1'
    hg.update(rev='Version 1.0')
    assert logic.get_current_version() == 'Version 1.0'
