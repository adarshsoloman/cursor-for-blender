bl_info = {
    "name": "AI Assistant",
    "author": "Adarsh Soloman Banjare",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > AI Assistant",
    "description": "AI-powered natural language assistant for Blender",
    "category": "3D View",
}

from . import properties, operators, panels, utils

def register():
    properties.register_properties()
    operators.register()
    panels.register()

def unregister():
    panels.unregister()
    operators.unregister()
    properties.unregister_properties()
