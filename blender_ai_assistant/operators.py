import bpy

class AIAssistant_OT_SubmitPrompt(bpy.types.Operator):
    bl_idname = "ai.submit_prompt"
    bl_label = "Submit Prompt"
    
    def execute(self, context):
        print("[AI] Submit triggered")
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
        print("[AI] Test connection triggered")
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
