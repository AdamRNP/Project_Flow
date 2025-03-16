# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:28:08 2025

@author: adamp
"""

"""
Centralized logging configuration and utility functions.
"""
import os
import logging
import logging.config
import yaml
from typing import Optional, Dict, Any

# Default logging format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class AppLogger:
    """Application logger utility class."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to ensure only one logger instance exists."""
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger if not already initialized."""
        if not self._initialized:
            self.root_logger = logging.getLogger('project_flow')
            self.configure_default_logging()
            self._initialized = True
    
    def configure_default_logging(self) -> None:
        """Configure logging with default settings."""
        # Create handlers
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(DEFAULT_FORMAT)
        console_handler.setFormatter(formatter)
        
        # Configure root logger
        self.root_logger.setLevel(logging.DEBUG)
        self.root_logger.addHandler(console_handler)
        
        # Default log file in user's home directory
        log_dir = os.path.join(os.path.expanduser('~'), '.project_flow', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(
            os.path.join(log_dir, 'project_flow.log')
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.root_logger.addHandler(file_handler)
    
    def configure_from_file(self, config_path: str) -> None:
        """Configure logging using a YAML configuration file.
        
        Args:
            config_path: Path to the YAML configuration file
        
        Raises:
            FileNotFoundError: If the configuration file doesn't exist
            yaml.YAMLError: If the configuration file has invalid YAML
        """
        if not os.path.exists(config_path):
            self.root_logger.error(f"Logging configuration file not found: {config_path}")
            raise FileNotFoundError(f"Logging configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                logging.config.dictConfig(config)
                self.root_logger.info(f"Loaded logging configuration from {config_path}")
        except yaml.YAMLError as e:
            self.root_logger.error(f"Error parsing logging configuration: {str(e)}")
            raise
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger for a specific module.
        
        Args:
            name: Name of the module, typically __name__
            
        Returns:
            Logger instance for the module
        """
        return logging.getLogger(f"project_flow.{name}")


# Global function to get a logger
def get_logger(name: str) -> logging.Logger:
    """Get a logger for a module.
    
    Args:
        name: Name of the module, typically __name__
        
    Returns:
        Logger instance for the module
    """
    return AppLogger().get_logger(name)
