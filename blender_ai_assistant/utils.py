import bpy
import threading
import queue
from . import api_client, code_executor

def log(message, level="INFO"):
    """
    Helper function to print formatted messages to the Blender System Console.
    Levels: INFO, WARNING, ERROR, DEBUG
    """
    prefix = f"[AI Assistant | {level}]"
    print(f"{prefix} {message}")


# ==============================================================================
# Threading / Async Request System
# ==============================================================================

# A queue to hold responses coming back from the API thread
api_queue = queue.Queue()

def execute_api_call_async(api_key, prompt, context_type="submit"):
    """
    Spawns a background thread to call the API so the Blender UI doesn't freeze.
    context_type: 'submit' (normal prompt) or 'test' (test connection button)
    """
    def worker():
        log(f"Starting API call on background thread (context: {context_type})", "DEBUG")
        result = api_client.send_prompt(api_key, prompt)
        # Put the result back on the queue to be read by the main thread
        api_queue.put({"context_type": context_type, "result": result})

    thread = threading.Thread(target=worker)
    thread.daemon = True # Kills thread if Blender closes
    thread.start()

def queue_processor():
    """
    Runs continuously via a bpy.app.timers timer.
    Checks if the background API thread has put a response into the queue.
    If so, it handles the UI updates on the main Blender thread.
    """
    try:
        # Try to get an item from the queue without blocking
        item = api_queue.get_nowait()
    except queue.Empty:
        # If queue is empty, just return 0.1 to tell Blender to check again in 0.1 seconds
        return 0.1

    # If we got an item, process it!
    context_type = item["context_type"]
    result = item["result"]
    scene = bpy.context.scene

    log(f"Queue processor handling result for {context_type}")

    if context_type == "test":
        scene.is_thinking = False
        if result["success"]:
            scene.last_exec_status = "success"
            scene.last_exec_message = "Connection successful!"
        else:
            scene.last_exec_status = "error"
            scene.last_exec_message = result["message"]

    elif context_type == "submit":
        scene.is_thinking = False
        
        if result["success"]:
            # 1. Try to extract the code
            extraction = code_executor.extract_code(result["message"])
            
            if not extraction["success"]:
                # The AI returned an ERROR string or bad formatting
                msg = scene.ai_chat_history.add()
                msg.role = "assistant"
                msg.content = extraction["message"].replace("\n", "<NL>")
                
                scene.last_exec_status = "error"
                scene.last_exec_message = "Generation failed"
            else:
                # 2. Add the actual extracted code to history so the user sees what is running
                code = extraction["code"]
                msg = scene.ai_chat_history.add()
                msg.role = "assistant"
                # Encode newlines to bypass Blender's StringProperty destruction
                msg.content = f"```python<NL>{code}<NL>```".replace("\n", "<NL>")
                
                # 3. Execute it!
                exec_result = code_executor.execute_code(code)
                
                if exec_result["success"]:
                    scene.last_exec_status = "success"
                    scene.last_exec_message = "Code executed successfully"
                else:
                    # Append the error as an AI message too
                    err_msg = scene.ai_chat_history.add()
                    err_msg.role = "assistant"
                    err_message = f"Execution failed:\n{exec_result['message']}"
                    err_msg.content = err_message.replace("\n", "<NL>")
                    
                    scene.last_exec_status = "error"
                    scene.last_exec_message = "Code execution failed"
        else:
            # Show error
            msg = scene.ai_chat_history.add()
            msg.role = "assistant"
            err_message = f"Network Error: {result['message']}"
            msg.content = err_message.replace("\n", "<NL>")
            
            scene.last_exec_status = "error"
            scene.last_exec_message = "API request failed."

    # Return 0.1 to keep the timer running forever
    return 0.1
