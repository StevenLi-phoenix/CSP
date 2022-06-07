import random, sys, os
import logging, datetime, atexit

# ======================================================== config ========================================================
DEBUG = False
VERBOSE = False
# ======================================================== classes ========================================================
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
    def __init__(self, log_path_and_name: str=None, logginglevel=logging.INFO, verbose: bool = True, debug: bool = False):
        """
        Initialize the logger
        create a logger with the given log_path_and_name and set the logging level
        if verbose is True, the logger will print the log to the console
        :param log_path_and_name: path and name of the log file
        :param logginglevel: [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        :param verbose: Boolean to print the log to the console
        """
        if not log_path_and_name:
            log_path_and_name = f"log/{os.path.split(sys.argv[0])[1].split('.')[0]}.log"
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
        self.checkList = []

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

    def CHECK(self):
        self.debug('================= Check: =================')
        self.sys_info()
        for check in self.checkList:
            self.debug(check)
        self.debug('================= Check: =================')

    def add_check_list(self, check):
        """
        Add a check to the check list, this must can be converted to a string
        :param check: object to be added to the check list
        :return: True if check is added, False if check is already in the check list
        """
        try:
            _ = str(check)
            self.checkList.append(check)
            return True
        except:
            return False


    def setLevel_manual(self, level) -> None:
        """
        Set the logging level
        :param level: [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        :return: None
        """
        super().setLevel(level)
        self.setLevel(level)
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
class imported_module:
    """
    This class is used to manage imported modules status
    """
    def __init__(self):
        self.__imported_modules = {}
    def add(self, module_name: str, status: bool = True):
        self.__imported_modules[module_name] = status
    def remove(self, module_name: str):
        del self.__imported_modules[module_name]
    def get(self, module_name: str):
        return self.__imported_modules.get(module_name) # return None if not found return False if not imported return True if imported
    def get_all(self):
        return self.__imported_modules
    def __contains__(self, item):
        return item in self.__imported_modules
    def __iter__(self):
        return iter(self.__imported_modules)
    def __len__(self):
        return len(self.__imported_modules)
    def __str__(self):
        return str(self.__imported_modules)
    def __repr__(self):
        return repr(self.__imported_modules)
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
# ======================================================== basic methods ========================================================
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
# ======================================================== init ========================================================
log = LOG(debug=DEBUG, verbose=VERBOSE)
im = imported_module()
P = OutputCache()
log.add_check_list(im)
# ======================================================== external packages ========================================================
# put external and optional packages here
try:
    import numpy as np
    im.add('numpy')
except ImportError:
    log.setLevel(logging.DEBUG)
    log.warning("numpy is not installed.Fallback to list")
    log.sys_info()
    im.add('numpy', False)
try:
    import uuid4
    im.add('uuid4')
except ImportError:
    log.setLevel(logging.DEBUG)
    log.warning("uuid4 is not installed.Fallback to random")
    log.sys_info()
    im.add('uuid4', False)

# ======================================================== rewrite methods ========================================================
storage_old_print = print
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
# ======================================================== main ========================================================
total = 0
class rabbit:
    def __init__(self):
        global total
        total += 2
        if im.get('uuid4'):
            self.id = uuid4.uuid4()
        else:
            self.id = random.randint(0, 1000000)
        self.name = "rabbit_" + str(self.id)
        self.child = []

    def reproduce(self):
        log.debug("reproducing {}".format(self.name))
        for i in self.child:
            i.reproduce()
        self.child.append(rabbit())

test = False
if __name__ == "__main__":
    if test:
        log.setLevel(logging.DEBUG)
        log.debug("test")
        log.sys_info()
        log.debug("imported_module: {}".format(im))
        log.debug("OutputCache: {}".format(P))
        log.debug("total: {}".format(total))
        n = 100
    else:
        n = int(input("How many rabbits? "))
    ra = rabbit()
    month = 0  # 0 is January, 11 is December
    month_dic = {0: "January", 1: "February", 2: "March", 3: "April", 4: "May", 5: "June", 6: "July", 7: "August",8: "September", 9: "October", 10: "November", 11: "December"}
    while total < n:
        if month % 3 == 0:
            ra.reproduce()
        month_index = month % 12
        year = month // 12
        print("Yr:{},\t {}:\t {} rabbits".format(year, month_dic[month_index], total))
        log.info("Yr:{},\t {}:\t total: {}".format(year, month_dic[month_index], total))
        month += 1
    month -= 1 # reset last add month
    year = month // 12 # assert month_index is defined
    month_index = month % 12 # assert month_index is defined
    print("Yr:{}, {}: {} rabbits".format(year, month_dic[month_index], total))
    flush()
