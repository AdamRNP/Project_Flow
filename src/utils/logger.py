# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:37:56 2025

@author: adamp
"""

"""
Logging facility for the application.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

# Global logger instance
_logger: Optional[logging.Logger] = None

def setup_logger(log_level: int = logging.INFO, log_to_file: bool = True) -> None:
    """Set up the application logger.
    
    Args:
        log_level: Logging level
        log_to_file: Whether to log to file
    """
    global _logger
    
    # Create logger
    logger = logging.getLogger("project_flow")
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.expanduser("~/.project_flow/logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # Create file handler
        log_file = os.path.join(log_dir, "project_flow.log")
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(file_handler)
    
    _logger = logger
    _logger.info("Logger initialized")

def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module.
    
    Args:
        name: Module name
        
    Returns:
        Logger instance for the module
    """
    global _logger
    
    # Initialize logger if not done yet
    if _logger is None:
        setup_logger()
    
    # Return child logger for the specified module
    return logging.getLogger(f"project_flow.{name}")
