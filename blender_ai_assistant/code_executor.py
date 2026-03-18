import bpy
import re
import traceback

def extract_code(response_text):
    """
    Extracts the Python code from the AI's markdown response.
    Returns the code string, or None if extraction failed.
    """
    response_text = response_text.strip()
    
    # Check if the AI returned a hard error (non-API instruction)
    if response_text.startswith("ERROR:"):
        return {"success": False, "code": None, "message": response_text}

    # Find the python code block using regex
    # Match ```python at the start, capture everything inside, until ```
    pattern = r"```(?:python)?\s*(.*?)```"
    match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        code = match.group(1).strip()
        return {"success": True, "code": code, "message": ""}
        
    # If no code block is found, see if the whole thing is just raw code
    if "import bpy" in response_text or "bpy." in response_text:
         return {"success": True, "code": response_text, "message": ""}

    return {"success": False, "code": None, "message": "ERROR: Could not find valid Python code in the AI response."}

def execute_code(code_string):
    """
    Executes the extracted Python code in the Blender environment.
    Catches ALL exceptions to prevent Blender from crashing.
    Returns a dict with success status and any error messages.
    """
    
    # Provide the standard bpy context to the exec environment
    exec_globals = {"bpy": bpy}
    
    try:
        # Find a 3D Viewport to override the execution context
        # This is critical because Blender timers restrict bpy.ops commands
        window = bpy.context.window_manager.windows[0]
        screen = window.screen
        area = next((a for a in screen.areas if a.type == 'VIEW_3D'), None)
        region = next((r for r in area.regions if r.type == 'WINDOW'), None) if area else None
        
        override = {'window': window, 'screen': screen, 'area': area, 'region': region}
    except Exception:
        override = {} # Fallback if UI is headless
        
    try:
        # Compile first to catch SyntaxErrors early
        compiled_code = compile(code_string, "<ai_generated>", "exec")
        
        # Execute the compiled code within the overridden 3D Viewport context
        with bpy.context.temp_override(**override):
            exec(compiled_code, exec_globals)
            
            # Push to the undo stack so the user can hit Ctrl+Z to revert AI actions
            bpy.ops.ed.undo_push(message="AI Assistant Action")
            
        # Force a UI and dependency graph update so the new objects appear instantly
        bpy.context.view_layer.update()
        for area in bpy.context.screen.areas:
            area.tag_redraw()
        
        return {"success": True, "message": "Execution successful"}
        
    except SyntaxError as e:
        error_msg = f"SyntaxError on line {e.lineno}:\n{e.msg}"
        return {"success": False, "message": error_msg}
        
    except Exception as e:
        # Catch everything else (AttributeError, TypeError, KeyError, etc)
        # We don't want the full huge traceback in the UI panel, just the last line or two
        tb_lines = traceback.format_exception(type(e), e, getattr(e, '__traceback__', None))
        # Usually the last line holds the actual error message like "AttributeError: ... "
        error_msg = tb_lines[-1].strip()
        return {"success": False, "message": error_msg}
