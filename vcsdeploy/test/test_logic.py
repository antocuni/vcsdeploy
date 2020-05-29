import py
import pytest
from vcsdeploy.config import DefaultConfig
from vcsdeploy.logic import UnknownRevisionError
from vcsdeploy.hg import MercurialLogic, MercurialRepo

class BaseTestLogic(object):

    LogicClass = None

    @pytest.fixture
    def logic(self, request):
        self.tmpdir = request.getfuncargvalue('tmpdir')
        self.create_test_repo(self.tmpdir)
        config = DefaultConfig()
        config.path = self.tmpdir
        return self.LogicClass(config)



class TestHgLogic(BaseTestLogic):

    LogicClass = MercurialLogic

    def create_test_repo(self, tmpdir):
        self._hg = MercurialRepo(tmpdir, create=True)
        myfile = tmpdir.join('myfile.py')
        myfile.write('version = 1.0')
        self.commit_file(myfile, 'initial checkin', tag='Version_1.0')
        myfile.write("ops, that's a bug")
        self.commit_file(myfile, 'introduce a bug', tag='intermediate_tag')
        myfile.write('version = 1.1')
        self.commit_file(myfile, 'fix the bug', tag='Version_1.1')

    def commit_file(self, fname, message, tag=None):
        self._hg.add(fname)
        self._hg.commit(message=message)
        if tag:
            self._hg.tag(tag)

    def test_get_current_version(self, logic):
        hg = logic.hg
        assert logic.get_current_version() == 'Latest version'
        hg.update('Version_1.1')
        assert logic.get_current_version() == 'Version_1.1'
        hg.update(rev='Version_1.0')
        assert logic.get_current_version() == 'Version_1.0'
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

def test_get_current_revision(logic):
    rev0 = logic.get_current_revision()
    logic.update_to('Version 1.0')
    rev1 = logic.get_current_revision()
    assert rev0 != rev1
    logic.update_to(rev0)
    assert logic.get_current_revision() == rev0


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

def test_log(tmpdir, logic):
    logfile = tmpdir.join('log')
    config = DefaultConfig()
    config.path = logic.hg.path
    config.logfile = str(logfile)
    logic = MercurialLogic(config)
    #
    logic.update_to('Version 1.0')
    rev0 = logic.get_current_revision()
    logic.update_to('Version 1.1')
    rev1 = logic.get_current_revision()
    #
    lines = logfile.readlines()
    assert len(lines) == 2
    assert lines[0].endswith('updated to: %s Version 1.0\n' % rev0)
    assert lines[1].endswith('updated to: %s Version 1.1\n' % rev1)