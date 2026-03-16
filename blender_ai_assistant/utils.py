import bpy

def log(message, level="INFO"):
    """
    Helper function to print formatted messages to the Blender System Console.
    Levels: INFO, WARNING, ERROR, DEBUG
    """
    prefix = f"[AI Assistant | {level}]"
    print(f"{prefix} {message}")
    
    # In future weeks, this could also write to a physical log file if needed
    pass
