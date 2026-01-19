import logging
from loguru import logger

class InterceptHandler(logging.Handler):
    """Capture logs Django and redirect in Loguru"""
    
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging():
    """seetings logging for Django"""
    
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
    
    for name in logging.root.manager.loggerDict:
        if name.startswith("uvicorn.") or name.startswith("gunicorn."):
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = False
    
    loggers = {
        "django": "INFO",
        "django.request": "WARNING",
        "django.db.backends": "INFO",  # SQL logs
        "django.security": "WARNING",
        "django.server": "INFO",
        "django.template": "WARNING",
        "reviews": "DEBUG",
    }
    
    for logger_name, level in loggers.items():
        logging.getLogger(logger_name).setLevel(level)
        logging.getLogger(logger_name).handlers = []
        logging.getLogger(logger_name).propagate = True