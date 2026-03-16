# 🤖 Cursor for Blender
 
> Type what you want. Watch it happen.
 
An AI-powered natural language assistant embedded directly inside Blender's interface. Describe what you want in plain English — the assistant translates it into Blender Python (`bpy`) code and executes it automatically.
 
Think of it as **Cursor IDE, but for 3D.**
 
---
 
## ✨ What It Does
 
Instead of this:
```python
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
mat = bpy.data.materials.new(name="Red")
mat.diffuse_color = (1, 0, 0, 1)
bpy.context.object.data.materials.append(mat)
```
 
You just type this:
```
Add a red cube at the origin
```
 
---
 
## 📸 Preview
 
![AI Assistant Panel](assets/preview.png)
> *AI Assistant panel inside Blender 5.0's N-sidebar*
 
---
 
## 🚦 Project Status
 
> 🚧 **Active Development** — Early Prototype Stage
 
| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 — UI Panel | ✅ Complete | Sidebar chat panel inside Blender |
| Phase 2 — API Connection | 🔄 In Progress | Connect to Groq / Claude / Gemini |
| Phase 3 — Scene Generation | ⏳ Planned | Generate objects from natural language |
| Phase 4 — Advanced Features | ⏳ Planned | Agents, image input, MCP integration |
 
---
 
## 🛠️ Installation
 
**Requirements:**
- Blender 4.0 or higher (tested on 5.0.1)
- An API key from Groq, Gemini, or OpenRouter (free tiers available)
 
**Steps:**
 
1. Download the latest `.zip` from [Releases](https://github.com/adarshsoloman/cursor-for-blender/releases)
2. Open Blender → `Edit` → `Preferences` → `Add-ons`
3. Click `Install` and select the downloaded `.zip`
4. Search for **"AI Assistant"** and enable it
5. Press `N` in the 3D Viewport to open the sidebar
6. Click the **AI Assistant** tab
7. Go to `Settings` → enter your API key → select your provider
 
---
 
## 🎮 Usage
 
1. Open the **AI Assistant** panel in the N-sidebar
2. Type a natural language instruction in the input box
3. Hit **Send**
4. Watch Blender execute it automatically
 
**Example prompts that work:**
```
Add a red cube at the origin
Create a point light above the scene
Delete all objects in the scene
Add a UV sphere with 32 segments
Move the selected object to position 2, 3, 0
Set the background color to dark blue
```
 
---
 
## 🔑 Supported AI Providers
 
| Provider | Model | Cost | Speed |
|----------|-------|------|-------|
| **Groq** | Llama 3.3 70B | Free tier | ⚡ Fastest |
| **Google Gemini** | Gemini 1.5 Flash | Free tier | 🟡 Fast |
| **OpenRouter** | Various | Free tier available | 🟡 Medium |
| **Ollama** | Llama 3 / CodeLlama | 100% Free (local) | 🔴 Depends on hardware |
 
---
 
## 📁 Project Structure
 
```
cursor-for-blender/
│
├── blender_ai_assistant/
│   ├── __init__.py         # Add-on entry point, bl_info
│   ├── properties.py       # Scene properties, chat history
│   ├── operators.py        # Submit, Clear, Test Connection
│   ├── panels.py           # UI panel and layout
│   └── utils.py            # Helper functions
│
├── README.md
└── LICENSE
```
 
---
 
## 🗺️ Roadmap
 
- [x] Sidebar chat panel UI
- [x] Message history display
- [x] Settings panel with API key input
- [ ] Groq API integration
- [ ] bpy code extraction and execution
- [ ] Async API calls (non-blocking UI)
- [ ] Error handling and retry logic
- [ ] Multi-provider support
- [ ] Scene context passing
- [ ] Image input (multimodal)
- [ ] Blender Extensions platform release
 
---
 
## 🤝 Contributing
 
Contributions are very welcome. This project is in early stages and there's a lot to build.
 
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request
 
---
 
## 📄 License
 
This project is licensed under the **GNU General Public License v3.0** — see [LICENSE](LICENSE) for details.
 
In short: you can use, modify, and distribute this freely, but any derivative work must also remain open source under GPL. This is consistent with Blender's own license.
 
---
 
## 🙏 Acknowledgements
 
- [Blender Foundation](https://www.blender.org/) — for building an incredible open source 3D tool
- [Groq](https://groq.com/) — for blazing fast free inference
- The Blender Python community — for years of `bpy` documentation and examples
 
---
 
<p align="center">
  Built with 🧠 + ☕ by <a href="https://github.com/adarshsoloman">adarshsoloman</a>
</p>