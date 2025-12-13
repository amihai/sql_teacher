import logging
import logging.config
from pathlib import Path
from datetime import datetime

from settings import settings


def get_logging_config(app_type="frontend"):
    """
    Generate logging configuration with date-based log files.
    
    Args:
        app_type: Type of application - "frontend" or "backend"
    
    Returns:
        dict: Logging configuration dictionary
    """
  
    log_dir = settings.LOG_DIR / app_type
    log_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    log_filename = log_dir / f"{app_type}_{date_str}.log"
    
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "main_formatter": {
                "format": "{asctime} - {levelname} - {name} - {message}",
                "style": "{",
            },
            "console_formatter": {
                "format": "{levelname} - {name} - {message}",
                "style": "{",
            }
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(log_filename),
                "formatter": "main_formatter",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf-8"
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console_formatter"
            }
        },
        "loggers": {
            "frontend": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False,
            },
            "backend": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["file", "console"],
            "level": "INFO",
        }
    }
    
    return LOGGING


def setup_frontend_logging():
    """Setup logging configuration for frontend services"""

    config = get_logging_config("frontend")
    logging.config.dictConfig(config)
    
    logger = logging.getLogger("frontend")
    logger.info("=" * 80)
    logger.info("Frontend logging system initialized")
    logger.info(f"Log file: {config['handlers']['file']['filename']}")
    logger.info("=" * 80)
    
    return logger


def setup_backend_logging():
    """Setup logging configuration for backend services"""

    config = get_logging_config("backend")
    logging.config.dictConfig(config)
    
    logger = logging.getLogger("backend")
    logger.info("=" * 80)
    logger.info("Backend logging system initialized")
    logger.info(f"Log file: {config['handlers']['file']['filename']}")
    logger.info("=" * 80)
    
    return logger


def get_frontend_logger(name: str) -> logging.Logger:
    """Get a logger for frontend modules"""

    return logging.getLogger(f"frontend.{name}")


def get_backend_logger(name: str) -> logging.Logger:
    """Get a logger for backend modules"""

    return logging.getLogger(f"backend.{name}")