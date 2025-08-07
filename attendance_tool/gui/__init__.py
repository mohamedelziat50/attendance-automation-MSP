"""
GUI Subpackage for Attendance Tool

This subpackage contains the graphical user interface components
for the attendance automation system.
"""

# The following lines exposes the launch_gui function for easy importing

# .gui : Relative import from the gui.py file in the same directory
# Import Purpose: Makes the function available in this __init__.py file
from .gui import launch_gui

# Special Python list that controls what gets exported
# ['launch_gui'] = Only this function will be available when someone imports
# from this subpackage (Other internal stuff are not exposed) - from attendance_tool.gui import launch_gui
__all__ = ["launch_gui"]
