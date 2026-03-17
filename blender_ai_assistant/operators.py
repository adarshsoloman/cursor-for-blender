import bpy
from . import utils

class AIAssistant_OT_SubmitPrompt(bpy.types.Operator):
    bl_idname = "ai.submit_prompt"
    bl_label = "Submit Prompt"
    
    def execute(self, context):
        scene = context.scene
        prompt = scene.user_prompt.strip()
        api_key = scene.api_key.strip()
        
        if not prompt:
            scene.last_exec_status = "error"
            scene.last_exec_message = "Please enter a prompt first."
            return {'CANCELLED'}
            
        if not api_key:
            scene.last_exec_status = "error"
            scene.last_exec_message = "Please set your API Key in the Settings panel."
            return {'CANCELLED'}

        # 1. Add User's message to chat history immediately
        msg = scene.ai_chat_history.add()
        msg.role = "user"
        msg.content = prompt
        
        # 2. Update UI state to "Thinking..."
        scene.is_thinking = True
        scene.last_exec_status = ""
        scene.last_exec_message = ""
        
        # 3. Clear the input box text so they can type the next thing
        scene.user_prompt = ""
        
        # 4. Fire the async API call in the background thread
        utils.execute_api_call_async(api_key, prompt, context_type="submit")
        
        return {'FINISHED'}

class AIAssistant_OT_ClearChat(bpy.types.Operator):
    bl_idname = "ai.clear_chat"
    bl_label = "Clear Chat"
    
    def execute(self, context):
        context.scene.ai_chat_history.clear()
        context.scene.user_prompt = ""
        context.scene.last_exec_status = ""
        context.scene.last_exec_message = ""
        return {'FINISHED'}

class AIAssistant_OT_TestConnection(bpy.types.Operator):
    bl_idname = "ai.test_connection"
    bl_label = "Test Connection"
    
    def execute(self, context):
        scene = context.scene
        api_key = scene.api_key.strip()
        
        if not api_key:
            scene.last_exec_status = "error"
            scene.last_exec_message = "Please enter an API Key first."
            return {'CANCELLED'}
            
        scene.is_thinking = True
        scene.last_exec_status = ""
        scene.last_exec_message = "Testing connection to Groq API..."
        
        # We send a tiny dummy prompt just to test authentication
        dummy_test = "Respond with 'Connected' if you can read this."
        utils.execute_api_call_async(api_key, dummy_test, context_type="test")
        
        return {'FINISHED'}

classes = (
    AIAssistant_OT_SubmitPrompt,
    AIAssistant_OT_ClearChat,
    AIAssistant_OT_TestConnection,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
