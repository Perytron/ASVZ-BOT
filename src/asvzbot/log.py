# Import from Python standard library
import logging
import datetime

class CustomFormatter(logging.Formatter):
    '''
    Expand the standard logging package with variable log format and colors.
    Taken (and modified) from https://alexandra-zaharia.github.io/posts/make-your-own-custom-color-formatter-with-python-logging/
    '''

    # Define multiple colors
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__() # We can utilize this method to access, for example, the variable 'blue' without having to hard code the base class: "self.blue" instead of "CustomFormatter.blue"
        self.fmt = fmt

        # Formats for each error level that the built in logger has
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Create custom logger logging all five levels
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define format for logs
fmt = '%(asctime)s | %(levelname)8s | %(message)s'

# Create stdout handler for logging to the console
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(fmt))

# Create file handler for logging to a file (uncomment for usage)
# today = datetime.date.today()
# file_handler = logging.FileHandler('my_app_{}.log'.format(today.strftime('%Y_%m_%d')))
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(logging.Formatter(fmt))

# Add both handlers to the logger
logger.addHandler(stdout_handler)
# logger.addHandler(file_handler) (uncomment for usage)