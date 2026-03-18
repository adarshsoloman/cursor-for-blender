bl_info = {
    "name": "AI Assistant",
    "author": "Adarsh Soloman Banjare",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > AI Assistant",
    "description": "AI-powered natural language assistant for Blender",
    "category": "3D View",
}

import bpy
from . import properties, operators, panels, utils, api_client, code_executor

def register():
    properties.register_properties()
    operators.register()
    panels.register()
    
    # Start the queue processor loop on the main Blender thread
    if not bpy.app.timers.is_registered(utils.queue_processor):
        bpy.app.timers.register(utils.queue_processor)

def unregister():
    # Stop the queue processor loop
    if bpy.app.timers.is_registered(utils.queue_processor):
        bpy.app.timers.unregister(utils.queue_processor)
        
    panels.unregister()
    operators.unregister()
    properties.unregister_properties()
