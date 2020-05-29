import py
import pytest
import git
from vcsdeploy.config import DefaultConfig
from vcsdeploy.logic import UnknownRevisionError
from vcsdeploy.gitlogic import GitLogic

def create_repo(tmpdir):
    r = git.Repo.init(str(tmpdir))
    myfile = tmpdir.join('myfile.py')
    myfile.write('version = 1.0')

    r.index.add([str(myfile)])
    r.index.commit('initial checkin')
    r.create_tag('Version_1.0')

    myfile.write("ops, that's a bug")
    r.index.add([str(myfile)])
    r.index.commit('introduce a bug')
    r.create_tag('intermediate_tag')

    myfile.write('version = 1.1')
    r.index.add([str(myfile)])
    r.index.commit('fix the bug')
    r.create_tag('Version_1.1')

    myfile.write('version = none')
    r.index.add([str(myfile)])
    r.index.commit('one untagged commit')

    myfile.write('version = latest')
    r.index.add([str(myfile)])
    r.index.commit('latest untagged commit')
    return r

@pytest.fixture
def logic(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    repo = create_repo(tmpdir)
    config = DefaultConfig()
    config.path = str(tmpdir)
    return GitLogic(config)


def test_get_current_version(logic):
    repo = logic.repo
    assert logic.get_current_version() == 'Latest version'
    repo.git.checkout('Version_1.1')
    assert logic.get_current_version() == 'Version_1.1'
    repo.git.checkout('Version_1.0')
    assert logic.get_current_version() == 'Version_1.0'
    repo.git.checkout('master')
    assert logic.get_current_version() == 'Latest version'
    repo.git.checkout('HEAD~1')
    assert logic.get_current_version() is None
