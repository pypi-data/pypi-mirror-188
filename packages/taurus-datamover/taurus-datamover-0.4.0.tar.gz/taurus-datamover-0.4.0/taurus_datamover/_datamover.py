import tempfile
import time
from pathlib import Path
import os
import warnings
import subprocess


class Wrapper:
    """
    General python wrapper for cluster command line tools.
    """

    def __init__(self, path_to_exe: str, glob_pattern: str,
                 verbosity: int = 0):
        """
        Sets up a wrapper for a set of command line tools matching glob_pattern.

        Parameters
        ----------
        path_to_exe : str
            Path to the datamover executables on the cluster, example: /usr/bin/
        glob_pattern : str
            pattern used to find executables within, example: 'ws_*'
        verbosity : int, optional
            set the verbosity level, by default 0. Possible values are:
            0 : no verbosity - all output is captured by subprocess and not printed. Both stdout and stderr can later be extracted from process by `process.communicate()` (which waits for the process to finish).
            1 : some verbosity - only stout is captured by subprocess and can be processed later. Errors are printed immediately (useful if you  want to know what is going on when you use Datamover directly in a jupyter notebook).
            2 : very verbose: all output is printed immediately and nothing is captured by subprocess
        """
        self.path_to_exe = Path(path_to_exe)
        self.verbosity = verbosity
        exe_files = self.path_to_exe.glob(glob_pattern)
        self.exe = [f.name for f in exe_files if os.access(f, os.X_OK)]
        self.current_command = None

    def __getattr__(self, attr):
        '''
        Modify the __getattr__ special function: Each executable name in self.exe becomes a callable function that executes the respective shell script.
        '''
        if attr in self.exe:
            self.current_command = attr
            return self._execute
        else:
            raise AttributeError('No executable with name {} found in path {}'.format(attr, str(self.path_to_exe)))

    def _execute(self, *args):
        """
        Execute the current command with arguments and return its output.

        Parameters
        ----------
        args : list of str
            The arguments to the command to be executed, e.g. for the command "dtls" sensible arguments would be ["-l", "/foo/bar"]

        Returns
        -------
        subprocess.Popen object (see: https://docs.python.org/3/library/subprocess.html#popen-constructor)
        """
        # we append the argument "--blocking" so that datamover uses srun
        # instead of sbatch for all arguments. That way, we can use
        # subprocess.poll to figure out whether the operation has finished.
        # Also, dtls behaves the same as all other processes (by default all
        # processes except dtls use sbatch)
        args = [self.path_to_exe / self.current_command] + list(args)
        stdout = subprocess.PIPE if self.verbosity < 2 else None
        stderr = subprocess.PIPE if self.verbosity < 1 else None
        return subprocess.Popen(args, stdout=stdout, stderr=stderr)

    def is_cluster(self):
        return len(self.exe) > 0


class Datamover(Wrapper):
    """
    Python wrapper for the zih datamover tools that enable exchanging files between a project space on the cluster and a fileserver share via an export node.

    See also
    --------
    .. [0] https://doc.zih.tu-dresden.de/data_transfer/datamover/
    """

    def __init__(
            self, path_to_exe: str = '/sw/taurus/tools/slurmtools/default/bin/', blocking: bool = True, verbosity: int = 0):
        """
        Sets up a datamover wrapper.

        Parameters
        ----------
        path_to_exe : str, optional
            Path to the datamover executables on the cluster, by default: /sw/taurus/tools/slurmtools/default/bin/
        blocking : bool, optional
            if set to True (default) the slurm jobs are spawned by srun, which runs in the foreground and we can see the output
            if set to False , the slurm jobs (except dtls) are spawned by sbatch, which runs the job in the background and we would need to extract the output from its log file
            Do not change this unless you have a good reason to do so.
        verbosity : int, optional
            set the verbosity level, by default 0. Possible values are:
            0 : no verbosity - all output is captured by subprocess and not printed. Both stdout and stderr can later be extracted from process by `process.communicate()` (which waits for the process to finish).
            1 : some verbosity - only stout is captured by subprocess and can be processed later. Errors are printed immediately (useful if you  want to know what is going on when you use Datamover directly in a jupyter notebook).
            2 : very verbose: all output is printed immediately and nothing is captured by subprocess
        """
        self.blocking = blocking
        super().__init__(
            path_to_exe=path_to_exe,
            verbosity=verbosity,
            glob_pattern='dt*')

    def _execute(self, *args):
        """
        Execute the current command with arguments and return its output.

        Parameters
        ----------
        args : list of str
            The arguments to the command to be executed, e.g. for the command "dtls" sensible arguments would be ["-l", "/foo/bar"]

        Returns
        -------
        subprocess.Popen object (see: https://docs.python.org/3/library/subprocess.html#popen-constructor)
        """
        # we append the argument "--blocking" so that datamover uses srun
        # instead of sbatch for all arguments. That way, we can use
        # subprocess.poll to figure out whether the operation has finished.
        # Also, dtls behaves the same as all other processes (by default all
        # processes except dtls use sbatch)
        if self.blocking:
            args += ('--blocking',)
        return super()._execute(*args)


class Workspace(Wrapper):
    """Python wrapper for the workspace management tools on taurus

        See also
        --------
        .. [0] https://doc.zih.tu-dresden.de/data_lifecycle/workspaces/
    """

    def __init__(
            self, path_to_exe: str = '/usr/bin/', verbosity: int = 0):
        """
        Initialize a wrapper for the workspace management tools on taurus.

        Parameters
        ----------
        path_to_exe : str
            Path to the datamover executables on the cluster, default: /usr/bin/
        verbosity : int, optional
            set the verbosity level, by default 0. Possible values are:
            0 : no verbosity - all output is captured by subprocess and not printed. Both stdout and stderr can later be extracted from process by `process.communicate()` (which waits for the process to finish).
            1 : some verbosity - only stout is captured by subprocess and can be processed later. Errors are printed immediately (useful if you  want to know what is going on when you use Datamover directly in a jupyter notebook).
            2 : very verbose: all output is printed immediately and nothing is captured by subprocess
        """
        super().__init__(
            path_to_exe=path_to_exe,
            verbosity=verbosity,
            glob_pattern='ws_*')


class CacheWorkspace:
    """Manage a cache workspace on the cluster

    Attributes
    ----------
    id : str
        identifier of the cache workspace
    name : str
        path to the cache workspace
    ws : Workspace object
        wrapper for the workspace manager tools on taurus

    Methods
    -------
    cleanup : releases the workspace on taurus - the data can still be recovered within 1 day after cleanup
    """

    def __init__(self, path_to_exe: str = '/usr/bin/',
                 id: str = 'cache', expire_in_days: int = 1) -> None:
        '''Allocate a workspace on the cluster where we can store temporary files.

        If the workspace already exists, it is automatically reused.

        Parameters
        ----------
        path_to_exe : str, optional
            path to the ws_* executables, by default '/usr/bin/'
        id : str, optional
            The id of the workspace. On the filesystem, it will be called something like /scratch/ws/0/username-id , by default 'cache'
        expire_in_days : int, optional
            this determines the number of tays until the workspace automatically expires, by default 1
        '''
        self.ws = Workspace(path_to_exe=path_to_exe)
        self.id = id
        self.expire_in_days = expire_in_days
        self.name = None
        self._mk_cache()

    def cleanup(self) -> None:
        '''release the allocated workspace.

        Files will be deleted automatically one day after release.
        '''
        process = self.ws.ws_release(self.id)
        waitfor(process)
        self.name = None

    def _mk_cache(self) -> str:
        '''Allocate a workspace on the cluster

        Returns
        -------
        str
            path to allocated workspace
        '''
        process = self.ws.ws_allocate(self.id, str(
            self.expire_in_days), '-c', 'temporary_files')
        out, _ = process.communicate()
        self.name = out.strip().decode('utf-8')
        assert Path(
            self.name).exists(), 'Could not create cache workspace with id {} and path {}'.format(
            self.id, self.name)
        assert self.name.startswith('/'), 'Cache workspace did not return an absolute path but {}'.format(self.name)

    def __enter__(self) -> None:
        if self.name is None:
            self._mk_cache()
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        if self.name is not None:
            self.cleanup()


def save_to_project(save_fn: callable, file_path: str, *args, file_path_arg_pos: int = 0,
                    cache_workspace: CacheWorkspace = None, path_to_datamover: str = '/sw/taurus/tools/slurmtools/default/bin/', path_to_workspace_tools: str = '/usr/bin/', quiet=False, **kw):
    '''Save data to a project space.

    Since we don't have direct access, we first save to a temporary file on a workspace and then copy to the project space.

    Parameters
    ----------
    save_fn : callable
        function that saves the data to a file. Must accept the file path as a string in a positional argument.
    file_path : str
        full path (on the project space) where the file should be saved
    file_path_arg_pos : int, optional
        position of the argument that defines the file path in `save_fn`
    path_to_datamover : str, optional
        path to the datamover tools, by default '/sw/taurus/tools/slurmtools/default/bin/'
    path_to_workspace_tools: str, optional
        path to the wrkspace tools, by default '/usr/bin/'
    cache_workspace : CacheWorkspace, optional
        A cache workspace on the cluster; if None is provided, a temporary workspace will be created and deleted once the process was successful, by default None
    '''
    file_path = file_path.replace("\\", "/")
    full_path = Path(file_path)

    cleanup_cache = False
    if cache_workspace is None:
        cleanup_cache = True
        cache_workspace = CacheWorkspace(path_to_exe=path_to_workspace_tools)
    # if we have write access to the target directory, we can write directly
    # there
    if os.access(full_path.parent, os.W_OK):
        args = args[0:file_path_arg_pos] + \
            (str(full_path),) + args[file_path_arg_pos:]
        return save_fn(*args, **kw)
    # if the target is a write protected project space, we need to use the
    # datamover tools
    dm = Datamover(path_to_exe=path_to_datamover)
    with tempfile.TemporaryDirectory(prefix=cache_workspace.name + '/') as tmp:
        temp_file = Path(tmp) / full_path.name
        args = args[0:file_path_arg_pos] + \
            (str(temp_file),) + args[file_path_arg_pos:]
        output = save_fn(*args, **kw)
        waitfor(dm.dtcp(str(temp_file), str(full_path)), quiet=quiet)
        print('target file: {}'.format(str(full_path)))
    if cleanup_cache:
        cache_workspace.cleanup()
    return output


def waitfor(process: subprocess.Popen, timeout_in_s: float = -1,
            discard_output: bool = True, quiet: bool = True) -> int:
    """
    Wait for a process to complete.

    Parameters
    ----------
    process: subprocess.Popen object (e.g. returned by the Datamover class)
    timeout_in_s: float, optional (default: endless)
        Timeout in seconds. This process will be interrupted when the timeout is reached.
    discard_output: bool, optional (default: True)
        The default behavior is to discard the process output (to avoid leaving open file pointers). If you need the output of the command, use discard_output=False.
    Returns
    -------
    int exit code of the process
    """
    start_time = time.time()
    if not quiet:
        print("Waiting .", end='', flush=True)
    while process.poll() is None:
        time.sleep(0.5)
        if not quiet:
            print(".", end='', flush=True)
        if timeout_in_s > 0 and (time.time() - start_time) > timeout_in_s:
            print("\n")
            warnings.warn(
                'Timeout while waiting for process: ' + ' '.join([str(arg) for arg in process.args]))
            process.kill()
            return process.poll()
    exit_code = process.poll()
    if discard_output:
        out, err = process.communicate()
        warning_message = 'process: {}\nexited with error: {}\nand output: {}'.format(
            ' '.join([str(arg) for arg in process.args]), err.strip().decode('utf-8'), out.strip().decode('utf-8'))
    else:
        warning_message = 'process: {}\nexited with error.'.format(' '.join([str(arg) for arg in process.args]))
    if exit_code > 0:
        warnings.warn(warning_message)
    return process.poll()
