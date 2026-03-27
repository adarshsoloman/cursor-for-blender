# Cursor for Blender
 
> 🚀 **v1.0.0 is LIVE!** The core MVP is officially complete and stable.

Look, Blender is amazing but it is arguably one of the hardest pieces of software to learn on the planet. I got so frustrated trying to remember exactly which nested menu hides the specific button I needed. And figuring out how to write the perfect `bpy` Python script just to do something basic like adding a red cube was driving me crazy.
 
So I built this.
 
It is an AI assistant panel that sits right inside Blender. You type what you want in plain English, and it writes the Python code and executes it for you. It is basically Cursor IDE, but directly inside the 3D viewport.
 
I am incredibly proud of getting this to work. This is my first real open source project and it actually functions the way I wanted it to. You type a prompt, it hits a free AI API, extracts the code, and manipulates your scene without freezing the UI. And yes, Ctrl+Z works if the AI messes up your scene.
 
## How it works
 
Instead of searching the docs and writing this:
```python
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
mat = bpy.data.materials.new(name="Red")
mat.diffuse_color = (1, 0, 0, 1)
bpy.context.object.data.materials.append(mat)
```
 
You literally just open the side panel and type:
`Add a red cube at the origin`
 
![AI Assistant Panel](assets/preview.png)
*(The UI panel lives in the N-sidebar)*
 
## Installation
 
You need Blender 4.0 or newer. I built and tested this on 4.0 and 5.0.
 
1. Go to the [Releases](https://github.com/adarshsoloman/cursor-for-blender/releases) page and grab the latest `.zip` file.
2. Open Blender. Go to Edit > Preferences > Add-ons.
3. Click Install and pick the `.zip` you just downloaded.
4. Check the box to enable "AI Assistant".
5. Expand the add-on preferences right there and paste in your API key. (I highly recommend getting a free Groq API key, it is insanely fast).
6. Press the `N` key in your 3D viewport to open the right sidebar. Click the AI Assistant tab.
 
## Usage
 
It is pretty straightforward. Open the panel, type what you want, and hit Send.
 
Try things like:
* "Add a red cube at the origin"
* "Create a point light above the scene"
* "Delete everything"
* "Add a UV sphere with 32 segments"
* "Move the selected object to position 2, 3, 0"
* "Set the background color to dark blue"
 
If the AI writes garbage code, it gets caught and prints the Python error in the chat panel instead of crashing Blender. If it actually places an object you hate, just hit Ctrl+Z to undo it.
 
## Supported AI
 
Right now I have it tuned to work best with Groq (specifically the Llama 3.3 70B model) because the free tier is extremely generous and it generates code in like two seconds. You can also use Google Gemini or OpenRouter if you prefer. Local Ollama support is planned so you can run it completely offline eventually.
 
## Under the Hood
 
I kept the codebase as simple as I possibly could. No massive frameworks, no external dependencies to trick into Blender's Python folder. Just pure Blender Python using standard libraries.
 
```text
blender_ai_assistant/
  __init__.py         # Registration and add-on info
  properties.py       # Stores your chat history and API key safely
  operators.py        # The logic for the Send and Clear buttons
  panels.py           # Draws the actual UI
  api_client.py       # Talks to the Groq/Gemini API
  code_executor.py    # Sandboxes and runs the AI's Python code
  utils.py            # Async threading so Blender does not freeze
```
 
## What is Next
 
The core system works right now. The MVP is officially done and stable.
 
Next on my radar is actually giving the AI context. Right now it generates code blindly. I want to pass your scene data to the API so it knows what objects you have selected. I also want to add vision support so you can upload a reference image directly into the panel.
 
## Want to help?
 
Contributions are fully welcome. I built this solo from India, building in public for the first time, and I am still figuring a lot of things out. If you know how to make the code cleaner or want to build one of the roadmap features, please fork the repo and open a Pull Request.
 
1. Fork the repo
2. Create your feature branch (`git checkout -b feature/cool-stuff`)
3. Commit your changes
4. Push to the branch
5. Open a PR
 
## License
 
This is licensed under the GNU General Public License v3.0 to match Blender's own license. Do whatever you want with it, just keep it open source if you modify it.
 
Built with 🧠 + ☕ by [adarshsoloman](https://github.com/adarshsoloman).