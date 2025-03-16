# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 15:09:55 2025

@author: adamp
"""

import os
import importlib.util
import inspect
from typing import Dict, List, Type

class PluginBase:
    """Base class for all plugins"""
    plugin_name = "Base Plugin"
    plugin_description = "Base plugin class"
    plugin_version = "1.0.0"
    
    def __init__(self, app_context):
        self.app_context = app_context
        
    def initialize(self):
        """Initialize plugin resources"""
        pass
        
    def cleanup(self):
        """Clean up plugin resources"""
        pass

class PluginManager:
    """Handles discovery, loading and management of all plugin modules"""
    
    def __init__(self, app_context):
        self.app_context = app_context
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_classes: Dict[str, Type[PluginBase]] = {}
        self.plugin_dirs = [
            "./plugins",           # Built-in plugins
            "./user_plugins",      # User-installed plugins
            os.path.expanduser("~/.openfoam_gui/plugins")  # User-specific plugins
        ]
        
    def discover_plugins(self) -> List[str]:
        """Scan directories for available plugins"""
        discovered_plugins = []
        
        for plugin_dir in self.plugin_dirs:
            if not os.path.exists(plugin_dir):
                continue
                
            for item in os.listdir(plugin_dir):
                module_path = os.path.join(plugin_dir, item)
                
                # Check if it's a directory with an __init__.py file
                if os.path.isdir(module_path) and os.path.exists(os.path.join(module_path, "__init__.py")):
                    plugin_name = item
                    discovered_plugins.append((plugin_name, os.path.join(module_path, "__init__.py")))
                
                # Or a single Python file
                elif item.endswith(".py"):
                    plugin_name = item[:-3]  # Remove .py extension
                    discovered_plugins.append((plugin_name, module_path))
        
        return discovered_plugins
        
    def load_plugin(self, plugin_name, plugin_path):
        """Load a specific plugin by name and path"""
        try:
            # Import the module
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                print(f"Failed to load plugin spec: {plugin_name}")
                return False
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin classes (subclasses of PluginBase)
            for item_name, item in inspect.getmembers(module):
                if (inspect.isclass(item) and 
                    issubclass(item, PluginBase) and 
                    item is not PluginBase):
                    
                    # Store the plugin class
                    self.plugin_classes[item.plugin_name] = item
                    
                    # Instantiate the plugin
                    plugin_instance = item(self.app_context)
                    self.plugins[item.plugin_name] = plugin_instance
                    
                    # Initialize the plugin
                    plugin_instance.initialize()
                    
                    print(f"Loaded plugin: {item.plugin_name} v{item.plugin_version}")
                    return True
            
            print(f"No valid plugin class found in {plugin_name}")
            return False
            
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {str(e)}")
            return False
            
    def initialize_all_plugins(self):
        """Discover and load all available plugins"""
        discovered = self.discover_plugins()
        
        for plugin_name, plugin_path in discovered:
            self.load_plugin(plugin_name, plugin_path)
