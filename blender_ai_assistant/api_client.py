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

    system_prompt = """
You are a Blender Python API assistant. 
The user is working in Blender 5.0.

Your job is to convert the user's natural language instruction 
into working Blender Python (bpy) code.

RULES:
- Always respond with ONLY a Python code block.
- No explanation before or after the code.
- Always use the bpy module.
- Write complete executable code for Blender's Python console.
- If you cannot complete the task, say ONLY: ERROR: <reason>

OUTPUT FORMAT:
```python
import bpy
# your code here
```
"""

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
