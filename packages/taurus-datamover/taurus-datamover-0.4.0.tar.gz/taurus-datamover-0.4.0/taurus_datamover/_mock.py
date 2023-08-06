from pathlib import Path
import tempfile
import os
import shutil

my_path = Path(__file__).parent


class MockCluster:
    def __init__(self, commands: list = ['dtls', 'dtcp', 'dtrm', 'dtmv', 'dtrsync'],
                 dtwrapper: str = 'dtwrapper') -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.tempdir.name)
        self.bin_path = Path(self.tempdir.name) / 'bin'
        self.workspace_exe_path = self.bin_path
        self.scratch_path = self.temp_path / 'scratch'
        self.scratch_path.mkdir(parents=True, exist_ok=True)
        self._source_path = my_path / 'mock_cluster_files'
        self._commands = commands
        self._dtwrapper_path = self.bin_path / dtwrapper

    def save_test_file(save_fn, target_path, testdata):
        save_fn(target_path, testdata)

    def __enter__(self):
        shutil.copytree(str(self._source_path), self.bin_path)
        for command in self._commands:
            os.symlink(
                self._dtwrapper_path, self.bin_path / command)
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.cleanup()

    def cleanup(self):
        self.tempdir.cleanup()


class RealCluster:
    def __init__(self, bin_path: str = '/sw/taurus/tools/slurmtools/default/bin/',
                 workspace_exe_path: str = '/usr/bin/') -> None:
        from ._datamover import CacheWorkspace, Datamover
        self.bin_path = Path(bin_path)
        self.workspace_exe_path = Path(workspace_exe_path)
        self._datamover = Datamover(path_to_exe=bin_path)
        self._workspace = CacheWorkspace(id='test_cache', path_to_exe=workspace_exe_path)
        self.tempdir = tempfile.TemporaryDirectory(prefix=self._workspace.name + '/')
        self.temp_path = Path(self.tempdir.name)
        self.scratch_path = Path('/scratch/ws/0/')

    def save_test_file(self, save_fn, target_path, testdata, *arg, **kwarg):
        from ._datamover import waitfor
        temp_file = tempfile.TemporaryFile(prefix=self._workspace.name + '/')
        save_fn(temp_file, testdata, *arg, **kwarg)
        process = self._datamover.dtcp(str(temp_file), str(target_path))
        waitfor(process)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.cleanup()

    def cleanup(self):
        self._workspace.cleanup()


def get_test_cluster():
    '''Returns a Cluster object for testing depending on the environment.

    If the file /sw/taurus/tools/slurmtools/default/bin/dtls exists, a real cluster is returned, otherwise, a mock cluster is returned.'''
    if Path('/sw/taurus/tools/slurmtools/default/bin/dtls').exists():
        # we are on a real cluster, use the real thing
        return RealCluster()
    else:
        return MockCluster()
