import logging
import sys
import ctypes

# Enable ANSI escape code processing on Windows
def enable_windows_ansi_support():
    if sys.platform.startswith('win'):
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to logging levels"""
    COLORS = {
        "WARNING": "\033[93m",  # Yellow
        "INFO": "\033[0m",     # White
        "DEBUG": "\033[94m",    # Light Blue
        "CRITICAL": "\033[95m", # Bright Magenta
        "ERROR": "\033[91m",    # Red
    }
    RESET_COLOR = "\033[0m"  # Reset to default

    def format(self, record):
        log_fmt = self._fmt
        format_orig = self._style._fmt

        # Modify the original format to include color codes
        if record.levelname in self.COLORS:
            self._style._fmt = self.COLORS[record.levelname] + log_fmt + self.RESET_COLOR

        # Call the original formatter class to do the grunt work
        formatted_message = super().format(record)

        # Restore the original format for subsequent messages
        self._style._fmt = format_orig

        return formatted_message

class Logger:
    def __init__(self, name, log_level):
        enable_windows_ansi_support()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

# usage
if __name__ == "__main__":
    logger = Logger("test", logging.DEBUG)
    logger.info("This is an info message")
    logger.error("This is an error message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
