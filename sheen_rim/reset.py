import bpy

class SHEEN_RIM_OT_reset(bpy.types.Operator):
    bl_idname = "sheen_rim.reset"
    bl_label = "Reset Values"
    bl_description = "Reset sheen rim settings to default"

    def execute(self, context):
        scene = context.scene

        scene.sheen_rim_sheen = 0.5
        scene.sheen_rim_roughness = 0.2
        scene.sheen_rim_hue = 0.0
        scene.sheen_rim_saturation = 0.0
        scene.sheen_rim_value = 5

        self.report({'INFO'}, "Sheen Rim values reset")
        return {'FINISHED'}