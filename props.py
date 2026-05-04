import bpy

def register_properties():
    bpy.types.Scene.sheen_rim_sheen = bpy.props.FloatProperty(
        name="Sheen",
        default=0.5,
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.sheen_rim_roughness = bpy.props.FloatProperty(
        name="Roughness",
        default=0.2,
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.sheen_rim_hue = bpy.props.FloatProperty(
        name="Hue",
        default=0.0,
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.sheen_rim_saturation = bpy.props.FloatProperty(
        name="Saturation",
        default=0.0,
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.sheen_rim_value = bpy.props.FloatProperty(
        name="Value",
        default=5,
        min=0.0
    )

    bpy.types.Scene.sheen_rim_preview = bpy.props.FloatVectorProperty(
        name="Preview",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0
    )


def unregister_properties():
    del bpy.types.Scene.sheen_rim_sheen
    del bpy.types.Scene.sheen_rim_roughness
    del bpy.types.Scene.sheen_rim_hue
    del bpy.types.Scene.sheen_rim_saturation
    del bpy.types.Scene.sheen_rim_value
    del bpy.types.Scene.sheen_rim_preview