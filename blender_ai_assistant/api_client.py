import urllib.request
import urllib.error
import json

def send_prompt(api_key, text_prompt, model="llama-3.3-70b-versatile"):
    """
    Synchronously sends a prompt to the Groq API using built-in urllib.
    Returns a dict with 'success' (bool) and 'message' (string response or error).
    """
    if not api_key:
        return {"success": False, "message": "API Key is missing. Please set it in Add-on Preferences."}

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Groq's API sits behind Cloudflare which blocks Python's default urllib User-Agent
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    system_prompt = (
        "You are an expert Python developer for Blender 4.0.\n"
        "Your goal is to parse the user's request and return ONLY executable Python code (bpy).\n"
        "RULES:\n"
        "- ONLY output python code wrapped in ```python ... ``` fences. No explanations.\n"
        "- Do not include markdown outside the code block.\n"
        "- Ensure the code is safe and handles missing contexts gracefully.\n"
        "- CRITICAL: ALWAYS use standard `bpy.ops` primitive commands (e.g. `bpy.ops.mesh.primitive_cube_add`) to spawn objects. NEVER manually calculate and build primitive objects using `from_pydata` or explicit vertex lists!\n"
        "- CRITICAL: When assigning colors/materials, you MUST set BOTH the `Principled BSDF` Base Color (for renders) AND the `material.diffuse_color` (for Solid Viewport visibility). If you don't do both, the user won't see the color!\n"
        "- CRITICAL: To change the background/world color, always use the World shader node tree: `bpy.context.scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (r, g, b, 1.0)` — never use `bpy.context.space_data` for background color.\n"
        "- If you cannot fulfill the request due to it not being a Blender task, return the exact string 'ERROR: <reason>' instead of code.\n"
        "\n"
        "OUTPUT FORMAT:\n"
        "```python\n"
        "import bpy\n"
        "# your code here\n"
        "```"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_prompt}
        ]
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    try:
        # 15 second timeout to prevent indefinite hangs
        with urllib.request.urlopen(req, timeout=15) as response:
            response_body = response.read().decode('utf-8')
            response_data = json.loads(response_body)
            
            # Extract the actual text completion from standard OpenAI-like JSON format
            text_response = response_data['choices'][0]['message']['content']
            return {"success": True, "message": text_response}
            
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        return {"success": False, "message": f"HTTP Error {e.code}: {error_msg}"}
    except urllib.error.URLError as e:
        return {"success": False, "message": f"Network Error: {e.reason}"}
    except Exception as e:
        return {"success": False, "message": f"Unexpected Error: {str(e)}"}
