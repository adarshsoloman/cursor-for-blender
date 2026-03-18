import bpy

# ==============================================================================
# Helper for Word Wrapping
# ==============================================================================

def draw_wrapped_text(layout, text, width=44):
    """Draws multi-line text by splitting on newlines first, then wrapping each line."""
    # First split by explicit newlines (decoded from <NL> token) so code blocks preserve shape
    raw_lines = text.replace("<NL>", "\n").split('\n')
    
    wrapped_lines = []
    for raw_line in raw_lines:
        if not raw_line.strip():
            wrapped_lines.append("") # Keep empty lines for spacing
            continue
            
        current_line = ""
        words = raw_line.split(" ")
        
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                current_line += (word + " ")
            else:
                wrapped_lines.append(current_line.rstrip())
                current_line = word + " "
        if current_line:
            wrapped_lines.append(current_line.rstrip())
            
    for line in wrapped_lines:
        if line == "":
            layout.separator(factor=0.5)
        else:
            layout.label(text=line)

# ==============================================================================
# UI Panel
# ==============================================================================

class VIEW3D_PT_AIAssistant(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI Assistant'
    bl_label = "AI Assistant"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='OUTLINER_OB_ARMATURE') # Robot-like icon

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # 1. Header Bar Status
        row = layout.row()
        if scene.is_thinking:
            row.label(text="⏳ Thinking...", icon='TIME')
        else:
            row.label(text="● Ready", icon='CHECKMARK')
            
        layout.separator()
        
        # 2. Message History Area
        history_box = layout.box()
        if len(scene.ai_chat_history) == 0:
            row = history_box.row()
            row.alignment = 'CENTER'
            row.label(text="Ask me anything about your Blender scene...")
        else:
            for i, msg in enumerate(scene.ai_chat_history):
                if msg.role == "user":
                    msg_col = history_box.column()
                    msg_box = msg_col.box()
                    msg_box.label(text="You:", icon='USER')
                    draw_wrapped_text(msg_box, msg.content)
                else:
                    # AI Message - Indented
                    row = history_box.row()
                    row.separator(factor=2.0) # Indent
                    msg_col = row.column()
                    msg_box = msg_col.box()
                    msg_box.label(text="AI Assistant:", icon='TEXT')
                    draw_wrapped_text(msg_box, msg.content)
                
                if i < len(scene.ai_chat_history) - 1:
                    history_box.separator(factor=0.5)
                    
        layout.separator()
        
        # 3. Input Area
        input_box = layout.box()
        # Note: Blender doesn't have a true multi-line text input widget exposed to python UI easily 
        # without hacking string properties. We use a standard string prop, which acts as a single line.
        input_box.prop(scene, "user_prompt", text="")
        
        # 4. Action Buttons Row
        row = layout.row(align=True)
        send_btn = row.operator("ai.submit_prompt", text="Send", icon='PLAY')
        
        # Disable send if thinking
        if scene.is_thinking:
            row.enabled = False
            
        row.operator("ai.clear_chat", text="Clear", icon='TRASH')
        
        layout.separator()
        
        # 5. Execution Feedback Row
        if scene.last_exec_status:
            feedback_row = layout.row()
            if scene.last_exec_status == "success":
                feedback_row.label(text="✅ " + scene.last_exec_message)
            elif scene.last_exec_status == "error":
                feedback_row.alert = True
                feedback_row.label(text="❌ " + scene.last_exec_message)
                
        layout.separator()
        
        # 6. Add-on Preferences Shortcut (Collapsible Section)
        settings_box = layout.box()
        row = settings_box.row()
        icon = 'TRIA_DOWN' if scene.settings_expanded else 'TRIA_RIGHT'
        row.prop(scene, "settings_expanded", text="Settings", icon=icon, emboss=False)
        
        if scene.settings_expanded:
            settings_box.prop(scene, "api_key")
            settings_box.prop(scene, "ai_provider")
            settings_box.operator("ai.test_connection", text="Test Connection")

# ==============================================================================
# Helper for Mocking Initialization UI
# ==============================================================================

def populate_dummy_data():
    """Populates the initial dummy data so the user can easily see what it looks like before API connection."""
    scene = bpy.context.scene
    scene.ai_chat_history.clear()
    
    msgs = [
        ("user", "Add a red cube at the origin"),
        ("assistant", "Done. I added a red cube at the origin with a red emission material applied."),
        ("user", "Now add a point light above it"),
        ("assistant", "Error: bpy.ops.object.light_add() missing argument 'type'"),
    ]
    
    for role, content in msgs:
        item = scene.ai_chat_history.add()
        item.role = role
        item.content = content.replace("\n", "<NL>")
        
    scene.is_thinking = False
    scene.last_exec_status = "success"
    scene.last_exec_message = "Executed successfully"


classes = (
    VIEW3D_PT_AIAssistant,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.timers.register(populate_dummy_data, first_interval=1.0)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
