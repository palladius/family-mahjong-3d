import bpy
print("bpy version:", bpy.app.version_string)
try:
    import bmesh
    print("bmesh imported directly!")
except Exception as e:
    print("Direct import failed:", e)
    import sys
    print("sys.modules has bmesh?", "bmesh" in sys.modules)
