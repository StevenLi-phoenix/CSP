import random, sys, os
import logging, datetime, atexit
DEBUG = False
VERBOSE = False

class bcolors:  # console and log colors setting
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class LOG(logging.Logger):
    def __init__(self, log_path_and_name: str, logginglevel=logging.INFO, verbose: bool = True, debug: bool = False):
        """
        Initialize the logger
        create a logger with the given log_path_and_name and set the logging level
        if verbose is True, the logger will print the log to the console
        :param log_path_and_name: path and name of the log file
        :param logginglevel: [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        :param verbose: Boolean to print the log to the console
        """
        if not log_path_and_name.endswith('.log'):
            log_path_and_name += '.log'
        if debug: logginglevel = logging.DEBUG
        super().__init__(log_path_and_name, logginglevel)

        # split log file name and extension
        log_name, log_ext = os.path.splitext(log_path_and_name)
        # check if log file exists use absolute path
        if os.path.exists(os.path.abspath(log_path_and_name)):
            # change log file name by adding date and time
            log_path_and_name = log_name + '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + log_ext
        # check if log path exists
        log_path_and_name = check_path(log_path_and_name, create=True)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.handlers = []
        # create file handler and stream handler
        if verbose:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.handlers.append(ch)
        fh = logging.FileHandler(log_path_and_name)
        fh.setFormatter(formatter)
        self.handlers.append(fh)
        # set log level if debug is True to DEBUG else logginglevel
        if debug:
            self.setLevel(logging.DEBUG)
        else:
            self.setLevel(logginglevel)
        fh.setLevel(logging.DEBUG)
        self.info('Logging started')
        self.info('Logging level: %s' % logging.getLevelName(self.getEffectiveLevel()))
        self.info('Logging file: %s' % log_path_and_name)
        self.sys_info()
        atexit.register(self.close)

    def sys_info(self):
        """
        Print system information to the log
        This function is called in the __init__ function and only should be called once
        Some information is not available due to different OS and Python versions
        :return: None
        """
        self.debug('================= System Info: =================')
        self.debug('OS: ' + os.name)
        self.debug('Python version: ' + sys.version.replace('\n', ''))
        self.debug('Platform: ' + sys.platform)
        self.debug('Architecture: ' + sys.platform)
        self.debug('CPU: ' + os.uname().machine)
        self.debug('CPU count: ' + str(os.cpu_count()))
        try:
            self.debug('Memory: ' + str(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')) + ' bytes')
        except ValueError:
            self.debug('Memory: Unknown due to os.sysconf error')
        self.debug('Platform: ' + sys.platform)
        self.debug('Time: ' + str(datetime.datetime.now()))
        self.debug('User: ' + os.getlogin())
        self.debug('=================================================')

    def setLevel(self, level:[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]) -> None:
        """
        Set the logging level
        :param level: [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        :return: None
        """
        super().setLevel(level)
        for handler in self.handlers:
            handler.setLevel(level)

    def close(self):
        self.info('Logging stopped')
        self.info('Logging file closed')
        for handler in self.handlers:
            handler.close()
    # overwrite the default error method with red bcolors
    def error(self, msg, *args, **kwargs):
        super().error(bcolors.FAIL + str(msg) + bcolors.ENDC, *args, **kwargs)

    # overwrite the default warning method with yellow bcolors
    def warning(self, msg, *args, **kwargs):
        super().warning(bcolors.WARNING + str(msg) + bcolors.ENDC, *args, **kwargs)

    # overwrite the default info method with green bcolors
    def info(self, msg, *args, **kwargs):
        super().info(bcolors.OKGREEN + str(msg) + bcolors.ENDC, *args, **kwargs)

    # overwrite the default debug method with blue bcolors
    def debug(self, msg, *args, **kwargs):
        super().debug(bcolors.OKBLUE + str(msg) + bcolors.ENDC, *args, **kwargs)

    # overwrite the default critical method with red bcolors
    def critical(self, msg, *args, **kwargs):
        super().critical(bcolors.FAIL + str(msg) + bcolors.ENDC, *args, **kwargs)

    # overwrite the default exception method with red bcolors
    def exception(self, msg, *args, **kwargs):
        super().exception(bcolors.FAIL + str(msg) + bcolors.ENDC, *args, **kwargs)


# check path exists
def check_path(path: str, create: bool = True, overwrite: bool = False) -> str:
    """
    check file path exists, if not, create it if create is True
    if tried to create a file but it is the name of a directory, raise an error
    if path input is a directory and create is True, it will attempt to create it
    if the directory already exists, it will return the directory path
    :param path: directory path must end with '/' and could be relative or absolute
    :param create: bool to create path if not exists default is True
    :param overwrite: bool to overwrite file or directionary if exists default is False <!> be careful it can delete all
    :return: path string
    """
    """
    1. path is a file and it exists √
    2. path is directory and it exists √
    3. path is a file and it does not exists √
    4. path is a file and it does not exist and it's parent directory does exist √
    5. path is a file and it does not exist and it's parent directory does not exist √
    6. path is a directory and it does not exist √
    7. path is a directory and it does not exist and it's parent directory does exist √
    8. path is a directory and it does not exist and it's parent directory does not exist √
    9. path is a file and it does exist a directory √
    10. path is a directory and it does exist a file √
    """
    path = os.path.abspath(path)
    dir, file = os.path.split(path)[0], os.path.split(path)[1]
    if overwrite:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            else:
                os.rmdir(path)
    if create: os.makedirs(dir, exist_ok=True)
    return os.path.join(dir, file)


log = LOG(__name__, debug=DEBUG, verbose=VERBOSE)

try:
    import numpy as np
    USENUMPY = True
except ImportError:
    log.setLevel(logging.DEBUG)
    log.warning("numpy is not installed.Fallback to list")
    log.sys_info()
    USENUMPY = False

storage_old_print = print
class OutputCache:
    """
    A class to cache the output of a function
    """
    def __init__(self):
        """
        Initialize the cache
        """
        log.debug("OutputCache init")
        self.string = ""

    def print(self, string, end="\n") -> None:
        """
        Add a string to the cache
        :param string: string to add or class that could be converted to string by str()
        :param end: common end of the string
        :return: None
        """
        log.debug("OutputCache print {}".format(string))
        self.string += str(string) + end

    def flush(self) -> None:
        """
        Flush the cache to the output
        :return: None, Print cache to output
        """
        log.debug("OutputCache flush")
        storage_old_print(self.string)
        self.string = ""


P = OutputCache()


def print(string: str = "", **kwargs) -> None:
    """
    replace the default print function with the cacheOutput
    :param string: string to print
    :param kwargs: extra arguments to pass to the print function
    :return: None
    """
    P.print(string, **kwargs)
def flush() -> None:
    """
    flush the cache to the output
    :return: Print cache to output
    """
    P.flush()


class Pattern():
    """
    A class to handle pattern randomization
    """
    def __init__(self, n: int, sym: str):
        """
        Initialize the pattern
        :param n: number of pattern
        :param sym: symbol to use
        """
        log.debug("Pattern {}, {} init".format(n, sym))
        self._output(n, sym)
    def _output(self, n: int, sym: str) -> None:
        """
        Output the pattern
        :param n: number of pattern
        :param sym: symbol to use
        :return: random pattern from 1 to 3
        """
        random.choice([self.print_pattern_1, self.print_pattern_2, self.print_pattern_3])(int(n), sym)

    def print_pattern_1(self, n: int = 9, symbol: str = "#") -> None:
        log.debug("Pattern 1")
        for i in range(1, n + 2):
            print(symbol * i, end='')
            print(" " * ((n - i + 1) * 2), end='')
            print(symbol * i, end='')
            print()
        flush()

    def print_pattern_2(self, n: int = 9, symbol: str = "#") -> None:
        log.debug("Pattern 2")
        index = n // 2 + n % 2
        for i in range(index):
            print(" " * (index - i), end='')
            print(symbol * (2 * i + 2 - n % 2), end='')
            print(" " * (n // 2), end='')
            print()
        for i in range(index)[::-1][1:]:
            print(" " * (index - i), end='')
            print(symbol * (2 * i + 2 - n % 2), end='')
            print(" " * (n // 2), end='')
            print()
        flush()

    def print_pattern_3(self, n: int = 10, symbol: str = "#") -> None:
        log.debug("Pattern 3")
        if USENUMPY:
            array = np.zeros((n, n))
            for i in range(n):
                array[i, i] = 1
                array[i, n - i - 1] = 1
        else:
            array = [[0 for _ in range(n)] for _ in range(n)]
            for i in range(n):
                array[i][i] = 1
                array[i][n - i - 1] = 1
        for row in array:
            for col in row:
                print(symbol if col else " ", end='')
            print()
        flush()


if __name__ == '__main__':
    n, sym = input("Pattern[number<space>symbol]:").split(" ")
    Pattern(n, sym)
