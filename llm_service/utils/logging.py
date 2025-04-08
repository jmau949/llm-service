"""
Logging Utilities
----------------
Utilities for setting up logging.
"""

import os
import logging
import sys
from typing import Optional


def setup_logging(
    log_level: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging with the specified configuration.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log format string
        
    Returns:
        Configured logger instance
    """
    # Get log level from environment or parameter
    level_str = log_level or os.environ.get('LOG_LEVEL', 'INFO')
    level = getattr(logging, level_str.upper(), logging.INFO)
    
    # Get log format from environment or parameter
    format_str = log_format or os.environ.get(
        'LOG_FORMAT',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format=format_str,
        stream=sys.stdout  # Use stdout instead of stderr
    )
    
    # Create and configure logger for this module
    logger = logging.getLogger('llm_service')
    logger.setLevel(level)
    
    # Ensure logging handlers don't duplicate
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(format_str))
        logger.addHandler(handler)
    
    # Log initial configuration
    logger.info(f"Logging initialized with level={level_str}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)