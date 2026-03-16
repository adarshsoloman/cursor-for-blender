# AI-Powered Blender Assistant 🤖

**"Type what you want in Blender. Watch it happen."**

An experimental Blender add-on (extension) that embeds a conversational AI panel directly inside the Blender 3D Viewport. The user types a natural language instruction, the add-on sends it to an AI provider (like Groq or Gemini), and the AI returns executable Python (`bpy`) code which is automatically run in the scene.

> ***Current Status:** Phase 1 (MVP) in active development.*

---

## 🎯 Project Goal

The primary goal of this add-on is to act as a translator between a user's mental model and Blender's intimidating Python API. 

Instead of searching the internet for "how to add a light with Python in Blender", the user simply types:
`"Add a red cube at the origin and put a point light above it"`

The add-on handles the API communication, code extraction, and safe execution within Blender.

## ⚠️ What This Is NOT (Scope Constraints)

To keep this project feasible and stable, **Phase 1** is strictly defined by what it *does not* do:
- ❌ **Not an Image-to-3D tool**: It generates native Blender objects via Python, it does not scan images.
- ❌ **Not a multi-step Agent**: It does not plan complex workflows. It executes single instructions.
- ❌ **Not context-aware (yet)**: The AI does not know what is currently in your scene.
- ❌ **Not for complex geometry**: "Build a castle" will fail. "Add a plane and scale it by 5" will succeed.

## 🛠️ Technical Architecture

This add-on is built on a clean, scalable 5-file architecture:

```text
blender_ai_assistant/
│
├── __init__.py       # Standard add-on registration entry point
├── properties.py     # Data model (Chat history, settings, API keys)
├── operators.py      # Execution logic (Submit prompt, clear chat)
├── panels.py         # UI rendering in the 3D Viewport N-Panel
└── utils.py          # Helper functions (API requests, logging, code extraction)
```

**Workflow:**
1. User types a prompt.
2. `operators.py` triggers an asynchronous API call to Groq (avoiding UI freezes).
3. The AI returns a Markdown block containing `bpy` code.
4. `utils.py` extracts the Python code from the Markdown.
5. The code is executed using `exec()` within a safe `try/except` block.
6. The UI updates to show success or the specific `SyntaxError`/`Exception` if the AI hallucinated.

## 🚀 Installation (Developer Build)

1. Download or clone this repository.
2. Zip the `blender_ai_assistant` folder into an archive (e.g., `blender_ai_assistant.zip`).
3. Open **Blender 4.0+**.
4. Go to **Edit > Preferences > Add-ons**.
5. Click **Install...** and select your zipped file.
6. Enable the add-on by checking the box next to **3D View: AI Assistant module**.
7. Open the 3D Viewport, press `N` to open the right sidebar, and select the **AI Assistant** tab.

## 📄 Documentation

For detailed information on the development phases, strict technical scope, and exact test cases required for the MVP, refer to the `docs/` folder:
- `docs/PRD.md`: The master Product Requirements Document.
- `docs/scope.md`: The strict stopping conditions for each development week.
- `docs/week_1_implementation_plan.md`: The Week 1 UI architecture setup plan.

---
*Developed by Adarsh Soloman Banjare*
