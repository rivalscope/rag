import logging
import sys
from typing import List, Dict, Any

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Intercept standard logging messages toward Loguru
    
    This allows us to capture and format logs from libraries 
    that use the standard logging module
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure logging for the application
    
    Args:
        log_level: The minimum log level to capture
    """
    # Remove default loggers
    logger.remove()
    
    # Add stderr logger
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {extra}",
        level=log_level,
        backtrace=True,
        diagnose=True
    )
    
    # Intercept standard library logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # Also log from these libraries
    for logger_name in ["uvicorn", "uvicorn.error", "fastapi"]:
        lib_logger = logging.getLogger(logger_name)
        lib_logger.handlers = [InterceptHandler()]


def get_logger():
    """Get the configured logger"""
    return logger