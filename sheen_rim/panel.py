import bpy

class SHEEN_RIM_PT_panel(bpy.types.Panel):
    bl_label = "Shader Helpers"
    bl_idname = "8G_TOOLS_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "8G Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Sheen Rim Settings")

        layout.prop(scene, "sheen_rim_sheen")
        layout.prop(scene, "sheen_rim_roughness")
        
        layout.label(text="Tint (HSV)")
        row = layout.row(align=True)
        row.prop(scene, "sheen_rim_hue", text="H")
        row.prop(scene, "sheen_rim_saturation", text="S")
        row.prop(scene, "sheen_rim_value", text="V")
        
        row = layout.row()
        row.enabled = False
        row.prop(scene, "sheen_rim_preview", text="Sheen color")

        layout.separator()

        layout.operator("sheen_rim.reset", icon='LOOP_BACK')
        layout.operator("sheen_rim.button", icon='SHADING_RENDERED')