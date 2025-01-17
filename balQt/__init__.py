import sys
import importlib
import os
import types
import re
from typing import Optional

# Type alias for a string representing a Qt binding
QtBindingType = str

# Module-level variable to store the name of the available Qt binding
QtBindings: Optional[QtBindingType] = None

# List of supported Qt binding names in preferred order
supported_qt_bindings = ["PySide6", "PyQt6", "PyQt5", "PySide2", "PyQt4", "PySide"]

# Check if any supported Qt binding has already been loaded into sys.modules
for qt_binding in supported_qt_bindings:
    if qt_binding in sys.modules:
        try:
            importlib.import_module(f"{qt_binding}.QtCore")
        except Exception:
            pass  # Ignore any errors and continue to check the next binding
        else:
            QtBindings = qt_binding  # Found a loaded binding
            break

# Attempt to load each supported binding in order if none were already imported
if not QtBindings:
    for qt_binding in supported_qt_bindings:
        try:
            importlib.import_module(f"{qt_binding}.QtCore")
            QtBindings = qt_binding
            break
        except ImportError:
            continue  # Skip to the next binding on failure

# Raise an error if no binding could be loaded
if not QtBindings:
    raise ImportError("Cannot load any of the supported Qt bindings: PySide6, PyQt6, PyQt5, PySide2, PyQt4, PySide")


def import_qt_module(module_name: str) -> types.ModuleType:
    """
    Import a module from the detected Qt binding.

    Args:
        module_name (str): Name of the Qt module to import (e.g., 'QtWidgets').

    Returns:
        types.ModuleType: The imported module from the chosen Qt binding.

    Raises:
        ImportError: If the module cannot be imported or no Qt binding is available.
    """
    global QtBindings
    if QtBindings:
        try:
            return importlib.import_module(f"{QtBindings}.{module_name}")
        except ImportError as e:
            raise ImportError(f"Module '{module_name}' could not be loaded: {str(e)}")
    raise ImportError("No Qt binding loaded.")


def __getattr__(name: str) -> types.ModuleType:
    """
    Dynamically import Qt modules on demand when accessed as attributes of this module.

    Args:
        name (str): Name of the Qt module to access.

    Returns:
        types.ModuleType: The imported Qt module.
    """
    return import_qt_module(name)


# Get the directory path of the current package for dynamic discovery
package_dir = os.path.dirname(__file__)

# List all Python files in the package folder excluding __init__.py
balQt_files = [
    f[:-3] for f in os.listdir(package_dir)
    if f.lower().endswith('.py') and f != '__init__.py'
]

# Aggregate all module and dynamic attribute names into __all__
balQt_attributes = list(set(balQt_files + ['balQt_attributes', 'qt_module'] + dir()))
__all__ = balQt_attributes

# Safely update __all__ with attributes from the chosen Qt binding
if QtBindings:
    try:
        qt_module = importlib.import_module(QtBindings)
        __all__ = balQt_attributes + [item for item in getattr(qt_module, '__all__', []) if item not in balQt_attributes]
    except Exception:
        pass  # Silently ignore any errors during dynamic updates


class QtModuleFinder:
    """
    Custom import hook to intercept and redirect `balQt.*` imports to the detected Qt binding.

    Attributes:
        package_name (str): The root package name for redirection.
    """

    def __init__(self, package_name: str):
        self.package_name = package_name

    def find_spec(self, name: str, path, target=None) -> Optional[importlib.machinery.ModuleSpec]:
        if name.startswith(self.package_name):
            if re.sub(r'^balQt\.', '', name) in balQt_attributes:
                return None  # Allow standard import for local modules
            qt_module_name = name.replace("balQt", QtBindings)
            try:
                return importlib.machinery.ModuleSpec(name, QtModuleLoader(qt_module_name))
            except ImportError:
                return None
        return None


class QtModuleLoader:
    """
    Custom module loader for dynamically resolving Qt modules.

    Attributes:
        module_name (str): Fully qualified name of the target module to load.
    """

    def __init__(self, module_name: str):
        self.module_name = module_name

    def create_module(self, spec) -> types.ModuleType:
        """Create an empty module instance."""
        return types.ModuleType(spec.name)

    def exec_module(self, module: types.ModuleType) -> None:
        """
        Execute the specified module, injecting it into sys.modules.

        Args:
            module (types.ModuleType): The module object to populate.

        Raises:
            ImportError: If the module cannot be imported.
        """
        try:
            imported_module = importlib.import_module(self.module_name)
            sys.modules[module.__name__] = imported_module
            module.__dict__.update(imported_module.__dict__)
        except ImportError:
            raise ImportError(f"Module '{self.module_name}' could not be loaded.")


# Add the custom finder to sys.meta_path to intercept relevant imports
sys.meta_path.insert(0, QtModuleFinder("balQt"))

# Description:
# This module dynamically detects and loads one of the supported Qt bindings for Python.
# It prioritizes any bindings already imported before attempting to load each binding in order.
# The `QtBindings` variable stores the name of the loaded binding, and an ImportError is raised if none are available.
