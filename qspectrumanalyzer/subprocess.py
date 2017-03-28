import sys, subprocess

# Basic attributes and exceptions
PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT
DEVNULL = subprocess.DEVNULL
SubprocessError = subprocess.SubprocessError
TimeoutExpired = subprocess.TimeoutExpired
CalledProcessError = subprocess.CalledProcessError

# Windows-only attributes and functions
if sys.platform == 'win32':
    import msvcrt
    import _winapi

    # creationflags
    CREATE_NEW_CONSOLE = subprocess.CREATE_NEW_CONSOLE
    CREATE_NEW_PROCESS_GROUP = subprocess.CREATE_NEW_PROCESS_GROUP

    # startupinfo
    STARTUPINFO = subprocess.STARTUPINFO
    STARTF_USESTDHANDLES = subprocess.STARTF_USESTDHANDLES
    STARTF_USESHOWWINDOW = subprocess.STARTF_USESHOWWINDOW
    SW_HIDE = subprocess.SW_HIDE

    # file handles
    Handle = subprocess.Handle
    STD_INPUT_HANDLE = subprocess.STD_INPUT_HANDLE
    STD_OUTPUT_HANDLE = subprocess.STD_OUTPUT_HANDLE
    STD_ERROR_HANDLE = subprocess.STD_ERROR_HANDLE

    def make_inheritable_handle(fd):
        """Create inheritable duplicate of handle from file descriptor"""
        h = _winapi.DuplicateHandle(
            _winapi.GetCurrentProcess(),
            msvcrt.get_osfhandle(fd),
            _winapi.GetCurrentProcess(), 0, 1,
            _winapi.DUPLICATE_SAME_ACCESS
        )
        return subprocess.Handle(h)


def hide_console_window(startupinfo=None):
    """Returns altered startupinfo to hide console window on Windows"""
    if sys.platform != 'win32':
        return None

    if not startupinfo:
        startupinfo = subprocess.STARTUPINFO()

    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return startupinfo


class Popen(subprocess.Popen):
    """subprocess.Popen with ability to hide console window on Windows"""
    def __init__(self, *pargs, console=True, **kwargs):
        if not console:
            kwargs['startupinfo'] = hide_console_window(kwargs.get('startupinfo'))
        super().__init__(*pargs, **kwargs)


def call(*pargs, console=True, **kwargs):
    """subprocess.call with ability to hide console window on Windows"""
    if not console:
        kwargs['startupinfo'] = hide_console_window(kwargs.get('startupinfo'))
    return subprocess.call(*pargs, **kwargs)


def check_call(*pargs, console=True, **kwargs):
    """subprocess.check_call with ability to hide console window on Windows"""
    if not console:
        kwargs['startupinfo'] = hide_console_window(kwargs.get('startupinfo'))
    return subprocess.check_call(*pargs, **kwargs)


def check_output(*pargs, console=True, **kwargs):
    """subprocess.check_output with ability to hide console window on Windows"""
    if not console:
        kwargs['startupinfo'] = hide_console_window(kwargs.get('startupinfo'))
    return subprocess.check_output(*pargs, **kwargs)
