import bpy

class AIChatMessage(bpy.types.PropertyGroup):
    role: bpy.props.StringProperty()
    content: bpy.props.StringProperty()

class AIAssistantPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    api_key: bpy.props.StringProperty(
        name="API Key",
        description="Enter your API Key here",
        default="",
        subtype='PASSWORD',
    )
    
    ai_provider: bpy.props.EnumProperty(
        name="Provider",
        description="Select the AI Backend to use",
        items=[
            ("groq", "Groq", "Use Groq (Llama 3)"),
            ("gemini", "Gemini", "Use Google Gemini"),
            ("openrouter", "OpenRouter", "Use OpenRouter"),
            ("ollama", "Ollama (Local)", "Use local Ollama instance"),
        ],
        default="groq"
    )

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="API Settings", icon='PREFERENCES')
        box.prop(self, "ai_provider")
        box.prop(self, "api_key")
        
        layout.separator()
        layout.operator("ai.test_connection", text="Test Connection", icon='URL')

classes = (
    AIChatMessage,
    AIAssistantPreferences,
)

def register_properties():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.ai_chat_history = bpy.props.CollectionProperty(type=AIChatMessage)
    
    bpy.types.Scene.user_prompt = bpy.props.StringProperty(
        name="Prompt", 
        default=""
    )
    
    bpy.types.Scene.is_thinking = bpy.props.BoolProperty(
        name="Thinking", 
        default=False
    )
    
    bpy.types.Scene.last_exec_status = bpy.props.StringProperty(
        name="Last Status", 
        default=""
    )
    
    bpy.types.Scene.last_exec_message = bpy.props.StringProperty(
        name="Last Message", 
        default=""
    )
    
    bpy.types.Scene.ai_provider = bpy.props.EnumProperty(
        name="Provider",
        items=[
            ("groq", "Groq", ""),
            ("gemini", "Gemini", ""),
            ("openrouter", "OpenRouter", ""),
            ("ollama", "Ollama (Local)", ""),
        ],
        default="groq"
    )
    
    bpy.types.Scene.api_key = bpy.props.StringProperty(
        name="API Key", 
        default="", 
        subtype='PASSWORD'
    )
    
    bpy.types.Scene.settings_expanded = bpy.props.BoolProperty(
        name="Settings Expanded",
        default=False
    )

def unregister_properties():
    del bpy.types.Scene.settings_expanded
    del bpy.types.Scene.api_key
    del bpy.types.Scene.ai_provider
    del bpy.types.Scene.last_exec_message
    del bpy.types.Scene.last_exec_status
    del bpy.types.Scene.is_thinking
    del bpy.types.Scene.user_prompt
    del bpy.types.Scene.ai_chat_history
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
